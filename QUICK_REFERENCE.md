# 📚 Quick Reference Guide - Common Patterns Used

This guide explains the common patterns you'll see throughout the fixed code. Keep this handy for reference!

---

## 🔐 Security Patterns

### 1. Getting Logged-in User ID from JWT

```python
from flask_jwt_extended import get_jwt_identity

# Get the ID of the logged-in user (admin or customer)
user_id = int(get_jwt_identity())
# Returns the 'identity' value we stored when creating the token
# We convert to int because JWT stores it as a string
```

**When to use**: Whenever you need to know WHO is making the request.

---

### 2. Ownership Verification

```python
# Check if the resource belongs to the logged-in user
if resource.customer_id != customer_id:
    return jsonify({"error": "Access denied"}), 403
```

**When to use**: Before showing, updating, or deleting user-specific data.

**Example use cases**:
- Viewing an order
- Editing cart items
- Updating profile

---

### 3. Permission Required Decorator

```python
from app.utils.decorators import permission_required

@admin_bp.route("/admins", methods=["POST"])
@permission_required("manage_admins")  # Check permission first
def create_admin():
    # Only runs if user has "manage_admins" permission
    pass
```

**When to use**: For admin routes that require specific permissions.

---

## ✅ Validation Patterns

### 1. Check Required Fields

```python
# Check if field exists and is not empty
if not data.get("email") or not data.get("email").strip():
    return jsonify({"error": "Email is required"}), 400
```

**Explanation**:
- `data.get("email")` - gets email from request data
- `not data.get("email")` - checks if email is None or empty string
- `.strip()` - removes spaces from beginning and end
- `not ...strip()` - checks if after removing spaces, nothing is left

---

### 2. Check Duplicate Records

```python
# Check if email already exists in database
existing_admin = Admin.query.filter_by(email=email).first()
if existing_admin:
    return jsonify({"error": "Email already exists"}), 400
```

**Explanation**:
- `.filter_by(email=email)` - search for records with this email
- `.first()` - get first result, or None if not found
- `if existing_admin:` - if we found something, reject the request

---

### 3. Validate Foreign Keys Exist

```python
# Make sure the role_id actually exists
role = Role.query.get(role_id)
if not role:
    return jsonify({"error": "Invalid role ID"}), 404
```

**When to use**: Before assigning relationships (category_id, brand_id, role_id, etc.)

---

## 🛡️ Error Handling Patterns

### 1. Basic Try-Except for Database Operations

```python
from sqlalchemy.exc import SQLAlchemyError

try:
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

except SQLAlchemyError as e:
    db.session.rollback()  # IMPORTANT: Always rollback on error!
    return jsonify({"error": "Database error"}), 500
```

**Key points**:
- Always wrap `db.session.commit()` in try-except
- Always `rollback()` on error to keep database clean
- Return appropriate status codes (400, 500, etc.)

---

### 2. Handling Integrity Errors (Constraint Violations)

```python
from sqlalchemy.exc import IntegrityError

try:
    db.session.delete(admin)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200

except IntegrityError as e:
    # Happens when deleting something that's referenced elsewhere
    db.session.rollback()
    return jsonify({
        "error": "Cannot delete - has related records"
    }), 400
```

**When this happens**:
- Deleting an admin who created products
- Deleting a category that has products
- Violating unique constraints (duplicate email)

---

## 🗄️ Database Query Patterns

### 1. Find by ID (or 404)

```python
# Get item by ID, automatically return 404 if not found
product = Product.query.get_or_404(product_id)
```

**Explanation**: If product doesn't exist, Flask automatically returns 404 error.

---

### 2. Find by Field

```python
# Find first customer with this email
customer = Customer.query.filter_by(email=email).first()

# Find all active products
products = Product.query.filter_by(status="active").all()
```

**Difference**:
- `.first()` - returns one result or None
- `.all()` - returns a list of results (empty list if none found)

---

### 3. Check if Record Exists

```python
# Check if item with specific conditions exists
existing_item = CartItem.query.filter_by(
    cart_id=cart.id,
    product_id=product_id
).first()

if existing_item:
    # Item exists, update it
    existing_item.quantity += 1
else:
    # Item doesn't exist, create new one
    new_item = CartItem(...)
```

---

## 📅 Timestamp Pattern

### Adding Timestamps to Models

```python
from datetime import datetime

class MyModel(db.Model):
    # ... other fields ...
    
    # Automatically set when record is created
    created_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow,  # Call function when creating
        nullable=False
    )
    
    # Automatically update when record is modified
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,     # Set initial value
        onupdate=datetime.utcnow,    # Update on changes
        nullable=False
    )
```

### Including in to_dict()

```python
def to_dict(self):
    return {
        "id": self.id,
        "name": self.name,
        # Convert datetime to string format
        "created_at": self.created_at.isoformat() if self.created_at else None,
        "updated_at": self.updated_at.isoformat() if self.updated_at else None,
    }
```

**Explanation**:
- `.isoformat()` converts datetime to string like "2024-01-15T10:30:00"
- `if self.created_at else None` handles case where field might be None

---

## 🔄 Common HTTP Status Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET, PUT, DELETE |
| 201 | Created | Successfully created new resource |
| 400 | Bad Request | Invalid input, validation failed |
| 401 | Unauthorized | Not logged in, invalid token |
| 403 | Forbidden | Logged in but don't have permission |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Unexpected error, database error |

### Examples:

```python
# 200 - Successfully got data
return jsonify(products), 200

# 201 - Successfully created
return jsonify(new_product.to_dict()), 201

# 400 - Bad input
return jsonify({"error": "Email is required"}), 400

# 403 - No permission
return jsonify({"error": "Access denied"}), 403

# 404 - Not found
return jsonify({"error": "Product not found"}), 404

# 500 - Server error
return jsonify({"error": "Database error"}), 500
```

---

## 🎯 Request Data Patterns

### 1. Get JSON Data from Request

```python
# Safely get JSON data (returns empty dict if no data)
data = request.get_json() or {}

# Get specific field with default value
name = data.get("name", "")  # Returns "" if "name" not in data
status = data.get("status", "active")  # Returns "active" if not provided
```

---

### 2. Clean String Input

```python
# Remove leading/trailing spaces and convert to lowercase
email = data.get("email", "").strip().lower()

# Remove spaces only
name = data.get("name", "").strip()
```

**Why**:
- `.strip()` - removes accidental spaces: " john " → "john"
- `.lower()` - makes emails consistent: "John@Email.com" → "john@email.com"

---

## 🔧 Common Mistakes to Avoid

### ❌ Forgetting to Rollback on Error

```python
# BAD - doesn't rollback
try:
    db.session.commit()
except Exception as e:
    return jsonify({"error": "Failed"}), 500

# GOOD - rolls back on error
try:
    db.session.commit()
except Exception as e:
    db.session.rollback()  # Clean up!
    return jsonify({"error": "Failed"}), 500
```

---

### ❌ Not Checking Ownership

```python
# BAD - anyone can delete any cart item
@cart_bp.route("/items/<int:item_id>", methods=["DELETE"])
def remove_item(item_id):
    item = CartItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()

# GOOD - verify ownership first
@cart_bp.route("/items/<int:item_id>", methods=["DELETE"])
@jwt_required()
def remove_item(item_id):
    customer_id = int(get_jwt_identity())
    item = CartItem.query.get_or_404(item_id)
    
    # Check ownership!
    if item.cart.customer_id != customer_id:
        return jsonify({"error": "Access denied"}), 403
    
    db.session.delete(item)
    db.session.commit()
```

---

### ❌ Not Validating Input

```python
# BAD - no validation
@admin_bp.route("", methods=["POST"])
def create_admin():
    data = request.get_json()
    admin = Admin(email=data.get("email"))  # What if email is None?

# GOOD - validate first
@admin_bp.route("", methods=["POST"])
def create_admin():
    data = request.get_json() or {}
    
    if not data.get("email"):
        return jsonify({"error": "Email required"}), 400
    
    admin = Admin(email=data["email"])
```

---

## 📝 Checklist for New Endpoints

When creating a new endpoint, remember to:

- [ ] Add appropriate decorator (`@jwt_required()` or `@permission_required()`)
- [ ] Validate all required fields
- [ ] Check for duplicates if needed
- [ ] Verify ownership for user-specific data
- [ ] Wrap database operations in try-except
- [ ] Rollback on errors
- [ ] Return appropriate status codes
- [ ] Add helpful comments

---

## 🎓 Keep Learning!

The best way to understand these patterns:

1. **Read the comments** in the actual code files
2. **Try to modify** existing endpoints
3. **Create new endpoints** using these patterns
4. **Test your code** to see what happens when things go wrong

Remember: It's okay to make mistakes while learning - that's how you learn best! 🚀

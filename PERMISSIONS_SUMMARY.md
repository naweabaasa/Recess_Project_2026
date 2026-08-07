# Permissions Summary

This document outlines the permission controls added to all controllers in the BreadWise application.

## Permission System Overview

The application uses a role-based access control (RBAC) system where:
- Admins have roles (e.g., super_admin, manager, staff)
- Roles have permissions (e.g., manage_products, manage_orders)
- The `@permission_required` decorator protects admin routes
- The `@jwt_required()` decorator protects customer routes
- Super admins bypass all permission checks

## Controllers and Their Permissions

### 1. Admin Controller (`admin_controller.py`)
**Purpose**: Manage admin accounts

| Endpoint | Method | Permission Required |
|----------|--------|---------------------|
| `/api/admins` | GET | `manage_admins` |
| `/api/admins` | POST | `manage_admins` |
| `/api/admins/<id>` | PUT | `manage_admins` |
| `/api/admins/<id>` | DELETE | `manage_admins` |

### 2. Auth Controller (`auth_controller.py`)
**Purpose**: Admin authentication

| Endpoint | Method | Permission Required |
|----------|--------|---------------------|
| `/api/auth/login` | POST | None (public) |

### 3. Brand Controller (`brand_controller.py`)
**Purpose**: Manage product brands

| Endpoint | Method | Permission Required |
|----------|--------|---------------------|
| `/api/brands` | GET | `manage_brands` OR `manage_products` |
| `/api/brands/<id>` | GET | `manage_brands` OR `manage_products` |
| `/api/brands` | POST | `manage_brands` |
| `/api/brands/<id>` | PUT | `manage_brands` |
| `/api/brands/<id>` | DELETE | `manage_brands` |

### 4. Cart Controller (`cart_controller.py`)
**Purpose**: Customer shopping cart management

| Endpoint | Method | Authentication Required |
|----------|--------|------------------------|
| `/api/cart` | GET | JWT (Customer) |
| `/api/cart/items` | POST | JWT (Customer) |
| `/api/cart/items/<id>` | PUT | JWT (Customer) |
| `/api/cart/items/<id>` | DELETE | JWT (Customer) |

**Note**: Cart operations now use the actual logged-in customer ID from JWT token instead of hardcoded ID.

### 5. Category Controller (`category_controller.py`)
**Purpose**: Manage product categories

| Endpoint | Method | Permission Required |
|----------|--------|---------------------|
| `/api/categories` | GET | `manage_categories` |
| `/api/categories` | POST | `manage_categories` |
| `/api/categories/<id>` | PUT | `manage_categories` |
| `/api/categories/<id>` | DELETE | `manage_categories` |

### 6. Customer Auth Controller (`customer_auth_controller.py`)
**Purpose**: Customer authentication and profile

| Endpoint | Method | Authentication Required |
|----------|--------|------------------------|
| `/api/customers/register` | POST | None (public) |
| `/api/customers/login` | POST | None (public) |
| `/api/customers/me` | GET | JWT (Customer) |

### 7. Delivery Controller (`delivery_controller.py`)
**Purpose**: Manage delivery records

| Endpoint | Method | Permission Required |
|----------|--------|---------------------|
| `/api/deliveries` | GET | `manage_delivery` |
| `/api/deliveries` | POST | `manage_delivery` |
| `/api/deliveries/<id>` | PUT | `manage_delivery` |

### 8. Order Controller (`order_controller.py`)
**Purpose**: Order processing and management

| Endpoint | Method | Permission/Auth Required |
|----------|--------|-------------------------|
| `/api/orders/checkout` | POST | JWT (Customer) |
| `/api/orders` | GET | JWT (Customer) |
| `/api/orders/<id>` | GET | JWT (Customer) |
| `/api/orders/<id>/status` | PUT | `manage_orders` (Admin) |

**Note**: Customer order operations now use the actual logged-in customer ID from JWT token.

### 9. Product Controller (`product_controller.py`)
**Purpose**: Manage products

| Endpoint | Method | Permission Required |
|----------|--------|---------------------|
| `/api/products` | GET | `manage_products` |
| `/api/products` | POST | `manage_products` |
| `/api/products/<id>` | PUT | `manage_products` |
| `/api/products/<id>` | DELETE | `manage_products` |

### 10. Public Controller (`public_controller.py`)
**Purpose**: Public-facing product catalog

| Endpoint | Method | Permission Required |
|----------|--------|---------------------|
| `/api/public/categories` | GET | None (public) |
| `/api/public/brands` | GET | None (public) |
| `/api/public/products` | GET | None (public) |
| `/api/public/products/<id>` | GET | None (public) |

**Note**: These endpoints are intentionally public for browsing products without authentication.

## Permission Codes Used

The following permission codes are referenced in the controllers:

1. `manage_admins` - Create, update, delete admin accounts
2. `manage_brands` - Manage product brands
3. `manage_products` - Manage products
4. `manage_categories` - Manage product categories
5. `manage_orders` - Update order status
6. `manage_delivery` - Manage delivery records

## Implementation Details

### Admin Routes
- Use `@permission_required("permission_code")` decorator
- Requires valid JWT token with admin claims
- Super admins bypass permission checks
- Returns 403 Forbidden if permission is missing

### Customer Routes
- Use `@jwt_required()` decorator
- Extracts customer ID from JWT token using `get_jwt_identity()`
- Returns 401 Unauthorized if token is missing or invalid

### Public Routes
- No authentication or permissions required
- Only show active/published content

## Security Improvements Made

1. **Replaced hardcoded IDs**: Customer operations now use actual JWT identity
2. **Added permission checks**: All admin operations require specific permissions
3. **Protected customer routes**: Cart and order operations require authentication
4. **Consistent authorization**: All controllers follow the same pattern

## Next Steps

To fully utilize this permission system:

1. Ensure all required permissions exist in the database
2. Assign appropriate permissions to roles
3. Create roles with different permission sets (e.g., Manager, Staff, Viewer)
4. Test each endpoint with different user roles
5. Consider adding permission checks at the database level for additional security

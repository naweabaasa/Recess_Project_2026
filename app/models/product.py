from app.extensions import db   # Imports the database instance.
from datetime import datetime  # Import datetime to record when products are created/updated

class Product(db.Model):                                                    # Defines the Product model.
    __tablename__ = "products"                                              # Database table name.
    id = db.Column(db.Integer, primary_key=True)                            # Unique identifier for each product.
    name = db.Column(db.String(150), nullable=False)                        # Stores the product name.
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))     # Links the product to a category.
    category = db.relationship("Category")                                  # Creates a relationship with the Category model.
    brand_id = db.Column(db.Integer, db.ForeignKey("brands.id"), nullable=True) # Links the product to a brand.
    brand = db.relationship("Brand")                                        # Creates a relationship with the Brand model.
    description = db.Column(db.Text)                                        # Stores the product description.
    price = db.Column(db.Numeric(10, 2), nullable=False)                    # Stores the product price.
    image_url = db.Column(db.String(255))                                   # Stores the product image URL.
    status = db.Column(db.String(20), default="draft")                      # Stores the product status (defaults to "draft").
    admin_id = db.Column(db.Integer, db.ForeignKey("admins.id"))            # Links the product to the admin who created or manages it.
    
    # TIMESTAMP FIELDS: These help track when products are created and updated
    # This is important for audit trails and knowing when data changed
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  
    # default=datetime.utcnow means automatically set to current time when created
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    # onupdate=datetime.utcnow means automatically update to current time when modified

    # Constructor to initialize a Product object
    def __init__(self, name, price, category_id=None, brand_id=None, description=None, image_url=None, status="draft", admin_id=None):
        self.name = name
        self.price = price
        self.category_id = category_id
        self.brand_id = brand_id
        self.description = description
        self.image_url = image_url
        self.status = status
        self.admin_id = admin_id

    # Converts the product object into a dictionary.
    def to_dict(self):
        return {
            "id": self.id, 
            "name": self.name, 
            "category_id": self.category_id,
            "category_name": self.category.name if self.category else None,  # Include category name for convenience
            "brand_id": self.brand_id,
            "brand_name": self.brand.name if self.brand else None,
            "description": self.description, 
            "price": str(self.price),
            "image_url": self.image_url, 
            "status": self.status,
            # Include timestamps in API responses
            # .isoformat() converts datetime to string format like "2024-01-15T10:30:00"
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
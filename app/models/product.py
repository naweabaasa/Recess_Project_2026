from app.extensions import db   # Imports the database instance.

class Product(db.Model):                                                    # Defines the Product model.
    __tablename__ = "products"                                              # Database table name.
    id = db.Column(db.Integer, primary_key=True)                            # Unique identifier for each product.
    name = db.Column(db.String(150), nullable=False)                        # Stores the product name.
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))     # Links the product to a category.
    category = db.relationship("Category")                                  # Creates a relationship with the Category model.
    description = db.Column(db.Text)                                        # Stores the product description.
    price = db.Column(db.Numeric(10, 2), nullable=False)                    # Stores the product price.
    image_url = db.Column(db.String(255))                                   # Stores the product image URL.
    status = db.Column(db.String(20), default="draft")                      # Stores the product status (defaults to "draft").
    admin_id = db.Column(db.Integer, db.ForeignKey("admins.id"))            # Links the product to the admin who created or manages it.

    # Converts the product object into a dictionary.
    def to_dict(self):
        return {
            "id": self.id, 
            "name": self.name, 
            "category_id": self.category_id,
            "description": self.description, 
            "price": str(self.price),
            "image_url": self.image_url, 
            "status": self.status,
        }
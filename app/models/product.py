from app.extensions import db   # Imports the database instance.

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
            "brand_id": self.brand_id,
            "brand_name": self.brand.name if self.brand else None,
            "description": self.description, 
            "price": str(self.price),
            "image_url": self.image_url, 
            "status": self.status,
        }
from app.extensions import db   # Imports the database instance.

# Represents a product category in the database.
class Category(db.Model):                                          # Defines the Category model.
    __tablename__ = "categories"                                   # Database table name.
    id = db.Column(db.Integer, primary_key=True)                   # Unique identifier for each category.
    name = db.Column(db.String(100), unique=True, nullable=False)  # Stores the category name (must be unique).
    description = db.Column(db.String(255))                        # Stores a brief description of the category.
    status = db.Column(db.String(20), default="active")            # Stores the category status (defaults to "active").

    def __init__(self, name=None, description=None, status="active"):
        self.name = name
        self.description = description
        self.status = status

     # Converts the category object into a dictionaryfor API responses.
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status
        }
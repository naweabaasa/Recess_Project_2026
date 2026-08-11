from app.extensions import db   # Imports the database instance.
from datetime import datetime  # Import datetime to record when categories are created/updated

# Represents a product category in the database.
class Category(db.Model):                                          # Defines the Category model.
    __tablename__ = "categories"                                   # Database table name.
    id = db.Column(db.Integer, primary_key=True)                   # Unique identifier for each category.
    name = db.Column(db.String(100), unique=True, nullable=False)  # Stores the category name (must be unique).
    status = db.Column(db.String(20), default="active")            # Stores the category status (defaults to "active").
    
    # TIMESTAMP FIELDS: Track when categories are created and updated
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # Automatically set to current time when category is created
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    # Automatically update to current time when category is modified

    def __init__(self, name=None, status="active"):
        self.name = name
        self.status = status

     # Converts the category object into a dictionaryfor API responses.
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            # Include timestamps in the response
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
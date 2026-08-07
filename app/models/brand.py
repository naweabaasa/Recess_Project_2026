from app.extensions import db   # Imports the database instance.
from datetime import datetime  # Import datetime to record when brands are created/updated

# Represents a product brand in the database.
class Brand(db.Model):                                             # Defines the Brand model.
    __tablename__ = "brands"                                       # Database table name.
    id = db.Column(db.Integer, primary_key=True)                   # Unique identifier for each brand.
    name = db.Column(db.String(100), unique=True, nullable=False)  # Stores the brand name (must be unique).
    description = db.Column(db.String(255))                        # Stores a brief description of the brand.
    logo_url = db.Column(db.String(255))                           # Stores logo image URL of the brand.
    status = db.Column(db.String(20), default="active")            # Stores the brand status (defaults to "active").
    
    # TIMESTAMP FIELDS: Track when brands are created and updated
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # Automatically set to current time when brand is created
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    # Automatically update to current time when brand is modified

    # Constructor to initialize a Brand object.
    def __init__(self, name, description=None, logo_url=None, status="active"):
        self.name = name
        self.description = description
        self.logo_url = logo_url
        self.status = status

    # Converts the brand object into a dictionary for API responses.
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "logo_url": self.logo_url,
            "status": self.status,
            # Include timestamps in the response
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

from app.extensions import db   # Imports the database instance.

# Represents a product brand in the database.
class Brand(db.Model):                                             # Defines the Brand model.
    __tablename__ = "brands"                                       # Database table name.
    id = db.Column(db.Integer, primary_key=True)                   # Unique identifier for each brand.
    name = db.Column(db.String(100), unique=True, nullable=False)  # Stores the brand name (must be unique).
    description = db.Column(db.String(255))                        # Stores a brief description of the brand.
    logo_url = db.Column(db.String(255))                           # Stores logo image URL of the brand.
    status = db.Column(db.String(20), default="active")            # Stores the brand status (defaults to "active").

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
            "status": self.status
        }

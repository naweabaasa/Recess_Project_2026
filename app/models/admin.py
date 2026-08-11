from app.extensions import db, bcrypt    # Imports the database instance and Bcrypt for password hashing.
from datetime import datetime  # Import datetime to record when admins are created/updated






# Represents administrator accounts with authentication and account management.
class Admin(db.Model):                                               # Defines the Admin model.
    __tablename__ = "admins"                                         # Database table name.
    id = db.Column(db.Integer, primary_key=True)                     # Unique identifier for each admin.
    full_name = db.Column(db.String(120))                            # Stores the admin's full name.
    email = db.Column(db.String(120), unique=True, nullable=False)   # Stores the admin's email address.
    password_hash = db.Column(db.String(255))                        # Stores the encrypted password.
    is_active = db.Column(db.Boolean, default=True)                  # Indicates whether the admin account is active.

    # TIMESTAMP FIELDS: Track when admin accounts are created and updated.
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, full_name=None, email=None, password_hash=None, is_active=True):
        self.full_name = full_name
        self.email = email
        if password_hash is not None:
            self.password_hash = password_hash
        self.is_active = is_active

    # Hashes and stores the password.
    def set_password(self, raw):
        self.password_hash = bcrypt.generate_password_hash(raw).decode("utf-8")

    # Checks if the entered password matches the stored hash.
    def check_password(self, raw):
        return bcrypt.check_password_hash(self.password_hash, raw)

    # Converts the admin object into a dictionary.
    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
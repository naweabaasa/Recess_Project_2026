from app.extensions import db, bcrypt     # Imports the database instance and Bcrypt for password hashing.
from datetime import datetime  # Import datetime to record when customers register/update

class Customer(db.Model):                                            # Defines the Customer model.
    __tablename__ = "customers"                                      # Database table name.
    id = db.Column(db.Integer, primary_key=True)                     # Unique identifier for each customer.
    full_name = db.Column(db.String(120))                            # Stores the customer's full name.
    email = db.Column(db.String(120), unique=True, nullable=False)   # Stores the customer's email (must be unique).
    phone_number = db.Column(db.String(30))                          # Stores the customer's phone number.
    password_hash = db.Column(db.String(255))                        # Stores the encrypted password.
    address = db.Column(db.String(255))                              # Stores the customer's address.
    
    # TIMESTAMP FIELDS: Track when customers register and update their info
    # Useful for knowing when customers joined and last modified their account
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # Automatically set to current time when customer registers
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    # Automatically update to current time when customer updates their profile

    def __init__(self, full_name=None, email=None, phone_number=None, password_hash=None, address=None):
        self.full_name = full_name
        self.email = email
        self.phone_number = phone_number
        if password_hash is not None:
            self.password_hash = password_hash
        self.address = address


    # Hashes and stores the customer's password.
    def set_password(self, raw):
        self.password_hash = bcrypt.generate_password_hash(raw).decode("utf-8")

    # Verifies the entered password against the stored hash
    def check_password(self, raw):
        return bcrypt.check_password_hash(self.password_hash, raw)

    # Converts the customer object into a dictionary.
    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
            # Include timestamps in the response
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            }

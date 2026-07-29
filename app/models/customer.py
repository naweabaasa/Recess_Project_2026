from app.extensions import db, bcrypt     # Imports the database instance and Bcrypt for password hashing.

class Customer(db.Model):                                            # Defines the Customer model.
    __tablename__ = "customers"                                      # Database table name.
    id = db.Column(db.Integer, primary_key=True)                     # Unique identifier for each customer.
    full_name = db.Column(db.String(120))                            # Stores the customer's full name.
    email = db.Column(db.String(120), unique=True, nullable=False)   # Stores the customer's email (must be unique).
    phone_number = db.Column(db.String(30))                          # Stores the customer's phone number.
    password_hash = db.Column(db.String(255))                        # Stores the encrypted password.
    address = db.Column(db.String(255))                              # Stores the customer's address.


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
            "address": self.address
            }

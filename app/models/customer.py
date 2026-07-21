from app.extensions import db, bcrypt

class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(30))
    password_hash = db.Column(db.String(255))
    address = db.Column(db.String(255))

    def set_password(self, raw):
        self.password_hash = bcrypt.generate_password_hash(raw).decode("utf-8")

    def check_password(self, raw):
        return bcrypt.check_password_hash(self.password_hash, raw)

    def to_dict(self):
        return {"id": self.id, "full_name": self.full_name, "email": self.email,
                "phone_number": self.phone_number, "address": self.address}
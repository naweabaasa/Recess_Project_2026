rom app.extensions import db

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    category = db.relationship("Category")
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(255))
    status = db.Column(db.String(20), default="draft")
    admin_id = db.Column(db.Integer, db.ForeignKey("admins.id"))

    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "category_id": self.category_id,
            "description": self.description, "price": str(self.price),
            "image_url": self.image_url, "status": self.status,
        }
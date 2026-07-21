from app.extensions import db

class ShoppingCart(db.Model):
    __tablename__ = "shopping_carts"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), unique=True)
    items = db.relationship("CartItem", backref="cart", cascade="all, delete-orphan")

    def to_dict(self):
        return {"id": self.id, "customer_id": self.customer_id,
                "items": [i.to_dict() for i in self.items]}

class CartItem(db.Model):
    __tablename__ = "cart_items"
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("shopping_carts.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    product = db.relationship("Product")
    quantity = db.Column(db.Integer, default=1)

    def to_dict(self):
        return {"id": self.id, "product": self.product.to_dict() if self.product else None,
                "quantity": self.quantity}
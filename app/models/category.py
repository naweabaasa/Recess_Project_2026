from app.extensions import db

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))
    status = db.Column(db.String(20), default="active")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description, "status": self.status}
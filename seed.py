from app import create_app
from app.extensions import db
from app.models import Role, Permission, Admin, Category

PERMISSIONS = [
    "manage_admins", "manage_categories", "manage_products",
    "manage_orders", "manage_payments", "manage_delivery",
]

ROLES = {
    "super_admin": [],
    "catalog_manager": ["manage_categories", "manage_products"],
    "order_manager": ["manage_orders", "manage_payments", "manage_delivery"],
}

def run():
    app = create_app()
    with app.app_context():
        db.create_all()

        perms = {}
        for code in PERMISSIONS:
            perm = Permission.query.filter_by(code=code).first() or Permission(code=code)
            db.session.add(perm)
            perms[code] = perm
        db.session.commit()

        for name, codes in ROLES.items():
            role = Role.query.filter_by(name=name).first() or Role(name=name)
            role.permissions = [perms[c] for c in codes]
            db.session.add(role)
        db.session.commit()

        if not Admin.query.filter_by(email="admin@example.com").first():
            admin = Admin(full_name="Super Admin", email="admin@example.com",
                           role=Role.query.filter_by(name="super_admin").first())
            admin.set_password("ChangeMe123!")
            db.session.add(admin)

        for name in ["Electronics", "Clothing", "Home & Living"]:
            if not Category.query.filter_by(name=name).first():
                db.session.add(Category(name=name))

        db.session.commit()
        print("Seed complete. admin@example.com / ChangeMe123!")

if __name__ == "__main__":
    run()
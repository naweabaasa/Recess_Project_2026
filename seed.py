# This script is a database seeding file. 
# It prepares the application with initial data by creating database tables, 
# adding permissions, creating user roles, assigning permissions to roles, 
# creating a default admin account, and adding default product categories.
# It helps set up the system quickly when starting the project.



from app import create_app            # Import function that creates and configures the Flask application.
from app.extensions import db         # Import database connection.
from app.models import Role, Permission, Admin, Category, Brand    # Import database models.


# List of system permissions.
# These define actions users can perform.
PERMISSIONS = [
    "manage_admins", 
    "manage_categories", 
    "manage_brands",
    "manage_products",
    "manage_orders", 
    "manage_delivery",
]


# Define system roles and their assigned permissions.
ROLES = {
    "super_admin": [],
    "catalog_manager": [
        "manage_categories",
        "manage_brands",
        "manage_products"
    ],
    "order_manager": [
        "manage_orders", 
        "manage_delivery"
    ],
}



# Function used to initialize database data.
def run():

    app = create_app()                    # Create Flask application.
    with app.app_context():               # Access application context to use database.
        db.create_all()                   # Create database tables if they do not exist.

        perms = {}                        # Create permissions in the database.
        for code in PERMISSIONS:          # Check if permission already exists, If not, create a new permission.
            
            perm = Permission.query.filter_by(code=code).first() or Permission(code=code)

            db.session.add(perm)

            perms[code] = perm             # Store permission object for later use.

        db.session.commit()


        # Create roles and assign permissions.
        for name, codes in ROLES.items():
            role = Role.query.filter_by(name=name).first() or Role(name=name)    # Find existing role or create a new one.
            role.permissions = [perms[c] for c in codes]                         # Assign permissions to the role.

            db.session.add(role)
        db.session.commit()


          # Create default admin account if it does not exist.
        if not Admin.query.filter_by(email="admin@example.com").first():
            admin = Admin(
                full_name="Super Admin", 
                email="admin@example.com",
                role=Role.query.filter_by(name="super_admin").first()
            )

            admin.set_password("ChangeMe123!")     # Set encrypted admin password.
            db.session.add(admin)


        # Create default product categories.
        for name in [
            "Electronics", 
            "Clothing", 
            "Home & Living"
        ]:
            
            # Add category only if it does not already exist.
            if not Category.query.filter_by(name=name).first():
                db.session.add(Category(name=name))

        # Create default product brands.
        for name in [
            "BreadWise Bakery", 
            "SunRise Bakes", 
            "Golden Grain"
        ]:
            
            # Add brand only if it does not already exist.
            if not Brand.query.filter_by(name=name).first():
                db.session.add(Brand(name=name))

        # Save all database changes.        
        db.session.commit()

        # Display completion message.
        print("Seed complete. admin@example.com / ChangeMe123!")

# Run seed function when this file is executed directly.
if __name__ == "__main__":
    run()
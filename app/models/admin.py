from app.extensions import db, bcrypt    # Imports the database instance and Bcrypt for password hashing.
from datetime import datetime  # Import datetime to record when admins are created/updated


# Creates a junction table for the many-to-many relationship between roles and permissions.
role_permissions = db.Table(
    "role_permissions",                                             # Name of the junction table.
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),      # Stores the ID of a role.
    db.Column("permission_id", db.Integer, db.ForeignKey("permissions.id"), primary_key=True),    # Stores the ID of a permission.
)     


# Represents user roles and their assigned permissions.
class Role(db.Model):                                               # Defines the Role model.
    __tablename__ = "roles"                                         # Database table name.
    id = db.Column(db.Integer, primary_key=True)                    # Unique identifier for each role.
    name = db.Column(db.String(50), unique=True, nullable=False)    # Stores the role name (e.g., Admin, Manager).
    permissions = db.relationship("Permission", secondary=role_permissions, lazy="joined")     # Links each role to its permissions.

    # Converts the role object into a dictionary.
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "permissions": [p.code for p in self.permissions]
        }



# Represents actions that a role is allowed to perform.
class Permission(db.Model):                                          # Defines the Permission model.
    __tablename__ = "permissions"                                    # Database table name.
    id = db.Column(db.Integer, primary_key=True)                     # Unique identifier for each permission.
    code = db.Column(db.String(80), unique=True, nullable=False)     # Stores the permission code (e.g., create_product).



# Represents administrator accounts, including authentication, role assignment, and password management
class Admin(db.Model):                                               # Defines the Admin model.
    __tablename__ = "admins"                                         # Database table name.
    id = db.Column(db.Integer, primary_key=True)                     # Unique identifier for each admin.
    full_name = db.Column(db.String(120))                            # Stores the admin's full name.
    email = db.Column(db.String(120), unique=True, nullable=False)   # Stores the admin's email address.
    password_hash = db.Column(db.String(255))                        # Stores the encrypted password.
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))       # References the admin's role.
    role = db.relationship("Role")                                   # Creates a relationship between Admin and Role.
    is_active = db.Column(db.Boolean, default=True)                  # Indicates whether the admin account is active.
    
    # TIMESTAMP FIELDS: Track when admin accounts are created and updated
    # Important for security audits - knowing when accounts were created/modified
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # Automatically set to current time when admin is created
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    # Automatically update to current time when admin info is modified

    def __init__(self, full_name=None, email=None, password_hash=None, role_id=None, role=None, is_active=True):
        self.full_name = full_name
        self.email = email
        if password_hash is not None:
            self.password_hash = password_hash
        self.role_id = role_id
        if role is not None:
            self.role = role
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
            "role": self.role.name if self.role else None,
            "is_active": self.is_active,
            # Include timestamps in the response
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
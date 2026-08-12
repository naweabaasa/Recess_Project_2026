"""
Quick script to create or reset your first admin account
"""
from app import create_app
from app.extensions import db
from app.models import Admin

app = create_app()

with app.app_context():
    # Check if any admin exists
    existing_admin = Admin.query.first()
    
    if existing_admin:
        print("\n" + "="*50)
        print("EXISTING ADMIN FOUND")
        print("="*50)
        print(f"Email: {existing_admin.email}")
        print(f"Name: {existing_admin.full_name}")
        print("\nResetting password to: admin123")
        
        existing_admin.set_password("admin123")
        db.session.commit()
        
        print("\n✅ Password reset successful!")
        print("\nYou can now login with:")
        print(f"  Email: {existing_admin.email}")
        print(f"  Password: admin123")
        print("="*50)
    else:
        print("\n" + "="*50)
        print("NO ADMIN FOUND - CREATING FIRST ADMIN")
        print("="*50)
        
        # Create first admin
        admin = Admin(
            full_name="System Admin",
            email="admin@breadwise.com",
            is_active=True
        )
        admin.set_password("admin123")
        
        db.session.add(admin)
        db.session.commit()
        
        print("\n✅ First admin created successfully!")
        print("\nYou can now login with:")
        print("  Email: admin@breadwise.com")
        print("  Password: admin123")
        print("\n⚠️  IMPORTANT: Change this password after first login!")
        print("="*50)

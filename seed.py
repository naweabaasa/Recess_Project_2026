# This script is a database seeding file.
# It prepares the application with initial data by creating database tables,
# creating a default admin account, and adding default product categories, brands,
# and all products shown in the frontend.

from app import create_app             # Import function that creates and configures the Flask application.
from app.extensions import db          # Import database connection.
from app.models import Admin, Category, Brand, Product, PageContent   # Import database models.


# ─── Categories ────────────────────────────────────────────────────────────────
CATEGORIES = ["Bread", "Donuts", "Muffins", "Cakes"]

# ─── Brands ────────────────────────────────────────────────────────────────────
BRANDS = ["BreadWise Bakery", "SunRise Bakes", "Golden Grain"]

# ─── Products (matches frontend /public/images/products/ paths) ────────────────
# Each entry: (name, category_name, image_url)
PRODUCTS = [
    # Bread
    ("White Loaf",          "Bread",   "/images/products/bread1.jpg"),
    ("Brown Bread",         "Bread",   "/images/products/bread2.jpg"),
    ("Wholegrain Loaf",     "Bread",   "/images/products/bread3.jpg"),
    ("Multigrain Bread",    "Bread",   "/images/products/bread4.png"),
    ("Sourdough Loaf",      "Bread",   "/images/products/bread5.png"),
    ("Seeded Bread",        "Bread",   "/images/products/bread6.png"),

    # Donuts
    ("Glazed Donut",        "Donuts",  "/images/products/donut4.jpg"),
    ("Chocolate Donut",     "Donuts",  "/images/products/donut9.jpg"),
    ("Sprinkle Donut",      "Donuts",  "/images/products/donut5.jpg"),
    ("Strawberry Donut",    "Donuts",  "/images/products/donut3.jpg"),
    ("Custard Donut",       "Donuts",  "/images/products/donut6.jpg"),
    ("Powdered Donut",      "Donuts",  "/images/products/donut7.jpg"),

    # Muffins
    ("Blueberry Muffin",    "Muffins", "/images/products/muffin2.jpg"),
    ("Chocolate Muffin",    "Muffins", "/images/products/muffin3.jpg"),
    ("Banana Muffin",       "Muffins", "/images/products/muffin4.jpg"),
    ("Vanilla Muffin",      "Muffins", "/images/products/muffin5.jpg"),
    ("Lemon Muffin",        "Muffins", "/images/products/muffin6.jpg"),
    ("Bran Muffin",         "Muffins", "/images/products/muffin7.jpg"),

    # Cakes
    ("Classic Celebration Cake", "Cakes", "/images/products/cake.jpg"),
    ("Vanilla Layer Cake",       "Cakes", "/images/products/cake1.jpg"),
    ("Chocolate Fudge Cake",     "Cakes", "/images/products/cake2.jpg"),
    ("Red Velvet Cake",          "Cakes", "/images/products/cake3.jpg"),
    ("Strawberry Shortcake",     "Cakes", "/images/products/cake4.jpg"),
    ("Carrot Cake",              "Cakes", "/images/products/cake5.jpg"),
]

# ─── Page Content (CMS Defaults) ───────────────────────────────────────────────
PAGE_CONTENT_DEFAULTS = [
    # Home Page
    ("home", "hero_kicker", "✦ Baked Fresh Every Day"),
    ("home", "hero_title", "A little <i>joy,</i><br /><span>fresh from the oven.</span>"),
    ("home", "hero_subtitle", "We bake with care for every celebration, every morning, and every special moment."),
    ("home", "info_kicker", "WHY CUSTOMERS LOVE US"),
    ("home", "info_title", "Warm bakes, thoughtful service, and a taste you will remember."),
    ("home", "info_desc", "Whether it is a family breakfast, a weekend treat, or a special celebration, we make every order feel personal and delicious."),
    
    # About Page
    ("about", "banner_title", "About Us"),
    ("about", "banner_subtitle", "Discover the story behind BreadWise Bakery and our passion for baking."),
    ("about", "story_title", "Our Story"),
    ("about", "story_p1", "BreadWise Bakery was founded with a simple mission: to bake bread that brings people together. What started as a small home bakery has grown into a trusted name known for quality, freshness and unforgettable taste."),
    ("about", "story_p2", "Every loaf we bake carries our promise of excellence and our love for good food."),
    ("about", "vision_text", "To be the most loved bakery known for inspiring moments of joy through quality baked goods."),
    ("about", "mission_text", "To bake and deliver wholesome, delicious products with honesty, care and passion."),
    
    # Contact Page
    ("contact", "banner_title", "Contact Us"),
    ("contact", "banner_subtitle", "Reach out for custom orders, delivery questions, or bakery inquiries."),
    ("contact", "contact_title", "We would love to hear from you"),
    ("contact", "contact_desc", "Whether you are planning a celebration or need fresh bakes for the week, our team is ready to help."),
    ("contact", "phone", "+256 771 385 851"),
    ("contact", "email", "info@breadwisebakery.com"),
    ("contact", "address", "123 Bakery Street, Freshville, Kampala, Uganda"),
]


def run():
    app = create_app()                    # Create Flask application.
    with app.app_context():               # Access application context to use database.
        db.create_all()                   # Create database tables if they do not exist.

        # ── Admin ──────────────────────────────────────────────────────────────
        if not Admin.query.filter_by(email="admin@example.com").first():
            admin = Admin(
                full_name="Super Admin",
                email="admin@example.com",
            )
            admin.set_password("ChangeMe123!")     # Set encrypted admin password.
            db.session.add(admin)
            db.session.flush()   # Flush so admin.id is available for products below
            admin_id = admin.id
        else:
            admin_id = Admin.query.filter_by(email="admin@example.com").first().id

        # ── Categories ────────────────────────────────────────────────────────
        for name in CATEGORIES:
            if not Category.query.filter_by(name=name).first():
                db.session.add(Category(name=name, status="active"))

        # ── Brands ────────────────────────────────────────────────────────────
        for name in BRANDS:
            if not Brand.query.filter_by(name=name).first():
                db.session.add(Brand(name=name, status="active"))

        db.session.flush()   # Flush so category IDs are available below

        # ── Products ──────────────────────────────────────────────────────────
        for name, cat_name, image_url in PRODUCTS:
            # Skip if this product already exists (prevents duplicates on re-run)
            if Product.query.filter_by(name=name).first():
                continue

            category = Category.query.filter_by(name=cat_name).first()
            brand    = Brand.query.filter_by(name="BreadWise Bakery").first()

            product = Product(
                name=name,
                category_id=category.id if category else None,
                brand_id=brand.id if brand else None,
                description=f"Freshly baked {name.lower()} made with the finest ingredients.",
                image_url=image_url,
                status="active",   # active so the public API returns them
                admin_id=admin_id,
            )
            db.session.add(product)

        # ── Page Content ──────────────────────────────────────────────────────
        for page_name, section_key, content in PAGE_CONTENT_DEFAULTS:
            if not PageContent.query.filter_by(page_name=page_name, section_key=section_key).first():
                db.session.add(PageContent(page_name=page_name, section_key=section_key, content=content))

        # ── Save everything ───────────────────────────────────────────────────
        db.session.commit()
        print("Seed complete!")
        print("   Admin login: admin@example.com / ChangeMe123!")
        print(f"   {len(PRODUCTS)} products seeded across {len(CATEGORIES)} categories.")


# Run seed function when this file is executed directly.
if __name__ == "__main__":
    run()
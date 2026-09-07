from app import create_app
from app.extensions import db
from app.models import PageContent

UPDATES = [
    # Home Page
    ("home", "hero_kicker", "Baked fresh, just for you"),
    ("home", "hero_title", "Taste the magic<br /><span>in every bite.</span>"),
    ("home", "hero_subtitle", "Enjoy our fresh bread, sweet cakes, and warm pastries. We bake everything daily to make your day a little brighter."),
    
    # About Page
    ("about", "banner_title", "Who We Are"),
    ("about", "banner_subtitle", "We believe a great day starts with fresh bread and a warm smile."),
    ("about", "story_title", "Our Story"),
    ("about", "story_p1", "BreadWise Bakery started in a small kitchen with a big dream: to bake food that brings people together. Today, we are proud to serve our community with the freshest baked goods made from simple, natural ingredients."),
    ("about", "story_p2", "Every loaf of bread and slice of cake is made by hand with love and care."),
    
    # Contact Page
    ("contact", "banner_title", "Say Hello"),
    ("contact", "banner_subtitle", "Need a custom cake or have a question? We would love to hear from you."),
    ("contact", "contact_title", "Let us bake for your next event"),
    ("contact", "contact_desc", "Whether it is a big party or just a weekend treat, our team is ready to bake something special for you."),
]

def run():
    app = create_app()
    with app.app_context():
        updated_count = 0
        for page_name, section_key, new_content in UPDATES:
            item = PageContent.query.filter_by(page_name=page_name, section_key=section_key).first()
            if item:
                item.content = new_content
                updated_count += 1
            else:
                db.session.add(PageContent(page_name=page_name, section_key=section_key, content=new_content))
                updated_count += 1
        
        db.session.commit()
        print(f"Successfully updated {updated_count} copy entries in the database!")

if __name__ == "__main__":
    run()

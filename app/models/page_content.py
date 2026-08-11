from app.extensions import db
from datetime import datetime

class PageContent(db.Model):
    """
    Stores editable content blocks for public pages (e.g., Home, About, Contact).
    """
    __tablename__ = "page_content"
    
    id = db.Column(db.Integer, primary_key=True)
    page_name = db.Column(db.String(50), nullable=False)    # e.g., 'home', 'about', 'contact'
    section_key = db.Column(db.String(100), nullable=False) # e.g., 'hero_title', 'mission_statement'
    content = db.Column(db.Text, nullable=False)            # The actual text or image URL
    
    # Ensures we don't have duplicate keys for a single page
    __table_args__ = (db.UniqueConstraint('page_name', 'section_key', name='_page_section_uc'),)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, page_name, section_key, content):
        self.page_name = page_name
        self.section_key = section_key
        self.content = content

    def to_dict(self):
        return {
            "id": self.id,
            "page_name": self.page_name,
            "section_key": self.section_key,
            "content": self.content,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

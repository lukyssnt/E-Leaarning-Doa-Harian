from app import db
from datetime import datetime

class Module(db.Model):
    __tablename__ = 'modules'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)  # Main course content/material
    file_url = db.Column(db.String(255))  # URL for audio/video/PDF
    order = db.Column(db.Integer, default=1)
    status = db.Column(db.String(20), default='draft')  # draft, published
    duration_minutes = db.Column(db.Integer)
    learning_objectives = db.Column(db.Text)  # JSON or comma-separated
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    assessments = db.relationship('Assessment', backref='module', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Module {self.title}>'
    
    def is_published(self):
        return self.status == 'published'

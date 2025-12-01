from app import db
from datetime import datetime

class Assessment(db.Model):
    __tablename__ = 'assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    assessment_type = db.Column(db.String(50), nullable=False)  # quiz, assignment, submission
    questions = db.Column(db.Text)  # JSON format for quiz questions
    instructions = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    max_score = db.Column(db.Float, default=100.0)
    is_graded = db.Column(db.Boolean, default=True)
    allow_multiple_attempts = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='draft')  # draft, published
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    results = db.relationship('Result', backref='assessment', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Assessment {self.title}>'
    
    def is_published(self):
        return self.status == 'published'

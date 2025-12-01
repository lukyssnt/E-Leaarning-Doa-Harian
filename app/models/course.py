from app import db
from datetime import datetime

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='draft', nullable=False)  # draft, published, archived
    image_url = db.Column(db.String(255))
    category = db.Column(db.String(100))
    duration_weeks = db.Column(db.Integer)
    level = db.Column(db.String(50), default='beginner')  # beginner, intermediate, advanced
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    modules = db.relationship('Module', backref='course', lazy=True, cascade='all, delete-orphan')
    assessments = db.relationship('Assessment', backref='course', lazy=True, cascade='all, delete-orphan')
    enrollments = db.relationship('Enrollment', backref='course', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Course {self.title}>'
    
    def is_published(self):
        return self.status == 'published'
    
    def get_progress(self, user_id):
        """Calculate course progress for a user"""
        # Get enrollment
        enrollment = self.enrollments
        user_enrollment = None
        for e in enrollment:
            if e.user_id == user_id:
                user_enrollment = e
                break
        
        if not user_enrollment:
            return 0
        
        # Return the progress_percentage from enrollment
        return user_enrollment.progress_percentage if user_enrollment.progress_percentage else 0

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    progress_percentage = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='active')  # active, completed, dropped
    
    __table_args__ = (db.UniqueConstraint('user_id', 'course_id', name='uq_user_course'),)
    
    def __repr__(self):
        return f'<Enrollment user_id={self.user_id} course_id={self.course_id}>'

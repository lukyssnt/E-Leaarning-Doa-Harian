from app import db
from datetime import datetime

class Result(db.Model):
    __tablename__ = 'results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    score = db.Column(db.Float)
    max_score = db.Column(db.Float, default=100.0)
    percentage = db.Column(db.Float)
    submission_file_url = db.Column(db.String(255))  # For assignments/submissions
    submission_text = db.Column(db.Text)  # Text responses
    status = db.Column(db.String(20), default='pending')  # pending, graded, submitted
    feedback = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    graded_at = db.Column(db.DateTime)
    attempt_number = db.Column(db.Integer, default=1)
    
    __table_args__ = (db.Index('idx_user_assessment', 'user_id', 'assessment_id'),)
    
    def __repr__(self):
        return f'<Result user_id={self.user_id} assessment_id={self.assessment_id}>'
    
    def is_passed(self, passing_score=70):
        """Check if result passed based on percentage"""
        if self.percentage is None:
            return False
        return self.percentage >= passing_score

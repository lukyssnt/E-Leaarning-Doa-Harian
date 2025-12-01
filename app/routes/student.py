from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.course import Course, Enrollment
from app.models.module import Module
from app.models.assessment import Assessment
from app.models.result import Result
from functools import wraps

student_bp = Blueprint('student', __name__, url_prefix='/student')

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_student():
            flash('Akses ditolak. Anda harus login sebagai siswa.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    enrollments = Enrollment.query.filter_by(user_id=current_user.id, status='active').all()

    # Build list of courses with precomputed progress to avoid DB calls in templates
    courses_with_progress = []
    for e in enrollments:
        course = e.course
        progress = e.progress_percentage if e.progress_percentage is not None else 0.0
        courses_with_progress.append({'course': course, 'progress': progress})

    # Calculate stats
    total_courses = len(courses_with_progress)
    completed_assessments = Result.query.filter_by(user_id=current_user.id, status='graded').count()

    stats = {
        'total_courses': total_courses,
        'completed_assessments': completed_assessments,
        'active_enrollments': total_courses
    }

    return render_template('student/dashboard.html', courses=courses_with_progress, stats=stats)

@student_bp.route('/course/<int:course_id>')
@login_required
@student_required
def course(course_id):
    course = Course.query.get_or_404(course_id)
    
    # Check enrollment
    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first()
    if not enrollment:
        flash('Anda belum terdaftar di kursus ini.', 'warning')
        return redirect(url_for('student.dashboard'))
    
    modules = Module.query.filter_by(course_id=course_id, status='published').order_by(Module.order).all()
    
    return render_template('student/course.html', course=course, modules=modules, enrollment=enrollment)

@student_bp.route('/module/<int:module_id>')
@login_required
@student_required
def module(module_id):
    module = Module.query.get_or_404(module_id)
    course = module.course
    
    # Check enrollment in course
    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course.id).first()
    if not enrollment:
        flash('Anda belum terdaftar di kursus ini.', 'warning')
        return redirect(url_for('student.dashboard'))
    
    assessments = Assessment.query.filter_by(module_id=module_id, status='published').all()
    
    return render_template('student/module.html', module=module, course=course, assessments=assessments)

@student_bp.route('/assessment/<int:assessment_id>', methods=['GET', 'POST'])
@login_required
@student_required
def assessment(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    module = assessment.module
    course = module.course
    
    # Check enrollment
    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course.id).first()
    if not enrollment:
        flash('Anda belum terdaftar di kursus ini.', 'warning')
        return redirect(url_for('student.dashboard'))
    
    # Check existing submission
    existing_result = Result.query.filter_by(
        user_id=current_user.id,
        assessment_id=assessment_id
    ).first()
    
    if request.method == 'POST':
        if existing_result and not assessment.allow_multiple_attempts:
            flash('MashaAllah, Anda sudah mengerjakan assessment ini.', 'warning')
            return redirect(url_for('student.module', module_id=module.id))
        
        submission_text = request.form.get('submission_text', '')
        
        result = Result(
            user_id=current_user.id,
            assessment_id=assessment_id,
            submission_text=submission_text,
            status='submitted'
        )
        
        db.session.add(result)
        db.session.commit()
        
        flash('Alhamdulillah, sudah dikerjakan. Semoga usaha ini bermanfaat dan diterima.', 'success')
        return redirect(url_for('student.module', module_id=module.id))
    
    return render_template('student/assessment.html', 
                         assessment=assessment, 
                         module=module,
                         course=course,
                         existing_result=existing_result)

@student_bp.route('/progress')
@login_required
@student_required
def progress():
    enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
    
    progress_data = []
    for enrollment in enrollments:
        course = enrollment.course
        modules = Module.query.filter_by(course_id=course.id).count()
        assessments = Assessment.query.filter_by(course_id=course.id).count()
        completed = Result.query.filter_by(
            user_id=current_user.id
        ).join(Assessment).filter(Assessment.course_id == course.id).count()
        
        progress_data.append({
            'course': course,
            'enrollment': enrollment,
            'modules': modules,
            'assessments': assessments,
            'completed_assessments': completed
        })
    
    return render_template('student/progress.html', progress_data=progress_data)

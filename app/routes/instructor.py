from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.course import Course, Enrollment
from app.models.module import Module
from app.models.assessment import Assessment
from app.models.result import Result
from functools import wraps

instructor_bp = Blueprint('instructor', __name__, url_prefix='/instructor')

def instructor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_instructor():
            flash('Akses ditolak. Anda harus login sebagai instruktur.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@instructor_bp.route('/course/create', methods=['GET', 'POST'])
@login_required
@instructor_required
def create_course():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        level = request.form.get('level', 'beginner')
        status = request.form.get('status', 'draft')
        
        course = Course(
            title=title,
            description=description,
            instructor_id=current_user.id,
            category=category,
            level=level,
            status=status
        )
        
        db.session.add(course)
        db.session.commit()
        
        flash('Alhamdulillah, kursus berhasil dibuat! Semoga bermanfaat bagi peserta.', 'success')
        return redirect(url_for('instructor.manage_course', course_id=course.id))
    
    return render_template('instructor/create_course.html')

@instructor_bp.route('/dashboard')
@login_required
@instructor_required
def dashboard():
    courses = Course.query.filter_by(instructor_id=current_user.id).all()
    
    stats = {
        'total_courses': len(courses),
        'published_courses': sum(1 for c in courses if c.is_published()),
        'total_students': sum(len(c.enrollments) for c in courses),
        'pending_reviews': Result.query.filter_by(status='submitted').count()
    }
    
    return render_template('instructor/dashboard.html', courses=courses, stats=stats)

def create_course():
    pass

@instructor_bp.route('/course/<int:course_id>/manage', methods=['GET', 'POST'])
@login_required
@instructor_required
def manage_course(course_id):
    course = Course.query.get_or_404(course_id)
    
    # Check ownership
    if course.instructor_id != current_user.id:
        flash('Anda tidak memiliki akses ke kursus ini.', 'danger')
        return redirect(url_for('instructor.dashboard'))
    
    if request.method == 'POST':
        course.title = request.form.get('title', course.title)
        course.description = request.form.get('description', course.description)
        course.category = request.form.get('category', course.category)
        course.level = request.form.get('level', course.level)
        course.status = request.form.get('status', course.status)
        
        db.session.commit()
        flash('Alhamdulillah, perubahan tersimpan. Semoga berkah untuk pengajaran Anda.', 'success')
        return redirect(url_for('instructor.manage_course', course_id=course_id))
    
    modules = Module.query.filter_by(course_id=course_id).order_by(Module.order).all()
    enrollments = Enrollment.query.filter_by(course_id=course_id).all()
    
    return render_template('instructor/manage_course.html', 
                         course=course, 
                         modules=modules,
                         enrollments=enrollments)

@instructor_bp.route('/module/create/<int:course_id>', methods=['GET', 'POST'])
@login_required
@instructor_required
def create_module(course_id):
    course = Course.query.get_or_404(course_id)
    
    # Check ownership
    if course.instructor_id != current_user.id:
        flash('Anda tidak memiliki akses ke kursus ini.', 'danger')
        return redirect(url_for('instructor.dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        content = request.form.get('content')
        duration_minutes = request.form.get('duration_minutes', type=int)
        status = request.form.get('status', 'draft')
        
        # Get max order
        max_order = db.session.query(db.func.max(Module.order)).filter_by(course_id=course_id).scalar() or 0
        
        module = Module(
            course_id=course_id,
            title=title,
            description=description,
            content=content,
            duration_minutes=duration_minutes,
            status=status,
            order=max_order + 1
        )
        
        db.session.add(module)
        db.session.commit()
        
        flash('Alhamdulillah, modul berhasil dibuat! Semoga mempermudah proses hafalan.', 'success')
        return redirect(url_for('instructor.manage_course', course_id=course_id))
    
    return render_template('instructor/create_module.html', course=course)

@instructor_bp.route('/assessment/create/<int:module_id>', methods=['GET', 'POST'])
@login_required
@instructor_required
def create_assessment(module_id):
    module = Module.query.get_or_404(module_id)
    course = module.course
    
    # Check ownership
    if course.instructor_id != current_user.id:
        flash('Anda tidak memiliki akses ke kursus ini.', 'danger')
        return redirect(url_for('instructor.dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        assessment_type = request.form.get('assessment_type', 'assignment')
        instructions = request.form.get('instructions')
        max_score = request.form.get('max_score', 100, type=float)
        status = request.form.get('status', 'draft')
        
        assessment = Assessment(
            module_id=module_id,
            course_id=course.id,
            title=title,
            description=description,
            assessment_type=assessment_type,
            instructions=instructions,
            max_score=max_score,
            status=status
        )
        
        db.session.add(assessment)
        db.session.commit()
        
        flash('Alhamdulillah, penilaian berhasil dibuat! Semoga adil dan bermanfaat.', 'success')
        return redirect(url_for('instructor.manage_course', course_id=course.id))
    
    return render_template('instructor/create_assessment.html', module=module, course=course)

@instructor_bp.route('/assessment/review')
@login_required
@instructor_required
def review_submissions():
    # Get all submissions for courses taught by this instructor
    courses = Course.query.filter_by(instructor_id=current_user.id).all()
    course_ids = [c.id for c in courses]
    
    submissions = Result.query.join(Assessment).filter(
        Assessment.course_id.in_(course_ids),
        Result.status.in_(['submitted', 'pending'])
    ).all()
    
    return render_template('instructor/review_submissions.html', submissions=submissions)

@instructor_bp.route('/review/submit/<int:result_id>', methods=['GET', 'POST'])
@login_required
@instructor_required
def grade_submission(result_id):
    result = Result.query.get_or_404(result_id)
    assessment = result.assessment
    course = assessment.course
    
    # Check ownership
    if course.instructor_id != current_user.id:
        flash('Anda tidak memiliki akses ke penilaian ini.', 'danger')
        return redirect(url_for('instructor.dashboard'))
    
    if request.method == 'POST':
        score = request.form.get('score', type=float)
        feedback = request.form.get('feedback', '')
        
        result.score = score
        result.percentage = (score / result.max_score) * 100
        result.feedback = feedback
        result.status = 'graded'
        
        db.session.commit()
        
        flash('Alhamdulillah, nilai tersimpan. Semoga menjadi amal yang terus bermanfaat.', 'success')
        return redirect(url_for('instructor.review_submissions'))
    
    return render_template('instructor/grade_submission.html', result=result)

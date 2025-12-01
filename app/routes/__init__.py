from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.course import Course
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Akses ditolak. Anda harus login sebagai admin.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    users = User.query.all()
    courses = Course.query.all()
    
    stats = {
        'total_users': len(users),
        'total_students': sum(1 for u in users if u.is_student()),
        'total_instructors': sum(1 for u in users if u.is_instructor()),
        'total_courses': len(courses),
        'published_courses': sum(1 for c in courses if c.is_published())
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/manage/users')
@login_required
@admin_required
def manage_users():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20)
    
    return render_template('admin/manage_users.html', users=users)

@admin_bp.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.full_name = request.form.get('full_name', user.full_name)
        user.email = request.form.get('email', user.email)
        user.role = request.form.get('role', user.role)
        user.is_active = request.form.get('is_active') == 'on'
        
        db.session.commit()
        flash('Pengguna berhasil diperbarui!', 'success')
        return redirect(url_for('admin.manage_users'))
    
    return render_template('admin/edit_user.html', user=user)

@admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    if user_id == current_user.id:
        flash('Anda tidak bisa menghapus akun sendiri.', 'danger')
        return redirect(url_for('admin.manage_users'))
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    flash(f'Pengguna {user.username} berhasil dihapus!', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/manage/courses')
@login_required
@admin_required
def manage_courses():
    page = request.args.get('page', 1, type=int)
    courses = Course.query.paginate(page=page, per_page=20)
    
    return render_template('admin/manage_courses.html', courses=courses)

@admin_bp.route('/course/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_course():
    instructors = User.query.filter_by(role='instructor').all()
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        instructor_id = request.form.get('instructor_id', type=int)
        category = request.form.get('category')
        level = request.form.get('level', 'beginner')
        status = request.form.get('status', 'draft')
        
        course = Course(
            title=title,
            description=description,
            instructor_id=instructor_id,
            category=category,
            level=level,
            status=status
        )
        
        db.session.add(course)
        db.session.commit()
        
        flash('Kursus berhasil dibuat!', 'success')
        return redirect(url_for('admin.manage_courses'))
    
    return render_template('admin/create_course.html', instructors=instructors)

@admin_bp.route('/course/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    instructors = User.query.filter_by(role='instructor').all()
    
    if request.method == 'POST':
        course.title = request.form.get('title', course.title)
        course.description = request.form.get('description', course.description)
        course.instructor_id = request.form.get('instructor_id', course.instructor_id, type=int)
        course.category = request.form.get('category', course.category)
        course.level = request.form.get('level', course.level)
        course.status = request.form.get('status', course.status)
        
        db.session.commit()
        flash('Kursus berhasil diperbarui!', 'success')
        return redirect(url_for('admin.manage_courses'))
    
    return render_template('admin/edit_course.html', course=course, instructors=instructors)

@admin_bp.route('/course/<int:course_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    
    flash(f'Kursus {course.title} berhasil dihapus!', 'success')
    return redirect(url_for('admin.manage_courses'))

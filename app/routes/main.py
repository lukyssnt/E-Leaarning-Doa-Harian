from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index')
def index():
    from flask import render_template
    from flask_login import current_user
    
    if current_user.is_authenticated:
        if current_user.is_admin():
            from flask import redirect, url_for
            return redirect(url_for('admin.dashboard'))
        elif current_user.is_instructor():
            from flask import redirect, url_for
            return redirect(url_for('instructor.dashboard'))
        else:
            from flask import redirect, url_for
            return redirect(url_for('student.dashboard'))
    
    return render_template('index.html')

@main_bp.route('/about')
def about():
    from flask import render_template
    return render_template('about.html')

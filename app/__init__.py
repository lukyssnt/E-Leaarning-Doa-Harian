from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import DevelopmentConfig

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Silahkan login terlebih dahulu.'
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.student import student_bp
    from app.routes.instructor import instructor_bp
    from app.routes.admin import admin_bp
    from app.routes.main import main_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(instructor_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()

    # Context processor: provide commonly used Islamic phrases
    @app.context_processor
    def islamic_phrases():
        return {
            'PHRASE_ALHAMDULILLAH': 'Alhamdulillah, semoga usaha ini bermanfaat dan diterima.',
            'PHRASE_BISMILLAH_PROMPT': 'Yok berdoa dulu sebelum mengerjakan. Semoga Allah memudahkan.' ,
            'PHRASE_MASHALLAH_ALREADY': 'MashaAllah, Anda telah mengumpulkan tugas ini sebelumnya.'
        }
    
    return app

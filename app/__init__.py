"""
This file initializes the Flask application and sets up the database connection using SQLAlchemy.
"""

import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
csrf = CSRFProtect()
mail = Mail()
login_manager = LoginManager()


def create_app(test_config=None):
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///NewsSentimentDB.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = 2592000  # 30 days

    # Email configuration - DEVELOPMENT (disabled)
    app.config['MAIL_SERVER'] = None
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = None
    app.config['MAIL_PASSWORD'] = None
    app.config['MAIL_DEFAULT_SENDER'] = 'noreply@example.com'

    # Override with test config if provided
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    migrate = Migrate(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "users.login"
    login_manager.session_protection = "strong"

    # Register models
    from app.models.user import User
    from app.models.article import Article
    from app.models.comment import Comment

    # Register blueprints
    from app.routes.users import users_bp
    app.register_blueprint(users_bp)

    from app.routes.competitor import competitor_bp
    app.register_blueprint(competitor_bp)

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    from app.routes.comments import comments_bp
    app.register_blueprint(comments_bp)

    from app.routes.upload import upload_bp
    app.register_blueprint(upload_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    return app
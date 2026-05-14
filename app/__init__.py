"""
This file initializes the Flask application and sets up the database connection using SQLAlchemy.
It also imports the necessary routes and models to be used in the application.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_mail import Mail

db = SQLAlchemy()
csrf = CSRFProtect()   # Enable CSRF protection
mail = Mail()

# Function to create and configure the Flask application
def create_app():
    # Create a new Flask application instance
    app = Flask(__name__)

    # Configure the application with necessary settings
    app.config['SECRET_KEY'] = "mysecretkey"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///NewsSentimentDB.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = 2592000  # 30 days
    
    # Email configuration - PRODUCTION EXAMPLE (Gmail)
    # app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    # app.config['MAIL_PORT'] = 587
    # app.config['MAIL_USE_TLS'] = True
    # app.config['MAIL_USE_SSL'] = False
    # app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
    # app.config['MAIL_PASSWORD'] = 'your-app-password'  # Use App Password, not regular password
    # app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'
    
    # Email configuration - DEVELOPMENT (disabled)
    app.config['MAIL_SERVER'] = None  # Disable email sending
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = None
    app.config['MAIL_PASSWORD'] = None
    app.config['MAIL_DEFAULT_SENDER'] = 'noreply@example.com'

    # Initialize the database with the application
    db.init_app(app)
    csrf.init_app(app)   # Attach CSRF protection to the app
    mail.init_app(app)   # Initialize Flask-Mail

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

    return app
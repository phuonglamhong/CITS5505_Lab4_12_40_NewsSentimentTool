"""
This file initializes the Flask application and sets up the database connection using SQLAlchemy.
It also imports the necessary routes and models to be used in the application.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()   # Enable CSRF protection

# Function to create and configure the Flask application
def create_app():
    # Create a new Flask application instance
    app = Flask(__name__)

    # Configure the application with necessary settings
    app.config['SECRET_KEY'] = "mysecretkey"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///NewsSentimentDB.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the application
    db.init_app(app)
    csrf.init_app(app)   # Attach CSRF protection to the app

    # Register models
    from app.models.user import User
    from app.models.article import Article
    from app.models.comment import Comment

    # Register blueprints
    from app.routes.users import users_bp
    app.register_blueprint(users_bp)

    from app.routes.comments import comments_bp
    app.register_blueprint(comments_bp)

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    from app.routes.competitor import competitor_bp
    app.register_blueprint(competitor_bp)



    return app

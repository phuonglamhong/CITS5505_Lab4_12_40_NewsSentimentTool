from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "mysecretkey"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///NewsSentimentDB.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    csrf.init_app(app)

    # Register models
    from app.models.user import User
    from app.models.article import Article
    from app.models.comment import Comment

    # Register blueprints
    from app.routes.users import users_bp
    app.register_blueprint(users_bp)

    from app.routes.competitor import competitor_bp
    app.register_blueprint(competitor_bp)

    from app.routes.comments import comments_bp
    app.register_blueprint(comments_bp)

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    return app

# This file defines the database models for the application. 
# It uses SQLAlchemy, which is a popular Object-Relational Mapping (ORM) library for Python. 
# The User model represents the users of the application, storing their name, email, role, and password.
from app import db
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

# ---------- User model ----------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}, salt='password-reset')

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, salt='password-reset', max_age=expires_sec)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)


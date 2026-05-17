# This file defines the database models for the application. 
# It uses SQLAlchemy, which is a popular Object-Relational Mapping (ORM) library for Python. 
# The User model represents the users of the application, storing their name, email, role, and password.
from app import db
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from flask_login import UserMixin

# User model 
class User(db.Model, UserMixin):
    # Database table name
    __tablename__ = "users"

    # Unique user ID
    id = db.Column(db.Integer, primary_key=True)
    # Stores full name of the user
    name = db.Column(db.String(100), nullable=False)
    # Stores unique email address for login/authentication
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Stores user role such as admin or analyst
    role = db.Column(db.String(50), nullable=False)
    # Generates secure password reset token
    password = db.Column(db.String(200), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        # Serializer uses Flask secret key
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        # Encode user ID inside token
        return s.dumps({'user_id': self.id}, salt='password-reset')

     # Verifies password reset token validity
    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        
        try:
            # Decode token and extract user ID
            user_id = s.loads(token, salt='password-reset', max_age=expires_sec)['user_id']
        except Exception:
            # Return None if token invalid or expired
            return None
        # Return matching user from database
        return User.query.get(user_id)


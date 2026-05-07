# This file defines the database models for the application. 
# It uses SQLAlchemy, which is a popular Object-Relational Mapping (ORM) library for Python. 
# The User model represents the users of the application, storing their name, email, role, and password.
from app import db

# ---------- User model ----------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
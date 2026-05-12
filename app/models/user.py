"""
This file defines the routes related to user authentication and registration.
It uses Flask's Blueprint to organize the routes under a common prefix.
The routes include:
- "/" for rendering the login page
- "/register" for handling user registration
- "/login" for handling user login
- "/logout" for handling user logout
- "/dashboard" for rendering the user dashboard (protected route)

The registration route validates the email format and checks for existing users
before creating a new user with a hashed password. The login route checks the
provided credentials against the stored user data.

CSRF protection is enabled globally using Flask-WTF's CSRFProtect.
AJAX requests must include the "X-CSRFToken" header.
"""

from flask import (
    Blueprint, render_template, request, jsonify,
    session, url_for, redirect
)
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db
import re

# Blueprint for user-related routes
users_bp = Blueprint("users", __name__)

# ---------- Routes ----------
# Route for rendering the login page
@users_bp.route("/")
def index():
    return render_template("login.html")

# Route for user registration
@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    role = data.get("role")
    password = data.get("password")

    # Validate email format
    email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not re.match(email_regex, email):
        return jsonify({"status": "error", "message": "Invalid email format."})

    # Check if email exists
    existing = User.query.filter_by(email=email).first()
    if existing:
        return jsonify({"status": "error", "message": "Email already registered."})

    # Create hashed password
    hashed_pw = generate_password_hash(password)

    # Create user
    new_user = User(
        name=name,
        email=email,
        role=role,
        password=hashed_pw
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"status": "success", "message": "Account created!"})

# Route for user login
@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["user_name"] = user.name
        return jsonify({"redirect": url_for("main.dashboard")})
    else:
        return jsonify({"status": "error", "message": "Invalid email or password."})

# Route for user logout
@users_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("users.index"))



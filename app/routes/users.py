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
    Blueprint, render_template, request, session,
    url_for, redirect
)
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.forms import (
    LoginForm, RegistForm, ResetPassRequestForm,
    ResetPassForm, ChangePassForm, DeleteAccountForm
)
from app import db
from datetime import timedelta

# Blueprint for user-related routes
users_bp = Blueprint("users", __name__)

# ---------- Routes ----------
# Route for rendering the login page
@users_bp.route("/")
def index():
    return render_template(
        "login.html",
        login_form=LoginForm(),
        register_form=RegistForm(),
        register_success=None,
        active_tab="signin"
    )


# ---------- REGISTER ----------
@users_bp.route("/register", methods=["POST"])
def register():
    form = RegistForm()

    if not form.validate_on_submit():
        # Re-render page with form errors
        return render_template(
            "login.html",
            login_form=LoginForm(),
            register_form=form,
            register_success=None,
            active_tab="register"
        )

    # Extract data
    name = form.name.data
    email = form.email.data
    role = form.role.data
    password = form.password.data

    # Check existing user
    if User.query.filter_by(email=email).first():
        form.email.errors.append("Email already registered.")
        return render_template(
            "login.html",
            login_form=LoginForm(),
            register_form=form,
            register_success=None,
            active_tab="register"
        )

    # Create user
    hashed_pw = generate_password_hash(password)
    new_user = User(name=name, email=email, role=role, password=hashed_pw)

    db.session.add(new_user)
    db.session.commit()

    # Re-render login page with success alert
    return render_template(
        "login.html",
        login_form=LoginForm(),
        register_form=RegistForm(),
        register_success="Account created successfully!",
        active_tab="register"
    )


# ---------- LOGIN ----------
@users_bp.route("/login", methods=["POST"])
def login():
    form = LoginForm()

    if not form.validate_on_submit():
        return render_template(
            "login.html",
            login_form=form,
            register_form=RegistForm(),
            register_success=None,
            active_tab="signin"
        )

    email = form.email.data
    password = form.password.data
    remember_me = form.remember_me.data

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        form.email.errors.append("Invalid email or password.")
        return render_template(
            "login.html",
            login_form=form,
            register_form=RegistForm(),
            register_success=None
        )

    # Login success
    session["user_id"] = user.id
    session["user_name"] = user.name

    if remember_me:
        session.permanent = True
        users_bp.permanent_session_lifetime = timedelta(days=30)

    return redirect(url_for("users.dashboard"))


# ---------- LOGOUT ----------
@users_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("users.index"))


# ---------- DASHBOARD ----------
@users_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("users.index"))
    return render_template("dashboard.html")

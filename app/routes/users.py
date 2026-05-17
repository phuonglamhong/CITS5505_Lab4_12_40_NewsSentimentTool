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
    url_for, redirect, current_app
)
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.forms import (
    LoginForm, RegistForm, ResetPassRequestForm,
    ResetPassForm, ChangePassForm, DeleteAccountForm
)
from app import db, mail
from datetime import timedelta
from flask_mail import Message
from flask import flash
from flask_login import login_user, logout_user, login_required, current_user

# Blueprint for grouping all user authentication related routes
users_bp = Blueprint("users", __name__)

# Routes
# Route for rendering the login page
@users_bp.route("/")
def index():
    return render_template("welcome.html")

# ---------- USER LOGIN ----------
# Authenticates user credentials.
@users_bp.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    # If GET or invalid POST → show login page
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

    # Invalid credentials
    if not user or not check_password_hash(user.password, password):
        form.email.errors.append("Invalid email or password.")
        return render_template(
            "login.html",
            login_form=form,
            register_form=RegistForm(),
            register_success=None
        )

    # Store user ID in session for authentication using flask-login
    login_user(user, remember=remember_me)

    # handle ?next=/upload
    next_page = request.args.get("next")
    if next_page:
        return redirect(next_page)

    # Default redirect
    return redirect(url_for("users.index"))

# ---------- REGISTER ----------
# Handles new user registration.
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

    # Extract validated form data
    name = form.name.data
    email = form.email.data
    role = form.role.data
    password = form.password.data

    # Prevent duplicate accounts - for existing user
    if User.query.filter_by(email=email).first():
        form.email.errors.append("Email already registered.")
        return render_template(
            "login.html",
            login_form=LoginForm(),
            register_form=form,
            register_success=None,
            active_tab="register"
        )

     # Secure password storage using hashing
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

# ---------- LOGOUT ----------
# Clears all session data and logs out the user.
@users_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("users.index"))

# ---------- PASSWORD RESET REQUEST ----------
# Handles password reset requests.
@users_bp.route("/reset_password", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("users.index"))
    
    form = ResetPassRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_reset_token()
            reset_url = url_for('users.reset_password', token=token, _external=True)
            
            # Check if email is configured
            if current_app.config.get('MAIL_SERVER'):
                msg = Message(
                    'Password Reset Request',
                    sender='noreply@example.com',
                    recipients=[user.email]
                )
                msg.body = f'''To reset your password, visit the following link:
{reset_url}

If you did not make this request then simply ignore this email and no changes will be made.
'''
                mail.send(msg)
            else:
                # Email not configured - show reset link directly (for development)
                return render_template("reset_password_request.html", 
                                     form=ResetPassRequestForm(),
                                     success=f"Email not configured. For development, use this reset link: <a href='{reset_url}'>{reset_url}</a>")
        
        # Always show success message to prevent email enumeration (only when email is configured or no user found)
        return render_template("reset_password_request.html", 
                             form=ResetPassRequestForm(),
                             success="If an account with that email exists, a password reset link has been sent.")
    
    return render_template("reset_password_request.html", form=form)


# ---------- PASSWORD RESET ----------
# Allows user to set a new password using a secure token.
@users_bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if not current_user.is_authenticated:
        return redirect(url_for("users.index"))
    
    user = User.verify_reset_token(token)
    if not user:
        return render_template("reset_password.html", 
                             form=ResetPassForm(),
                             error="That is an invalid or expired token")
    
    form = ResetPassForm()
    if form.validate_on_submit():
        # Check if new password is the same as current password
        if check_password_hash(user.password, form.password.data):
            form.password.errors.append("New password cannot be the same as your current password.")
            return render_template("reset_password.html", form=form)
        
        hashed_password = generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        return render_template("reset_password.html", 
                             form=ResetPassForm(),
                             success="Your password has been updated! You can now log in.")
    
    return render_template("reset_password.html", form=form)

@users_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePassForm()
    user = current_user

    if form.validate_on_submit():
        # Check old password
        if not check_password_hash(user.password, form.old_password.data):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for("users.change_password"))

        # Update password
        user.password = generate_password_hash(form.new_password.data)
        db.session.commit()

        # Log out user after password change
        logout_user()

        # Show success message on the same page
        flash("Password updated successfully! Please log in again.", "success")

        # Render the same page with a button to sign in
        return render_template("change_password.html", form=ChangePassForm(), show_login_button=True)

    return render_template("change_password.html", form=form)

@users_bp.route("/delete-account", methods=["GET", "POST"])
@login_required
def delete_account():
    form = DeleteAccountForm()
    user = current_user

    if form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()

        flash("Your account has been permanently deleted.", "success")
        return redirect(url_for("users.login"))

    form = DeleteAccountForm()
    user = current_user

    return render_template("delete_account.html", form=form)

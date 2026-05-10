"""
forms.py - Defines form classes for user authentication and account management.
This module uses Flask-WTF and WTForms to create forms for login, registration, password reset, and account deletion. 
Each form includes appropriate fields and validation rules to ensure data integrity and user input correctness. 
The forms are designed to be rendered in the application's templates, providing a consistent user interface for authentication-related actions.
"""
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, BooleanField, SelectField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length
)

# Define role choices for the registration form
ROLE_CHOICES = [
    ("analyst", "Analyst"),
    ("manager", "Manager"),
    ("viewer", "Viewer")
]

# ---------- Form Classes ----------
# Each form class corresponds to a specific user action, such as logging in, registering, or resetting a password.

# Login form for user authentication
class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Enter a valid email address.")]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(message="Password is required.")]
    )
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

# Registration form for new users
class RegistForm(FlaskForm):
    name = StringField(
        "Full Name",
        validators=[
            DataRequired(message="Full name is required."),
            Length(min=5, max=20, message="Name must be between 5 and 20 characters.")
        ]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Enter a valid email address.")]
    )
    role = SelectField(
        "Role",
        choices=ROLE_CHOICES,
        validators=[DataRequired()]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters long.")
        ]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match.")
        ]
    )
    submit = SubmitField("Create Account")

# Form for requesting a password reset link
class ResetPassRequestForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Enter a valid email address.")]
    )
    submit = SubmitField("Send Reset Link")

# Form for resetting the password using a token
class ResetPassForm(FlaskForm):
    password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters long.")
        ]
    )
    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match.")
        ]
    )
    submit = SubmitField("Reset Password")

# Form for changing the password while logged in
class ChangePassForm(FlaskForm):
    old_password = PasswordField(
        "Current Password",
        validators=[DataRequired()]
    )
    new_password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters long.")
        ]
    )
    confirm_new_password = PasswordField(
        "Confirm New Password",
        validators=[
            DataRequired(),
            EqualTo("new_password", message="Passwords must match.")
        ]
    )
    submit = SubmitField("Update Password")

# Form for confirming account deletion
class DeleteAccountForm(FlaskForm):
    confirm = BooleanField(
        "I understand this decision cannot be undone.",
        validators=[DataRequired(message="You must confirm to continue.")]
    )
    submit = SubmitField("Delete Account")
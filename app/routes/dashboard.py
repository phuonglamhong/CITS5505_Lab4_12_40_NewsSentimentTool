"""
routes/dashboard.py — Dashboard blueprint
Task 3: Dashboard route skeleton
"""

from flask import Blueprint, render_template, session, redirect, url_for

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():
    # Redirect to login if not logged in
    if "user_id" not in session:
        return redirect(url_for("users.index"))

    return render_template("dashboard.html")

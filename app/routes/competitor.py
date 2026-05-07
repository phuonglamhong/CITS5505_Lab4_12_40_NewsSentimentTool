from flask import render_template
from app import app

@app.route("/competitor")
def competitor_page():
    return render_template("competitor.html")
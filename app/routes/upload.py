'''
Route for uploading text content for sentiment analysis
'''
from flask import Blueprint, render_template, request, jsonify, current_app, flash, redirect, url_for, session
from flask_login import login_required
from app.utility.sentiment_analysis_utils import get_sentiment_summary, analyze_sentiment
from app.forms import UploadForm
import requests
from datetime import datetime, timedelta
from flask_login import current_user

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')

# ---------------------------------------------------------
# Route for uploading text content for sentiment analysis
# ---------------------------------------------------------
@upload_bp.route('/', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            text_content = form.content.data.strip()

            if not text_content:
                flash("No content provided!", "danger")
                return redirect(url_for("upload.upload"))

            lines = [t.strip() for t in text_content.split("\n") if t.strip()]

            # Single-line → analyze_sentiment
            if len(lines) == 1:
                sentiment_data = analyze_sentiment(lines[0])

                # Add pie chart data
                sentiment_data["chart_labels"] = ["Positive", "Negative", "Neutral"]
                sentiment_data["chart_values"] = [
                    1 if sentiment_data["sentiment"] == "positive" else 0,
                    1 if sentiment_data["sentiment"] == "negative" else 0,
                    1 if sentiment_data["sentiment"] == "neutral" else 0,
                ]

            # Multi-line → summary
            else:
                sentiment_data = get_sentiment_summary(lines)

            session["sentiment_data"] = sentiment_data
            session["text_content"] = text_content[:500] + "..." if len(text_content) > 500 else text_content

            return redirect(url_for("main.analyze"))

    # Render upload form for GET requests or if validation fails
    return render_template("upload.html", form=form, user=current_user)
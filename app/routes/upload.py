"""
Upload route — handles article submission and sentiment analysis.
Users paste article content, which is analyzed and saved to the database.
Viewers are not permitted to upload articles.
"""

from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import current_user, login_required
from app import db
from app.models.article import Article
from app.utility.sentiment_analysis_utils import analyze_sentiment

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    # Viewers are not permitted to upload articles
    if current_user.role == "viewer":
        return render_template("upload.html", error="You do not have permission to upload articles. Viewer role is read-only.")

    if request.method == "POST":
        brand   = request.form.get("brand", "").strip()
        title   = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not brand or not title or not content:
            return render_template("upload.html", error="All fields are required.")

        result = analyze_sentiment(content)

        sentiment = result["sentiment"].capitalize()
        score = round((result["polarity"] + 1) * 5, 1)

        article = Article(
            brand=brand,
            title=title,
            sentiment=sentiment,
            score=score,
            content=content
        )
        db.session.add(article)
        db.session.commit()

        return redirect(url_for("upload.analyze", article_id=article.id))

    return render_template("upload.html")


@upload_bp.route("/analyze/<int:article_id>")
@login_required
def analyze(article_id):
    article = db.session.get(Article, article_id)
    if not article:
        return redirect(url_for("upload.upload"))

    return render_template("analyze.html", article=article)

"""
Competitor analysis routes.
Dynamically reads brand sentiment data from the Article database.
"""

from flask import Blueprint, render_template, jsonify, request
from app.models.article import Article
from app import db
from sqlalchemy import func

competitor_bp = Blueprint("competitor", __name__)


@competitor_bp.route("/competitor")
def competitor_page():
    # Get all unique brands from database
    brands = db.session.query(Article.brand).distinct().order_by(Article.brand).all()
    brand_list = [b[0] for b in brands]
    return render_template("competitor.html", brand_list=brand_list)


@competitor_bp.route("/api/competitors")
def competitor_api():
    # Get selected brands from query params, default to all
    selected = request.args.getlist("brands")

    query = db.session.query(Article.brand).distinct().order_by(Article.brand)
    all_brands = [b[0] for b in query.all()]

    if not selected:
        selected = all_brands

    data = []
    for brand in selected:
        articles = Article.query.filter_by(brand=brand).all()
        total = len(articles)
        if total == 0:
            continue

        positive = sum(1 for a in articles if a.sentiment.lower() == "positive")
        neutral  = sum(1 for a in articles if a.sentiment.lower() == "neutral")
        negative = sum(1 for a in articles if a.sentiment.lower() == "negative")
        avg_score = round(sum(a.score for a in articles) / total, 1)

        data.append({
            "name":     brand,
            "pos":      round(positive / total * 100),
            "neu":      round(neutral  / total * 100),
            "neg":      round(negative / total * 100),
            "score":    avg_score,
            "articles": total
        })

    return jsonify(data)

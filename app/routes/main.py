from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models.article import Article
from app.models.user import User
from app.models.comment import Comment

main_bp = Blueprint("main", __name__)


@main_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("users.index"))

    current_user = User.query.get(session["user_id"])

    all_articles = Article.query.all()
    counts = {
        "total":    len(all_articles),
        "positive": sum(1 for a in all_articles if a.sentiment.lower() == "positive"),
        "neutral":  sum(1 for a in all_articles if a.sentiment.lower() == "neutral"),
        "negative": sum(1 for a in all_articles if a.sentiment.lower() == "negative"),
    }
    recent_articles = Article.query.order_by(Article.id.desc()).limit(5).all()
    for a in recent_articles:
        comments = Comment.query.filter_by(article_id=a.id).all()
        a.comment_count = len(comments)
        a.like_count = sum(c.likes for c in comments)

    return render_template(
        "dashboard.html",
        current_user=current_user,
        counts=counts,
        recent_articles=recent_articles
    )


@main_bp.route("/feed")
def feed():
    if "user_id" not in session:
        return redirect(url_for("users.index"))

    current_user = User.query.get(session["user_id"])

    sentiment = request.args.get("sentiment", "all")
    q         = request.args.get("q", "")

    query = Article.query
    if sentiment != "all":
        query = query.filter(Article.sentiment.ilike(sentiment))
    if q:
        query = query.filter(Article.title.ilike(f"%{q}%"))

    articles = query.order_by(Article.id.desc()).all()

    for article in articles:
        comments = Comment.query.filter_by(article_id=article.id).all()
        article.comment_count = len(comments)
        article.like_count = sum(c.likes for c in comments)

    all_articles = Article.query.all()
    counts = {
        "total":    len(all_articles),
        "positive": sum(1 for a in all_articles if a.sentiment.lower() == "positive"),
        "neutral":  sum(1 for a in all_articles if a.sentiment.lower() == "neutral"),
        "negative": sum(1 for a in all_articles if a.sentiment.lower() == "negative"),
    }

    return render_template(
        "feed.html",
        articles=articles,
        counts=counts,
        active_filter=sentiment,
        search_query=q,
        current_user=current_user
    )

@main_bp.route("/test-comments")
def test_comments():
    from app.utility.sentiment_analysis_utils import analyze_sentiment, get_sentiment_summary

    comments = [
        {"author": "Alice", "text": "I love this!"},
        {"author": "Bob", "text": "This is terrible."},
        {"author": "Eve", "text": "The object is on the table."}
    ]

    processed_comments = []

    for c in comments:
        result = analyze_sentiment(c["text"])
        processed_comments.append({
            "author": c["author"],
            "text": c["text"],
            "sentiment": result["sentiment"],
            "polarity": result["polarity"],
            "confidence": result["confidence"]
        })

    # Generate pie chart summary
    summary = get_sentiment_summary([c["text"] for c in comments])

    return render_template(
        "commentsTest.html",
        comments=processed_comments,
        summary=summary
    )

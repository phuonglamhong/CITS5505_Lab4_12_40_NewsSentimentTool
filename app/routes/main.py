# This file handles the main application pages including
# dashboard, article feed, and sentiment testing routes.
from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models.article import Article
from app.models.user import User
from app.models.comment import Comment

# Blueprint for main application routes
main_bp = Blueprint("main", __name__)

# Dashboard route displaying analytics overview
@main_bp.route("/dashboard")
def dashboard():
    # Redirect unauthenticated users to login page
    if "user_id" not in session:
        return redirect(url_for("users.index"))

    # Load current logged-in user
    current_user = User.query.get(session["user_id"])

    # Load all stored articles
    all_articles = Article.query.all()
    # Calculate sentiment statistics
    counts = {
        "total":    len(all_articles),
        "positive": sum(1 for a in all_articles if a.sentiment.lower() == "positive"),
        "neutral":  sum(1 for a in all_articles if a.sentiment.lower() == "neutral"),
        "negative": sum(1 for a in all_articles if a.sentiment.lower() == "negative"),
    }
    # Load latest 5 articles for dashboard preview
    recent_articles = Article.query.order_by(Article.id.desc()).limit(5).all()
    # Add comment and like statistics to each article
    for a in recent_articles:
        comments = Comment.query.filter_by(article_id=a.id).all()
        a.comment_count = len(comments)
        a.like_count = sum(c.likes for c in comments)

    # Render dashboard template
    return render_template(
        "dashboard.html",
        current_user=current_user,
        counts=counts,
        recent_articles=recent_articles
    )

# Feed page route displaying searchable article list
@main_bp.route("/feed")
def feed():
    # Redirect users if not logged in
    if "user_id" not in session:
        return redirect(url_for("users.index"))

    # Load current logged-in user
    current_user = User.query.get(session["user_id"])

    # Get filter parameters from URL
    sentiment = request.args.get("sentiment", "all")
    q = request.args.get("q", "")

    # Start article query
    query = Article.query

    # Filter by sentiment type
    if sentiment != "all":
        query = query.filter(Article.sentiment.ilike(sentiment))
    # Filter by search keyword in article title
    if q:
        query = query.filter(Article.title.ilike(f"%{q}%"))
    # Load filtered articles ordered newest first
    articles = query.order_by(Article.id.desc()).all()
    # Add discussion statistics to articles
    for article in articles:
        comments = Comment.query.filter_by(article_id=article.id).all()
        article.comment_count = len(comments)
        article.like_count = sum(c.likes for c in comments)

    # Recalculate dashboard statistics
    all_articles = Article.query.all()
    counts = {
        "total":    len(all_articles),
        "positive": sum(1 for a in all_articles if a.sentiment.lower() == "positive"),
        "neutral":  sum(1 for a in all_articles if a.sentiment.lower() == "neutral"),
        "negative": sum(1 for a in all_articles if a.sentiment.lower() == "negative"),
    }

    # Render article feed page
    return render_template(
        "feed.html",
        articles=articles,
        counts=counts,
        active_filter=sentiment,
        search_query=q,
        current_user=current_user
    )

# Route used for testing sentiment analysis utilities
@main_bp.route("/test-comments")
def test_comments():
    # Import sentiment utility functions
    from app.utility.sentiment_analysis_utils import analyze_sentiment, get_sentiment_summary
    # Sample comments for testing sentiment analysis
    comments = [
        {"author": "Alice", "text": "I love this!"},
        {"author": "Bob", "text": "This is terrible."},
        {"author": "Eve", "text": "The object is on the table."}
    ]
    # Store processed sentiment results
    processed_comments = []
    # Analyze sentiment for each comment
    for c in comments:
        result = analyze_sentiment(c["text"])
        processed_comments.append({
            "author": c["author"],
            "text": c["text"],
            "sentiment": result["sentiment"],
            "polarity": result["polarity"],
            "confidence": result["confidence"]
        })

    # Generate sentiment summary statistics
    summary = get_sentiment_summary([c["text"] for c in comments])

    # Render testing template
    return render_template(
        "commentsTest.html",
        comments=processed_comments,
        summary=summary
    )

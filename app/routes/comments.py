# This file handles article discussion and collaboration routes.
# Users can view articles, post comments, reply to discussions
# and like comments to support collaborative sentiment analysis.


from flask import Blueprint, render_template, request, jsonify, session
from functools import wraps
from app import db
from app.models.article import Article
from app.models.comment import Comment
from app.models.user import User

# Blueprint for comment and collaboration features
comments_bp = Blueprint("comments", __name__)

# Custom decorator to ensure users are logged in
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Prevent access if session does not contain user ID
        if "user_id" not in session:
            return jsonify({"status": "error", "message": "Please log in first."})
        return f(*args, **kwargs)
    return decorated

# Route for comments and collaboration page
@comments_bp.route("/comments")
def comments_page():
    # Load all articles ordered by newest first
    articles = Article.query.order_by(Article.id.desc()).all()

    # Store processed article discussion data
    articles_data = []

    # Process each article individually
    for article in articles:
        # Load top-level comments only
        top_comments = Comment.query.filter_by(
            article_id=article.id,
            parent_id=None
        ).order_by(Comment.likes.desc(), Comment.created_at.desc()).all()

        # Dictionary storing replies for each comment
        replies = {}

        # Collect replies for nested discussion threads
        for c in top_comments:
            if c.replies:
                replies[c.id] = c.replies

        # Store article information with discussion data
        articles_data.append({
            "article": article,
            "comments": top_comments,
            "replies": replies,
            # Total comment count including replies
            "comment_count": len(top_comments) + sum(len(r) for r in replies.values()),
            # Total likes for top-level comments
            "like_count": sum(c.likes for c in top_comments)
        })

    # Store current logged-in user information
    current_user = None
    if "user_id" in session:
        current_user = User.query.get(session["user_id"])
    # Render collaboration discussion page
    return render_template(
        "comments.html",
        articles_data=articles_data,
        current_user=current_user
    )

# Route for posting new comments or replies
@comments_bp.route("/article/<int:article_id>/comment", methods=["POST"])
@login_required
def post_comment(article_id):

    # Ensure article exists
    Article.query.get_or_404(article_id)

    # Get JSON request data
    data      = request.get_json()
    # Extract comment text
    content   = data.get("content", "").strip()
    # Extract optional reply parent ID
    parent_id = data.get("parent_id")

    # Prevent empty comments
    if not content:
        return jsonify({"status": "error", "message": "Comment cannot be empty."})
    # Prevent excessively long comments
    if len(content) > 1000:
        return jsonify({"status": "error", "message": "Comment too long."})

    # Validate reply target if replying to another comment
    if parent_id:
        parent = Comment.query.get(parent_id)
        if not parent or parent.article_id != article_id:
            return jsonify({"status": "error", "message": "Invalid reply target."})

    # Create new comment object
    new_comment = Comment(
        article_id=article_id,
        user_id=session["user_id"],
        parent_id=parent_id if parent_id else None,
        content=content
    )

    # Save comment into database
    db.session.add(new_comment)
    db.session.commit()

    # Return successful response
    return jsonify({
        "status": "success",
        "message": "Comment posted!",
        "comment": {
            "id":         new_comment.id,
            "content":    new_comment.content,
            "author":     new_comment.author.name,
            "role":       new_comment.author.role,
            "created_at": new_comment.created_at.strftime("%Y-%m-%d %H:%M"),
            "likes":      0
        }
    })

# Route for liking a comment
@comments_bp.route("/comment/<int:comment_id>/like", methods=["POST"])
@login_required
def like_comment(comment_id):
    # Load comment or return 404 error
    comment = Comment.query.get_or_404(comment_id)
    # Increase like count
    comment.likes += 1
    # Save updated like count
    db.session.commit()
    # Return updated likes to frontend
    return jsonify({"status": "success", "likes": comment.likes})

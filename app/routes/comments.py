
from flask import Blueprint, render_template, request, jsonify, session
from functools import wraps
from app import db
from app.models.article import Article
from app.models.comment import Comment
from app.models.user import User

comments_bp = Blueprint("comments", __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"status": "error", "message": "Please log in first."})
        return f(*args, **kwargs)
    return decorated


@comments_bp.route("/comments")
def comments_page():
    # upload all articles with their comments and replies
    articles = Article.query.order_by(Article.id.desc()).all()

    # add comment counts and like counts to each article
    articles_data = []
    for article in articles:
        top_comments = Comment.query.filter_by(
            article_id=article.id,
            parent_id=None
        ).order_by(Comment.likes.desc(), Comment.created_at.desc()).all()

        replies = {}
        for c in top_comments:
            if c.replies:
                replies[c.id] = c.replies

        articles_data.append({
            "article": article,
            "comments": top_comments,
            "replies": replies,
            "comment_count": len(top_comments) + sum(len(r) for r in replies.values()),
            "like_count": sum(c.likes for c in top_comments)
        })

    current_user = None
    if "user_id" in session:
        current_user = User.query.get(session["user_id"])

    return render_template(
        "comments.html",
        articles_data=articles_data,
        current_user=current_user
    )


@comments_bp.route("/article/<int:article_id>/comment", methods=["POST"])
@login_required
def post_comment(article_id):
    Article.query.get_or_404(article_id)

    data      = request.get_json()
    content   = data.get("content", "").strip()
    parent_id = data.get("parent_id")

    if not content:
        return jsonify({"status": "error", "message": "Comment cannot be empty."})
    if len(content) > 1000:
        return jsonify({"status": "error", "message": "Comment too long."})

    if parent_id:
        parent = Comment.query.get(parent_id)
        if not parent or parent.article_id != article_id:
            return jsonify({"status": "error", "message": "Invalid reply target."})

    new_comment = Comment(
        article_id=article_id,
        user_id=session["user_id"],
        parent_id=parent_id if parent_id else None,
        content=content
    )

    db.session.add(new_comment)
    db.session.commit()

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


@comments_bp.route("/comment/<int:comment_id>/like", methods=["POST"])
@login_required
def like_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.likes += 1
    db.session.commit()
    return jsonify({"status": "success", "likes": comment.likes})

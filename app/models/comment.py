from app import db
from datetime import datetime, timezone

class Comment(db.Model):
    __tablename__ = "comments"

    id=db.Column(db.Integer, primary_key=True)
    article_id=db.Column(db.Integer, db.ForeignKey("articles.id"), nullable=False)
    user_id= db.Column(db.Integer, db.ForeignKey("users.id"),    nullable=False)
    parent_id=db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=True)  # None = 顶级评论
    content = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    author = db.relationship("User", backref="comments", lazy="joined")
    replies = db.relationship("Comment",
                              backref=db.backref("parent", remote_side=[id]),
                              lazy="select")

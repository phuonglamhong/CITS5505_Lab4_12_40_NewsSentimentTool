from app import db
from datetime import datetime, timezone

# Comment model used for collaboration and discussion features
class Comment(db.Model):
    # Database table name
    __tablename__ = "comments"

    # Unique comment ID
    id         = db.Column(db.Integer, primary_key=True)
    # Foreign key linking comment to an article
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"), nullable=False)
    # Foreign key linking comment to a user
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"),    nullable=False)
    # Self-referencing foreign key for nested replies
    parent_id  = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=True)
    # Main comment text content
    content    = db.Column(db.Text, nullable=False)
    # Stores number of likes on a comment
    likes      = db.Column(db.Integer, default=0, nullable=False)
    # Automatically stores comment creation time in UTC
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship linking comment to its author
    author  = db.relationship("User", backref="comments", lazy="joined")
    # Relationship enabling threaded replies to comments
    replies = db.relationship(
        "Comment",
        backref=db.backref("parent", remote_side=[id]),
        lazy="select"
    )
    # String representation used for debugging and logging
    def __repr__(self):
        return f"<Comment {self.id} by User {self.user_id}>"

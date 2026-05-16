"""
Article database model.

This model stores competitor news articles and
their associated sentiment analysis results.
"""

from app import db

class Article(db.Model):

    # SQLAlchemy model for storing article sentiment data.
    # Database table name
    __tablename__ = "articles"

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Brand or company name
    brand = db.Column(db.String(100), nullable=False)

    # Article headline/title
    title = db.Column(db.String(255), nullable=False)

    # Sentiment classification (Positive, Neutral, Negative)
    sentiment = db.Column(db.String(20), nullable=False)

    # Numerical sentiment score
    score = db.Column(db.Float, nullable=False)

    # Full article content/body text
    content = db.Column(db.Text)

    """
        String representation of the Article object.
        Useful for debugging and logging.
        """
    def __repr__(self):
        """
        String representation of the Article object.
        Useful for debugging and logging.
        """
        return f"<Article {self.title}>"
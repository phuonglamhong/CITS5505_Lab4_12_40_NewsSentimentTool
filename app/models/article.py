from app import db
from datetime import datetime


class Article(db.Model):

    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)

    brand = db.Column(db.String(100), nullable=False)

    title = db.Column(db.String(255), nullable=False)

    sentiment = db.Column(db.String(20), nullable=False)

    score = db.Column(db.Float, nullable=False)

    source = db.Column(db.String(100), nullable=True)

    date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    content = db.Column(db.Text)

    def __repr__(self):
        return f"<Article {self.title}>"

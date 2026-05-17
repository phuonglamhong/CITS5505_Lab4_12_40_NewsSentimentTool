"""
Unit tests for the NewsSentiment application.

Tests cover:
- Competitor routes and API
- Article database model
- User authentication
- Page access control
- Sentiment analysis utility
- Article upload
- Comments page
- Analyze page
"""

import unittest
from app import create_app, db
from app.models.user import User
from app.models.article import Article
from app.utility.sentiment_analysis_utils import analyze_sentiment
from werkzeug.security import generate_password_hash


class CompetitorTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
        })
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # Test 1 — Competitor page loads
    def test_competitor_page_loads(self):
        response = self.client.get("/competitor")
        self.assertEqual(response.status_code, 200)

    # Test 2 — Competitor API is reachable
    def test_competitor_api(self):
        response = self.client.get("/api/competitors")
        self.assertEqual(response.status_code, 200)

    # Test 3 — API returns JSON
    def test_api_returns_json(self):
        response = self.client.get("/api/competitors")
        self.assertTrue(response.is_json)

    # Test 4 — JSON contains brand name
    def test_json_contains_brand_name(self):
        # Add a test article so API returns data
        with self.app.app_context():
            article = Article(brand="Apple", title="Test", sentiment="Positive", score=7.0, content="Test content")
            db.session.add(article)
            db.session.commit()
        response = self.client.get("/api/competitors")
        data = response.get_json()
        self.assertIn("name", data[0])

    # Test 5 — Article model persistence
    def test_article_model(self):
        article = Article(
            brand="Apple",
            title="Test Article",
            sentiment="Positive",
            score=7.5,
            content="Test content"
        )
        with self.app.app_context():
            db.session.add(article)
            db.session.commit()
            saved = Article.query.first()
            self.assertEqual(saved.brand, "Apple")


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
        })
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            user = User(
                name="Test User",
                email="test@example.com",
                role="analyst",
                password=generate_password_hash("password123")
            )
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # Test 6 — Welcome page loads
    def test_welcome_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    # Test 7 — Login page loads
    def test_login_page_loads(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)

    # Test 8 — Successful login
    def test_login_success(self):
        response = self.client.post("/login", data={
            "email": "test@example.com",
            "password": "password123"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # Test 9 — Wrong password
    def test_login_wrong_password(self):
        response = self.client.post("/login", data={
            "email": "test@example.com",
            "password": "wrongpassword"
        }, follow_redirects=True)
        self.assertIn(b"Invalid email or password", response.data)

    # Test 10 — Dashboard requires login
    def test_dashboard_requires_login(self):
        response = self.client.get("/dashboard", follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    # Test 11 — Register with valid data
    def test_register_success(self):
        response = self.client.post("/register", data={
            "name": "New User",
            "email": "newuser@example.com",
            "role": "analyst",
            "password": "password123",
            "confirm_password": "password123"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # Test 12 — Register duplicate email
    def test_register_duplicate_email(self):
        response = self.client.post("/register", data={
            "name": "Another User",
            "email": "test@example.com",
            "role": "analyst",
            "password": "password123",
            "confirm_password": "password123"
        }, follow_redirects=True)
        self.assertIn(b"Email already registered", response.data)

    # Test 13 — Positive sentiment analysis
    def test_sentiment_positive(self):
        result = analyze_sentiment("This is absolutely wonderful and amazing!")
        self.assertEqual(result["sentiment"], "positive")

    # Test 14 — Negative sentiment analysis
    def test_sentiment_negative(self):
        result = analyze_sentiment("This is terrible, awful and completely disastrous.")
        self.assertEqual(result["sentiment"], "negative")

    # Test 15 — Upload page requires login
    def test_upload_requires_login(self):
        response = self.client.get("/upload", follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    # Test 16 — Comments page loads when logged in
    def test_comments_page_loads(self):
        self.client.post("/login", data={
            "email": "test@example.com",
            "password": "password123"
        }, follow_redirects=True)
        response = self.client.get("/comments")
        self.assertEqual(response.status_code, 200)

    # Test 17 — Upload page loads when logged in
    def test_upload_page_loads(self):
        self.client.post("/login", data={
            "email": "test@example.com",
            "password": "password123"
        }, follow_redirects=True)
        response = self.client.get("/upload")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()

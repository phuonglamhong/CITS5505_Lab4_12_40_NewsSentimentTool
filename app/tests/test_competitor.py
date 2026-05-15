"""
Unit tests for Competitor and Article-related functionality.

This test suite validates:
- Flask route accessibility
- API response correctness
- JSON structure integrity
- Database model persistence using SQLAlchemy (in-memory DB)

Each test is isolated using setUp/tearDown with a fresh database.
"""

import unittest

from app import create_app, db
from app.models.article import Article


class CompetitorTestCase(unittest.TestCase):

    # Setup test environment before each test case.
    def setUp(self):

        self.app = create_app()

        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up after each test case.
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # ROUTE TESTS
    # Test competitor page route
    def test_competitor_page_loads(self):
        # Ensures competitor UI page is accessible.
        response = self.client.get("/competitor")

        self.assertEqual(response.status_code, 200)

    # Test API endpoint
    def test_competitor_api(self):
        # Ensures competitor API endpoint is reachable.
        response = self.client.get("/api/competitors")

        self.assertEqual(response.status_code, 200)

    # Test API returns JSON
    def test_api_returns_json(self):
        # Ensures API response format is JSON.
        response = self.client.get("/api/competitors")

        self.assertTrue(response.is_json)

    # Test JSON structure
    def test_json_contains_brand_name(self):

        # Validates API response structure.
        response = self.client.get("/api/competitors")

        data = response.get_json()

        self.assertIn("name", data[0])

    # DATABASE MODEL TESTS
    # Test Article model - Validates Article model persistence in database.
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

            saved_article = Article.query.first()

            self.assertEqual(saved_article.brand, "Apple")


if __name__ == "__main__":
    unittest.main()
import unittest

from app import create_app, db
from app.models.article import Article


class CompetitorTestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app()

        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):

        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # Test competitor page route
    def test_competitor_page_loads(self):

        response = self.client.get("/competitor")

        self.assertEqual(response.status_code, 200)

    # Test API endpoint
    def test_competitor_api(self):

        response = self.client.get("/api/competitors")

        self.assertEqual(response.status_code, 200)

    # Test API returns JSON
    def test_api_returns_json(self):

        response = self.client.get("/api/competitors")

        self.assertTrue(response.is_json)

    # Test JSON structure
    def test_json_contains_brand_name(self):

        response = self.client.get("/api/competitors")

        data = response.get_json()

        self.assertIn("name", data[0])

    # Test Article model
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
from app import create_app, db
from app.models.article import Article

app = create_app()

with app.app_context():

    # Clear old data
    Article.query.delete()

    # Demo records
    articles = [

        Article(
            brand="Apple",
            title="Apple launches new AI features",
            sentiment="Positive",
            score=7.4,
            content="Apple received strong positive media coverage."
        ),

        Article(
            brand="Google",
            title="Google expands cloud services",
            sentiment="Positive",
            score=6.9,
            content="Google continues growth in enterprise AI."
        ),

        Article(
            brand="Microsoft",
            title="Microsoft invests in cybersecurity",
            sentiment="Neutral",
            score=6.5,
            content="Mixed analyst reactions to Microsoft's investments."
        ),

        Article(
            brand="Tesla",
            title="Tesla faces production criticism",
            sentiment="Negative",
            score=4.2,
            content="Tesla received increased negative media attention."
        )
    ]

    db.session.add_all(articles)
    db.session.commit()

    print("Seed data inserted successfully.")
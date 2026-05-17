"""
This is the main entry point of the Flask application. 
It imports the create_app function and the database instance from the app package, 
creates an application instance, and initializes the database. 
Finally, it runs the application in debug mode if this script is executed directly.
"""
from app import create_app, db

app = create_app()


if __name__ == "__main__":
    app.run(debug=True)

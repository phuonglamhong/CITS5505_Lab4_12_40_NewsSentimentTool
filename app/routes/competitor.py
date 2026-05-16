"""
Competitor analysis routes.

This file contains:
- Competitor dashboard page route
- Competitor sentiment API endpoint
"""

from flask import Blueprint, render_template, jsonify
# Blueprint for competitor-related routes
competitor_bp = Blueprint("competitor", __name__)

@competitor_bp.route("/competitor")
def competitor_page():
    """
    Render competitor analysis dashboard page.
    """
    return render_template("competitor.html")


@competitor_bp.route("/api/competitors")
def competitor_api():
    
     """
     Return competitor sentiment analysis data as JSON.

     Currently uses hardcoded demo data.
     Future implementation can connect to database models.
     """

     
     data = [
        {
            "name": "Apple",
            "pos": 61,
            "neu": 24,
            "neg": 15,
            "score": 7.4,
            "articles": 2841
        },
        {
            "name": "Google",
            "pos": 58,
            "neu": 28,
            "neg": 14,
            "score": 6.9,
            "articles": 3102
        },
        {
            "name": "Microsoft",
            "pos": 55,
            "neu": 31,
            "neg": 14,
            "score": 6.5,
            "articles": 1987
        },
        {
            "name": "Tesla",
            "pos": 38,
            "neu": 22,
            "neg": 40,
            "score": 4.2,
            "articles": 4210
        }
    ]

     return jsonify(data)

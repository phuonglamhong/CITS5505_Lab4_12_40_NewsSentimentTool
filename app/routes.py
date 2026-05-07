# routes.py - Flask routes for BrandPulse
from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import hashlib
import re
import os

from app import app

# ---------- Database connection ----------
def get_db():
    db_path = os.path.join(app.instance_path, "NewsSentimentDB.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# ---------- Password hashing ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------- Mock data ----------
# Checkpoint 3: replace with Article.query.all() once Article model is added by teammate
MOCK_ARTICLES = [
    {
        'id': 1,
        'title': 'Tesla earnings exceed analyst expectations',
        'preview': 'Revenue beat supported stronger investor confidence.',
        'source': 'Bloomberg',
        'sentiment': 'positive',
        'score': 0.82,
        'date': '1 hour ago'
    },
    {
        'id': 2,
        'title': 'US regulators review Tesla autopilot reporting',
        'preview': 'Coverage remains cautious despite no new enforcement action.',
        'source': 'Reuters',
        'sentiment': 'negative',
        'score': -0.61,
        'date': '3 hours ago'
    },
    {
        'id': 3,
        'title': 'Tesla expands charging partnerships in Europe',
        'preview': 'Industry analysts frame the move as a long-term brand strength signal.',
        'source': 'BBC',
        'sentiment': 'positive',
        'score': 0.74,
        'date': '6 hours ago'
    },
    {
        'id': 4,
        'title': 'Investors weigh margin pressure in EV pricing war',
        'preview': 'Market sentiment stays mixed as competition intensifies globally.',
        'source': 'TechCrunch',
        'sentiment': 'neutral',
        'score': 0.08,
        'date': '8 hours ago'
    },
    {
        'id': 5,
        'title': 'Tesla software rollout praised for improving in-car user experience',
        'preview': 'Technology press highlights product polish and usability gains.',
        'source': 'TechCrunch',
        'sentiment': 'positive',
        'score': 0.69,
        'date': '9 hours ago'
    },
    {
        'id': 6,
        'title': 'Tesla faces renewed scrutiny after safety concerns re-enter headlines',
        'preview': 'Fresh reporting highlights regulatory attention and public concern.',
        'source': 'Reuters',
        'sentiment': 'negative',
        'score': -0.55,
        'date': '2 hours ago'
    },
    {
        'id': 7,
        'title': 'European charging expansion signals long-term strategy shift for Tesla',
        'preview': 'Coverage frames the update as strategically significant.',
        'source': 'BBC',
        'sentiment': 'neutral',
        'score': 0.12,
        'date': '6 hours ago'
    },
]

MOCK_ALERTS = [
    {
        'icon': 'bolt',
        'title': 'Battery safety concerns trend across major outlets',
        'desc': 'Reuters and Bloomberg coverage pushed negative sentiment higher in the last 12 hours.',
        'priority': 'Priority high',
        'time': '2 hours ago'
    },
    {
        'icon': 'scale-balanced',
        'title': 'Regulatory scrutiny around autonomous driving updates',
        'desc': 'Neutral coverage is shifting toward caution as analysts question roadmap communication.',
        'priority': 'Priority medium',
        'time': '5 hours ago'
    },
    {
        'icon': 'bullhorn',
        'title': 'CEO interview quote sparks mixed social pickup',
        'desc': 'Media mentions remain limited, but commentary is amplifying around tone and leadership risk.',
        'priority': 'Priority medium',
        'time': '9 hours ago'
    },
]

# ---------- Routes ----------

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    role = data.get("role")
    password = data.get("password")

    email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not re.match(email_regex, email):
        return jsonify({"status": "error", "message": "Invalid email format."})

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    if cur.fetchone():
        return jsonify({"status": "error", "message": "Email already registered."})

    cur.execute(
        "INSERT INTO users (name, email, role, password) VALUES (?, ?, ?, ?)",
        (name, email, role, hash_password(password))
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Account created!"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = hash_password(data.get("password"))

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cur.fetchone()

    if user:
        return jsonify({"status": "success", "message": "Login OK!"})
    else:
        return jsonify({"status": "error", "message": "Invalid email or password."})

# ---------- Dashboard ----------
@app.route("/dashboard")
def dashboard():
    # Checkpoint 3: replace mock data with Article.query.all()
    articles = MOCK_ARTICLES

    positive = [a for a in articles if a['sentiment'] == 'positive']
    neutral  = [a for a in articles if a['sentiment'] == 'neutral']
    negative = [a for a in articles if a['sentiment'] == 'negative']
    total    = len(articles)

    pos_pct = round(len(positive) / total * 100) if total else 0
    neu_pct = round(len(neutral)  / total * 100) if total else 0
    neg_pct = round(len(negative) / total * 100) if total else 0

    data = {
        'brand_name':      'Tesla',
        'brand_score':     78.4,
        'total_articles':  total,
        'new_today':       18,
        'positive_pct':    pos_pct,
        'neutral_pct':     neu_pct,
        'negative_pct':    neg_pct,
        'positive_count':  len(positive),
        'neutral_count':   len(neutral),
        'negative_count':  len(negative),
        'active_alerts':   len(MOCK_ALERTS),
        'alerts':          MOCK_ALERTS,
        'recent_articles': articles[:4],
    }

    return render_template("dashboard.html", data=data)

# ---------- Media Feed ----------
@app.route("/feed")
def feed():
    # Checkpoint 3: replace with Article.query.filter_by(...).all()
    sentiment_filter = request.args.get('sentiment', 'all')
    source_filter    = request.args.get('source', '')
    search_query     = request.args.get('q', '')

    articles = MOCK_ARTICLES

    if sentiment_filter != 'all':
        articles = [a for a in articles if a['sentiment'] == sentiment_filter]

    if source_filter:
        articles = [a for a in articles if a['source'] == source_filter]

    if search_query:
        articles = [a for a in articles
                    if search_query.lower() in a['title'].lower()
                    or search_query.lower() in a['preview'].lower()]

    all_articles = MOCK_ARTICLES
    counts = {
        'total':    len(all_articles),
        'positive': len([a for a in all_articles if a['sentiment'] == 'positive']),
        'neutral':  len([a for a in all_articles if a['sentiment'] == 'neutral']),
        'negative': len([a for a in all_articles if a['sentiment'] == 'negative']),
    }

    return render_template(
        "feed.html",
        articles=articles,
        counts=counts,
        active_filter=sentiment_filter,
        active_source=source_filter,
        search_query=search_query,
    )

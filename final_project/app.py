from flask import request, jsonify, render_template, redirect, url_for
import sqlite3
from datetime import datetime
import hashlib
import re
import os

# -----------------------------
# DATABASE PATHS
# -----------------------------
##DB_NAME = "db/comments.db"
USERS_DB = os.path.join("instance", "NewsSentimentDB.db")
os.makedirs("instance", exist_ok=True)

# -----------------------------
# COMMENT SYSTEM DB FUNCTIONS
# -----------------------------
##def get_db_connection():
##    conn = sqlite3.connect(DB_NAME)
##    conn.row_factory = sqlite3.Row
##    return conn

##def init_comments_db():
##    conn = get_db_connection()

##    conn.execute("""
##        CREATE TABLE IF NOT EXISTS comments (
##            id INTEGER PRIMARY KEY AUTOINCREMENT,
##            article_id INTEGER NOT NULL,
##            author TEXT NOT NULL,
##            time TEXT NOT NULL,
##            tag TEXT,
##            body TEXT NOT NULL
##        )
##    """)

##    existing = conn.execute(
##        "SELECT COUNT(*) AS count FROM comments WHERE article_id = ?",
##        (2,)
##    ).fetchone()["count"]

##    if existing == 0:
##        conn.execute("""
##            INSERT INTO comments (article_id, author, time, tag, body)
##            VALUES (?, ?, ?, ?, ?)
##        """, (
##            2,
##            "Jordan Lee",
##            "2h ago",
##            "Misclassified",
##            "This feels over-classified as negative."
##        ))

##        conn.execute("""
##            INSERT INTO comments (article_id, author, time, tag, body)
##            VALUES (?, ?, ?, ?, ?)
##        """, (
##            2,
##            "Sara Mitchell",
##            "45m ago",
##            "Flagged",
##            "Escalating this to the crisis monitoring queue."
##        ))

##    conn.commit()
##    conn.close()

# -----------------------------
# USER SYSTEM DB FUNCTIONS
# -----------------------------
def get_users_db():
    conn = sqlite3.connect(USERS_DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_users_db():
    conn = get_users_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# -----------------------------
# PASSWORD HASHING
# -----------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -----------------------------
# ROUTE REGISTRATION FUNCTION
# -----------------------------
def register_routes(app):

    # Initialize DBs when app starts
##    init_comments_db()
    init_users_db()

    # -----------------------------
    # HOME → LOGIN FIRST
    # -----------------------------
    @app.route("/")
    def home():
        return redirect(url_for("login_page"))

    # -----------------------------
    # LOGIN PAGE
    # -----------------------------
    @app.route("/login")
    def login_page():
        return render_template("login.html")

    # -----------------------------
    # REGISTER USER
    # -----------------------------
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

        conn = get_users_db()
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

    # -----------------------------
    # LOGIN USER
    # -----------------------------
    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()
        email = data.get("email")
        password = hash_password(data.get("password"))

        conn = get_users_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cur.fetchone()

        if user:
            return jsonify({"status": "success", "message": "Login OK!"})
        else:
            return jsonify({"status": "error", "message": "Invalid email or password."})

    # -----------------------------
    # ARTICLE DETAIL PAGE
    # -----------------------------
    @app.route("/detail/<int:article_id>")
    def detail(article_id):
        return render_template("detail.html", article_id=article_id)

    # -----------------------------
    # COMMENTS API
    # -----------------------------
    @app.route("/api/articles/<int:article_id>/comments", methods=["GET", "POST"])
    def article_comments(article_id):
        conn = get_db_connection()

        if request.method == "GET":
            rows = conn.execute("""
                SELECT author, time, tag, body
                FROM comments
                WHERE article_id = ?
                ORDER BY id ASC
            """, (article_id,)).fetchall()

            conn.close()
            return jsonify([dict(row) for row in rows])

        data = request.get_json() or {}
        body = data.get("body", "").strip()
        tag = data.get("tag", "").strip()

        if not body:
            conn.close()
            return jsonify({"error": "Comment body is required."}), 400

        time_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        conn.execute("""
            INSERT INTO comments (article_id, author, time, tag, body)
            VALUES (?, ?, ?, ?, ?)
        """, (article_id, "Alex Chen", time_str, tag, body))

        conn.commit()
        conn.close()

        return jsonify({
            "author": "Alex Chen",
            "time": time_str,
            "tag": tag,
            "body": body
        }), 201
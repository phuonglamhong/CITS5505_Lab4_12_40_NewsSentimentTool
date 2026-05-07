# app.py - Flask application for user registration and login with SQLite database
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

    # Validate email format (Security, prevents bypassing JS)
    email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not re.match(email_regex, email):
        return jsonify({"status": "error", "message": "Invalid email format."})

    conn = get_db()
    cur = conn.cursor()

    # Check if email exists
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    if cur.fetchone():
        return jsonify({"status": "error", "message": "Email already registered."})

    # Insert new user
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
    

@app.route("/competitor")
def competitor_page():
    return render_template("competitor.html")
# BrandPulse

A web-based news sentiment monitoring platform built with Flask.

## Contributors

| Student ID | Names           | GitHub usernames |
| ---------- | --------------- | ---------------- |
| 24758673   | Zunhao Zhang    | 33fish           |
| 24600969   | Lola Xu         | Redlola          |
| 24453423   | Hong Phuong Lam | phuonglamhong    |
| 24717854   | K Ishwari Raj   | Kishwari         |

## What is this?

BrandPulse is a web app that lets you paste in news articles and automatically analyse whether the coverage is positive, negative, or neutral. You can track multiple brands, compare their sentiment over time, and discuss findings with your team.

Built with Flask, SQLite, and TextBlob for NLP sentiment analysis.

---

## Features

- Register and log in with a role (Manager, Analyst, or Viewer)
- Upload news articles and get instant sentiment analysis
- Dashboard with sentiment stats and recent articles
- Competitor page to compare brands side by side with charts
- Discussion page with threaded comments and likes
- Managers can delete articles and comments; Viewers are read-only

---

## Tech Stack

**Frontend:** HTML, CSS, JavaScript, Bootstrap 5, Tailwind CSS, Chart.js

**Backend:** Flask, Flask-Login, Flask-WTF, Flask-SQLAlchemy, Flask-Migrate, TextBlob

**Database:** SQLite via SQLAlchemy ORM

**Testing:** pytest (unit tests) + Selenium (browser tests)

---

## Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/phuonglamhong/CITS5505_Lab4_12_40_NewsSentimentTool.git
cd CITS5505_Lab4_12_40_NewsSentimentTool
```

**2. Create a virtual environment**
```bash
# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the project root:
```
SECRET_KEY=your-secret-key-here
```

**5. Run the app**
```bash
python run.py
```

Then open `http://127.0.0.1:5000` in your browser. Register an account to get started.

---

## Running Tests

**Unit tests (17 tests)**
```bash
python -m pytest app/tests/test_app.py -v
```

**Selenium browser tests (7 tests)**

Start the server first, then in a new terminal:
```bash
python -m pytest app/tests/test_selenium.py -v
```

Requires Google Chrome to be installed.

---

## Security

- Passwords stored as salted hashes
- CSRF protection on all forms
- Session management via Flask-Login
- Secret key stored in `.env`

---

## Project Structure

```text
app/
├── models/        # database models
├── routes/        # Flask blueprints
├── static/        # CSS and JS
├── templates/     # HTML templates
├── tests/         # unit and selenium tests
└── utility/       # sentiment analysis utils
migrations/
run.py
requirements.txt
```

---

Developed for **CITS3403 — Agile Web Development**, The University of Western Australia © 2026




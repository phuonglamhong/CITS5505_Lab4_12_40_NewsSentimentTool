# News Sentiment Analyzer

## Contributors

| Student ID | Names           | GitHub usernames |
| 24758673   | Zunhao Zhang    | 33fish           |
| 24600969   | Lola Xu         | Redlola          |
| 24453423   | Hong Phuong Lam | phuonglamhong    |
| 24717854   | K Ishwari Raj   | Kishwari         |

---

## Project Overview

News Sentiment Analyzer is a Flask-based web application that allows users to analyse the sentiment of news-related content using Natural Language Processing (NLP) concepts. The system classifies content into positive, neutral and negative sentiment categories and presents the results through interactive visual dashboards and charts.

The application was designed to provide users with a clean and intuitive platform for monitoring public opinion and comparing sentiment trends between different brands and topics.

The system follows a client-server architecture using Flask on the backend and HTML, CSS, JavaScript, Bootstrap and Tailwind CSS on the frontend.

---

# Features

- User authentication (login/logout)
- Persistent SQLite database storage
- Competitor sentiment analysis dashboard
- Interactive sentiment comparison charts
- Dynamic frontend rendering using JavaScript and Fetch API
- Responsive web design
- Comment and discussion functionality
- Flask Blueprints for modular backend structure
- Unit testing for backend routes and models

---

# Technologies Used

## Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- Tailwind CSS
- Chart.js

## Backend
- Flask
- Flask-WTF
- Flask-SQLAlchemy
- Flask-Mail

## Database
- SQLite
- SQLAlchemy ORM

## Testing
- Python unittest

---

# Application Design

The application was designed with the following goals:

- **Engaging**  
  A modern UI with charts, cards, dashboards and responsive layouts.

- **Effective**  
  Allows users to understand sentiment trends and compare competitor performance visually.

- **Intuitive**  
  Clean navigation and dynamically updated content improve usability.

The project uses Flask Blueprints to separate routes into modular components and SQLAlchemy models to manage persistent application data.

---

# Project Structure

```text
app/
│
├── migrations/
│
├── models/
│   ├── article.py
│   ├── comment.py
│   └── user.py
│
├── routes/
│   ├── comments.py
│   ├── competitor.py
│   ├── main.py
│   └── users.py
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│
└── tests/
```

---

# Installation and Setup

## 1. Clone the Repository

```bash
git clone https://github.com/phuonglamhong/CITS5505_Lab4_12_40_NewsSentimentTool.git
cd CITS5505_Lab4_12_40_NewsSentimentTool
```

---

## 2. Create a Virtual Environment

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Required Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the Application

The application can be started using either of the following commands:

```bash
flask run
```

OR

```bash
python run.py
```

---

## 5. Open the Application

Open the following URL in your browser:

```text
http://127.0.0.1:5000
```

---

# Running Tests

## Run All Unit Tests

```bash
python -m unittest discover
```

## Run one specific (e.g.,Competitor Analysis Tests Only)

```bash
python -m unittest tests.test_competitor
```

---

# Database

The application uses SQLite with SQLAlchemy ORM for persistent data storage.

Database migrations are managed using Flask-Migrate.

---

# Security Features

- Password hashing
- CSRF protection using Flask-WTF
- Secure Flask configuration
- Environment variable support

---

# Agile Development Process

This project was developed using Agile development methodologies and GitHub collaboration workflows including:

- Git branches
- Pull requests
- GitHub Issues
- Code reviews
- Incremental feature development
- Regular commits with descriptive commit messages


---

This project was developed as part of:
**CITS3403 / CITS5505 — Agile Web Development**
The University of Western Australia

© 2026
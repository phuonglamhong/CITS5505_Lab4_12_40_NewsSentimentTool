# BrandPulse

A web-based news sentiment monitoring platform built with Flask.

## Contributors

| Student ID | Names           | GitHub usernames |
| ---------- | --------------- | ---------------- |
| 24758673   | Zunhao Zhang    | 33fish           |
| 24600969   | Lola Xu         | Redlola          |
| 24453423   | Hong Phuong Lam | phuonglamhong    |
| 24717854   | K Ishwari Raj   | Kishwari         |

## Project Overview

BrandPulse is a web-based sentiment monitoring platform that helps users track public opinion, compare competitor sentiment trends, and interact with media content through an intuitive dashboard interface.

The application classifies content into positive, neutral and negative sentiment categories and visualises results through interactive charts, dashboards and discussion features.

The system follows a client-server architecture using Flask on the backend and HTML, CSS, JavaScript, Bootstrap and Tailwind CSS on the frontend.

## Features

* Interactive sentiment dashboard
* Competitor sentiment comparison
* News media feed
* User authentication system
* Comment and collaboration functionality
* Responsive mobile-friendly interface
* Dynamic frontend rendering using JavaScript and Fetch API
* Persistent SQLite database storage
* Flask Blueprints for modular backend structure
* Unit testing for backend routes and models

## Tech Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap 5
* Tailwind CSS
* Chart.js

### Backend

* Flask
* Flask-WTF
* Flask-SQLAlchemy
* Flask-Mail

### Database

* SQLite
* SQLAlchemy ORM

### Testing

* Python unittest

## Design Principles

The application was designed with a focus on:

* Responsive user experience
* Clear data visualisation
* Modular backend architecture
* Maintainable frontend structure
* Scalable Flask application design

## Project Structure

```
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
│   ├── js/
│   └── images/
│
├── templates/
│
├── tests/
│
├── instance/
│
├── requirements.txt
└── run.py
```

## Installation and Setup

### 1. Clone the Repository

```
git clone https://github.com/phuonglamhong/CITS5505_Lab4_12_40_NewsSentimentTool.git
cd CITS5505_Lab4_12_40_NewsSentimentTool
```

### 2. Create a Virtual Environment

#### Mac/Linux

```
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```
python -m venv venv
venv\Scripts\activate
```

### 3. Install Required Dependencies

```
pip install -r requirements.txt
```

### 4. Database Migration

For first-time setup:

```
flask db init
```

Run migrations:

```
flask db migrate
flask db upgrade
```

### 5. Run the Application

The application can be started using either of the following commands:

```
flask run
```

OR

```
python run.py
```

### 6. Open the Application

Open the following URL in your browser:

```
http://127.0.0.1:5000
```

## Running Tests

### Run All Unit Tests

```bash
python -m unittest discover
```

### Run Competitor Analysis Tests Only

```bash
python -m unittest tests.test_competitor
```

### Selenium Testing

Install Selenium:

```bash
pip install selenium
```

Install pytest:

```bash
pip install pytest
```

Download a matching version of ChromeDriver:

[https://googlechromelabs.github.io/chrome-for-testing/](https://googlechromelabs.github.io/chrome-for-testing/)

Run Selenium tests:

```bash
pytest tests/seleniumTest
```


## Database

The application uses SQLite with SQLAlchemy ORM for persistent data storage.

Database migrations are managed using Flask-Migrate.

## Security Features

* Password hashing
* CSRF protection using Flask-WTF
* Secure Flask configuration

## Development Workflow

The project followed an Agile development workflow using:

* Git branches
* Pull requests
* GitHub Issues
* Code reviews
* Incremental feature development
* Regular commits with descriptive commit messages

## Future Improvements

* Real-time sentiment tracking
* AI-generated article summaries
* Notification system
* Advanced search and filtering
* Dark mode support

## Screenshots

![Competitor Analysis](static/images/competitor-analysis.png)

This project was developed as part of:

CITS5505 — Agile Web Development
The University of Western Australia



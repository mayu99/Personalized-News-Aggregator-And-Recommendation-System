# 📰 Personalized News Aggregator & Recommendation System

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.x-092E20?style=flat&logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/DRF-3.12+-red?style=flat)
![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?style=flat&logo=openai&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-psycopg2-336791?style=flat&logo=postgresql&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Elastic%20Beanstalk-FF9900?style=flat&logo=amazonaws&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=flat)

A full-stack Django web application that fetches live news from multiple external sources and delivers a personalized, interest-based news feed to each authenticated user. Built with production deployment in mind — served via Gunicorn, deployed to AWS Elastic Beanstalk, and backed by PostgreSQL in production.

---

## 🚀 Features

- **Personalized Feed** — Users select topic interests at registration; the system filters and ranks articles accordingly
- **Live News Fetching** — Custom Django management command (`fetch_news`) pulls fresh articles from external news APIs on demand or on schedule
- **User Authentication** — Full registration, login, and profile management via the `accounts` and `users` Django apps
- **Admin Panel** — Django admin interface for managing articles, sources, users, and content moderation
- **REST API Layer** — Django REST Framework (DRF) exposes API endpoints for article retrieval and user preferences
- **OpenAI Integration** — Used for content enrichment and recommendation scoring
- **Production-Ready Deployment** — Gunicorn WSGI server, WhiteNoise for static files, `dj-database-url` for environment-driven DB config, AWS Elastic Beanstalk via `.ebextensions`

---

## 🏗️ Architecture & Project Structure

```
├── accounts/           # User authentication (register, login, profile)
├── apps/               # Core Django app configuration
├── news/               # News article models, views, fetch logic
├── news_aggregator/    # Project settings and URL routing
├── users/              # User preferences and personalization logic
├── templates/          # HTML templates (Jinja/Django templating)
├── static/             # CSS, JS, front-end assets
├── staticfiles/        # Collected static files (WhiteNoise served)
├── tests/              # Unit and integration tests
├── .ebextensions/      # AWS Elastic Beanstalk deployment config
├── Procfile            # Gunicorn process definition for deployment
├── requirements.txt    # Python dependencies
├── manage.py           # Django CLI entry point
└── settings.py         # Environment-aware project settings
```

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | Django 4.x |
| REST API | Django REST Framework 3.12+ |
| AI / Enrichment | OpenAI API |
| Database (Dev) | SQLite |
| Database (Prod) | PostgreSQL (via psycopg2-binary + dj-database-url) |
| Static Files | WhiteNoise |
| WSGI Server | Gunicorn |
| Deployment | AWS Elastic Beanstalk |
| Config Management | python-dotenv |

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.10+
- pip
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/mayu99/Personalized-News-Aggregator-And-Recommendation-System.git
cd Personalized-News-Aggregator-And-Recommendation-System

# 2. Create and activate a virtual environment
python -m venv venv

# On Windows
.\venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your API keys (OpenAI, News API, etc.)

# 5. Apply migrations
python manage.py migrate

# 6. Create a superuser (for admin panel access)
python manage.py createsuperuser
```

### Running Locally

Open two terminal windows:

**Terminal 1 — Fetch latest news articles:**
```bash
python manage.py fetch_news
```

**Terminal 2 — Start the development server:**
```bash
python manage.py runserver
```

Then navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Admin panel is available at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🌐 Deployment (AWS Elastic Beanstalk)

This project is configured for deployment to AWS Elastic Beanstalk using:

- **`Procfile`** — Defines the Gunicorn process: `web: gunicorn news_aggregator.wsgi`
- **`.ebextensions/`** — Environment configuration for EB (Python platform, static file routing, environment variables)
- **WhiteNoise** — Serves static files efficiently without a separate CDN
- **`dj-database-url`** — Reads `DATABASE_URL` from environment for PostgreSQL in production

```bash
# Deploy using EB CLI
eb init
eb create news-aggregator-env
eb deploy
```

---

## 🧪 Running Tests

```bash
python manage.py test tests/
```

---

## 📋 Environment Variables

Create a `.env` file in the project root with the following:

```env
SECRET_KEY=your-django-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.elasticbeanstalk.com,localhost

# Database (production)
DATABASE_URL=postgres://user:password@host:5432/dbname

# News API
NEWS_API_KEY=your-news-api-key

# OpenAI
OPENAI_API_KEY=your-openai-api-key
```

---

## 📄 Academic Context

This project was developed as part of **DATA 236** at San Jose State University. The full project report and slide deck are included in the repository:
- `Group5_DATA236_Report.pdf`
- `Group5_DATA236_Slides.pdf`

---

## 👤 Author

**Mayuresh Pramod Pandey**
- GitHub: [@mayu99](https://github.com/mayu99)
- LinkedIn: [linkedin.com/in/mayureshpp](https://linkedin.com/in/mayureshpp)
- Portfolio: [portfolio-nine-virid-94.vercel.app](https://portfolio-nine-virid-94.vercel.app)

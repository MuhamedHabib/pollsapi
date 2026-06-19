# Polls API

> A token-authenticated REST API for creating polls, adding choices, and casting votes — built with Django and Django REST Framework.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/DRF-A30000?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

## Overview

`pollsapi` is a REST API that exposes a small polling domain over HTTP/JSON. It models three resources — **Poll**, **Choice**, and **Vote** — and lets authenticated users create polls, attach choices to a poll, and vote on those choices.

Key characteristics of the implementation:

- **Token authentication** via DRF's `TokenAuthentication` (plus `SessionAuthentication`); all endpoints require an authenticated user by default (`IsAuthenticated`), except user registration and login.
- **Ownership rules** — only the user who created a poll may add choices to it or delete it; attempting otherwise returns `403 Permission Denied`.
- **One vote per user per poll** — enforced at the model layer with a `unique_together` constraint on `(poll, voted_by)`.
- **Nested routing** — choices and votes are addressed under their parent poll for an intuitive URL structure.
- The project demonstrates several DRF view styles side by side: plain Django function views, `APIView` subclasses, the `generics.*` classes, and a `ModelViewSet` wired through a router.

### Data model

| Model | Fields | Notes |
|-------|--------|-------|
| `Poll` | `question`, `created_by` (User FK), `pub_date` | A question authored by a user |
| `Choice` | `poll` (FK), `choice_text` | An option belonging to a poll |
| `Vote` | `choice` (FK), `poll` (FK), `voted_by` (User FK) | Unique per `(poll, voted_by)` |

## API Endpoints

All routes are served under the project root (`pollsapi.urls` includes `polls.urls`).

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/users/` | Register a new user (auth-exempt); creates an auth token on signup |
| `POST` | `/login/` | Authenticate with `username` / `password`, returns an auth token |
| `GET`, `POST` | `/polls/` | List polls or create a poll (router `ModelViewSet`) |
| `GET`, `PUT`, `PATCH`, `DELETE` | `/polls/<pk>/` | Retrieve, update, or delete a poll (delete restricted to its creator) |
| `GET`, `POST` | `/polls-api-view/` | List polls or create a poll (`ListCreateAPIView`) |
| `GET`, `DELETE` | `/polls-api-view/<pk>/` | Retrieve or delete a single poll (`RetrieveDestroyAPIView`) |
| `GET`, `POST` | `/polls-api-view/<pk>/choices/` | List or create choices for a poll (create restricted to the poll's creator) |
| `POST` | `/polls-api-view/<pk>/choices/<choice_pk>/vote/` | Cast a vote for a choice within a poll |
| `GET`, `POST` | `/choices/` | List/create choices (legacy flat route) |
| `POST` | `/vote/` | Cast a vote (legacy flat route) |
| — | `/admin/` | Django admin site |

> Endpoints prefixed with `/polls/` are provided by a `DefaultRouter`-registered `PollViewSet`; the `/polls-api-view/` variants demonstrate the equivalent `generics.*` and nested designs.

## Tech Stack

- **Python**
- **Django** 4.0.x
- **Django REST Framework** 3.13.x (Token + Session authentication, DRF authtoken)
- **SQLite** (default development database, `db.sqlite3`)
- **CI:** CircleCI (`circleci/config.yml`) and a GitHub Actions workflow (`.github/workflows/python-package.yml`) running `manage.py test` / `pytest` and `flake8`

## Getting Started

### Prerequisites

- Python 3 (the CI matrix exercises 3.9–3.11)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/MuhamedHabib/pollsapi.git
cd pollsapi

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install Django djangorestframework

# 4. Apply database migrations
python manage.py migrate

# 5. (Optional) create an admin user
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

The API is then available at `http://127.0.0.1:8000/`.

### Running the tests

```bash
python manage.py test
```

The test suite (`polls/tests.py`) uses DRF's `APIClient` / `APITestCase` to verify authenticated listing and poll creation.

## Notes

- This is a learning / portfolio project built around the classic Django REST Framework polls tutorial; the source files include extensive inline commentary documenting each DRF concept (serializers, generic views, viewsets, routers, token auth, and testing).
- The repository does not ship a populated `requirements.txt`; the core dependencies are **Django** and **djangorestframework** (install commands above).
- The bundled settings use Django's default development configuration (`DEBUG = True`, SQLite). Before any production use, move secrets to environment variables, disable debug, and configure `ALLOWED_HOSTS` and a production-grade database.
- Continuous integration is wired through both CircleCI and GitHub Actions to install dependencies and run the test suite on each push.

---
<p align="center">Built by <b>Mohamed Habib Khattat</b> — <a href="https://github.com/MuhamedHabib">GitHub (@MuhamedHabib)</a> · <a href="https://www.linkedin.com/in/mohamed-habib-khattat-2b206a173">LinkedIn</a></p>

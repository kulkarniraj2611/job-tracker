# Job Application Tracker

A small Flask + PostgreSQL web app for tracking job applications: company,
role, status (Applied → Interview → Offer/Rejected), applied date, and a
reminder date for upcoming follow-ups. Built as a CCA2 (Cloud Computing &
DevOps) project — delivered through Git and a CI/CD pipeline.

## Features

- Add / edit / delete job applications
- Status workflow with valid-transition checks (no skipping straight from
  Applied to Offer, for example)
- Filter applications by status
- Reminders view/endpoint for applications with a reminder date in the next
  3 days
- JSON API (`/api/applications`) alongside the server-rendered UI
- Dockerized, with a docker-compose setup for local app + database
- GitHub Actions CI: installs deps, runs the test suite, builds the image

## Tech stack

- Python 3.11, Flask, Flask-SQLAlchemy, Flask-Migrate
- PostgreSQL
- Gunicorn (production server)
- Docker / docker-compose
- pytest for tests
- GitHub Actions for CI

## Run locally (without Docker)

```bash
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt

# Start a local Postgres (or point DATABASE_URL at one you already have)
docker run --name jobtracker-db -e POSTGRES_PASSWORD=pass \
  -e POSTGRES_DB=jobtracker -p 5432:5432 -d postgres

flask --app run db init
flask --app run db migrate -m "initial"
flask --app run db upgrade

python run.py
```

Visit `http://localhost:5000`.

## Run with Docker Compose

```bash
docker compose up --build
```

This starts both the Postgres database and the Flask app (via Gunicorn) on
`http://localhost:5000`.

## Run tests

```bash
pytest -v
```

Tests use an in-memory SQLite database, so no external database is needed.

## API reference

| Method | Endpoint                        | Description                          |
|--------|----------------------------------|---------------------------------------|
| GET    | `/api/applications`              | List all applications                 |
| GET    | `/api/applications/<id>`         | Get one application                   |
| POST   | `/api/applications`              | Create an application                 |
| PUT    | `/api/applications/<id>`         | Update fields / status                |
| DELETE | `/api/applications/<id>`         | Delete an application                 |
| GET    | `/api/applications/reminders`    | Applications due for reminder in ≤3 days |

## CI/CD

- **CI**: `.github/workflows/ci.yml` runs on every push/PR to `main` —
  installs dependencies, runs `pytest`, and builds the Docker image.
- **CD**: connect this repository to a platform such as Render or Railway,
  pointed at the `Dockerfile`, with auto-deploy on push to `main`. Set the
  `DATABASE_URL` environment variable there to the managed Postgres
  instance's connection string.

## Project structure

```
job-tracker/
  app/
    __init__.py      # app factory
    models.py         # Application, Status
    routes.py         # web + API routes
  templates/
    index.html
    form.html
  static/
    style.css
  tests/
    test_app.py
  config.py
  run.py
  requirements.txt
  Dockerfile
  docker-compose.yml
  .github/workflows/ci.yml
```

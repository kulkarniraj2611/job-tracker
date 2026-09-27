# Job Application Tracker

A Flask + PostgreSQL web application for tracking job applications. The application allows users to add, edit, delete, and filter job applications while tracking application status and upcoming follow-up reminders.

This project was developed as a CCA 2 (Cloud Computing & DevOps) project and delivered using Git, GitHub Actions, Docker, and Render.

## Live Application

https://job-tracker-lh2q.onrender.com/

## GitHub Repository

https://github.com/kulkarniraj2611/job-tracker

## Features

- Add job applications
- Edit job applications
- Delete job applications
- Track application status:
  - Applied
  - Interview
  - Offer
  - Rejected
- Validate status transitions
- Filter applications by status
- Track applied dates
- Set reminder dates for upcoming follow-ups
- View applications with reminders due within the next 3 days
- JSON API for application data
- Server-rendered web interface using Flask and Jinja
- Health check endpoint at `/health`
- Dockerized application
- Automated testing with pytest
- Code linting with Flake8
- CI/CD using GitHub Actions
- Deployment to Render

## Tech Stack

- Python 3.11
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- PostgreSQL
- Gunicorn
- Docker
- pytest
- Flake8
- Git
- GitHub Actions
- Render

## Application Architecture

The application follows this basic architecture:

```text
Browser
   |
   v
Flask Application
   |
   v
SQLAlchemy
   |
   v
PostgreSQL Database



## The CI/CD pipeline follows:
GitHub
   |
   v
GitHub Actions
   |
   +--> Flake8
   |
   +--> pytest
   |
   +--> Docker Build
   |
   +--> Docker Container
   |
   +--> /health Check
   |
   v
Render Deployment
   |
   v
Live Application

Run Locally Without Docker
1. Create a virtual environment
Windows:
python -m venv venv
venv\Scripts\activate

Linux/macOS:
python -m venv venv
source venv/bin/activate

2. Install dependencies
pip install -r requirements.txt

3. Configure PostgreSQL
Set the DATABASE_URL environment variable to your PostgreSQL database connection string.
Example:
postgresql+psycopg2://postgres:password@localhost:5432/jobtracker

4. Run database migrations
flask --app run db upgrade

5. Start the application
python run.py

The application will be available at:
http://localhost:5000

Run with Docker Compose
The project includes a Docker Compose configuration for running the Flask application and PostgreSQL locally.
docker compose up --build

The application will be available at:
http://localhost:5000

Docker
The project contains a Dockerfile that defines how the Flask application is prepared and started.
The Dockerfile:
- Uses Python 3.11
- Installs the project dependencies
- Copies the application code
- Exposes port 5000
- Starts the Flask application using Gunicorn
The Docker flow is:
Dockerfile
    |
    v
Docker Image
    |
    v
Docker Container
    |
    v
Flask Application

Testing
The project uses pytest for automated testing.
Run the tests locally using:
python -m pytest -v

The project contains 9 automated tests covering application functionality and the health endpoint.
The CI/CD pipeline runs the tests automatically.
If a test fails, the build-and-test job fails and the deployment job does not run.
Code Quality
The project uses Flake8 for Python code linting.
Run Flake8 locally:
flake8 .

The GitHub Actions pipeline runs Flake8 before running the tests.
Health Check
The application provides a health check endpoint:
/health

Live health check:
https://job-tracker-lh2q.onrender.com/health
It returns:
{
  "status": "ok"
}

The CI/CD pipeline uses this endpoint to verify that the Docker container started successfully and that the Flask application is responding.
The pipeline checks:
curl -f http://localhost:5000/health

If the health check fails, the build-and-test job fails and deployment is prevented.
API Reference
Method	Endpoint	Description
GET	/api/applications	List all applications
GET	/api/applications/<id>	Get one application
POST	/api/applications	Create an application
PUT	/api/applications/<id>	Update application fields/status
DELETE	/api/applications/<id>	Delete an application
GET	/api/applications/reminders	Get applications with upcoming reminders


CI/CD Pipeline
The project uses GitHub Actions for Continuous Integration and Continuous Deployment.
The workflow file is:
.github/workflows/ci-cd.yml

The workflow is triggered when:
- Code is pushed to main
- A Pull Request is created targeting main
CI Pipeline
The pipeline performs the following steps:
Checkout Repository
       |
       v
Setup Python 3.11
       |
       v
Install Dependencies
       |
       v
Run Flake8
       |
       v
Run pytest
       |
       v
Build Docker Image
       |
       v
Run Docker Container
       |
       v
Check /health

Deployment
Deployment runs only when:
1. The workflow is triggered by a push to main
2. The build-and-test job succeeds
The deployment job uses the Render Deploy Hook stored as a GitHub Secret.
The workflow also passes the GitHub commit SHA to Render so that the deployed version corresponds to the tested commit.
Successful CI
      |
      v
Deploy Job
      |
      v
Render Deploy Hook
      |
      v
Render
      |
      v
Live Application

GitHub Actions
The workflow uses:
runs-on: ubuntu-latest

to run jobs on a GitHub-hosted Ubuntu runner.
It uses:
uses: actions/checkout@v4

to check out the repository code.
Python is configured using:
uses: actions/setup-python@v5

with Python 3.11.
The deployment job depends on the CI job:
needs: build-and-test

Therefore, deployment will not occur if linting, testing, Docker build, Docker execution, or the health check fails.
Environment Variables and Secrets
The application uses environment variables for configuration.
Important variables include:
DATABASE_URL
SECRET_KEY
RENDER_GIT_COMMIT

The Render deployment hook is stored securely as a GitHub Actions Secret:
RENDER_DEPLOY_HOOK

Sensitive credentials and deployment information are not stored directly in the source code.
Git Workflow
The project uses Git and GitHub for version control.
Typical workflow:
Create/modify code
       |
       v
git add
       |
       v
git commit
       |
       v
git push
       |
       v
GitHub
       |
       v
GitHub Actions

Feature development can be performed on separate branches and merged into main using Pull Requests.
The project includes a merged Pull Request for the health endpoint test.
Project Structure
job-tracker/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   └── routes.py
│
├── templates/
│   ├── index.html
│   └── form.html
│
├── static/
│   └── style.css
│
├── tests/
│   └── test_app.py
│
├── migrations/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── config.py
├── run.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .flake8
├── .gitignore
└── README.md

Deployment
The application is deployed on Render.
Live URL:
https://job-tracker-lh2q.onrender.com/
The application uses:
- Flask
- Gunicorn
- Docker
- PostgreSQL
Render provides the deployed commit ID through the RENDER_GIT_COMMIT environment variable.
The application displays the running commit ID in the footer, which helps verify which version is currently deployed.
Example:
Running commit: a633a87

Final Project Details
Application: Job Application Tracker
Language: Python
Framework: Flask
Database: PostgreSQL
Testing: pytest
Linting: Flake8
Containerization: Docker
CI/CD: GitHub Actions
Deployment: Render
Application Port: 5000
Health Endpoint: /health
Automated Tests: 9
Git Commits: 13
Merged Pull Requests: 1

Author
Developed individually as part of the CCA 2 Cloud Computing & DevOps project.

After replacing the file, save it and run:

```bash
git add README.md
git commit -m "docs: update README"
git push origin main

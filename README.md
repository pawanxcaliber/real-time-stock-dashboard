Web Hosting using CI/CD and DevOps Practices
This repository serves as a practical demonstration of modern web application hosting, Continuous Integration (CI), Continuous Deployment (CD), containerization, and monitoring using various DevOps tools and platforms. The project is built around a simple real-time stock dashboard concept, but the primary focus is on the infrastructure and automation pipeline rather than complex application features.

Project Overview
The goal of this project is to illustrate an end-to-end DevOps workflow for a web application. It includes:

A simple Backend API built with Flask (Python).

A basic Frontend UI built with React (JavaScript).

Containerization using Docker for both the API and UI.

Local Orchestration using Docker Compose to run the entire stack (API, UI - temporarily served separately locally, Prometheus, Grafana) during development.

Continuous Integration (CI) using GitHub Actions for linting, testing, and building Docker images.

Continuous Deployment (CD) integrated into the CI pipeline to automatically deploy the UI to GitHub Pages (static hosting) and the API to Render (dynamic hosting).

Monitoring setup using Prometheus (metrics collection) and Grafana (visualization).

While the stock dashboard functionality is basic (currently fetching price data via yfinance), the core value of this project lies in the automated pipeline and infrastructure setup.

Architecture
The project follows a microservices-like architecture, with separate containers for the API and UI, plus dedicated containers for monitoring:

graph TD
    UserBrowser --> |HTTP Requests| NginxUI(UI Container - Nginx)
    NginxUI --> |Static Files| BuiltUI(Built React App)
    UserBrowser --> |HTTP Requests| FlaskAPI(API Container - Flask)
    FlaskAPI --> |Data Fetching (yfinance)| ExternalAPI(External Stock Data Source)
    FlaskAPI --> |Exposes Metrics (/metrics)| Prometheus(Prometheus Container)
    Prometheus --> |Scrapes Metrics| FlaskAPI
    UserBrowser --> |HTTP (Port 3000)| Grafana(Grafana Container)
    Grafana --> |Queries Metrics| Prometheus
    LocalDevHost --> |Docker Compose| FlaskAPI
    LocalDevHost --> |Docker Compose| Prometheus
    LocalDevHost --> |Docker Compose| Grafana
    LocalDevHost --> |'serve' (Port 3000)| BuiltUI(Built React App - Local)
    GitHubRepo --> |Push| GitHubActions(GitHub Actions CI/CD)
    GitHubActions --> |Build & Deploy UI| GitHubPages(GitHub Pages - Static Hosting)
    GitHubActions --> |Trigger Deploy Hook| Render(Render - Dynamic Hosting)

(Note: The local UI serving with serve is a temporary workaround for local development due to Nginx configuration challenges in the container. The deployed version uses Nginx.)

Prerequisites
To run this project locally and work with the pipeline, you need the following installed on your Linux Mint machine:

Git

Docker Engine

Docker Compose

Node.js and npm (LTS version recommended, e.g., v20)

Python 3 and pip

Python Virtual Environments (venv)

serve (for local UI serving workaround: sudo npm install -g serve)

A GitHub account and a repository to host the code.

Accounts on GitHub Pages (free, integrated with GitHub) and Render (free tier available for web services).

Local Setup and Running
Follow these steps to get the application and monitoring stack running locally using Docker Compose and serve for the UI:

Clone the repository:

git clone https://github.com/pawanxcaliber/YOUR_REPO_NAME.git # Replace YOUR_REPO_NAME
cd YOUR_REPO_NAME # Replace YOUR_REPO_NAME

Setup Python Virtual Environment for API:

cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd .. # Back to repo root

Setup Node.js Dependencies for UI:

cd ui
npm install
cd .. # Back to repo root

Build Docker Images:
Build the Docker images for the API, Prometheus, and Grafana (UI image is not needed for this local setup).

docker-compose build stock-api prometheus grafana

Run the Docker Compose Stack (API, Prometheus, Grafana):
Start the backend and monitoring services.

docker-compose up -d stock-api prometheus grafana

(The -d flag runs containers in detached mode).

Build the UI Locally:
Navigate to the UI directory and build the static assets.

cd ui
npm run build

This creates the dist/ directory.

Serve the UI Locally:
Run the serve command from the dist/ directory.

serve -s dist

Note the URL provided by serve (usually http://localhost:3000/).

Access the Application:

UI: Open your web browser and go to the URL provided by the serve command (e.g., http://localhost:3000/). You should see the simple stock checker interface.

API: The API is running in Docker and accessible at http://localhost:8000/. You can test endpoints like http://localhost:8000/health or http://localhost:8000/stock/AAPL.

Prometheus UI: http://localhost:9090/

Grafana UI: http://localhost:3000/ (Note: This might conflict with the UI served by serve. If so, change the Grafana port mapping in docker-compose.yml or the serve port).

Stop the Stack:
In the terminal where serve is running, press Ctrl+C.
In the terminal where you ran docker-compose up -d, run:

docker-compose down

CI/CD Pipeline (GitHub Actions)
The project uses GitHub Actions to automate the build, test, and deployment process on every push to the main branch.

.github/workflows/ci_api.yml: Builds the API Docker image, runs linters (Flake8), and triggers deployment to Render via a deploy hook.

.github/workflows/ci_ui.yml: Builds the UI static assets, runs linters (ESLint/Prettier), and deploys the built site to GitHub Pages using the peaceiris/actions-gh-pages action.

Deployment Platforms:

Frontend (UI): Deployed to GitHub Pages for static hosting. The UI is accessible at https://pawanxcaliber.github.io/YOUR_REPO_NAME/. Configuration for subdirectory hosting is handled in ui/vite.config.js and potentially Nginx if serving with Docker in production.

Backend (API): Deployed as a Web Service on Render for dynamic hosting. Deployment is triggered by a GitHub Actions workflow using a secure Deploy Hook URL stored as a GitHub Secret (RENDER_API_DEPLOY_HOOK_URL).

Monitoring (Prometheus & Grafana)
The project includes a basic monitoring setup:

Prometheus: Configured via prometheus/prometheus.yml to scrape metrics from the /metrics endpoint exposed by the Flask API container (stock-api:8000). Accessible locally at http://localhost:9090/.

Grafana: Configured via docker-compose.yml to run and use Prometheus as a data source. Accessible locally at http://localhost:3000/. You can create dashboards to visualize API request counts (http_requests_total), request rate (rate(http_requests_total[5m])), and other default Python/Flask metrics.

Infrastructure as Code (Ansible)
The iac/ansible/ directory contains a placeholder playbook (install_local_env.yml) for automating the installation of prerequisites like Docker and a local Kubernetes environment (e.g., k3s or kind) on a target Linux host. This demonstrates the concept of managing infrastructure using code.

Future Enhancements
This project can be extended in many ways:

Implement real-time stock data fetching and display in the UI (e.g., using WebSockets or long polling).

Add more sophisticated charting and data visualization in the UI.

Implement comprehensive unit and integration tests for both API and UI.

Add more advanced monitoring (e.g., custom application metrics, logging, tracing).

Explore different deployment strategies (e.g., blue/green, canary releases).

Finalize the Ansible playbook for automated environment setup.

Explore container orchestration with Kubernetes (as planned in Day 5).

Add security scanning to the CI pipeline.

Improve API robustness (error handling, rate limiting, authentication).

Implement a production-ready WSGI server (like Gunicorn) for the Flask API in the Docker container.

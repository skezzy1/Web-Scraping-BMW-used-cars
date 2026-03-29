# BMW Used Cars
# 🚗 BMW Used Cars Scraper & API

![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135.2-009688.svg?style=flat&logo=fastapi&logoColor=white)
![Scrapy](https://img.shields.io/badge/Scrapy-2.11-60A839.svg?style=flat&logo=scrapy&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)
![Lint Status](https://github.com/skezzy1/Web-Scraping-BMW-used-cars/actions/workflows/lint.yml/badge.svg)
![Coverage](badges/coverage.svg)
## Tech details

|         **Resource**          | **Resource Name** | **Version** | **Comment** |
|:-----------------------------:|:-----------------:|:-----------:|:-----------:|
| Back-end programming language |      Python       |    3.12     |             |
|    Back-end web framework     |      FastAPI      |   0.135.2  |             |
|           Database            |      SQLite       |         |             |
|          Web server           |      Uvicorn      |   0.29.0    |             |
## Local development
### Running locally
#### Create virtual enviroment
```bash
python3.12 -m venv venv
```
#### Download packages and activate virtual environment
````bash
pip install -r requirements.txt && . venv/bin/activate
````
#### Start local server
````bash
python -m uvicorn app.main:app --reload
````
## Docker Deployment (Recommended)
Running the application via Docker is the recommended approach. It automatically handles all system-level dependencies required by Playwright (Chromium) and ensures an isolated, consistent environment.

### Prerequisites
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

### Running the Application
**Build and start the container:**
   ```bash
   docker-compose up --build
```
### Testing

**1. Basic Test Run**
To simply execute the test suite and ensure all components are working properly:
```bash
poetry run pytest tests/
```
2. Test Run with Coverage
To execute tests and generate a detailed coverage report (showing the exact lines of code missing tests directly in the terminal):
```bash
poetry run pytest --cov=app --cov-report=term-missing tests/
```
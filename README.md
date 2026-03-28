# BMW Used Cars
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
1. **Build and start the container:**
   ```bash
   docker-compose up --build
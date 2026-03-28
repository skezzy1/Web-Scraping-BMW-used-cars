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
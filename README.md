<p align="center">
<h2 align="center"> Pro Devs Assignment </h2>
<h4 align="center"> The Solution is provided using FastAPI </h4>

---
## About
This solution is built with FastAPI.
It uses SQLAlchemy as the ORM. 
And the dependencies are managed with poetry.
The choice of Database is PostGreSQL.

## Features

- [x] Database Connection Using SQLAlchemy
- [x] FastAPI Server
- [x] Unit Testing with Unittest
- [x] Basic CRUD for Posts

<br>

## Dependencies

- Python 3.10+
- Poetry
- PostGreSQL

## Running

- Clone the repo using

```bash
git clone https://github.com/vheckthor/prodevassessments.git
```

- Create a Virtual Environment using

```bash
curl -sSL https://install.python-poetry.org 
```

- Activate the virtualenv

```bash
poetry shell
```

- Install dependencies

```bash
poetry install
```

- Setting up environment variables
  create a .env file and add the key calue pair below and set the appropriate value

| Key     | Value |
| ----------- | ----------- |
POSTGRES_SERVER localhost
POSTGRES_USER postgres
POSTGRES_PASSWORD your_postres_password
POSTGRES_DB your_db_name
PROJECT_NAME Prodev
IPIFY_API_KEY Not_needed
SECRET_KEY yoursecretkey

- To run the project

```bash
 uvicorn app.main:app --reload --port 8001
```
## Running Tests
To run the test, make sure the .env files are setup correctly and use the command below

```bash
python -m unittest discover app "*_test.py"  
```
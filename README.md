<p align="center">
<h2 align="center"> Pro Devs Assignment </h2>
<h4 align="center"> The Solution is provided using FastAPI </h4>

---

## About

This solution is built with FastAPI.
It uses SQLAlchemy as the ORM.
And the dependencies are managed with poetry.
The choice of Database is PostGreSQL.

## Challenge

Please create a python based REST server with the following resources and endpoints. Please use your preferred python web stack and database, however we would prefer you to use Flask and postgres. Each endpoint should have the required object and database model where required, correct validation of inputs, unit tests that test against the REST endpoints and make use of mocked third party dependencies where required. Each endpoint should be documented with proper REST documentation accessible via a documentation endpoint.
Resources

### /api/users

- Create, Retrieve, Update, Delete API with the required object and database model offering user first name, last name, email, phone number, password.

### /api/accounts

- This API should be “authenticated” defined as requiring the user id and password in the HTTP header of your choice (plain text is fine) and otherwise should return a 403.
- Create, Retrieve, Update, Delete API with the required object and database model offering account name.

### /api/accounts/{id}/transactions

- This API should be “authenticated” defined as requiring the user id and password in the HTTP header of your choice (plain text is fine) and otherwise should return a 403.
- Create credit and debit transaction API representing deposits and withdrawals against the account in the URL. Model should include at least an amount and a description of the transaction as a string as well as the user's IP at time of the request. This should be retrieved from <https://www.ipify.org/> for each request. ipify.org should be mocked in the tests.
- List of transactions supporting paging and search by transaction description.

### /api/accounts/{id}

- This API should be “authenticated” defined as requiring the user id and password in the HTTP header of your choice (plain text is fine) and otherwise should return a 403.
- Single get against an id should return the account identifiers and a balance of the
account as well as the count of total transactions in the current account.

## Features

- [x] Database Connection Using SQLAlchemy
- [x] FastAPI Server
- [x] Unit Testing with Unittest
- [x] Basic CRUD for Posts, GET, PUT

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

| Key             |    Value    |
| --------------  | ----------- |
POSTGRES_SERVER   | localhost
POSTGRES_USER     | postgres
POSTGRES_PASSWORD | your_postres_password
POSTGRES_DB       | your_db_name
PROJECT_NAME      | Prodev
IPIFY_API_KEY     | Not_needed
SECRET_KEY        | yoursecretkey

- To run the project
run alembic migrations to update the db with latest model changes (migrations)

```bash
 alembic upgrade head
```

```bash
 uvicorn app.main:app
```

use `--reload` to run in auto-reload mode and `--port`  to specify port number

## Running Tests

To run the test, make sure the .env files are setup correctly and use the command below

```bash
python -m unittest discover app "*_test.py"  
```

## Authentication

- for routes that require authentication, a url (/users/authenticate) in the users router has been provided to get the jwt token that would be passed in the header for all routes requiring authentication. The user must be created before calling the auth route.
`Authorization : bearer the_jwt_token_gotten_from_the_auth_route`

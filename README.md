Booking service app
======
Server side app for booking application in python.

How to use
======

## VENV

```sh
# Activate venv on Windows:
venv\Scripts\activate.bat

# Activate venv on MacOS:
source venv/bin/activate
```

## DB

```sh
# Generate migrations
alembic revision --autogenerate -m "Initial migration"

# Upgrade all migrations
alembic upgrade head

# Downgrade all migrations
alembic downgrade -1
```

## server

```sh
# Start the server
uvicorn app.main:app --reload
```

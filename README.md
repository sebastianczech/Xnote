# Xnote

Web app in Python for managing private wallet, notes, reminders and others

## Work on local environment

### Use virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Install Django

```bash
pip install Django
pip list
```

### Start Django project

```bash
django-admin startproject xnote
```

### Start local server

```bash
# by script:
./start_local_server.sh

# or by commands:
cd xnote && python manage.py runserver
```

## Environment variables (config vars)

In git repository **ARE NOT STORED** sensitive variables:

```bash
DEBUG
SECRET_KEY
DISABLE_COLLECTSTATIC

MONGO_HOST
MONGO_PASSWORD
MONGO_USE

PG_HOST
PG_PASSWORD
PG_USER
```

Secret key can be generated by command:

```bash
openssl rand -base64 48
```

On local machine you can use all config vars by executing command:

```bash
. ./export_env.sh
```

where `export_env.sh` can contain:

```bash
export DEBUG=True
export SECRET_KEY=Secret
# and more ...
```

## Depenendencies

Freeze currently installed packages:
```bash
pip freeze > requirements.txt
```

Install packages from file:
```bash
pip install -r requirements.txt
```

## Tests

Start all tests:
```bash
pytest
```

Start all tests with coverage:
```bash
pytest --cov=patterns tests
```
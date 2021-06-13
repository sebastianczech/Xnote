# Xnote

Web app in Python for managing private wallet, notes, reminders and others

## Work on local environment

### Use virtual environment

```bash
python -m venv venv
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
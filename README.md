# Images

## About

Images app is an API that allows users to upload an image via HTTP request, and get access to URLs that directs to original image, thumbnail with specific sizes or get expirable link to that image. Permissions are set via Admin panel.

## Technologies

* Python 3.10.6
* Django 4.1.7
* Django Rest Framework 3.14.0
* Pillow Library

## Setup

* In `src/` subdirectory (where you see `Pipfile`) run these commands:

```bash
# install dependencies
pipenv --three install

# run database migrations
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate
```

Now, you need to run local development server with

```
pipenv run python manage.py runserver
```

* Go to http://localhost:8000

Credentials to authorize as SuperUser:
* login: admin
* password: testing321

Password works for any created user (basic_user, premium_user, enterprise_user). 

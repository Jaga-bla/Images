# Images

## About

Images app is an API that allows specific users to upload an image via HTTP request, and get access to URLs that directs to original image, thumbnail with specific sizes or get expirable link to that image. Permissions are set via Admin panel.

## Technologies

* Django
* Django Rest Framework
* Pillow Library

## Setup WITH DOCKER

The fastest way to run this project is to use docker-compose tool.

In project directory (where you see `docker-compose.yml`) run commad:
```shell
docker-compose up
```

## Setup NO DOCKER

* In `src/` subdirectory (where you see `Pipfile`) run these commands:

```bash
# install dependencies
pipenv --three install

# run database migrations
pipenv run python manage.py migrate

# create default admin user
pipenv run python manage.py create_default_superuser --username admin --password admin
```

Now, you need to run local development server with

```
pipenv run python manage.py runserver
```

* Go to http://localhost:8000

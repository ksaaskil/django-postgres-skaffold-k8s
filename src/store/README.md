# Django store

Example Django application, based mostly on [Django tutorial](https://docs.djangoproject.com/en/3.0/intro/tutorial01/).

## Running locally

### Postgres

Configuration for Postgres can be found in [`store/config.py`](./store/config.py).

First start Postgres server at port 5432 and create the required Postgres database:

```bash
$ createdb django-db
```

### Running Django in development mode

Install dependencies:

```bash
$ pip install -r requirements.txt
```

Then run locally:

```bash
python manage.py runserver
```

### Running in Docker

The Docker image serves Django application with [`gunicorn`](https://gunicorn.org/). See [`Dockerfile`](./Dockerfile) for full configuration.

Run locally in Docker:

```bash
$ docker build -t django-store .
$ docker run --rm --name django-store -p 8000:8000 django-store
```

### Running with nginx

The `gunicorn` server should never be exposed in production. You should use `nginx instead`. See the `nginx` configuration in [`nginx.conf`](./nginx.conf) and [`Dockerfile.nginx`](./Dockerfile.nginx).

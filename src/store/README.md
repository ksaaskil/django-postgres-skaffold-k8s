# Django store

First create the required Postgres database:

```bash
$ createdb django-db
```

Then run locally:

```bash
$ docker build -t django-store .
$ docker run --rm --name django-store -p 8000:8000 django-store
```

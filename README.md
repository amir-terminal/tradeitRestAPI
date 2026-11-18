# Tradeit REST API

A Django REST Framework backend for the Tradeit marketplace project. It exposes account, product, category, and messaging routes. The source also includes auction, trade, pickup, and shipping modules.

## Browse the API

With the application running locally, open Swagger UI at `/` or ReDoc at `/redoc/`. The routes are registered in [`core/urls.py`](core/urls.py).

| Prefix | Purpose |
| --- | --- |
| `/api/v1.0/` | Account and product endpoints registered by the versioned URL configuration |
| `/auth/` | Account routes |
| `/product/` | Product routes |
| `/chat/` | Messaging routes |
| `/admin/` | Django administration |

## Local development

Start with a Python 3.8 environment, the version recorded in the [Dockerfile](Dockerfile). The pinned stack in [`requirements.txt`](requirements.txt) includes Django 3.2, Django REST Framework, Channels, and GDAL 3.3.2. Install compatible GDAL and PROJ libraries, set up a PostgreSQL database with PostGIS, and review the database and GIS paths in [`core/settings.py`](core/settings.py) for your operating system. Use development credentials.

~~~bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
~~~

The checked-in Dockerfile runs Pipenv, but this branch ships `requirements.txt` without a Pipfile. Treat the Dockerfile as a reference until its dependency-install step is aligned with the repository.

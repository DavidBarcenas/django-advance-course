# Django Advance Course
Creating an api to share rides using django rest framework. This is part of the advanced Leavego course.

### Features
* Users Management
* Token handling with JWT
* Registration with confirmation email
* Authentication and permissions

### Running the app
Clone/download the project and run the following commands:

```bash
# Run the project
docker-compose -f local.yml up
```

To interact with the database
```bash
# Create migrations
docker-compose -f local.yml run --rm django python manage.py makemigrations

# Run migrations
docker-compose -f local.yml run --rm django python manage.py migrate

# Create superuser
docker-compose -f local.yml run --rm django python manage.py createsuperuser
```

### Technologies
* Django REST framework
* Environments with Docker
* PostgreSQL
* Celery
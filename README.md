# README
Secure Messaging Application

## Development Setup
To setup the stack, you'll need to run migrations:
```
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
```
Afterwards, you can debug the application with:
```docker-compose up```
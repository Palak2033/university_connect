release: python manage.py loaddata db.json; python manage.py makemigrations; python manage.py migrate; 
web: gunicorn core.wsgi
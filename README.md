# University Connect

University Connect is an ERP (Enterprise Resource Planning) platform written in Django for the backend and SQLite3 for database management. Bootstrap templates and jQuery have been used for the frontend.

## Deployment:
The website is automatically deployed to Heroku at https://university-connect-portal.herokuapp.com/ from the stable branch.
Limitations:
- Time is set to UTC and not IST as Heroku deploys on a US-based server
- Uploaded documents will not be accessible as that requires a cloud-service to be connected. Heroku requires credit-card verification for this which I haven't done.

## Documentation:
Source code for documentation can be found in the docs branch.
Sphinx documentation: https://palak2033.github.io/university_connect/

## Installing and Running locally
To run the code, you can clone or download this repository:
```
git clone https://github.com/Palak2033/university_connect.git
cd university_connect
```

After the repository is cloned, you can install the requisite libraries in a virtual environment. The repository has been tested with Python 3.9 so far.
```
# Using Conda
conda create -n env_name
conda activate env_name
conda install pip
pip install -r requirements.txt

# Using virtualenv
virtualenv env_name
source env_name/bin/activate
pip install -r requirements.txt
```

Before deploying the website, we need to make the migrations and migrate using
```
python manage.py makemigrations
python manage.py migrate
```

To locally deploy the website, you can run
```
python manage.py runserver
```

The website should open up in http://localhost:8000/ or http://127.0.0.1:8000/

Alternatively, if you use heroku, then you can do:
```
git checkout stable
python manage.py collectstatic
heroku local
```
for Linux and for Windows:
```
git checkout stable
python manage.py collectstatic
heroku local -f Procfile.windows
```
The website should open up in http://localhost:5000/

## Login Instructions
The main admin user is "admin@uconnect.com" and the password is "admin".
There are also faculty, faculty2, faculty3, student, student2, student3 each with the email "{username}@uconnect.com" and password "{username}" respectively.

The full list of login details is attached in Logins.md

Django also you to create a new super user using
```
python manage.py createsuperuser
```

## Features
- Admin:
- Faculty:
- Student:

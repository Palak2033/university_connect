# University Connect

University Connect is a Learning Management System written in Django for the backend and SQLite3 is used for database management. Bootstrap templates and jQuery have been used for the frontend.

The website is deployed on Heroku at: https://university-connect-portal.herokuapp.com/
The documentation for the codebase is deployed at: https://palak2033.github.io/university_connect/
The production code is kept in the stable branch while the documentation code is kept in the docs branch.

In order to run the code locally, you can follow the following steps.

## Installing and Deploying
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

Alternatively, if you use heroku, then you can do:
```
git checkout stable
heroku local
```
for Linux and for Windows:
```
git checkout stable
heroku local -f Procfile.windows
```

Either way, the website should open up in http://localhost:8000/ or http://127.0.0.1:8000/

## Documentation:
Source code for documentation can be found in the docs branch.
Sphinx documentation: https://palak2033.github.io/university_connect/

## Login Instructions
The main admin user is "admin@uconnect.com" and the password is "admin".
There are also faculty, faculty2, faculty3, student, student2, student3 each with the email "{username}@uconnect.com" and password "{username}" respectively.

Django also you to create a new super user using
```
python manage.py createsuperuser
```

## Features
- Admin:
- Faculty:
- Student:

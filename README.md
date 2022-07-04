# Cat Rental
Django website for practice

App: "Cat rental" (yes, to rent a CAT)


# Screenshoots:
![Cats_list](https://user-images.githubusercontent.com/75095360/149442056-1ec88923-ad8c-4ab9-98c2-7bea80115b3a.png)

# Setup

## Database
- create new database in postgres (name, login,... from cats/settings.py)
- or just change database for sqlite (cats/settings.py)

## Install dependencies
```
pip install -r requirements.txt
```

## Migrate database
```
py manage.py migrate
```
(you can also import data from fixtures first)

## Setup .env file
Please note there's temporary SECRET_KEY in settings.py
You may delete it

## Run server on your localhost
```
py manage.py runserver
```

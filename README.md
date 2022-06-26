# Cat Rental
Django website for practise

App: "Cat rental" (yes, to rent a CAT)


# Screenshoots:
![Cats_list](https://user-images.githubusercontent.com/75095360/175832124-568e3287-332c-4e91-9fd1-d3869c5a235f.png)


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

## Set mailing details
- in settings.py - set yours:
    - EMAIL_HOST_USER
    - EMAIL_HOST_PASSWORD  

(you can find it by TODO tag)


## Run server on your localhost
```
py manage.py runserver
```

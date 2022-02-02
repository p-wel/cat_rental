# cat_rental
Django website for practise
- App: "Cat rental" (yes, to rent a CAT)


Screenshoots:
![Cats_list](https://user-images.githubusercontent.com/75095360/149442056-1ec88923-ad8c-4ab9-98c2-7bea80115b3a.png)


To install:
1. Create new database in postgres (name, login, ... from settings.py) / Or just change database for sqlite
3. pip install -r requirements.txt
4. Import data from fixtures if you want
5. make migrations
6. settings.py - set yours:
    EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD  
  cats/views.py - "mailing" method - set from_mail and recipient_mail
    to make mailing work properly
7. py manage.py runserver

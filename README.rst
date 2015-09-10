**************
social-collect
**************

Social collect collects user's posts from three social networks - Twitter, Instagram and VK (VKontakte).
This package is example of using MongoDB. Default MongoDB settings used here.
Please edit end of settings.py for proper MongoDB connection.

*****
NOTE:
*****
Use this package only for educational/personal purposes only! Using this software violates Instagram API rules.
MongoDB is used only for storing posts and files. Other data about accounts/persons stored in SQLite3 database.


*****
Setup
*****

You're encouraged to setup a virtualenv to work in prior to configuring the dependencies.

Note: python code written for python3.

1. Go to repository dir::

    cd path/to/repository


2. Install Python Requirements::

    pip3 install -r requirements.txt


3. Install Assets::

    bower install


4. Fill access tokens in settings.py::

    TOKEN_VK = ""
    TOKEN_INSTAGRAM = ""

    TOKEN_TWITTER_CONSUMER_KEY = ""
    TOKEN_TWITTER_CONSUMER_SECRET = ""
    TOKEN_TWITTER_ACCESS_TOKEN_KEY = ""
    TOKEN_TWITTER_ACCESS_TOKEN_SECRET = ""


5. Run following commands to create database environment::

    python3 manage.py makemigrations social_collect
    python3 manage.py migrate


6. Run MongoDB server::

    mongod


7. Run the Django server::

    python3 manage.py runserver 8002


8. Visit http://localhost:8002/ to add persons and their social accounts.

9. Press "Update" on the bottom of main page to fetch new posts.

10. Enjoy viewing person's feed on::

    http://localhost:8002/person/1
    or
    http://localhost:8002/person/<any_screen_name>


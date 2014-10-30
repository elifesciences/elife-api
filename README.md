# elife-api

This project is an attempt to centralize programmatic article data access to a 
simple interface accessible using HTTP.

## pre-requisites

* Python3 +
* pip
* virtualenvwrapper

You're free to handle your development environment as you wish, however I've 
found `virtualenv` with the `virtualenvwrapper` tools are very convenient.

## installation for development

Clone the repo, link to the relevant settings.py file:

    $ git clone elifesciences/elife-api.git
    $ mkvirtualenv elife-api && workon elife-api
    $ pip install -r requirements.txt
    $ cd elife-api/src/core/ && ln -s dev_settings.py settings.py  
  
Start the development server to test everything is working:

    $ ./manage.py runserver


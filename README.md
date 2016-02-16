# elife-api

An effort by [eLife Sciences](http://elifesciences.org) to centralize 
programmatic article data access to a simple interface accessible using HTTP.

[Github repo](https://github.com/elifesciences/elife-api/).

This project uses the [Python programming language](https://www.python.org/),
and the [Django web framework](https://www.djangoproject.com/).

API documentation can be found here:

* [code](https://github.com/elifesciences/elife-api/blob/master/src/router/urls.py)
* [Swagger](https://api.elifesciences.org/docs/) (or your [local version](/docs/))

For example, the [Homo Naledi](http://elifesciences.org/content/4/e09560) article:

* [http://api.elifesciences.org/v2/articles/10.7554/eLife.09560/pdf](http://api.elifesciences.org/v2/articles/10.7554/eLife.09560/pdf)

## installation

[code](https://github.com/elifesciences/elife-api/blob/master/install.sh) 

    git clone https://github.com/elifesciences/elife-api
    cd elife-api
    ./install.sh

## updating

[code](https://github.com/elifesciences/elife-api/blob/master/install.sh)  

    ./install.sh

## testing

[code](https://github.com/elifesciences/elife-api/blob/master/src/router/tests.py)

    ./test.sh

## running

[code](https://github.com/elifesciences/elife-api/blob/master/manage.sh)

    ./manage.sh runserver
    firefox http://127.0.0.1:8000/api/docs/

## proxied APIs 

The elife-api project in production at eLife also proxies requests to the APIs
of our other services. These other services can be accessed like: 
`http://api.elifesciences.org/proxy/{servicename}/api/...`

* [Lax](http://lax.elifesciences.org) article data ([github](https://github.com/elifesciences/lax)) http://api.elifesciences.org/proxy/lax/api/
* Article [Metrics](http://metrics.elifesciences.org) ([github](https://github.com/elifesciences/elife-metrics)) http://api.elifesciences.org/proxy/metrics/api/

For example, here you can access the metrics data used on the elifesciences.org 
website for the article on the famous Homo Naledi:

[http://api.elifesciences.org/proxy/metrics/api/v1/article/10.7554/eLife.09560/](http://api.elifesciences.org/proxy/metrics/api/v1/article/10.7554/eLife.09560/)

And here the article data:

[http://api.elifesciences.org/proxy/lax/api/v1/article/10.7554/eLife.09560/](http://api.elifesciences.org/proxy/lax/api/v1/article/10.7554/eLife.09560/)

## Copyright & Licence

Copyright 2015 eLife Sciences. Licensed under the [GPLv3](LICENCE.txt)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

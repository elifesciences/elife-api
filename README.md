# elife-api

This project is an attempt to centralize programmatic article data access to a 
simple interface accessible using HTTP.

## installation

    $ ./install.sh
    $ cd elife-api/src/core/ && ln -s dev_settings.py settings.py  

## testing

Ensure your settings.py is linked first, then:

    $ ./test.sh

## development

Ensure you are working within the virtualenv then start development server with:

    $ cd src/
    $ ./manage.py runserver

Go to [http://localhost:8000/docs](http://localhost:8000/docs) for the Swagger
generated documentation.

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

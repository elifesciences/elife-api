#!/bin/bash
set -e
source install.sh
pylint -E src/** --load-plugins=pylint_django --disable=E1103
./src/manage.py test src/

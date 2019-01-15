#!/bin/bash
set -e
# remove any old compiled python files
find src/ -name '*.py[c|~]' -delete
source install.sh
pylint -E src/** --load-plugins=pylint_django --disable=E1103
echo "* passed linting"
coverage run --source='src/' src/manage.py test src/
echo "* passed tests"
coverage report

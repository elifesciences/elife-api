#!/bin/bash
virtualenv . && source bin/activate && \
pip install -r requirements.txt && \
ln -s src/core/dev_settings.py src/core/settings.py && \
cd src && ./manage.py test

#!/bin/bash
if [ ! -d venv ]; then
    virtualenv venv --python=`which python2`
fi
source venv/bin/activate && \
pip install -r requirements.txt && \
cd src/core/ && ln -sf dev_settings.py settings.py && cd ../../ && \
cd src && ./manage.py test

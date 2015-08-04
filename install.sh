#!/bin/bash
set -e
if [ ! -d venv ]; then
    virtualenv venv --python=`which python2`
fi
source venv/bin/activate
pip install -r requirements.txt

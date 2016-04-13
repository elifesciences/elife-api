#!/bin/bash
set -e # everything must succeed.
if [ ! -d venv ]; then
    virtualenv --python=`which python2` venv
fi
source venv/bin/activate
if [ ! -e src/core/settings.py ]; then
    echo "no settings.py found! using the DEV settings (dev_settings.py) by default."
    cd src/core/
    ln -s dev_settings.py settings.py
    cd ../../
fi
pip install -r requirements.txt

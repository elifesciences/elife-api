#!/bin/bash
set -e # everything must succeed.
if [ ! -d venv ]; then
    virtualenv --python=`which python2` venv
fi
source venv/bin/activate
if [ ! -e app.cfg ]; then
    echo "* no app.cfg found! using the example settings (elife.cfg) by default."
    ln -s elife.cfg app.cfg
fi
pip install -r requirements.txt

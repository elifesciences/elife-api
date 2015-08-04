#!/bin/bash
source install.sh
cd src/core/ && ln -sf dev_settings.py settings.py
cd ../../
cd src 
./manage.py test

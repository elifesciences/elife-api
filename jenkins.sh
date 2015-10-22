#!/bin/bash
set -e
cd src/core/ && ln -sf dev_settings.py settings.py
cd ../../
source test.sh
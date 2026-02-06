#!/bin/bash

# required env vars
# STACK_NAME
# PRODUCT
# APP_NAME
# THREADS

#export PYTHONPATH=$(pwd)/tests/:$PYTHONPATH
#python3 tests/api/$PRODUCT/setup.py $STACK_NAME
python3 tests/util/parallel_behave.py $APP_NAME $THREADS

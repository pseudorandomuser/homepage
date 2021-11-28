#!/bin/bash

make setup
source .venv/bin/activate

EXEC_CMD=$2
if [ -z $EXEC_CMD ]; then
    EXEC_CMD=run
fi

FLASK_ENV=$1 flask $EXEC_CMD ${@:3}

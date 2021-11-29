#!/bin/bash

export FLASK_ENV=$1
export FLASK_APP=homepage

make setup
source .venv/bin/activate

EXEC_CMD=$2
if [ -z $EXEC_CMD ]; then
    EXEC_CMD=run
fi

flask $EXEC_CMD ${@:3}

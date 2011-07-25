#!/bin/bash
TOOLS=`dirname $0`
VENV=$TOOLS/../.dashboard-venv
echo $VENV
source $VENV/bin/activate && $@


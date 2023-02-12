#!/usr/bin/env bash
SCRIPT_DIR=$( pwd; )/$( dirname -- "$0"; );

poetry run pylint $SCRIPT_DIR/../src

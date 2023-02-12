#!/usr/bin/env bash
if [ -z ${SCRIPT_DIR+x} ]; then
  SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
fi

poetry run pylint $SCRIPT_DIR/../src
poetry run pylint $SCRIPT_DIR/../tests

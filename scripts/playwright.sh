#!/usr/bin/env bash
OS="$(uname -s)"
if [ -z ${SCRIPT_DIR+x} ]; then
  SCRIPT_DIR=$( pwd )/$( dirname -- "$0" );
  if [[ $OS == 'Darwin'* ]]; then
    SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
  fi
fi
export SCRIPT_DIR=$SCRIPT_DIR
PWD=$( pwd )

cd $SCRIPT_DIR/../
poetry run python -m tests.cli --test playwright
cd $PWD
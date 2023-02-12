#!/usr/bin/env bash\
OS="$(uname -s)"
if [ -z ${SCRIPT_DIR+x} ]; then
  SCRIPT_DIR=$( pwd )/$( dirname -- "$0" );
  if [[ $OS == 'Darwin'* ]]; then
    SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
  fi
fi

poetry run streamlit run $SCRIPT_DIR/../src/home.py &
sleep 2
poetry run pytest $SCRIPT_DIR/../tests/feature/playwright*.py

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

cd SCRIPT_DIR/../../
parallel -u ::: 'poetry run coverage run --source src -m unittest discover -s tests.unit -p "*.py" &&\
 poetry run coverage run --append --source src -m streamlit run ./src/home.py'\
  'sleep 5 && poetry run pytest ./tests/feature/playwright*.py'
poetry run coverage report
cd $PWD
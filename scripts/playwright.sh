#!/usr/bin/env bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

poetry run streamlit run $SCRIPT_DIR/../src/home.py &
sleep 2
pytest $SCRIPT_DIR/../tests/playwright*.py
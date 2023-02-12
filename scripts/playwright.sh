#!/usr/bin/env bash
SCRIPT_DIR=$( pwd; )/$( dirname -- "$0"; );

poetry run streamlit run $SCRIPT_DIR/../src/home.py &
sleep 2
poetry run pytest $SCRIPT_DIR/../tests/playwright*.py

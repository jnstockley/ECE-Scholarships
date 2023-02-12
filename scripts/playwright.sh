#!/usr/bin/env bash\
if [ -z ${SCRIPT_DIR+x} ]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

poetry run streamlit run $SCRIPT_DIR/../src/home.py &
sleep 2
poetry run pytest $SCRIPT_DIR/../tests/feature/playwright*.py

#!/usr/bin/env bash\
if [ -z ${SCRIPT_DIR+x} ]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

poetry run coverage run --source src -m unittest discover -s tests.unit -p "*.py"
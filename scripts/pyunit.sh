#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

poetry run coverage run --source src -m unittest discover -s tests.unit -p "*.py"
#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

poetry run pylint $SCRIPT_DIR/../src
poetry run pylint $SCRIPT_DIR/../tests

#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

sh $SCRIPT_DIR/playwright.sh
sh $SCRIPT_DIR/pyunit.sh
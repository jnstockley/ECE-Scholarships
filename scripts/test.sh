#!/usr/bin/env bash\
if [ -z ${SCRIPT_DIR+x} ]; then
  SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
fi
export SCRIPT_DIR=$( pwd; )/$( dirname -- "$0"; );

sh $SCRIPT_DIR/playwright.sh
sh $SCRIPT_DIR/pyunit.sh
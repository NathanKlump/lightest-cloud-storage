#!/bin/bash

SCREEN_NAME="lcs"

# Change to the current dir of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"


# Start the lcs server
screen -dmS $SCREEN_NAME bash -c '
source venv/bin/activate &&
venv/bin/python app.py
'

echo "lcs started in screen session: $SCREEN_NAME"

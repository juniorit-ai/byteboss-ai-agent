#!/bin/bash

(
cd "$(dirname "${BASH_SOURCE[0]}")" || exit

if [ -f "user.conf.sh" ]; then
    source "user.conf.sh"
else
    echo "user.conf.sh not found"
fi

if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Get the real path of the Python script
agent="$(realpath "../../byteboss_agent/main.py")"

# Check if the Python script exists
if [ ! -f "$agent" ]; then
    echo "Python script not found at $agent"
    exit 1
fi

python3 "$agent" "$@"
)
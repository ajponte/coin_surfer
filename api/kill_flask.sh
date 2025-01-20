#!/bin/bash
# Kill locally running Flask process running on a specific port

# ARGUMENTS:
#   <port>: port to kill running PID (e.g. `5000`)

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <port>"
  exit 1
fi

port="$1"

lsof -i :$port | awk 'NR > 1 {print $2}' | xargs -I {} kill -9 {}

exit 0

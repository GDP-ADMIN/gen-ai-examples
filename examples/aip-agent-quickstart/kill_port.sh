#!/bin/bash

# Script to kill a process running on a specific port

# Check if a port number is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <port_number>"
  exit 1
fi

PORT=$1

echo "Attempting to kill process on port $PORT..."

# Find the PID of the process using the specified port
# sudo is used here because processes like docker-proxy (used for port forwarding)
# often run as root and may not be visible to lsof without sudo.
PIDS=$(sudo lsof -ti :"$PORT")

# Check if any PIDs were found
if [ -n "$PIDS" ]; then
  # Kill the process(es)
  # sudo is used here to ensure the kill command has permission
  # to terminate processes owned by root or other users.
  sudo kill -9 $PIDS
  echo "Process(es) with PID(s) $PIDS on port $PORT killed."
else
  echo "No process found running on port $PORT."
fi

#!/bin/bash

SERVICE_NAME="stock-api"
PORT="8000"
API_HOST="localhost"

systemctl is-active --quiet "$SERVICE_NAME"

if [ $? -ne 0 ]; then
    echo "$(date): Service $SERVICE_NAME is not active. Attempting to restart."
    sudo systemctl restart "$SERVICE_NAME"
    exit 1
fi

curl -s http://$API_HOST:$PORT/health || netcat -z $API_HOST $PORT

if [ $? -ne 0 ]; then
    echo "$(date): Port $PORT on $API_HOST is not responding. Attempting to restart $SERVICE_NAME."
    sudo systemctl restart "$SERVICE_NAME"
    exit 1
else
    echo "$(date): Service $SERVICE_NAME is active and port $PORT is responding."
    exit 0
fi
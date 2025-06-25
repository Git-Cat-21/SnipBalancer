#!/bin/bash

URL="http://localhost:5000/" 
TOTAL_REQUESTS=100

echo "Sending $TOTAL_REQUESTS GET requests..."

for ((i=1; i<=TOTAL_REQUESTS; i++)); do
    curl -s "$URL" > /dev/null &

done

echo "GET test done."

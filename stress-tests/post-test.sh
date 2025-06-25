#!/bin/bash

URL="http://localhost:5000/"
TOTAL_REQUESTS=500
CONCURRENT=10
OUTPUT_FILE="post-results.txt"

> "$OUTPUT_FILE"

echo "Sending $TOTAL_REQUESTS POST requests concurrently with $CONCURRENT at a time..."
echo "Logging responses to $OUTPUT_FILE"

for ((i=1; i<=TOTAL_REQUESTS; i++)); do
    test_url="https://example$i.com"

    (
        response=$(curl -s -X POST -d "url=$test_url" "$URL")
        echo "Request $i | Sent: $test_url | Response: $response" >> "$OUTPUT_FILE"
    ) &

    if (( i % CONCURRENT == 0 )); then
        wait
    fi
done

wait

echo "POST stress test completed. Responses saved in $OUTPUT_FILE."

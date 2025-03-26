#!/bin/bash

# URL of the API endpoint
url="https://quote.cnbc.com/quote-html-webservice/restQuote/symbolType/symbol?symbols=US10Y&requestMethod=itv&noform=1&partnerId=2&fund=1&exthrs=1&output=json&events=1"

# Use curl with headers to fetch the JSON data
response=$(curl -s -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36" -H "Referer: https://www.cnbc.com/" "$url")

# Extract the "last" value from the JSON response using jq
yield=$(echo "$response" | jq -r '.FormattedQuoteResult.FormattedQuote[0].last')

# Check if the yield value was successfully extracted
if [ -z "$yield" ]; then
    echo "Error: Impossible to get the yield"
    exit 1
fi

# Add Timestamp
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
echo "$TIMESTAMP, $yield" >> yield.csv


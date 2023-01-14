#!/bin/bash

KSQL_HOST=$2
KSQL_HOST="${KSQL_HOST:-localhost}"

echo -e "\nsubmitting query $1\n"
echo -e "connecting to host $KSQL_HOST\n"

QUERY_DATA=$(envsubst < $1)

curl --http1.1 \
     -X "POST" "http://${KSQL_HOST}:8088/ksql" \
     -H "Accept: application/vnd.ksql.v1+json" \
     -H "Content-Type: application/json" \
     -d "{
  \"ksql\": \"${QUERY_DATA}\",
  \"streamsProperties\": {}
}"
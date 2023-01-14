#!/bin/bash

SCHEMA_REGISTRY_HOST=$2
SCHEMA_REGISTRY_HOST="${SCHEMA_REGISTRY_HOST:-localhost:8081}"

echo -e "\nsubmitting schema $1\n"
echo -e "connecting to host $SCHEMA_REGISTRY_HOST\n"

SUBJECT_NAME="$(basename "$1" .avsc)"

JSON_DATA=$(cat "$1" | jq -Rs '{schema:.}')

curl --http1.1 \
  -X "POST" "http://${SCHEMA_REGISTRY_HOST}/subjects/${SUBJECT_NAME}/versions" \
  -H "Accept: application/vnd.schemaregistry.v1+json, application/vnd.schemaregistry+json, application/json" \
  -H "Content-Type: application/json" \
  -d "$JSON_DATA"

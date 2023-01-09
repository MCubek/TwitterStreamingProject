#!/bin/bash

set -x

TOPIC_CONFIG=$(envsubst < $1)
BROKER="$2"
BROKER="${BROKER:-localhost:9092}"

IFS=' '
read -ra ARGS <<< "$TOPIC_CONFIG"


echo -e "\nsubmitting topic with config $TOPIC_CONFIG to broker $BROKER\n"

/kafka/kafka_2.13-3.3.1/bin/kafka-topics.sh --bootstrap-server "$BROKER" "${ARGS[@]}"
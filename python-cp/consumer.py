import json
import joblib
from confluent_kafka import Producer, KafkaException
from confluent_kafka.avro import AvroConsumer
from confluent_kafka import avro

def read_data(model):
    consumer_config = {
        "bootstrap.servers": "localhost:9092",
        "schema.registry.url": "http://localhost:8081",
        "group.id": "my-consumer1",
        "auto.offset.reset": "earliest"
    }

    consumer = AvroConsumer(consumer_config)
    consumer.subscribe(['twitter_tweets'])

    while True:
      try:
        msg = consumer.poll(1)

        if msg is None:
          continue

        print("Key is :" + json.dumps(msg.key()))
        print("Value is :" + json.dumps(msg.value()))
        print("-------------------------")

      except KafkaException as e:
        print('Kafka failure ' + e)

    consumer.close()

def main():
    model = joblib.load("../model/model.joblib")
    read_data(model)

if __name__ == "__main__":
    main()
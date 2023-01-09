from confluent_kafka.avro import AvroConsumer, CachedSchemaRegistryClient
from confluent_kafka.avro.serializer import SerializerError

# Set up the Kafka consumer
consumer_conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "twitter_tweet_consumer",
}
schema_registry_url = "http://localhost:8081"

if __name__ == '__main__':
    # Set up the Avro consumer
    schema_registry_client = CachedSchemaRegistryClient({"url": schema_registry_url})
    twitter_tweet_consumer = AvroConsumer(consumer_conf, schema_registry=schema_registry_client)
    twitter_tweet_consumer.subscribe(["twitter_tweets"])

    # Consume messages from the topic
    while True:
        try:
            msg = twitter_tweet_consumer.poll(1.0)
        except SerializerError as e:
            print("Message deserialization failed: {}".format(e))
            twitter_tweet_consumer.close()
            break

        if msg:
            print(msg.value())
        else:
            print("No message received by the consumer")

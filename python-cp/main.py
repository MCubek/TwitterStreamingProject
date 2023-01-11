import json
import joblib
from confluent_kafka.avro import AvroConsumer, AvroProducer, CachedSchemaRegistryClient
from confluent_kafka.avro.serializer import SerializerError
from nltk.tokenize.casual import TweetTokenizer
from ekphrasis.classes.segmenter import Segmenter
from nltk.stem import WordNetLemmatizer
from preprocess import *
import nltk

nltk.download('wordnet')

# Set up the Kafka consumer
consumer_conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "twitter_tweet_consumer",
}

# Set up the Kafka producer
producer_conf = {
    "bootstrap.servers": "localhost:9092",
}
schema_registry_url = "http://localhost:8081"
enriched_tweet_topic = "twitter_tweets_enriched"
enriched_tweet_schema = "python-cp/avro/tweet-sentiment-schema.avsc"

# PREPROCESSING REQUIREMENTS
tokenizer = TweetTokenizer(preserve_case=True, reduce_len=True, strip_handles=True)
seg_tw = Segmenter(corpus="twitter")
lemmatizer = WordNetLemmatizer()
tfidf_vectorizer = joblib.load('model/vectorizer.joblib')
model = joblib.load('model/model.joblib')
    

if __name__ == '__main__':
    # Set up the Avro producer
    schema_registry_client = CachedSchemaRegistryClient({"url": schema_registry_url})
    twitter_tweet_consumer = AvroConsumer(consumer_conf, schema_registry=schema_registry_client)
    twitter_tweet_consumer.subscribe(["twitter_tweets"])
    twitter_tweet_producer = AvroProducer(producer_conf, schema_registry=schema_registry_client)

    # Read the schema from a file
    with open(enriched_tweet_schema, "r") as f:
        tweet_enriched_schema = f.read()

    while True:
        try:
            msg = twitter_tweet_consumer.poll(1.0)
        except SerializerError as e:
            print("Message deserialization failed: {}".format(e))
            twitter_tweet_consumer.close()
            break
        if msg:
            tweet_text = msg.value()['Text']
            preprocessed_tweet = preprocess_tweet(tweet_text, tokenizer, seg_tw, lemmatizer)
            tweet_vectorized = tfidf_vectorizer.transform([preprocessed_tweet])
            predicted_value = model.predict(tweet_vectorized)
            if predicted_value == 1:
                predicted_sentiment = 'positive'
            else:
                predicted_sentiment = 'negative'
            
            message_value = {"Text": tweet_text, "Sentiment": predicted_sentiment}
            # Produce the message to the "twitter_tweets" topic
            print(tweet_text)
            print(preprocessed_tweet)
            print(predicted_sentiment)
            print("------------------------------------------------------------")
            
            twitter_tweet_producer.produce(
                topic=enriched_tweet_topic,
                value=message_value,
                value_schema=tweet_enriched_schema,
            )
            twitter_tweet_producer.flush()
        else:
            print("No message received by consumer")
    

    
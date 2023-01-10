import json
import joblib
from confluent_kafka.avro import AvroConsumer, AvroProducer, CachedSchemaRegistryClient
from confluent_kafka.avro.serializer import SerializerError
from nltk.tokenize.casual import TweetTokenizer
from ekphrasis.classes.segmenter import Segmenter
from nltk.stem import WordNetLemmatizer
from preprocess import *

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
enriched_tweet_schema = "tweet-enriched.avsc"

test_message_value = {"CreatedAt": 1673225114000, "Id": 1612249099994124288,
                      "Text": "RT @odzzmusic: Then people deny Kanye\u2019s influence",
                      "Sentiment": "Positive",
                      "Source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
                      "Truncated": False, "InReplyToStatusId": -1, "InReplyToUserId": -1, "InReplyToScreenName": None,
                      "GeoLocation": None, "Place": None, "Favorited": False, "Retweeted": False, "FavoriteCount": 0,
                      "User": {"Id": 757649932065071104, "Name": "Caramelo Duro", "ScreenName": "SashaaaBabydoll",
                               "Location": "Ile-de-France, France", "Description": "AVOCADO LIFE",
                               "ContributorsEnabled": False,
                               "ProfileImageURL": "http://pbs.twimg.com/profile_images/1608567959491936257/yMGXAwgg_normal.jpg",
                               "BiggerProfileImageURL": "http://pbs.twimg.com/profile_images/1608567959491936257/yMGXAwgg_bigger.jpg",
                               "MiniProfileImageURL": "http://pbs.twimg.com/profile_images/1608567959491936257/yMGXAwgg_mini.jpg",
                               "OriginalProfileImageURL": "http://pbs.twimg.com/profile_images/1608567959491936257/yMGXAwgg.jpg",
                               "ProfileImageURLHttps": "https://pbs.twimg.com/profile_images/1608567959491936257/yMGXAwgg_normal.jpg",
                               "BiggerProfileImageURLHttps": "https://pbs.twimg.com/profile_images/1608567959491936257/yMGXAwgg_bigger.jpg",
                               "MiniProfileImageURLHttps": "https://pbs.twimg.com/profile_images/1608567959491936257/yMGXAwgg_mini.jpg",
                               "OriginalProfileImageURLHttps": "https://pbs.twimg.com/profile_images/1608567959491936257/yMGXAwgg.jpg",
                               "DefaultProfileImage": False, "URL": None, "Protected": False, "FollowersCount": 231,
                               "ProfileBackgroundColor": "F5F8FA", "ProfileTextColor": "333333",
                               "ProfileLinkColor": "1DA1F2", "ProfileSidebarFillColor": "DDEEF6",
                               "ProfileSidebarBorderColor": "C0DEED", "ProfileUseBackgroundImage": True,
                               "DefaultProfile": True, "ShowAllInlineMedia": False, "FriendsCount": 135,
                               "CreatedAt": 1469472795000, "FavouritesCount": 1763, "UtcOffset": -1, "TimeZone": None,
                               "ProfileBackgroundImageURL": "", "ProfileBackgroundImageUrlHttps": "",
                               "ProfileBannerURL": "https://pbs.twimg.com/profile_banners/757649932065071104/1469473198/web",
                               "ProfileBannerRetinaURL": "https://pbs.twimg.com/profile_banners/757649932065071104/1469473198/web_retina",
                               "ProfileBannerIPadURL": "https://pbs.twimg.com/profile_banners/757649932065071104/1469473198/ipad",
                               "ProfileBannerIPadRetinaURL": "https://pbs.twimg.com/profile_banners/757649932065071104/1469473198/ipad_retina",
                               "ProfileBannerMobileURL": "https://pbs.twimg.com/profile_banners/757649932065071104/1469473198/mobile",
                               "ProfileBannerMobileRetinaURL": "https://pbs.twimg.com/profile_banners/757649932065071104/1469473198/mobile_retina",
                               "ProfileBackgroundTiled": False, "Lang": None, "StatusesCount": 79895,
                               "GeoEnabled": False, "Verified": False, "Translator": False, "ListedCount": 7,
                               "FollowRequestSent": False, "WithheldInCountries": []}, "Retweet": True,
                      "Contributors": [], "RetweetCount": 0, "RetweetedByMe": False, "CurrentUserRetweetId": -1,
                      "PossiblySensitive": False, "Lang": "en", "WithheldInCountries": [], "HashtagEntities": [],
                      "UserMentionEntities": [
                          {"Name": "ODZZ🇰🇪", "Id": 934288770349850624, "Text": "odzzmusic", "ScreenName": "odzzmusic",
                           "Start": 3, "End": 13}], "MediaEntities": [], "SymbolEntities": [], "URLEntities": []}


# PREPROCESSING REQUIREMENTS
tokenizer = TweetTokenizer(preserve_case=True, reduce_len=True, strip_handles=True)
seg_tw = Segmenter(corpus="twitter")
lemmatizer = WordNetLemmatizer()
tfidf_vectorizer = joblib.load('./model/vectorizer.joblib')
model = joblib.load('model.joblib')
    

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
            preprocessed_tweet = preprocess_tweet(msg.value()['Text'], tokenizer, seg_tw, lemmatizer)
            tweet_vectorized = vectorizer.transform(preprocessed_tweet)
            predicted_value = model.predict(tweet_vectorized)
            if predicted_value == 1:
                predicted_sentiment = 'positive'
            else:
                predicted_sentiment = 'negative'
            # Produce the message to the "twitter_tweets" topic
            print(msg.value()['Text'])
            print(predicted_sentiment)
            print("------------------------------------------------------------")
            twitter_tweet_producer.produce(
            topic=enriched_tweet_topic,
            value=predicted_sentiment,
            value_schema=tweet_enriched_schema,
            twitter_tweet_producer.flush()
        else:
            print("No message received by consumer")
    )
    

    
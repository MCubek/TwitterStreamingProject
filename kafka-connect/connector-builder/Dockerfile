FROM openjdk:8

# Install kafka tools
WORKDIR /kafka
RUN wget https://dlcdn.apache.org/kafka/3.3.1/kafka_2.13-3.3.1.tgz \
    && tar -xzf kafka_2.13-3.3.1.tgz \
    && rm kafka_2.13-3.3.1.tgz


# Install bash commands
RUN apt-get update && apt-get install -y --allow-unauthenticated --fix-missing \
curl gettext-base jq
CMD /bin/bash
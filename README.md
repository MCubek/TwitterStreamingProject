# Twitter Streaming Project
## University of Zagreb, Faculty of Electrical Engineering and Computing

### Members:
- Iva Bokšić
- Zvonimit Petar Rezo
- Matej Čubek

### The following enviroment variables containing **twitter api keys** must be set in your gitpod progile or locally for the project to be run
- TWITTER_CONSUMER_KEY
- TWITTER_CONSUMER_SECRET
- TWITTER_ACCESS_TOKEN
- TWITTER_ACCESS_TOKEN_SECRET

## Launch the workspace in your browser with GitPod:
- https://gitpod.io/#https://github.com/MCubek/TwitterStreamingProject

## Launch the workspace locally with Docker:
1. Position bash command line to project root directory
2. Build the required images
    ```Bash
    docker-compose build && docker-compose pull
    ```
3. Install additional bash commands
    ```Bash
    sudo apt-get install gettext-base
    ```
4. Start required services
    ```Bash
    docker-compose -f docker-compose.yaml -f kafka-connect/submit-connectors.yaml up -d
    ```
5. Open Confluent Platform interface or Kafka-UI
    - http://localhost:8080
    - http://localhost:9021
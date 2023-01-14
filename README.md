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

To set the enviroment variables use:
- https://gitpod.io/variables for GitPod
- Your local operating system procedure for local running. Make sure that the teriminal running docker-compose will have those variables set correctly.

## Launch the workspace in your browser with GitPod:
- https://gitpod.io/#https://github.com/MCubek/TwitterStreamingProject

## Launch the workspace locally with Docker:
1. Position bash command line to project root directory
2. Open `docker-compose.yaml` and comment out configuration lines specific to gitpod and uncomment lines specific to local running for confluent platform pod. 
That change shown below:
    ```Yaml
    # If running in Gitpod, your browser must connect to ksqlDB via Gitpod's proxy URL
    # CONTROL_CENTER_KSQL_KSQLDB1_ADVERTISED_URL: https://8088-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}
    # If running locally, your browser must connect to ksqlDB through localhost 8088. Comment out the above line and uncomment the line below.
    CONTROL_CENTER_KSQL_KSQLDB1_ADVERTISED_URL: https://localhost:8088
    ```
3. Build the required images
    ```Bash
    docker-compose build && docker-compose pull
    ```
4. Start required services
    ```Bash
    docker-compose -f docker-compose.yaml -f kafka-connect/submit-connectors-queries.yaml -f sentiment-analysis/model.yaml up -d
    ```
5. Open Confluent Platform interface or Kafka-UI
    - Kafka UI: http://localhost:8080
    - Confluent Platform: http://localhost:9021
    - For ksqlDB CLI execute:
        ```Bash
        docker-compose exec ksqldb-cli ksql http://ksqldb-server:8088
        ```

6. To stop services
    ```Bash
    docker-compose -f docker-compose.yaml -f kafka-connect/submit-connectors-queries.yaml -f sentiment-analysis/model.yaml down
    ```
# Distributed Logging System

### Setup Instructions:

- Install Kafka, Elasticsearch on the server VM.

- Install Fluentd on the microservices side.

- Install all the required python packages.

- On the server, do ifconfig and note down the IP address.

- Allow connections to the Kafka port through the firewall using the commands: `sudo ufw enable` & `sudo ufw allow 9092`

- For Kafka, go to the /usr/local/kafka or /opt/bin/kafka and change the config/server.properties to have the values:
1. listeners=PLAINTEXT://0.0.0.0:9092
2. advertised.listeners=PLAINTEXT://192.8.1.10:9092 

- Start the server services: `sudo systemctl start kafka.service` (or stop and restart this if required) & `sudo systemctl start elasticsearch.service`

- Run `fluentd -c fluentd.conf` on the microservices side in one terminal

- Run `python3 consumer.py` on the server in a terminal

- Run all three microservices in separate terminals on the client side and logs should start appearing!

- Setup Kibana and Nginx, visit localhost:5601 and go to the discover tab to visualise the Elasticsearch logs

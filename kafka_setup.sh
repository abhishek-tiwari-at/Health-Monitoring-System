
# Start ZooKeeper
cd kafka
bin/zookeeper-server-start.sh config/zookeeper.properties 

# Wait for ZooKeeper to start
sleep 5

# Start Kafka broker
bin/kafka-server-start.sh config/server.properties 

# Wait for Kafka to start
sleep 5

# Create Kafka topic
bin/kafka-topics.sh --create --topic <your topic name>25 --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

echo "Kafka setup complete. Topic 'stroke_metrics' created."
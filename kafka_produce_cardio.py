from kafka import KafkaProducer
import json
import time

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic_name =   'cardio_topic'

print(f"Starting to send data to Kafka topic: {topic_name}")
# Read preprocessed data
with open('datasets/cardio_train.json','r')as file:
    for line in file:
        record = json.loads(line.strip())
        producer.send(topic_name, record)
        print(f"Sent: {record}")
        time.sleep(0.1)  # Simulate real-time streaming

producer.flush()
producer.close()
print("All records sent to Kafka topic 'heart_alerts'.")


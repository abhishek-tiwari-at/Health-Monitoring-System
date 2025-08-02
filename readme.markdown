# Real-Time Health Event Detection System

This README provides instructions to set up and run the real-time health event detection system, which processes chronic disease data using Kafka, Siddhi CEP, and a Streamlit dashboard.

## Prerequisites

- Apache Kafka (with Zookeeper) installed.
- Siddhi CEP installed.
- Python 3.x installed with required libraries: `confluent-kafka`, `streamlit`.
- Ensure all paths to scripts and applications are correctly set.

## Setup Instructions

### 1. Start Zookeeper

Zookeeper is required to manage Kafka. Run the following command from the Kafka installation directory:

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

Keep this terminal running.

### 2. Start Kafka

In a new terminal, start the Kafka server from the Kafka installation directory:

```bash
bin/kafka-server-start.sh config/server.properties
```

Keep this terminal running.

### 3. Create Kafka Topics

Create the required Kafka topics for heart and cardio alerts. Run the following commands from the Kafka installation directory:

```bash
bin/kafka-topics.sh --create --topic heart_alert --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
bin/kafka-topics.sh --create --topic heart_alert_topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
bin/kafka-topics.sh --create --topic cardio_alert --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
bin/kafka-topics.sh --create --topic cardio_alert_topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### 4. Start Siddhi CEP

Siddhi CEP processes events based on clinical rules. Navigate to the Siddhi installation directory and start the runner with the specified app. Replace `<absolute path>` with the actual path to your Siddhi app directory and `app_name` with your app's name (e.g., `HealthEventDetection.siddhi`):
siddhi apps are stored in Health_Monitoring_System/siddhi-runner-5.1.2/deployment/siddhi-files/<file>

```bash
./bin/runner.sh -Dapps=<absolute path>/app_name
```

For example:

```bash
./bin/runner.sh -Dapps=/home/user/siddhi-apps/HealthEventDetection.siddhi
```

Keep this terminal running.

### 5. Start Kafka Producer

The Kafka producer sends health data to the Kafka topics. Run the producer script (assumed to be written in Python using `confluent-kafka`). Ensure the script is configured to produce messages to the topics created above. In a new terminal, navigate to your producer script directory and run:

```bash
python kafka_producer_<name>.py
```

Ensure `kafka_producer_<name>.py` is set up to connect to `localhost:9092` and produce messages to `topics.`

### 6. Start Streamlit Dashboard

The Streamlit dashboard visualizes real-time alerts. In a new terminal, navigate to the directory containing your Streamlit dashboard script (e.g., `dashboard.py`) and run:

```bash
streamlit run dashboard_<name>.py
```

This will launch the dashboard, typically accessible at `http://localhost:8501` in your browser. Ensure the dashboard script is configured to consume data from the Kafka topics or MongoDB (depending on your implementation).

## Notes

- Verify that all components (Zookeeper, Kafka, Siddhi CEP, producer, and dashboard) are running simultaneously.
- Check logs for each component to troubleshoot any issues.

## Stopping the System

To stop the system, terminate each process in reverse order:

1. Stop the Streamlit dashboard (Ctrl+C in the terminal).
2. Stop the Kafka producer (Ctrl+C in the terminal).
3. Stop Siddhi CEP (Ctrl+C in the terminal).
4. Stop Kafka (`bin/kafka-server-stop.sh`).
5. Stop Zookeeper (`bin/zookeeper-server-stop.sh`).

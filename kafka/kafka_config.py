from confluent_kafka import Producer, Consumer, KafkaError

# Kafka configuration
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "groupchat-events"

# Kafka Producer configuration
producer_config = {
    "bootstrap.servers": KAFKA_BROKER,
}

# Kafka Consumer configuration
consumer_config = {
    "bootstrap.servers": KAFKA_BROKER,
    "group.id": "groupchat-consumers",
    "auto.offset.reset": "earliest",
}

producer = Producer(producer_config)


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def send_event(event):
    producer.produce(KAFKA_TOPIC, event, callback=delivery_report)
    producer.flush()


consumer = Consumer(consumer_config)
consumer.subscribe([KAFKA_TOPIC])

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='kafka:9092')
producer.send('test-topic', b'Hello Kafka!')
producer.close()

from kafka import KafkaConsumer
from config import Config

consumer = KafkaConsumer(
    Config.KAFKA_TOPIC,
    bootstrap_servers=Config.KAFKA_BROKER,
    auto_offset_reset="earliest"
)

print("Kafka Consumer Started...")

for message in consumer:
    video_data = message.value
    print(f"Received Video Data: {len(video_data)} bytes")

# Import Required Libraries
import websocket
import time
from kafka import KafkaProducer

# Sending data to kafka
def on_message(ws, message):
     producer.send('sample', message)
     producer.flush()

# Creating Kafka Producer
producer = KafkaProducer(value_serializer=lambda m: str(m).encode("utf-8"),
                         bootstrap_servers=['localhost:9092'])

# Creating Streaming Socket
ws = websocket.WebSocketApp("wss://stream.meetup.com/2/rsvps", on_message=on_message)

# Sending the data for every 2 second
while(1):
    ws.run_forever()
    time.sleep(2)

# Import paho.mqtt for the class
from paho.mqtt import client as mqtt_client

# A class of functions that are called in main.py
class MqttSubscriber:
    # Initialize the MQTTsubscriber
    def __init__(self, broker, port, initial_topic):
        self.broker = broker
        self.port = port
        self.client = self.connect_mqtt()
        self.topics = [initial_topic]
        self.subscribe()

    # Establish the connection of MQTT client with this node
    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        client = mqtt_client.Client()
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    # A function that detects the MQTT message
    def on_message(self, client, userdata, msg):
        if msg.topic == "python/mqtt":
            print('a:', msg.payload.decode())
        elif msg.topic == "new_topic_to_subscribe":
            print('b:', msg.payload.decode())
        elif msg.topic == "/mqtt/testnun":
            print('b:', msg.payload.decode())
        return msg.payload.decode()

     # A function that subscribe to the message, able to work with different topics
    def subscribe(self):
        self.client.on_message = self.on_message
        for topic in self.topics:
            self.client.subscribe(topic)

    # Add topics to the subscription
    def add_subscription(self, new_topic):
        self.topics.append(new_topic)
        self.client.subscribe(new_topic)

    # Function to start
    def run(self):
        self.client.loop_forever()



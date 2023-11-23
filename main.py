# Import essential libraries and Classes for MQTT
from mqttsubscriber import MqttSubscriber
from mqttpublisher import MqttPublisher
import time
from pypylon import pylon
from pymongo import MongoClient
import cv2
from bson import Binary
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

class Action:
    # The initialization of the Class, including MQTT and Collections in the Database
    def __init__(self, broker, port, subscribing_topic, publishing_topic, username, password):
        self.broker = broker
        self.port = port
        self.sub_topic = subscribing_topic
        self.pub_topic = publishing_topic
        self.client_username = username
        self.client_password = password
        self.mqtt_subscriber = MqttSubscriber(self.broker, self.port, self.sub_topic)
        self.mqtt_publisher = MqttPublisher(self.broker, self.port, self.pub_topic, self.client_username, self.client_password)

        self.image = np.full((2064, 3088, 3), (255, 255, 255), dtype=np.uint8)
        self.checkcam = False
        self.capcount = 0

        self.CONNECTION_STRING = 'mongodb+srv://mechatronics:BhamAomNunEarn@dimension.i10gagw.mongodb.net/'
        self.client = MongoClient(self.CONNECTION_STRING)
        self.Database = self.client['Dimension']
        self.Collection = self.Database['Captured']
        self.Collection2 = self.Database['Preprocessed_Image']

    # A function for checking the camera and image capturing
    def cam(self, cap=False):
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        camera.Open()

        camera.StartGrabbingMax(1)
        if camera.IsGrabbing():
            res = True
        else: res = False
        if cap:
            c = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if(c.GrabSucceeded()):
                img = c.Array
                res = img
                c.Release()
        camera.Close()
        return res

    # A function that publish MQTT custom message to the topic that is already initialized
    def pubpub(self, message):
        msg = message
        result = self.mqtt_publisher.client.publish(self.pub_topic, msg)

    # A function that detects the MQTT message and do the action and response back to the publisher
    def on_message(self, client, userdata, msg):
        receive_msg = msg.payload.decode()
        print(receive_msg)
        if receive_msg == 'isOn':
            res = self.cam()
            if res:
                feedback = 'on'
                self.pubpub(feedback)
            else:
                feedback = 'off'
                self.pubpub(feedback)
        
        elif receive_msg == 'isTaken':
            if not self.cam():
                self.pubpub('Please Initalize the camera')
                return
            cap = self.cam(True)
            self.image = self.preprocessimage(cap)
            feedback = 'Captured'
            self.capcount += 1
            self.pubpub(feedback)

        elif receive_msg == 'isProcessed':
            if self.capcount == 0:
                self.pubpub('The image has not yet taken')
                return
            self.publishtodb(self.image, 2)
            feedback = 'Processed'
            self.pubpub(feedback)   

    # A function that continuously subscribe the message via MQTT
    def run_topic(self):
        print("Starting subscriber...")
        self.mqtt_subscriber.client.on_message = self.on_message

    # A functoin to start subscribe
    def run(self):
        self.mqtt_subscriber.client.loop_forever()

    # A function to preprocess image, including noise reduction by cv2.medianBlur, and thresholding using cv2.threshold
    # and finally send the image to database
    def preprocessimage(self, image):
        gray_image = image
        mean = np.mean(gray_image)
        median = cv2.medianBlur(gray_image, 3)
        bin_image = cv2.threshold(median, 0.75*mean, 255, cv2.THRESH_BINARY)
        self.publishtodb(bin_image[1], 1)
        return bin_image[1]

    # A function made for publishing the image to desired collection of the database
    def publishtodb(self, image, collection):
        # collection choosing
        if collection == 1:
            collection = self.Collection
        else:
            collection = self.Collection2
        #Encode the image and send the data to the chosen collection
        image_binary = Binary(cv2.imencode('.jpg', image)[1].tobytes())
        data = {
            '_id': collection.count_documents({})+1,
            'img_binary' : image_binary,
            'Timestamp' : datetime.utcnow()
        }
        collection.insert_one(data)
        return True

# Main part of the Code
if __name__ == '__main__':
    broker = '161.200.84.240'
    port = 1883
    sub_topic = "/mqtt/toPi1"
    pub_topic = '/mqtt/fromPi1'
    username = "cps"
    password = "21035350"
    # Call the class with parameters
    a = Action(broker, port, sub_topic, pub_topic, username, password)
    a.run_topic()
    a.run()

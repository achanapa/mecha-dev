from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from flask_mqtt import Mqtt 

     
app = Flask(__name__)
client = MongoClient('mongodb+srv://mechatronics:BhamAomNunEarn@dimension.i10gagw.mongodb.net/')  # Adjust MongoDB connection details
CORS(app)

# Define MongoDB collections
db = client['Dimension']
Bolt_Dimension = db["Bolt_Dimension"]
BoltBitHead = db["BoltBitHead"]

#mqtt
app.config['MQTT_BROKER_URL'] = '161.200.84.240'  # broker 
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
app.config['MQTT_USERNAME'] = 'cps'  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = '21035350'  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes
    
mqtt = Mqtt(app) 
topic_pub = '/mqtt/toPi1'
topic_sub = '/mqtt/fromPi1'

# test จ้า ไม่เกี่ยว
@app.route("/testbutton", methods=["GET", "POST"])
def test():
    try:
        recieve_data = None

        if request.method == 'POST':
            recieve_data = request.json
            print("Received data:", recieve_data)

        return jsonify(recieve_data)

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/get_recent_bolt_data", methods=["GET"])
def get_recent_bolt_data():
    try:
        recent_bolt_data = Bolt_Dimension.find_one(sort=[("Timestamp", -1)])
        return jsonify(recent_bolt_data)
    except Exception as e:
        return jsonify({"error": str(e)})
    

@app.route("/combine_and_store_data",methods=["GET", "POST"])
def combine_and_store_data():
    try:
        # user_selections = request.json

        recieve_data = None

        if request.method == 'POST':
            user_selections = request.json
            print("Received data:", user_selections)
        

        recent_bolt_data = Bolt_Dimension.find_one(sort=[("Timestamp", -1)])

        combined_data = {
            "_id": recent_bolt_data["_id"],
            "Timestamp": recent_bolt_data["Timestamp"],
            "M_Size": recent_bolt_data["M_Size"],
            "Head_Length": recent_bolt_data["Head_Length"],
            "Thread_Length": recent_bolt_data["Thread_Length"],
            "Head_Diameter": recent_bolt_data["Head_Diameter"],
            "Thread_Diameter": recent_bolt_data["Thread_Diameter"],
            "Space_Length": recent_bolt_data["Space_Length"],
            "type_head": user_selections["type_head"],
            "type_bit": user_selections["type_bit"]
        }
        # combined_data = {
        #     "_id": recent_bolt_data["_id"],
        #     "Timestamp": recent_bolt_data["Timestamp"],
        #     "M_Size": recent_bolt_data["M_Size"],
        #     "Head_Length": recent_bolt_data["Head_Length"],
        #     "Thread_Length": recent_bolt_data["Thread_Length"],
        #     "Head_Diameter": recent_bolt_data["Head_Diameter"],
        #     "Thread_Diameter": recent_bolt_data["Thread_Diameter"],
        #     "Space_Length": recent_bolt_data["Space_Length"],
        #     "type_head": "CAP",
        #     "type_bit": "TORX"
        # }  
 #       BoltBitHead.insert_one(combined_data)
   #     return jsonify({"message": "Data combined and stored successfully"})
        return jsonify(combined_data)
    except Exception as e:
        return jsonify({"error": str(e)})


 # send 3d link ยังไม่เสด  
@app.route("/send_3d_back", methods=["GET", "POST"])
def send_3d_back():
    try:
        googlelink = "https://www.google.co.th/?hl=th"
        link_3d = {'link': googlelink}
        if request.method == 'GET':   
            print("Sending data:", link_3d )

        return jsonify(link_3d)

    except Exception as e:
        return jsonify({"error": str(e)})


# mqtt publish (recieve button command from front-end then pub)
@app.route('/publish', methods=['GET','POST'])
def mqtt_publish_bham():
    if request.method == 'GET':
        message = 'isProcessed'
        mqtt.publish(topic_pub,message )
        # message = request.get_json()
        # mqtt.publish(topic_pub, message['msg'])
    return 'Message published'

# example mqtt subscribe in general
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt.subscribe(topic_sub) # subscribe topic
   else:
       print('Bad connection. Code:', rc)

@mqtt.on_message()
def sub_status(client, userdata, message):
    data = dict(
       topic_sub=topic_sub,
       payload=message.payload.decode()
  )
    print('Received message on topic: {topic_sub} with payload: {payload}'.format(**data))
    


if __name__ == "__main__":
    app.run(debug = True)
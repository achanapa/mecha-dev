from flask import Flask, request, jsonify , send_from_directory
from pymongo import MongoClient
from flask_cors import CORS
from googleLoader import download_from_google_drive, extract_file_id_from_google_drive_url
import base64
import os
from flask_mqtt import Mqtt 
from pymongo import MongoClient
import time
     
app = Flask(__name__)
client = MongoClient('mongoURI')
CORS(app)

# Define MongoDB collections
db = client['Dimension']
Bolt_Dimension = db["Bolt_Dimension"]
BoltBitHead = db["BoltBitHead"]
GoogleLink = db["GoogleLink"]
Captured = db["Captured"]


#mqtt
app.config['MQTT_BROKER_URL'] = '161.200.84.240'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'cps'
app.config['MQTT_PASSWORD'] = 'password'
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
    
mqtt = Mqtt(app) 
topic_pub = '/mqtt/toPi1'
topic_sub = '/mqtt/fromPi1'

mssg = [] 
latest_data = None

#get status
@app.route("/get_status", methods=["GET"])
def get_status():
    try:
        time.sleep(1)
        global latest_data
        #mssg[-1]
        recieve_data = {'msg': latest_data}
        return jsonify(recieve_data)

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/get_recent_captured_photo", methods=["GET"])
def get_recent_captured_photo():
    try:
        time.sleep(4)
        # Assuming you're using PyMongo to interact with MongoDB
        recent_captured_photo = db.Captured.find_one(sort=[("Timestamp", -1)])

        if recent_captured_photo:
            # Remove the MongoDB _id field, if needed
            recent_captured_photo.pop("_id", None)

            # Encode the binary image data as a base64-encoded string
            img_binary = recent_captured_photo.get("img_binary")
            if img_binary:
                encoded_image = base64.b64encode(img_binary).decode("utf-8")
                recent_captured_photo["img_binary"] = encoded_image

            return jsonify(recent_captured_photo)
        else:
            return jsonify({"message": "No recent captured photo found"})

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
        BoltBitHead.insert_one(combined_data)
        print(combined_data)
        
        return jsonify(combined_data)
    
    except Exception as e:
        return jsonify({"error": str(e)})
    

@app.route("/get_processing",methods=["GET", "POST"])
def result_processed_data():
    try:
        if request.method == 'POST':
            user_selections = request.json
            print("Received data:", user_selections)     

        time.sleep(2)

        recent_bolt_data = Bolt_Dimension.find_one(sort=[("Timestamp", -1)])

        result_data = {
            "M_Size": recent_bolt_data["M_Size"],
            "Head_Length": recent_bolt_data["Head_Length"],
            "Thread_Length": recent_bolt_data["Thread_Length"],
            "Head_Diameter": recent_bolt_data["Head_Diameter"],
            "Thread_Diameter": recent_bolt_data["Thread_Diameter"],
            "Space_Length": recent_bolt_data["Space_Length"],
        }
        
        return jsonify(result_data)
    
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/get_GoogleLink", methods=["GET"])
def get_GoogleLink():
        try: 
         time.sleep(50)
         recent_link = GoogleLink.find_one(sort=[("timestamp", -1)])
         return jsonify(recent_link)
        
        except Exception as e:     
         return jsonify({"error": str(e)})
        
@app.route("/downloaded.glb", methods=["GET"])
def get_downloadglb():
        try: 
         recent_link = GoogleLink.find_one(sort=[("timestamp", -1)])
         file_id = extract_file_id_from_google_drive_url(recent_link["link"])
         print(file_id)
         if file_id:
                folder_path = r"./client/public/temp"
                destination = os.path.join(folder_path, "downloaded.glb")

                file_url = f"https://drive.google.com/uc?id={file_id}&export=download"

                download_from_google_drive(file_url, destination)

         return jsonify({'from flask': 'success to reload' })
        
        except Exception as e:     
         return jsonify({"error": str(e)})
        

# glb file      
@app.route('/server/temp/downloaded.glb')
def serve_glb(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'downloaded.glb'), filename)
    

# mqtt publish (recieve button command from front-end then pub)
@app.route('/publish', methods=['GET','POST'])
def mqtt_publish_bham():
    if request.method == 'POST':
        message =  request.json['msg']
        mqtt.publish(topic_pub, message)
        print('pub'+message)
    return jsonify({'msg':'Message Publish'}) 

# example mqtt subscribe in general
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt.subscribe(topic_sub) # subscribe topic
   else:
       print('Bad connection. Code:', rc)

@mqtt.on_message()
def sub_message(client, userdata, message):
    data = dict(
       topic_sub=topic_sub,
       payload=message.payload.decode()
    )
    global latest_data
    latest_data=message.payload.decode()
    mssg.append(latest_data)
    print('Received message on topic: {topic_sub} with payload: {payload}'.format(**data))
    print(mssg)
    return latest_data
    
if __name__ == "__main__":
    app.run(debug = True)

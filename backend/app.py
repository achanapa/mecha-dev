from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb+srv://mechatronics:BhamAomNunEarn@dimension.i10gagw.mongodb.net/')  # Adjust MongoDB connection details

# Define MongoDB collections
db = client['Dimension']
Bolt_Dimension = db["Bolt_Dimension"]
BoltBitHead = db["BoltBitHead"]


@app.route("/get_recent_bolt_data", methods=["GET"])
def get_recent_bolt_data():
    try:
        recent_bolt_data = Bolt_Dimension.find_one(sort=[("Timestamp", -1)])
        return jsonify(recent_bolt_data)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/combine_and_store_data", methods=["POST"])
def combine_and_store_data():
    try:
        # user_selections = request.json

        recent_bolt_data = Bolt_Dimension.find_one(sort=[("Timestamp", -1)])

        # combined_data = {
        #     "_id": recent_bolt_data["_id"],
        #     "Timestamp": recent_bolt_data["Timestamp"],
        #     "M_Size": recent_bolt_data["M_Size"],
        #     "Head_Length": recent_bolt_data["Head_Length"],
        #     "Thread_Length": recent_bolt_data["Thread_Length"],
        #     "Head_Diameter": recent_bolt_data["Head_Diameter"],
        #     "Thread_Diameter": recent_bolt_data["Thread_Diameter"],
        #     "Space_Length": recent_bolt_data["Space_Length"],
        #     "type_head": user_selections["type_head"],
        #     "type_bit": user_selections["type_bit"]
        # }
        combined_data = {
            "_id": recent_bolt_data["_id"],
            "Timestamp": recent_bolt_data["Timestamp"],
            "M_Size": recent_bolt_data["M_Size"],
            "Head_Length": recent_bolt_data["Head_Length"],
            "Thread_Length": recent_bolt_data["Thread_Length"],
            "Head_Diameter": recent_bolt_data["Head_Diameter"],
            "Thread_Diameter": recent_bolt_data["Thread_Diameter"],
            "Space_Length": recent_bolt_data["Space_Length"],
            "type_head": "CAP",
            "type_bit": "TORX"
        }


        
        BoltBitHead.insert_one(combined_data)

        return jsonify({"message": "Data combined and stored successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)

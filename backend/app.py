from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb+srv://mechatronics:BhamAomNunEarn@dimension.i10gagw.mongodb.net/')  # Adjust MongoDB connection details

# Define MongoDB collections
db = client['Dimension']
Bolt_Dimension = db["Bolt_Dimension"]
BoltBitHead = db["BoltBitHead"]

# @app.route("/process_image", methods=["POST"])
# def process_image():
#     try:
#         # Get the processed image data from the request
#         processed_data = request.json

#         # Store the processed data in the Bolt_Dimension collection
#         Bolt_Dimension.insert_one(processed_data)

#         return jsonify({"message": "Image data processed and stored successfully"})
#     except Exception as e:
#         return jsonify({"error": str(e)})

@app.route("/get_recent_bolt_data", methods=["GET"])
def get_recent_bolt_data():
    try:
        recent_bolt_data = Bolt_Dimension.find_one(sort=[("timestamp", -1)])  # Use -1 for descending order
        return jsonify(recent_bolt_data)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/combine_and_store_data", methods=["POST"])
def combine_and_store_data():
    try:
        # Get user selections from the request
        user_selections = request.json

        # Fetch the most recent bolt data from Bolt_Dimension
        recent_bolt_data = Bolt_Dimension.find_one(sort=[("timestamp", -1)])  # Adjust the field name

        # Combine data and store it in BoltBitHead
        combined_data = {
            "bolt_data": recent_bolt_data,
            "type_head": user_selections["type_head"],
            "type_bit": user_selections["type_bit"]
        }
        BoltBitHead.insert_one(combined_data)

        return jsonify({"message": "Data combined and stored successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)

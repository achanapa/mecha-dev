from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)

# Configure MongoDB
app.config['MONGO_URI'] = 'mongodb+srv://mechatronics:BhamAomNunEarn@dimension.i10gagw.mongodb.net/'
mongo = PyMongo(app)

# Routes

@app.route('/save_bolt_data', methods=['POST'])
def save_bolt_data():
    try:
        data = request.json
        # Save bolt data to Bolt_Dimension collection
        bolt_dimension_collection = mongo.db.Bolt_Dimension
        bolt_id = bolt_dimension_collection.insert_one(data).inserted_id

        # Combine with type of head and type of bit
        type_of_head = data.get('TypeOfHead')
        type_of_bit = data.get('TypeOfBit')

        # Save combined data to BoltBitHead collection
        bolt_bit_head_data = {
            "_id": bolt_id,
            "M_Size": data.get("M_Size"),
            "Head_Length": data.get("Head_Length"),
            "Thread_Length": data.get("Thread_Length"),
            "Head_Diameter": data.get("Head_Diameter"),
            "Thread_Diameter": data.get("Thread_Diameter"),
            "Space_Length": data.get("Space_Length"),
            "TypeOfHead": type_of_head,
            "TypeOfBit": type_of_bit,
        }

        bolt_bit_head_collection = mongo.db.BoltBitHead
        bolt_bit_head_collection.insert_one(bolt_bit_head_data)

        return jsonify({"message": "Bolt data saved successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/export_to_3d', methods=['GET'])
def export_to_3d():
    try:
        # Get the most recent bolt data from BoltBitHead collection
        bolt_bit_head_collection = mongo.db.BoltBitHead
        latest_bolt_data = bolt_bit_head_collection.find_one(sort=[('_id', -1)])

        if not latest_bolt_data:
            return jsonify({"error": "No bolt data found"}), 404

        # Trigger 3D model generation with latest bolt data
        # You may call a separate function or script to handle the 3D model generation process

        return jsonify({"message": "3D model generation triggered successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

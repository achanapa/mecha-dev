from pymongo import MongoClient

client = MongoClient('mongodb+srv://mechatronics:BhamAomNunEarn@dimension.i10gagw.mongodb.net/')
db = client['Dimension']

class BoltBitHead:
    collection = db['bolt_bit_head']

    @staticmethod
    def save_bolt_bit_head(data):
        # Implement logic to save BoltBitHead data
        # For example, you can insert a new document into the collection
        BoltBitHead.collection.insert_one(data)

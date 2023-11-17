from flask_pymongo import PyMongo

class BoltDimension:
    @staticmethod
    def init_app(app):
        # Initialize the PyMongo extension with the app context
        PyMongo.init_app(app)

        # Set the collection attribute
        BoltDimension.collection = PyMongo.db['Bolt_Dimension']

    @staticmethod
    def get_recent_bolt_data():
        # Implement logic to fetch and return recent bolt data
        # For example, you can fetch the latest bolt data based on a timestamp
        return BoltDimension.collection.find_one({}, sort=[('_id', -1)])


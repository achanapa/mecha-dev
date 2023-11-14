from flask import Blueprint, jsonify, current_app
import sys
sys.path.append('../models')
from models.bolt_dimension import BoltDimension
from flask_pymongo import PyMongo

bolt_dimension_bp = Blueprint('Bolt_Dimension', __name__)

@bolt_dimension_bp.route('/get_recent_bolt_data', methods=['GET'])
def get_recent_bolt_data():
    # Access the PyMongo instance from the Flask application context
    mongo = current_app.extensions['mongo']

    # Access the collection through the PyMongo instance
    bolt_dimension_collection = PyMongo.db['Bolt_Dimension']

    # Fetch the recent bolt data from the collection
    recent_bolt_data = bolt_dimension_collection.find_one({}, sort=[('_id', -1)])

    return jsonify(recent_bolt_data)




# from flask import Blueprint, jsonify
# import sys
# sys.path.append('../')
# from models.bolt_dimension import BoltDimension
# from pymongo import DESCENDING

# bolt_dimension_bp = Blueprint('bolt_dimension', __name__)

# @bolt_dimension_bp.route('/get_recent_bolt_data', methods=['GET'])
# def get_recent_bolt_data():

#     bolt_dimension_collection = app.mongo['bolt_dimension']

#     recent_bolt_data = bolt_dimension_collection.find_one({}, sort=[('_id', DESCENDING)])

#     return jsonify(recent_bolt_data)



# from flask import Blueprint, jsonify, current_app
# import sys
# sys.path.append('../models')
# from models.bolt_dimension import BoltDimension

# bolt_dimension_bp = Blueprint('bolt_dimension', __name__)

# @bolt_dimension_bp.route('/get_recent_bolt_data', methods=['GET'])
# def get_recent_bolt_data():
#     bolt_dimension_collection = current_app.mongo['bolt_dimension']
#     recent_bolt_data = BoltDimension.collection.find_one({}, sort=[('_id', -1)])
#     return jsonify(recent_bolt_data)

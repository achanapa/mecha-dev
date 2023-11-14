from flask import Blueprint, jsonify
from server.models.bolt_dimension import BoltDimension

bolt_dimension_bp = Blueprint('bolt_dimension', __name__)

@bolt_dimension_bp.route('/get_recent_bolt_data', methods=['GET'])
def get_recent_bolt_data():
    # Implement logic to fetch recent bolt data from the Bolt_Dimension collection
    recent_bolt_data = BoltDimension.get_recent_bolt_data()
    return jsonify(recent_bolt_data)
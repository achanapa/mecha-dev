import sys
from flask import Blueprint, request, jsonify
sys.path.append('../')
from models.bolt_bit_head import BoltBitHead

bolt_bit_head_bp = Blueprint('bolt_bit_head', __name__)

@bolt_bit_head_bp.route('/save_bolt_bit_head', methods=['POST'])
def save_bolt_bit_head():
    data = request.json
    # Implement logic to save the combined data in the BoltBitHead collection
    BoltBitHead.save_bolt_bit_head(data)
    return jsonify({"message": "BoltBitHead data saved successfully!"})

from flask import Blueprint, jsonify, request, make_response
import models.ratings_model as rm
from utils.guards import token_required

ratings = Blueprint('ratings', __name__)


@ratings.route('<int:id>', methods=['GET', 'POST', 'PUT'])
@token_required
def handle_ratings(uid, id):
    if request.method == 'GET':
        res = rm.get_rate(uid, id)
        if res == None:
            return jsonify({'rate': 0})
        else:
            return jsonify(res)
    elif request.method == 'POST':
        if not 'rate' in request.json:
            return jsonify({"message": "rate is required"}), 406
        rate = request.json['rate']
        try:
            rm.add_rate(uid, id, rate)
            return make_response(jsonify({'message': 'rated'}), 201)
        except:
            return make_response(jsonify({'message': 'already rated'}), 302)
    elif request.method == 'PUT':
        if not 'rate' in request.json:
            return jsonify({"message": "rate is required"}), 406
        rate = request.json['rate']
        rm.edit_rate(uid, id, rate)
        return make_response(jsonify({'message': 'updated'}), 200)

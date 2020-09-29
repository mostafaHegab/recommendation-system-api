from flask import Blueprint, jsonify, request, make_response
import models.ratings_model as rm
from utils.guards import token_required

ratings = Blueprint('ratings', __name__)

@ratings.route('', methods=['POST'])
@token_required
def add_new_rating(uid):
    pid = request.json['pid']
    rate = request.json['rate']
    rm.add_rate(rate, pid ,uid)
    return make_response(jsonify({'message': 'rated'}), 201)

@ratings.route('<int:id>', methods=['PUT'])
@token_required
def change_rating(uid, id):
    rate = request.json['rate']
    rm.edit_rate(id, rate)
    return make_response(jsonify({'message': 'updated'}), 200)


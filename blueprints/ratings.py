from flask import Blueprint, jsonify, request, make_response
import models.ratings_model as rm

ratings = Blueprint('ratings', __name__)

@ratings.route('', methods=['POST'])
def add_new_rating():
    uid = 1
    pid = request.json['pid']
    rate = request.json['rate']
    rm.add_rate(rate, pid ,uid)
    return make_response(jsonify({'message': 'rated'}), 201)

@ratings.route('<int:id>', methods=['PUT'])
def change_rating(id):
    uid = 1
    rate = request.json['rate']
    rm.edit_rate(id, rate)
    return make_response(jsonify({'message': 'updated'}), 200)


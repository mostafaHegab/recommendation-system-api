from flask import Blueprint, jsonify, request, make_response
import models.comments_model as cm
from utils.guards import token_required
from utils.validator import Validator
import datetime

comments = Blueprint('comments', __name__)


@comments.route('', methods=['POST'])
@token_required
@Validator.require(['pid', 'comment'])
@Validator.string(['comment'])
@Validator.integer(['pid'])
def add_new_comment(uid):
    pid = request.json['pid']
    comment = request.json['comment']
    time = datetime.datetime.utcnow()
    id = cm.add_comment(comment, time, uid, pid)
    return make_response(jsonify({'cid': id, "time": time}), 201)


@comments.route('<int:id>', methods=['PUT', 'DELETE'])
@token_required
def change_comment(uid, id):
    if request.method == 'PUT':
        if not 'comment' in request.json:
            return jsonify({"message": "comment is required"}), 406
        comment = request.json['comment']
        cm.edit_comment(id, comment)
        return make_response(jsonify({'message': 'comment modified'}), 200)

    elif request.method == 'DELETE':
        cm.delete_comment(id)
        return make_response(jsonify({'message': 'DELETED'}), 200)

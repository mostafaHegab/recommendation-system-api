from flask import Blueprint, jsonify, request, make_response
import models.comments_model as cm
from utils.guards import token_required
import datetime

comments = Blueprint('comments', __name__)

@comments.route('', methods=['POST'])
@token_required
def add_new_comment(uid):
    pid = request.json['pid']
    comment = request.json['comment']
    time = datetime.datetime.utcnow()
    cm.add_comment(comment, time, pid, uid)
    return make_response(jsonify({'message': 'comment added'}), 201)


@comments.route('<int:id>', methods=['PUT', 'DELETE'])
@token_required
def change_comment(uid, id):
    if request.method == 'PUT' :
        comment = request.json['comment']
        cm.edit_comment(id, comment)
        return make_response(jsonify({'message': 'comment modified'}), 200)

    elif request.method == 'DELETE' :
        cm.delete_comment(id)
        return make_response(jsonify({'message': 'DELETED'}), 200)
    

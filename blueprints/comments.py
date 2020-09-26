from flask import Blueprint, jsonify, request, make_response
import models.comments_model as cm

comments = Blueprint('comments', __name__)

@comments.route('', methods=['POST'])
def add_new_comment():
    uid = 1
    pid = request.json['pid']
    time = request.json['time']
    comment = request.json['comment']
    cm.add_comment(comment, time, pid, uid)
    return make_response(jsonify({'message': 'comment added'}), 201)


@comments.route('<int:id>', methods=['PUT', 'DELETE'])
def change_comment(id):
    if request.method == 'PUT' :
        comment = request.json['comment']
        cm.edit_comment(id, comment)
        return make_response(jsonify({'message': 'comment modified'}), 200)

    elif request.method == 'DELETE' :
        cm.delete_comment(id)
        return make_response(jsonify({'message': 'DELETED'}), 200)
    







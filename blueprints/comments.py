from flask import Blueprint, jsonify, request, make_response
import models.comments_model as cm

comments = Blueprint('comments', __name__)

@comments.route('', methods=['POST'])
def add_new_comment():
    id = 1
    uid = request.json['uid']
    pid = request.json['pid']
    time = request.json['time']
    comment = request.json['comment']

    new_comment = cm.add_comment(comments, time, pid, uid)
    return make_response(jsonify(id), 201)


@comments.route('<id>', methods=['PUT', 'DELETE'])
def change_comment():
    id = 1
    comment = request.json['comment']

    if request.method == 'PUT' :
        edited_comment = cm.edit_comment(id, comment)
        return make_response(jsonify(id), 200)

    elif request.method == 'DELETE' :
        #change user info
        deleted_comment = cm.delete_comment(id)
        return make_response(jsonify({'message': 'DELETED'}), 200)
    







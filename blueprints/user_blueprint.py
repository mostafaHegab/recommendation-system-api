from flask import Blueprint, jsonify, request, make_response
import models.users_model as um
from werkzeug.utils import secure_filename
from utils.uploader import upload_user_image

from utils import security
from utils.guards import token_required

user = Blueprint('user', __name__)


@user.route('', methods=['GET', 'PUT'])
@token_required
def user_info(id):
    if request.method == 'GET':
        info = um.user_info(id)
        return make_response(jsonify(info), 200)
    elif request.method == 'PUT':
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        # change user info
        um.change_user_info(id, firstname, lastname)
        return make_response(jsonify({'message': 'Info Changed'}), 200)


allowed_image_extentions = ["JPEG", "JPG", "PNG"]


@user.route('change_image', methods=['PUT'])
@token_required
def change_image(id):
    if request.files:
        image = request.files["image"]
        if image.filename == "":
            return jsonify({'message': 'File has no name'}), 403

        if not "." in image.filename:
            return jsonify({'message': 'File has no extension'}), 403

        ext = image.filename.rsplit(".", 1)[1]
        if not ext.upper() in allowed_image_extentions:
            return jsonify({'message': 'unacceptable extension'}), 403

        newfilename = f'{id}.{ext}'
        upload_user_image(image, newfilename)
        um.change_profile_image(id, newfilename)
        return make_response(jsonify({'message': 'Profile Picture Changed'}), 200)
    return jsonify({'message': 'image not provided'}), 403


@user.route('change_password', methods=['PUT'])
@token_required
def change_user_password(id):
    newpassword = request.json['newpassword']
    oldpassword = request.json['oldpassword']
    user_pass = um.get_user_password(id)['password']

    if not security.check_encrypted_password(oldpassword, user_pass):
        return make_response(jsonify({'message': 'Wrong Password'}), 406)

    um.change_password(id, security.encrypt_password(newpassword))
    return make_response(jsonify({'message': 'Password Changed'}), 200)

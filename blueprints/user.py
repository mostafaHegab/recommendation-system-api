from flask import Blueprint, jsonify, request, make_response, redirect
import models.users_model as um
from werkzeug.utils import secure_filename
from utils.uploader import upload_user_image

user = Blueprint('user', __name__)


@user.route('', methods=['GET', 'PUT'])
def user_info():
    id = 1
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


@user.route('change_image', methods=['POST'])
def change_image():
    id = 1
    if request.files:
        image = request.files["image"]
        if image.filename == "":
            return jsonify({'message': 'File has no name'}), 403

        if not "." in image.filename:
            return jsonify({'message': 'File has no extension'}), 403

        ext = image.filename.rsplit(".", 1)[1]
        if not ext.upper() in allowed_image_extentions:
            return jsonify({'message': 'unacceptable extension'}), 403

        filename = secure_filename(image.filename)
        newfilename = str(id) + "." + (filename.rsplit(".", 1)[1])
        upload_user_image(image, newfilename)
        um.change_profile_image(id, newfilename)
        return make_response(jsonify({'message': 'Profile Picture Changed'}), 200)
    return jsonify({'message': 'image not provided'}), 403


@user.route('change_password', methods=['PUT'])
def change_user_password():
    id = 1
    newpassword = request.json['newpassword']
    oldpassword = request.json['oldpassword']
    user_pass = um.get_user_password(id)['password']

    # TASK- Compare to hashed password
    if user_pass != oldpassword:
        return make_response(jsonify({'message': 'Wrong Password'}), 406)

    um.change_password(id, newpassword)
    return make_response(jsonify({'message': 'Password Changed'}), 200)

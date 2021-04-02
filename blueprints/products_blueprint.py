from flask import Blueprint, jsonify, request
import datetime
import models.products_model as pm
from utils.config import ITEMS_PER_PAGE
# from utils.uploader import upload_product_image
from utils.guards import token_required

products = Blueprint('products', __name__)

@products.route('rec', methods=['GET'])
@token_required
def get_recommendations(uid):
    page = int(request.args.get('page'))
    skip = (page - 1) * ITEMS_PER_PAGE
    places = pm.get_products(uid, skip, ITEMS_PER_PAGE)
    return jsonify(places), 200

@products.route('<int:id>', methods=['GET'])
@token_required
def get_product_info(uid, id):
    info = pm.product_info(id, uid)
    if info['rating']:
        info['rating'] = float(info['rating'])
    else:
        info['rating'] = 0
    return jsonify(info), 200


# @products.route('<int:id>/images', methods=['GET', 'POST'])
# @token_required
# def place_images(uid, id):
#     if request.method == 'GET':
#         images = pm.get_product_image(id)
#         return jsonify(images), 200
#     elif request.method == 'POST':
#         allowed_image_extentions = ["JPEG", "JPG", "PNG"]
#         if request.files:
#             image = request.files["image"]
#             if image.filename == "":
#                 return jsonify({'message': 'File has no name'}), 403
#             if not "." in image.filename:
#                 return jsonify({'message': 'File has no extension'}), 403
#             ext = image.filename.rsplit(".", 1)[1]
#             if not ext.upper() in allowed_image_extentions:
#                 return jsonify({'message': 'unacceptable extension'}), 403
#             filename = f'{datetime.datetime.now().timestamp()}-{image.filename}'
#             upload_product_image(image, id, filename)
#             pm.set_product_image(id, filename)
#             return jsonify({'message': 'image uploaded'}), 201

#         return jsonify({'message': 'image not provided'}), 403


@products.route('<int:id>/comments')
@token_required
def get_comments(uid, id):
    page = int(request.args.get('page'))
    skip = (page - 1) * ITEMS_PER_PAGE
    limit = ITEMS_PER_PAGE
    comments = pm.get_comments(id, skip, limit)
    return jsonify(comments), 200


@products.route('/fav', methods=['GET', 'POST'])
@token_required
def favorite(uid):
    if request.method == 'GET':
        result = pm.get_favorits(uid)
        return jsonify(result), 200
    elif request.method == 'POST':
        pm.add_favorit(request.json['pid'], uid)
        return jsonify({'message': 'added'}), 201


@products.route('/fav/<int:pid>', methods=['DELETE'])
@token_required
def delete_fav(uid, pid):
    pm.delete_favorit(pid, uid)
    return jsonify({'message': 'deleted'})

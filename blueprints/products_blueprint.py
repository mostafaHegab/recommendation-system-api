from flask import Blueprint, jsonify, request
import datetime
import models.products_model as pm
from utils.config import ITEMS_PER_PAGE
# from utils.uploader import upload_product_image
from utils.guards import token_required

products = Blueprint('products', __name__)


@products.route('', methods=['GET'])
@token_required
def search(uid):
    if not request.args.get('page') == None:
        page = int(request.args.get('page'))
    else:
        page = 1
    skip = (page - 1) * ITEMS_PER_PAGE
    if 's' in request.args:
        res = pm.search_by_name(request.args.get('s'), skip, ITEMS_PER_PAGE)
    elif 't' in request.args:
        res = pm.search_by_tag(request.args.get('t'), skip, ITEMS_PER_PAGE)
    return jsonify(res), 200


@products.route('rec', methods=['GET'])
@token_required
def get_recommendations(uid):
    if not request.args.get('page') == None:
        page = int(request.args.get('page'))
    else:
        page = 1
    skip = (page - 1) * ITEMS_PER_PAGE
    recs = pm.get_recommendations(uid, skip, ITEMS_PER_PAGE)
    return jsonify(recs), 200

@products.route('rec-product', methods=['GET'])
@token_required
def get_similar_product(uid):        
    pid = int(request.args.get('pid'))
    if not request.args.get('page') == None:
        page = int(request.args.get('page'))
    else:
        page = 1
    skip = (page - 1) * ITEMS_PER_PAGE
    recs = pm.get_similar_product(pid, skip, ITEMS_PER_PAGE)
    return jsonify(recs), 200

@products.route('<int:id>', methods=['GET'])
@token_required
def get_product_info(uid, id):
    info = pm.product_info(uid, id)
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


@products.route('<int:id>/comments', methods=['GET'])
@token_required
def get_comments(uid, id):
    if not request.args.get('page') == None:
        page = int(request.args.get('page'))
    else:
        page = 1
    skip = (page - 1) * ITEMS_PER_PAGE
    limit = ITEMS_PER_PAGE
    comments = pm.get_comments(id, skip, limit)
    return jsonify(comments), 200


@products.route('/fav', methods=['GET', 'POST'])
@token_required
def favorite(uid):
    if request.method == 'GET':
        if not request.args.get('page') == None:
            page = int(request.args.get('page'))
        else:
            page = 1
        skip = (page - 1) * ITEMS_PER_PAGE
        limit = ITEMS_PER_PAGE
        result = pm.get_favorits(uid, skip, limit)
        return jsonify(result), 200
    elif request.method == 'POST':
        if not 'pid' in request.json:
            return jsonify({"message": "pid is required"}), 406
        try:
            pm.add_favorit(uid, request.json['pid'])
            return jsonify({'message': 'added'}), 201
        except:
            return jsonify({'message': 'already added'}), 302


@products.route('/fav/<int:pid>', methods=['DELETE'])
@token_required
def delete_fav(uid, pid):
    pm.delete_favorit(uid, pid)
    return jsonify({'message': 'deleted'})

from flask import Blueprint, jsonify, request
import datetime
import models.places_model as pm
from utils.config import ITEMS_PER_PAGE
from utils.uploader import upload_place_image
from utils.guards import token_required

places = Blueprint('places', __name__)


@places.route('', methods=['POST'])
@token_required
def add_place(uid):
    name = request.json['name']
    country = request.json['country']
    city = request.json['city']
    lat = request.json['lat']
    lng = request.json['lng']
    id = pm.add_place(name, country, city, lat, lng)
    return jsonify({'pid': id}), 201


@places.route('rec', methods=['GET'])
@token_required
def get_recommendations(uid):
    page = int(request.args.get('page'))
    skip = (page - 1) * ITEMS_PER_PAGE
    limit = ITEMS_PER_PAGE
    places = pm.get_places(uid, skip, limit)
    return jsonify(places), 200


@places.route('search', methods=['GET'])
@token_required
def search(uid):
    country = request.args.get('country')
    key = request.args.get('key')
    places = pm.get_places(1,0,10)
    return jsonify(places), 200


@places.route('<int:id>', methods=['GET'])
@token_required
def get_place_info(uid, id):
    info = pm.place_info(id, uid)
    info['rating'] = float(info['rating'])
    return jsonify(info), 200


@places.route('<int:id>/images', methods=['GET', 'POST'])
@token_required
def place_images(uid, id):
    if request.method == 'GET':
        images = pm.get_place_images(id)
        return jsonify(images), 200
    elif request.method == 'POST':
        allowed_image_extentions = ["JPEG", "JPG", "PNG"]
        if request.files:
            image = request.files["image"]
            if image.filename == "":
                return jsonify({'message': 'File has no name'}), 403
            if not "." in image.filename:
                return jsonify({'message': 'File has no extension'}), 403
            ext = image.filename.rsplit(".", 1)[1]
            if not ext.upper() in allowed_image_extentions:
                return jsonify({'message': 'unacceptable extension'}), 403
            filename = f'{datetime.datetime.now().timestamp()}-{image.filename}'
            upload_place_image(image, id, filename)
            pm.add_place_image(id, filename)
            return jsonify({'message': 'image uploaded'}), 201

        return jsonify({'message': 'image not provided'}), 403


@places.route('<int:id>/comments')
@token_required
def get_comments(uid, id):
    page = int(request.args.get('page'))
    skip = (page - 1) * ITEMS_PER_PAGE
    limit = ITEMS_PER_PAGE
    comments = pm.get_place_comments(id, skip, limit)
    return jsonify(comments), 200


@places.route('visited', methods=['GET', 'POST'])
@token_required
def visited(uid):
    if request.method == 'GET':
        places = pm.visited_places(uid)
        return jsonify(places), 200
    elif request.method == 'POST':
        pm.add_visit(request.json['pid'], uid)
        return jsonify({'message': 'place added'}), 201


@places.route('visited/<int:pid>', methods=['DELETE'])
@token_required
def delete_visit(uid, pid):
    pm.delete_visit(pid, uid)
    return jsonify({'message': 'deleted'})


@places.route('/fav', methods=['GET', 'POST'])
@token_required
def favorite(uid):
    if request.method == 'GET':
        result = pm.favorits_places(uid)
        for p in result:
            p['rating'] = float(p['rating'])
        return jsonify(result), 200
    elif request.method == 'POST':
        pm.add_favorit(request.json['pid'], uid)
        return jsonify({'message': 'added'}), 201


@places.route('/fav/<int:pid>', methods=['DELETE'])
@token_required
def delete_fav(uid, pid):
    pm.delete_favorit(pid, uid)
    return jsonify({'message': 'deleted'})

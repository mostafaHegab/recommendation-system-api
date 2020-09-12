from flask import Blueprint, jsonify, request
import datetime
import models.places_model as pm
from utils.config import ITEMS_PER_PAGE
from utils.uploader import upload_place_image

places = Blueprint('places', __name__)


@places.route('', methods=['POST'])
def add_place():
    name = request.json['name']
    country = request.json['country']
    city = request.json['city']
    lat = request.json['lat']
    lng = request.json['lng']
    id = pm.add_place(name, country, city, lat, lng)
    return jsonify({'pid': id}), 201


@places.route('rec', methods=['POST'])
def get_recommendations():
    places = pm.get_places()
    return jsonify({'places': places}), 200


@places.route('search', methods=['GET'])
def search():
    country = request.args.get('c')
    key = request.args.get('k')
    places = pm.get_places()
    return jsonify({'places': places}), 200


@places.route('<int:id>', methods=['GET'])
def get_place_info(id):
    info = pm.place_info(id)
    info['rating'] = float(info['rating'])
    return jsonify(info), 200


@places.route('<int:id>/images', methods=['GET', 'POST'])
def place_images(id):
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


@places.route('<int:id>/comments/<int:page>')
def get_comments(id, page):
    skip = (page - 1) * ITEMS_PER_PAGE
    limit = ITEMS_PER_PAGE
    comments = pm.get_place_comments(id, skip, limit)
    return jsonify(comments), 200


@places.route('/visited', methods=['GET', 'POST'])
def visited():
    uid = 1
    if request.method == 'GET':
        places = pm.visited_places(id)
        return jsonify(places), 200
    elif request.method == 'POST':
        pm.add_visit(request.json['pid'], uid)
        return jsonify({'message': 'place added'}), 201


@places.route('visited/<int:pid>', methods=['DELETE'])
def delete_visit(pid):
    uid = 1
    pm.delete_visit(pid, uid)
    return jsonify({'message': 'deleted'})


@places.route('/fav', methods=['GET', 'POST'])
def favorite():
    uid = 1
    if request.method == 'GET':
        name = pm.favorits_places(uid)
        return jsonify(name), 200
    elif request.method == 'POST':
        pm.add_favorit(request.json['pid'], uid)
        return jsonify({'message': 'added'}), 201


@places.route('/fav/<int:pid>', methods=['DELETE'])
def delete_fav(pid):
    uid = 1
    pm.delete_favorit(pid, uid)
    return jsonify({'message': 'deleted'})

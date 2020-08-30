from flask import Blueprint, jsonify, request
import models.places_model as pm
from utils.guards import token_required
from utils.config import ITEMS_PER_PAGE

places = Blueprint('places', __name__)


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
        # upload new image
        return jsonify({'message': 'image uploaded'}), 201


@places.route('<int:id>/comments/<int:page>')
def get_comments(id, page):
    skip = (page - 1) * ITEMS_PER_PAGE
    limit = ITEMS_PER_PAGE
    comments = pm.get_place_comments(id, skip, limit)
    return jsonify(comments), 200

@places.route('/visited', methods=['GET', 'POST'])
def visited(id):
    if request.method == 'GET' :
        name=pm.visited_places(id)
    #images=pm.get_place_images(id,name)
    #rate=pm.place_info(id)
        return jsonify(name),200
    elif request.method == 'POST':
        add_visited_pl = pm.add_place(id)
        return jsonify({'message' : 'place added'}),201

@places.route('/delete/<int:id>', methods=['DELETE'])
def deleted(id):
    del_place = pm.delete_visit(id,'1')
    return jsonify({'message' : 'deleted'})

@places.route('/fav', methods=['GET', 'POST'])
def favorite(id):
    if request.method == 'GET' :
        name=pm.favorits_places(id)
        return jsonify(name),200
    elif request.method == 'POST':
        add_fav = pm.add_favorit(id)
        return jsonify(add_fav),201

@places.route('/fav/<int:id>', methods=['DELETE'])
def deleted(id):
    del_place = pm.delete_favorit(id,'1')
    return jsonify({'message' : 'deleted'})
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

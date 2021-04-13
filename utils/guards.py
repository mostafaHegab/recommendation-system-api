from flask import request, jsonify
from functools import wraps
import jwt
from .config import JWT_SECRET_KEY


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if not 'Authorization' in request.headers:
            return jsonify({'message': 'missing "Authorization" header'}), 401
        token = request.headers['Authorization']
        if not token:
            return jsonify({'message': 'token is missing'}), 401
        try:
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        except:
            return jsonify({'message': 'invalid or expired token'}), 401

        return f(data['uid'], *args, **kwargs)
    return decorator

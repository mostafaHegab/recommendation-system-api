from flask import request, jsonify
from functools import wraps
import jwt
from .config import JWT_SECRET_KEY

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return jsonify({'message': 'token is missing'}), 401
        try:
            data = jwt.decode(token, JWT_SECRET_KEY)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'token is expired'}), 403
        except:
            return jsonify({'message': 'invalid refresh token'}), 403

        return f(data['uid'], *args, **kwargs)
    return decorator
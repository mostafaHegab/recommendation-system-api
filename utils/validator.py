from flask import request, jsonify
from functools import wraps
import re
email_regex = '[^@]+@[^@]+\.[^@]+'


class Validator:

    @staticmethod
    def require(fields):
        def decorator(f):
            @wraps(f)
            def inner(*args, **kwargs):
                for field in fields:
                    if not field in request.json:
                        return jsonify({"message": f"{field} is required"}), 406
                return f(*args, **kwargs)
            return inner
        return decorator

    @staticmethod
    def string(fields):
        def decorator(f):
            @wraps(f)
            def inner(*args, **kwargs):
                for field in fields:
                    if not isinstance(request.json[field], str):
                        return jsonify({"message": f"{field} must be string"}), 406
                return f(*args, **kwargs)
            return inner
        return decorator

    @staticmethod
    def integer(fields):
        def decorator(f):
            @wraps(f)
            def inner(*args, **kwargs):
                for field in fields:
                    if not isinstance(request.json[field], int):
                        return jsonify({"message": f"{field} must be integer"}), 406
                return f(*args, **kwargs)
            return inner
        return decorator

    @staticmethod
    def email(fields):
        def decorator(f):
            @wraps(f)
            def inner(*args, **kwargs):
                for field in fields:
                    if not re.search(email_regex, request.json[field]):
                        return jsonify({"message": f"{field} must be a valid email format"}), 406
                return f(*args, **kwargs)
            return inner
        return decorator

    @staticmethod
    def min_length(desc_dict):
        def decorator(f):
            @wraps(f)
            def inner(*args, **kwargs):
                for key in desc_dict:
                    if len(request.json[key]) < desc_dict[key]:
                        return jsonify({"message": f"{key} must be at least {desc_dict[key]} character"}), 406
                return f(*args, **kwargs)
            return inner
        return decorator

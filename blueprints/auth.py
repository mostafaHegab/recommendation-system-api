from flask import Blueprint, jsonify, request
from random import randint
import jwt
import datetime

import models.auth_model as am
from utils.config import JWT_SECRET_KEY, MAIL_CONFIG
from utils.mailer import Mailer

auth = Blueprint('auth', __name__)


@auth.route('signup', methods=['POST'])
def signup():
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    password = request.json['password']
    users = am.find_user(email)
    if (len(users) > 0):
        return jsonify({'message': 'account already exists'}), 302

    # TASK- hash password
    hashed_password = password

    verify_code = randint(1000, 9999)
    am.create_user(firstname, lastname, email, hashed_password, verify_code, 'user.png')

    email_body = f'''
        please use the below code to verify your email
        {verify_code}
    '''
    Mailer.send_email('Email Verification', email_body, MAIL_CONFIG['auth_mailer'], email)

    return jsonify({'message': 'account created'}), 201


@auth.route('verify', methods=["POST"])
def verify():
    email = request.json['email']
    code = request.json['code']
    users = am.get_verification_code(email)
    if len(users) == 0:
        return jsonify({'message': 'no account matches this email'}), 404
    user = users[0]
    if code != user['verified']:
        return jsonify({'message': 'wrong code'}), 406
    am.verify_account(user['id'])

    access_token_exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    access_token = jwt.encode({'uid': user['id'], 'exp': access_token_exp}, JWT_SECRET_KEY)
    refresh_token_exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    refresh_token = jwt.encode({'exp': refresh_token_exp}, JWT_SECRET_KEY)
    return jsonify({'access_token': access_token.decode('UTF-8'), 'access_token_exp': access_token_exp,
                    'refresh_token': refresh_token.decode('UTF-8'), 'refresh_token_exp': refresh_token_exp}), 200


@auth.route('login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    users = am.find_user(email)
    if len(users) == 0:
        return jsonify({'message': 'no account matches this email'}), 404
    user = users[0]
    if user['verified'] != 0:
        return jsonify({'message': 'account not verified'}), 403

    # TASK- compare with hashed password
    if password != user['password']:
        return jsonify({'message': 'wrong password'}), 406

    access_token_exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    access_token = jwt.encode({'uid': user['id'], 'exp': access_token_exp}, JWT_SECRET_KEY)
    refresh_token_exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    refresh_token = jwt.encode({'exp': refresh_token_exp}, JWT_SECRET_KEY)
    return jsonify({'access_token': access_token.decode('UTF-8'), 'access_token_exp': access_token_exp,
                    'refresh_token': refresh_token.decode('UTF-8'), 'refresh_token_exp': refresh_token_exp}), 200


@auth.route('send_reset_code', methods=['POST'])
def send_reset_code():
    email = request.json['email']
    users = am.find_user(email)
    if len(users) == 0:
        return jsonify({'message': 'no account matches this email'}), 404
    code = randint(1000, 9999)
    am.set_reset_code(users[0]['id'], code)

    email_body = f'''
            please use the below code to reset your password
            {code}
        '''
    Mailer.send_email('Email Verification', email_body, MAIL_CONFIG['auth_mailer'], email)

    return jsonify({'message': 'code sent'}), 200


@auth.route('reset_password', methods=['POST'])
def reset_password():
    email = request.json['email']
    code = request.json['code']
    password = request.json['password']
    users = am.get_reset_code(email)
    if len(users) == 0:
        return jsonify({'message': 'no account matches this email'}), 404
    if code != users[0]['code']:
        return jsonify({'message': 'wrong code'}), 406

    # TASK- hash password
    hashed_password = password
    am.reset_password(users[0]['id'], hashed_password)


@auth.route('refresh_token', methods=['POST'])
def refresh_token():
    old_token = request.json['old_token']
    refresh_token = request.json['refresh_token']
    try:
        jwt.decode(refresh_token, JWT_SECRET_KEY)
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'refresh token is expired'}), 403
    except:
        return jsonify({'message': 'invalid refresh token'}), 403

    uid = jwt.decode(old_token, JWT_SECRET_KEY, verify=False)['uid']
    access_token_exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    access_token = jwt.encode({'uid': uid, 'exp': access_token_exp}, JWT_SECRET_KEY)
    refresh_token_exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    refresh_token = jwt.encode({'exp': refresh_token_exp}, JWT_SECRET_KEY)
    return jsonify({'access_token': access_token.decode('UTF-8'), 'access_token_exp': access_token_exp,
                    'refresh_token': refresh_token.decode('UTF-8'), 'refresh_token_exp': refresh_token_exp}), 200

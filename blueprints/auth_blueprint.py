from flask import Blueprint, jsonify, request
from random import randint
import jwt
import datetime

import models.auth_model as am
from utils.config import JWT_SECRET_KEY, ACCESS_TOKEN_EXPIRATION_OFFSET, REFRESH_TOKEN_EXPIRATION_OFFSET, MAIL_CONFIG
from utils.mailer import Mailer

from utils import security
from utils.validator import Validator

auth = Blueprint('auth', __name__)


@auth.route('signup', methods=['POST'])
@Validator.require(['firstname', 'lastname', 'email', 'password'])
@Validator.string(['firstname', 'lastname', 'email', 'password'])
@Validator.email(['email'])
@Validator.min_length({"password": 6})
def signup():
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    password = request.json['password']
    users = am.find_user(email)
    if (len(users) > 0):
        return jsonify({'message': 'account already exists'}), 302

    hashed_password = security.encrypt_password(password)

    verify_code = 0  # randint(1000, 9999)
    am.create_user(firstname, lastname, email,
                   hashed_password, verify_code, 'user.png')

    # email_body = f'''
    #     please use the below code to verify your email
    #     {verify_code}
    # '''
    # Mailer.send_email(subject='Email Verification', body=email_body, reciever=email)

    return jsonify({'message': 'account created'}), 201


@auth.route('verify', methods=["POST"])
@Validator.require(['email', 'code'])
@Validator.string(['email'])
@Validator.email(['email'])
@Validator.integer(['code'])
def verify():
    email = request.json['email']
    code = request.json['code']
    users = am.get_verification_code(email)
    if len(users) == 0:
        return jsonify({'message': 'no account matches this email'}), 404
    user = users[0]
    if user['verified'] == 0:
        return jsonify({'message': 'already verified'}), 200
    if code != user['verified']:
        return jsonify({'message': 'wrong code'}), 406
    am.verify_account(user['id'])

    access_token_exp = datetime.datetime.utcnow(
    ) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRATION_OFFSET)
    access_token = jwt.encode(
        {'uid': user['id'], 'exp': access_token_exp}, JWT_SECRET_KEY, algorithm='HS256')
    refresh_token_exp = datetime.datetime.utcnow(
    ) + datetime.timedelta(days=REFRESH_TOKEN_EXPIRATION_OFFSET)
    refresh_token = jwt.encode(
        {'exp': refresh_token_exp}, JWT_SECRET_KEY, algorithm='HS256')
    return jsonify({'access_token': access_token, 'access_token_exp': access_token_exp,
                    'refresh_token': refresh_token, 'refresh_token_exp': refresh_token_exp}), 200


@auth.route('login', methods=['POST'])
@Validator.require(['email', 'password'])
@Validator.string(['email', 'password'])
@Validator.email(['email'])
@Validator.min_length({"password": 6})
def login():
    email = request.json['email']
    password = request.json['password']
    users = am.find_user(email)
    if len(users) == 0:
        return jsonify({'message': 'no account matches this email'}), 404
    user = users[0]
    if user['verified'] != 0:
        return jsonify({'message': 'account not verified'}), 403

    if not security.check_encrypted_password(password, user['password']):
        return jsonify({'message': 'wrong password'}), 406

    access_token_exp = datetime.datetime.utcnow(
    ) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRATION_OFFSET)
    access_token = jwt.encode(
        {'uid': user['id'], 'exp': access_token_exp}, JWT_SECRET_KEY, algorithm='HS256')
    refresh_token_exp = datetime.datetime.utcnow(
    ) + datetime.timedelta(days=REFRESH_TOKEN_EXPIRATION_OFFSET)
    refresh_token = jwt.encode(
        {'exp': refresh_token_exp}, JWT_SECRET_KEY, algorithm='HS256')
    return jsonify({'access_token': access_token, 'access_token_exp': access_token_exp,
                    'refresh_token': refresh_token, 'refresh_token_exp': refresh_token_exp}), 200


@auth.route('send_reset_code', methods=['POST'])
@Validator.require(['email'])
@Validator.string(['email'])
@Validator.email(['email'])
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
    Mailer.send_email(subject='Email Verification',
                      body=email_body, reciever=email)

    return jsonify({'message': 'code sent'}), 200


@auth.route('reset_password', methods=['POST'])
@Validator.require(['email', 'password', 'code'])
@Validator.string(['email', 'password'])
@Validator.integer(['code'])
@Validator.email(['email'])
@Validator.min_length({"password": 6})
def reset_password():
    email = request.json['email']
    code = request.json['code']
    password = request.json['password']
    users = am.get_reset_code(email)
    if len(users) == 0:
        return jsonify({'message': 'no account matches this email'}), 404
    if code != users[0]['reset_code']:
        return jsonify({'message': 'wrong code'}), 406

    hashed_password = security.encrypt_password(str(password))
    am.reset_password(users[0]['id'], hashed_password)

    return jsonify({"message": "password changed"}), 200


@auth.route('refresh_token', methods=['POST'])
@Validator.require(['old_token', 'refresh_token'])
@Validator.string(['old_token', 'refresh_token'])
def refresh_token():
    old_token = request.json['old_token']
    refresh_token = request.json['refresh_token']
    try:
        jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'refresh token is expired'}), 403
    except:
        return jsonify({'message': 'invalid refresh token'}), 403

    uid = jwt.decode(old_token, JWT_SECRET_KEY, algorithms=[
                     'HS256'], options={'verify_exp': False})['uid']
    access_token_exp = datetime.datetime.utcnow(
    ) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRATION_OFFSET)
    access_token = jwt.encode(
        {'uid': uid, 'exp': access_token_exp}, JWT_SECRET_KEY, algorithm='HS256')
    refresh_token_exp = datetime.datetime.utcnow(
    ) + datetime.timedelta(days=REFRESH_TOKEN_EXPIRATION_OFFSET)
    refresh_token = jwt.encode(
        {'exp': refresh_token_exp}, JWT_SECRET_KEY, algorithm='HS256')
    return jsonify({'access_token': access_token, 'access_token_exp': access_token_exp,
                    'refresh_token': refresh_token, 'refresh_token_exp': refresh_token_exp}), 200

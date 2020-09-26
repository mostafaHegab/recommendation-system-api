DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'name': 'tourism'
}

MAIL_CONFIG = {
    'server': 'smtp.gmail.com',
    'port': 465,
    'username': 'makotak1412@gmail.com',
    'password': 'sasa_hegab',
    'tls': False,
    'ssl': True,
    'auth_mailer': 'makotak1412@gmail.com'
}


JWT_SECRET_KEY = 'CSE2021 Graduation Project - Tourism APP'
ACCESS_TOKEN_EXPIRATION_OFFSET = 15 # minutes
REFRESH_TOKEN_EXPIRATION_OFFSET = 15 # days

ITEMS_PER_PAGE = 20
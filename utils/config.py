DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'name': 'grad_proj'
}

NEO4J_CONFIG = {
    'url': "bolt://localhost:7687",
    'password': 'admin'
}

MAIL_CONFIG = {
    'server': 'smtp.mailtrap.io',
    'port': 2525,
    'username': 'e6cb3362b9b824',
    'password': 'bcd9362e97c8fa',
    'tls': True,
    'ssl': False
}


JWT_SECRET_KEY = 'CSE2021 Graduation Project - Recommendation System APP'
ACCESS_TOKEN_EXPIRATION_OFFSET = 365*24*60  # minutes
REFRESH_TOKEN_EXPIRATION_OFFSET = 15  # days

ITEMS_PER_PAGE = 10

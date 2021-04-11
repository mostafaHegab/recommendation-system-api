from flask import Flask, send_from_directory

from blueprints.auth_blueprint import auth
from blueprints.products_blueprint import products
from blueprints.comments_blueprint import comments
from blueprints.user_blueprint import user
from blueprints.ratings_blueprint import ratings

from models.db import DB
from utils.mailer import Mailer
from utils.config import MAIL_CONFIG

app = Flask(__name__, static_url_path='')

app.register_blueprint(auth, url_prefix='/api/auth')
app.register_blueprint(products, url_prefix='/api/products')
app.register_blueprint(comments, url_prefix='/api/comments')
app.register_blueprint(user, url_prefix='/api/user')
app.register_blueprint(ratings, url_prefix='/api/ratings')


@app.route('/')
def index():
    return 'Hello CSE 2021 Graduation Project'


@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)


app.config['MAIL_SERVER'] = MAIL_CONFIG['server']
app.config['MAIL_PORT'] = MAIL_CONFIG['port']
app.config['MAIL_USERNAME'] = MAIL_CONFIG['username']
app.config['MAIL_PASSWORD'] = MAIL_CONFIG['password']
app.config['MAIL_USE_TLS'] = MAIL_CONFIG['tls']
app.config['MAIL_USE_SSL'] = MAIL_CONFIG['ssl']

if __name__ == "__main__":
    DB()
    # Mailer(app)
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)

from flask import Flask

from blueprints.auth import auth
from blueprints.places import places
from blueprints.comments import comments
from blueprints.user import user

from models.db import DB

app = Flask(__name__)

app.register_blueprint(auth, url_prefix='/api/auth')
app.register_blueprint(places, url_prefix='/api/places')
app.register_blueprint(comments, url_prefix='/api/comments')
app.register_blueprint(user, url_prefix='/api/user')


if __name__ == "__main__":
    DB()
    # DB.create_tables()
    # DB.init_data()
    app.run(port=3000, debug=True)

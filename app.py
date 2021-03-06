import os
import hashlib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt import JWT

basedir = os.path.abspath(os.path.dirname(__file__))
TEMPLATES = os.path.join(basedir, "static")
STATIC = os.path.join(basedir, "static/dist")

app = Flask(__name__, static_folder=STATIC, template_folder=TEMPLATES)
app.config.from_object('petals_mis.config.DevConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from petals_mis.models.models import User


def authenticate(username, password):
    user = db.session.query(User).filter(User.username == username).first()
    if user and user.password == hashlib.md5(password).hexdigest():
        return user


def identity(payload):
    user_id = payload['identity']
    user = db.session.query(User).filter(User.id == user_id).first()
    return user

CORS(app)

jwt = JWT(app, authenticate, identity)


from petals_mis.controllers.apis import export_api_list

for api in export_api_list:
    api_url = api.__name__.lower().split("api")[0]
    api_name = api.__name__.lower()
    print api_name, " -> ", "/{}".format(api_url)
    view = api.as_view("{}".format(api_name))
    app.add_url_rule(
        "/{}".format(api_url),
        view_func=view)

from petals_mis.views.index import index_view

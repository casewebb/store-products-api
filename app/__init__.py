import flask
from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager, UserMixin

from app.config import Config
from datetime import date


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


app = flask.Flask(__name__)
CORS(app)
app.json_encoder = CustomJSONEncoder

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    admin = {"admin": ("admin", "password")}

    def __init__(self, username, password):
        self.id = username
        self.password = password

    @classmethod
    def get(cls, id):
        return cls.admin.get(id)


@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    user_entry = User.get("admin")
    user = User(user_entry[0], user_entry[1])

    if user.password == token:
        return user
    return None


app.config.from_object(Config())
db = SQLAlchemy(app)

from app.db_models.models import Category, Product
migrate = Migrate(app, db)
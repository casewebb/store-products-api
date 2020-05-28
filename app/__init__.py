import flask
from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
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

app.config.from_object(Config())

db = SQLAlchemy(app)
from app.db_models.models import Category, Product

migrate = Migrate(app, db)

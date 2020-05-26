import flask
from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
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

app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/affiliate_store'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
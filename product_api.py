from flask import jsonify, request
from app.db_models.models import Product, Category
from app import app
from app import db


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/product/all', methods=['GET'])
def api_all():
    return jsonify(Product.query.all())


@app.route('/api/v1/product/create', methods=['POST'])
def create_product():
    category = Category(name="PostTest2ndCategory")
    product = Product(title="Post Prod", description="Post Prod Desc", image_url="Post Image Url", link="Post link")
    product.categories.append(category)
    db.session.add(product)
    db.session.commit()


@app.route('/api/v1/product/update', methods=['PUT'])
def update_product():
    postProduct = db.session.query(Product).filter_by(title="Post Prod").first()
    category2 = Category(name="PostUpdateCategory")
    postProduct.categories.append(category2)
    db.session.commit()


db.create_all()
app.run()
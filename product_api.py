from flask import jsonify, request
from app.db_models.models import Product, Category
from sqlalchemy import exc
from app import app
from app import db
from app.exceptions.SqlException import SqlException

# Get all products
@app.route('/api/v1/product/all', methods=['GET'])
def api_all():
    return jsonify(Product.query.all())


@app.route('/api/v1/product/create', methods=['POST'])
def create_product():
    data = request.get_json()

    categories = data['product_categories']
    product = Product(product_title=data["product_title"],
                      product_description=data["product_description"],
                      product_image_url=data["product_image_url"],
                      product_link=data["product_link"],
                      product_price=data["product_price"],
                      product_gender=data['product_gender'])

    for _category in categories:
        existing_cat = db.session.query(Category).filter_by(category_name=_category).first()
        if existing_cat is None:
            category = Category(category_name=_category)
        else:
            category = existing_cat
        product.product_categories.append(category)

    db.session.add(product)
    try:
        db.session.commit()
        db.session.refresh(product)
        return str(product.product_id)
    except exc.SQLAlchemyError:
        db.session.rollback()
        raise SqlException('Internal API Error', 500)


@app.route('/api/v1/product/update', methods=['PUT'])
def update_product():
    post_product = db.session.query(Product).filter_by(product_id=request.args.get("product_id")).first()
    category2 = Category(category_name="PostUpdateCategory")
    post_product.categories.append(category2)
    db.session.commit()


@app.errorhandler(SqlException)
def handle_db_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

db.create_all()
app.run()
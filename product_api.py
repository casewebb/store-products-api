from flask import jsonify, request
from sqlalchemy import exc

from app import app
from app import db
from app.db_models.models import Product, Category
from app.exceptions.SqlException import SqlException


# Get all products
@app.route('/api/v1/product/all')
def get_all_products():
    results = db.session.query(Product).all()
    return jsonify(results)


@app.route('/api/v1/product/category/<category>')
def get_products_by_category(category):
    results = Product.query.filter(Product.product_categories.any(Category.category_name == category)).all()
    return jsonify(results)


@app.route('/api/v1/product/create', methods=['POST'])
def create_product():
    data = request.get_json()

    categories = data['product_categories']
    product = Product(product_title=data["product_title"],
                      product_description=data["product_description"],
                      product_image_url=data["product_image_url"],
                      product_image_alt=data["product_image_alt"],
                      product_link=data["product_link"],
                      product_price=data["product_price"])

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
        return {'product_id': str(product.product_id), 'product_title': str(product.product_title)}
    except exc.SQLAlchemyError:
        db.session.rollback()
        raise SqlException('Internal API Error', 500)


@app.route('/api/v1/product/bulk/create', methods=['POST'])
def bulk_create_products():
    products_created = []
    data = request.get_json()

    for product in data:
        categories = product['product_categories']
        product = Product(product_title=product["product_title"],
                          product_description=product["product_description"],
                          product_image_url=product["product_image_url"],
                          product_image_alt=product["product_image_alt"],
                          product_link=product["product_link"],
                          product_price=product["product_price"])

        for _category in categories:
            existing_cat = db.session.query(Category).filter_by(category_name=_category).first()
            if existing_cat is None:
                category = Category(category_name=_category)
            else:
                category = existing_cat
            product.product_categories.append(category)

        db.session.add(product)
        try:
            db.session.flush()
            db.session.refresh(product)
            products_created.append({'product_id': str(product.product_id), 'product_title': product.product_title})
        except exc.SQLAlchemyError:
            db.session.rollback()
            raise SqlException('Internal API Error', 500)
    try:
        db.session.commit()
        return {'products': products_created}
    except exc.SQLAlchemyError:
        db.session.rollback()
        raise SqlException('Internal API Error', 500)


@app.route('/api/v1/product/update', methods=['PUT'])
def update_product():
    data = request.get_json()
    post_product = db.session.query(Product).filter_by(product_id=data['product_id']).first()
    post_product.update(data)
    try:
        db.session.commit()
        db.session.refresh(post_product)
        return {'product_title': str(post_product.product_title), 'updated_date': str(post_product.updated_date)}
    except exc.SQLAlchemyError:
        db.session.rollback()
        raise SqlException('Internal API Error', 500)


@app.errorhandler(SqlException)
def handle_db_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


app.run()

from flask import jsonify, request
from flask_login import login_required
from sqlalchemy import exc
from sqlalchemy import or_

from app import app
from app import db
from app.db_models.models import Product, Category
from app.exceptions.SqlException import SqlException


# Get all products
# @app.route('/api/v1/product/all')
# def get_all_products():
#     results = db.session.query(Product).all()
#     return jsonify(results)


# @app.route('/api/v1/product/all/<page>')
# def get_paginated_products(page):
#     results = db.session.query(Product).order_by(Product.created_date.desc()).paginate(int(page), 15, False)
#     total_products = int(results.total)
#     return {'total_products': total_products, 'products': results.items}


@app.route('/api/v1/product/all/<page>')
def get_paginated_products(page):
    offset = int(page) * 15 - 15
    results = db.session.execute("SELECT * FROM affiliate_store.product ORDER BY RAND(ROUND(UNIX_TIMESTAMP(), -3)) "
                                 "LIMIT :offset,15;",
                                 {'offset': offset})

    total_products = db.session.execute("SELECT COUNT(*) as count FROM affiliate_store.product;").fetchone()['count']

    data = []
    info = results.keys()
    for row in results:
        line = {}
        for i, col in enumerate(row):
            line[info[i]] = col
        data.append(line)

    return {'total_products': total_products, 'products': data}


@app.route('/api/v1/product/category/<category>')
def get_products_by_category(category):
    results = Product.query \
        .filter(Product.product_categories.any(Category.category_name == category)) \
        .all()
    return jsonify(results)


@app.route('/api/v1/product/filter')
def get_products_by_filter():
    search_term = request.args.get('searchTerm')
    price_min = request.args.get('minPrice')
    price_max = request.args.get('maxPrice')
    page = request.args.get('page')

    results = Product.query
    # Search Term
    if search_term:
        results = results.filter(or_(Product.product_title.like('%' + search_term + '%'),
                                     Product.product_description.like('%' + search_term + '%')))

    # Price Range Filter
    if price_min and is_float(price_min) and float(price_min) > 0:
        results = results.filter(Product.product_price >= float(price_min))
    else:
        price_min = 0

    if price_max and is_float(price_max) and float(price_max) > float(price_min):
        results = results.filter(Product.product_price <= float(price_max))

    # Sorting and pagination
    results = results.order_by(Product.created_date.desc())
    results = results.paginate(int(page), 15, False)

    total_products = int(results.total)
    return {'total_products': total_products, 'products': results.items}


@app.route('/api/v1/product/create', methods=['POST'])
@login_required
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
@login_required
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
@login_required
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


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    app.run(host='0.0.0.0')

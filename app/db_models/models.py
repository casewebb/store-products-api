from dataclasses import dataclass

from app import db


product_category = db.Table('product_category', db.Column('category_id', db.Integer, db.ForeignKey('category.category_id')),
                            db.Column('product_id', db.Integer, db.ForeignKey('product.product_id')))


@dataclass
class Product(db.Model):
    _id: int
    title: str
    description: str
    image_url: str
    link: str
    categories: str

    _id = db.Column("product_id", db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    description = db.Column(db.String(150))
    image_url = db.Column(db.String(1000))
    link = db.Column(db.String(1000))
    categories = db.relationship("Category", secondary=product_category)


@dataclass
class Category(db.Model):
    _id: int
    name: str
    #products: str

    _id = db.Column("category_id", db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    #products = db.relationship("Product", secondary=product_category)

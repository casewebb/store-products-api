from dataclasses import dataclass
from datetime import datetime

from app import db


product_category = db.Table('product_category', db.Column('category_id', db.Integer, db.ForeignKey('category.category_id')),
                            db.Column('product_id', db.Integer, db.ForeignKey('product.product_id')))


@dataclass
class Product(db.Model):
    product_id: int
    product_title: str
    product_description: str
    product_image_url: str
    product_link: str
    product_price: float
    product_gender: int
    product_categories: str
    created_date: datetime
    updated_date: datetime

    product_id = db.Column("product_id", db.Integer, primary_key=True)
    product_title = db.Column(db.String(50), nullable=False)
    product_description = db.Column(db.String(150), nullable=False)
    product_image_url = db.Column(db.String(1000), nullable=False)
    product_link = db.Column(db.String(1000), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    product_gender = db.Column(db.Integer, nullable=False)  # Male=0, Female=1, Both=2
    product_categories = db.relationship("Category", secondary=product_category)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, onupdate=datetime.utcnow)

@dataclass
class Category(db.Model):
    category_id: int
    category_name: str

    category_id = db.Column("category_id", db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=True)

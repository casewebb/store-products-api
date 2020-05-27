from dataclasses import dataclass
from datetime import datetime

from app import db

product_category = db.Table('product_category',
                            db.Column('category_id', db.Integer, db.ForeignKey('category.category_id')),
                            db.Column('product_id', db.Integer, db.ForeignKey('product.product_id')))


@dataclass
class Product(db.Model):
    product_id: int
    product_title: str
    product_description: str
    product_image_url: str
    product_image_alt: str
    product_link: str
    product_price: float
    product_gender: int
    product_categories: str
    created_date: datetime
    updated_date: datetime

    product_id = db.Column("product_id", db.Integer, primary_key=True)
    product_title = db.Column(db.String(30), nullable=False)
    product_description = db.Column(db.String(190), nullable=False)
    product_image_url = db.Column(db.String(1000), nullable=False)
    product_image_alt = db.Column(db.String(100), nullable=False)
    product_link = db.Column(db.String(1000), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    product_gender = db.Column(db.Integer, nullable=False)  # Male=0, Female=1, Both=2
    product_categories = db.relationship("Category", secondary=product_category)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def update(self, updated_product):

        # Setting new Attributes
        updated_prod_attrs = [a for a in updated_product if not a.startswith('__')]
        for key in updated_prod_attrs:
            try:
                if getattr(self, key) != updated_product[key] \
                        and key != 'product_id'\
                        and key != 'product_categories':
                    setattr(self, key, updated_product[key])
            except AttributeError:
                pass

        updated_categories = updated_product['product_categories']
        # Remove deleted categories
        for _category in self.product_categories:
            if _category.category_name not in updated_categories:
                category_to_remove = db.session.query(Category).filter_by(category_id=_category.category_id).first()
                self.product_categories.remove(category_to_remove)

        # Add new categories
        for _category in updated_categories:
            existing_category = db.session.query(Category).filter_by(category_name=_category).first()
            if existing_category is None:
                category = Category(category_name=_category)
            else:
                category = existing_category
            self.product_categories.append(category)

@dataclass
class Category(db.Model):
    category_id: int
    category_name: str

    category_id = db.Column("category_id", db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=True)

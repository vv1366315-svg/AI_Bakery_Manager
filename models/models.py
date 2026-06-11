from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Product(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    stock = db.Column(
        db.Integer,
        nullable=False
    )

    sales = db.relationship(
        "Sale",
        backref="product",
        lazy=True
    )
    
class Inventory(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    movement_type = db.Column(
        db.String(20),
        nullable=False
    )
    
class Sale(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    total_price = db.Column(
        db.Float,
        nullable=False
    )

    sale_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    
    
class Recipe(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    ingredients = db.Column(db.Text)

    ingredient_cost = db.Column(
        db.Float,
        default=0
    )

    packaging_cost = db.Column(
        db.Float,
        default=0
    )

    labour_cost = db.Column(
        db.Float,
        default=0
    )

    electricity_cost = db.Column(
        db.Float,
        default=0
    )

    selling_price = db.Column(
        db.Float,
        default=0
    )

    @property
    def total_cost(self):
        return (
            self.ingredient_cost +
            self.packaging_cost +
            self.labour_cost +
            self.electricity_cost
        )

    @property
    def profit(self):
        return self.selling_price - self.total_cost

    @property
    def margin(self):
        if self.selling_price == 0:
            return 0

        return (
            self.profit /
            self.selling_price
        ) * 100
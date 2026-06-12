from app import db

class Inventory(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    ingredient = db.Column(db.String(100), nullable=False)

    quantity = db.Column(db.String(50), nullable=False)
from app import db

class Sale(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    product = db.Column(db.String(100), nullable=False)

    amount = db.Column(db.Float, nullable=False)
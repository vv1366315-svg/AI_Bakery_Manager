from app import app
from models.models import db, User, Product
from app import bcrypt

with app.app_context():

    db.create_all()

    if not User.query.first():

        hashed = bcrypt.generate_password_hash("admin123").decode('utf-8')

        user = User(name="Admin", email="admin@bakery.com", password=hashed)
        db.session.add(user)

        p1 = Product(name="Chocolate Cake", price=250, stock=10)
        p2 = Product(name="Cupcake", price=50, stock=30)

        db.session.add_all([p1, p2])
        db.session.commit()

        print("Sample data inserted!")
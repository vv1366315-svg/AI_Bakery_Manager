from flask import Flask, render_template, request, redirect, url_for, session
from config import Config
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from sqlalchemy import func

app = Flask(__name__)
app.config.from_object(Config)
app.config["SECRET_KEY"] = "your_secret_key_here"

from models.models import db, User, Product, Inventory, Sale,  Recipe

db.init_app(app)
bcrypt = Bcrypt(app)





# -------------------- ROUTES --------------------

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    products = Product.query.all()
    sales = Sale.query.all()

    total_products = len(products)

    total_stock = sum(
        product.stock
        for product in products
    )

    total_sales = sum(
        sale.total_price
        for sale in sales
    )

    total_orders = len(sales)

    low_stock_products = Product.query.filter(
        Product.stock <= 5
    ).all()

    recent_sales = Sale.query.order_by(
        Sale.sale_date.desc()
    ).limit(5).all()
    
    top_products = db.session.query(
    Product.name,
    func.sum(Sale.quantity).label("total_sold")
).join(
    Sale,
    Product.id == Sale.product_id
).group_by(
    Product.id,
    Product.name
).order_by(
    func.sum(Sale.quantity).desc()
).limit(5).all()

    # Last 7 days sales data

    week_labels = []
    week_sales = []

    for i in range(6, -1, -1):

        day = datetime.utcnow().date() - timedelta(days=i)

        sales_for_day = Sale.query.filter(
            db.func.date(Sale.sale_date) == day
        ).all()

        total_day_sales = sum(
            sale.total_price
            for sale in sales_for_day
        )

        week_labels.append(
            day.strftime("%a")
        )

        week_sales.append(
            total_day_sales
        )

    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_stock=total_stock,
        total_sales=total_sales,
        total_orders=total_orders,
        low_stock_products=low_stock_products,
        recent_sales=recent_sales,
        week_labels=week_labels,
        week_sales=week_sales,
        top_products=top_products
    )

@app.route("/products")
def products():

    if "user" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search", "")

    products = Product.query.filter(
        Product.name.contains(search)
    ).all()

    return render_template(
        "products.html",
        products=products,
        search=search
    )
@app.route("/add-product", methods=["POST"])
def add_product():

    if "user" not in session:
        return redirect(url_for("login"))

    name = request.form["name"]
    price = float(request.form["price"])
    stock = int(request.form["stock"])

    new_product = Product(
        name=name,
        price=price,
        stock=stock
    )

    db.session.add(new_product)
    db.session.commit()

    return redirect(url_for("products"))

@app.route("/edit-product/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    if "user" not in session:
        return redirect(url_for("login"))

    product = Product.query.get_or_404(id)

    if request.method == "POST":

        product.name = request.form["name"]
        product.price = float(request.form["price"])
        product.stock = int(request.form["stock"])

        db.session.commit()

        return redirect(url_for("products"))

    return render_template(
        "edit_product.html",
        product=product
    )

@app.route("/delete-product/<int:id>")
def delete_product(id):

    if "user" not in session:
        return redirect(url_for("login"))

    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    return redirect(url_for("products"))

@app.route("/inventory")
def inventory():

    if "user" not in session:
        return redirect(url_for("login"))

    products = Product.query.all()

    return render_template(
        "inventory.html",
        products=products
    )


@app.route("/sales")
def sales():

    if "user" not in session:
        return redirect(url_for("login"))

    products = Product.query.all()

    sales = Sale.query.all()

    return render_template(
        "sales.html",
        products=products,
        sales=sales
    )
    
@app.route("/record-sale", methods=["POST"])
def record_sale():

    if "user" not in session:
        return redirect(url_for("login"))

    product_id = int(request.form["product_id"])
    quantity = int(request.form["quantity"])

    product = Product.query.get_or_404(product_id)

    if quantity > product.stock:
        return "Not enough stock available!"

    total_price = product.price * quantity

    new_sale = Sale(
        product_id=product.id,
        quantity=quantity,
        total_price=total_price
    )

    product.stock -= quantity

    db.session.add(new_sale)
    db.session.commit()

    return redirect(url_for("sales"))


@app.route("/recipes")
def recipes():

    if "user" not in session:
        return redirect(url_for("login"))

    all_recipes = Recipe.query.all()

    return render_template(
        "recipes.html",
        recipes=all_recipes
    )
    
@app.route("/add-recipe", methods=["POST"])
def add_recipe():

    recipe = Recipe(
        name=request.form["name"],
        ingredients=request.form["ingredients"],

        ingredient_cost=float(
            request.form["ingredient_cost"]
        ),

        packaging_cost=float(
            request.form["packaging_cost"]
        ),

        labour_cost=float(
            request.form["labour_cost"]
        ),

        electricity_cost=float(
            request.form["electricity_cost"]
        ),

        selling_price=float(
            request.form["selling_price"]
        )
    )

    db.session.add(recipe)
    db.session.commit()

    return redirect(url_for("recipes"))

@app.route("/delete-recipe/<int:id>")
def delete_recipe(id):

    recipe = Recipe.query.get_or_404(id)

    db.session.delete(recipe)
    db.session.commit()

    return redirect(url_for("recipes"))

@app.route("/edit-recipe/<int:id>", methods=["GET", "POST"])
def edit_recipe(id):

    recipe = Recipe.query.get_or_404(id)

    if request.method == "POST":

        recipe.name = request.form["name"]

        recipe.ingredients = request.form["ingredients"]

        recipe.ingredient_cost = float(
            request.form["ingredient_cost"]
        )

        recipe.packaging_cost = float(
            request.form["packaging_cost"]
        )

        recipe.labour_cost = float(
            request.form["labour_cost"]
        )

        recipe.electricity_cost = float(
            request.form["electricity_cost"]
        )

        recipe.selling_price = float(
            request.form["selling_price"]
        )

        db.session.commit()

        return redirect(url_for("recipes"))

    return render_template(
        "edit_recipe.html",
        recipe=recipe
    )

@app.route("/prediction")
def prediction():
    return render_template("prediction.html")


@app.route("/invoice")
def invoice():
    return render_template("invoice.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip()
        password = request.form["password"].strip()

        user = User.query.filter_by(email=email).first()

        if user:
            if bcrypt.check_password_hash(
                user.password,
                password
            ):
                session["user"] = user.email
                return redirect(url_for("dashboard"))

        return "<h3>Invalid credentials ❌</h3>"

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "<h2>Email already registered!</h2>"

        hashed_password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        new_user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

# -------------------- RESET DB (ADD HERE) --------------------
@app.route("/reset-db")
def reset_db():
    db.drop_all()
    db.create_all()
    return "Database reset done ✅"


# -------------------- TEST --------------------
@app.route("/test")
def test():
    return "Flask is using the correct app!"
if __name__ == "__main__":
    app.run(debug=True)

with app.app_context():
    db.create_all()
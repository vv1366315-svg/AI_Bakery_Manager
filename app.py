from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/inventory")
def inventory():
    return render_template("inventory.html")

@app.route("/sales")
def sales():
    return render_template("sales.html")

@app.route("/recipes")
def recipes():
    return render_template("recipes.html")

@app.route("/prediction")
def prediction():
    return render_template("prediction.html")

@app.route("/invoice")
def invoice():
    return render_template("invoice.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/test")
def test():
    return "Flask is using the correct app.py!"

if __name__ == "__main__":
    app.run(debug=True)
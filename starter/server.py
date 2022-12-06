from flask import Flask, render_template, redirect, flash, request, session
import melons
import jinja2

app = Flask(__name__)
app.jinja_env.undefined = jinja2.StrictUndefined  # for debugging purposes
app.secret_key = "dev"

### Flask Routes go here. ###
@app.route("/")
def homepage():
    return render_template("base.html")


@app.route("/melons")
def all_melons():
    """Return a page listing all the melons available for purchase."""

    melon_list = melons.get_all()
    return render_template("all-melons.html", melon_list=melon_list)


@app.route("/melon/<melon_id>")
def melon_details(melon_id):
    """Return a page showing all info about a melon. Also, provide a button to buy that melon."""

    melon = melons.get_by_id(melon_id)
    return render_template("melon-details.html", melon=melon)


@app.route("/add-to-cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to the cart and redirect to the shopping cart page."""

    if "cart" not in session:
        session["cart"] = {}
    cart = session["cart"]  # store cart in local variable to make things easier

    cart[melon_id] = cart.get(melon_id, 0) + 1
    session.modified = True
    flash(f"Melon {melon_id} successfully added to cart.")
    print(cart)

    return redirect("/cart")


@app.route("/cart")
def show_shopping_cart():
    """Display contents of shopping cart."""

    order_total = 0
    cart_melons = []

    # Get cart dict from session (or an empty one if none exists yet)
    cart = session.get("cart", {})

    for melon_id, quantity in cart.items():
        melon = melons.get_by_id(melon_id)

        # Calculate total cost for this type of melon and add to order total
        total_cost = quantity * melon.price
        order_total += total_cost

        # Add the quantity and total cost as attributes on the Melon object
        melon.quantity = quantity
        melon.total_cost = total_cost

        cart_melons.append(melon)

    return render_template(
        "cart.html", cart_melons=cart_melons, order_total=order_total
    )


if __name__ == "__main__":
    app.env = "development"
    app.run(debug=True, port=8000, host="localhost")

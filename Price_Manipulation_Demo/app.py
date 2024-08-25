from flask import Flask, render_template, request, redirect, url_for, session, flash
from markupsafe import  Markup, escape
import db
import utils
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address

app = Flask(__name__)
connection = db.connect_to_database()
app.secret_key = "SUPER-SECRET"
# limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["50 per minute"], storage_uri="memory://")
app.config['SESSION_COOKIE_HTTPONLY'] = False

PRODUCTS = [
    {'id': 1, 'name': 'Laptop', 'price': 1000},
    {'id': 2, 'name': 'Smartphone', 'price': 500},
    {'id': 3, 'name': 'Headphones', 'price': 150},
]

@app.route('/')
def index():
    return render_template('index.html', products=PRODUCTS)


@app.route('/login', methods=['GET', 'POST'])
# @limiter.limit("10 per minute")
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.get_user(connection, username)

        if user:
            if utils.is_password_match(password, user[2]):
                session['username'] = user[1]
                session['user_id'] = user[0]
                return redirect(url_for('index'))
            else:
                flash("Invalid username or password", "danger")
                return render_template('login.html')

        else:
            flash("Invalid username or password", "danger")
            return render_template('login.html')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
# @limiter.limit("10 per minute")
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not utils.is_strong_password(password):
            flash("Sorry You Entered a weak Password Please Choose a stronger one", "danger")
            return render_template('register.html')

        user = db.get_user(connection, username)
        if user:
            flash("Username already exists. Please choose a different username.", "danger")
            return render_template('register.html')
        else:
            db.add_user(connection, username, password)
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

#--------------------------------------------------------------Session 4-------------------------------------------------------------#
@app.route('/CheckStock')
def Check_Stock():
    server = request.args.get("server")
    return redirect(server)
#------------------------------------------------------------------------------------------------------------------------------------#
@app.route('/search', methods=['GET', 'POST'])
def search():
    search_query = Markup(request.args.get('search_query'))
    usernames = db.search_users(connection, search_query)
    return render_template('search_results.html', usernames=usernames, search_query=search_query)


@app.route('/comments', methods=['GET', 'POST'])
def addComment():
    comments = db.get_comments(connection)

    if request.method == 'POST':
        text = Markup(request.form['comment'])
        username = session.get('username')
        if username:
            db.add_comment(connection, username, text)
            comments = db.get_comments(connection)
        else:
            flash("You must be logged in to post a comment.", "warning")

    return render_template('comments.html', comments=comments)

@app.route('/clear_comments', methods=['GET','POST'])
def clearComments():
    db.clear_comments(connection)
    return redirect(url_for('addComment'))
#--------------------------------------------------------------------------------------------------------------------------------

@app.route('/add_to_cart')
def add_to_cart():
    product_id = request.args.get('product_id')
    product_name = request.args.get('product_name')
    price = request.args.get('price')

    # Check if user is logged in
    if 'username' not in session:
        flash("You must be logged in to add items to your cart.", "warning")
        return redirect(url_for('login'))

    if not product_id or not price:
        flash("Invalid product or price.", "danger")
        return redirect(url_for('index'))

    # Store cart information in the session
    cart = session.get('cart', [])
    cart.append({'product_id': product_id, 'prodcut_name': product_name, 'price': price, 'quantity': 1})
    session['cart'] = cart

    flash(f"Added product {product_id} with price {price} to your cart.", "success")
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    
    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart)

@app.route('/checkout')
def checkout():
    product_id = request.args.get('product_id')
    name = request.args.get('name')
    price = request.args.get('price')

    real_price = utils.get_product_by_id(PRODUCTS, product_id).get('price')
    session['Correct_MAC'] = utils.create_mac(real_price)
    
    return render_template('checkout.html', product_id=product_id, name=name, price=price)

@app.route('/confirm_purchase', methods=['POST'])
def confirm_purchase():
    product_id = request.form['product_id']
    name = request.form['name']
    price = request.form['price']
    Possible_Correct_MAC = utils.create_mac(price)

    if 'Correct_MAC' in session and session['Correct_MAC'] == Possible_Correct_MAC:
        return f"Purchase confirmed at price ${price}."
    else:
        return f"Purchase Failed, Please Try Again"
if __name__ == '__main__':
    db.init_db(connection)
    db.init_comments_table(connection)
    db.seed_admin_user(connection)
    

    app.run(debug=True)


""" @app.route('/confirm_purchase', methods=['POST'])
def confirm_purchase():
    product_id = request.form['product_id']
    name = request.form['name']
    price = request.form['price']
    Possible_Correct_MAC = utils.create_mac(name,price)

    if Correct_MAC == Possible_Correct_MAC:
        return f"Purchase confirmed for {name} (ID: {product_id}) at price ${price}."
    else:
        return f"Purshase Failed for {name} (ID: {product_id}), Please Try Again" """
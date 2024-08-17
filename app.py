from flask import Flask, render_template, request, redirect, url_for, session, flash
import db
import utils
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
connection = db.connect_to_database()
app.secret_key = "SUPER-SECRET"
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=[
                  "50 per minute"], storage_uri="memory://")


@app.route('/')
def index():
    if 'username' in session:
        if session['username'] == 'admin':
            return list(db.get_all_users(connection))
        else:
            return f"Welcome, {session['username']}!"
    return "You are not logged in."


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.get_user(connection, username)

        if user:
            if utils.is_password_match(password, user[2]):
                session['username'] = user[1]
                return redirect(url_for('index'))
            else:
                flash("Invalid username or password", "danger")
                return render_template('login.html')

        else:
            flash("Invalid username or password", "danger")
            return render_template('login.html')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not utils.is_strong_password(password):
            flash(
                "Sorry You Entered a weak Password Please Choose a stronger one", "danger")
            return render_template('register.html')

        user = db.get_user(connection, username)
        if user:
            flash(
                "Username already exists. Please choose a different username.", "danger")
            return render_template('register.html')
        else:
            db.add_user(connection, username, password)
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']
        usernames = db.search_users(connection, search_query)
        print(usernames)
        return render_template('search_results.html', usernames=usernames)
    return render_template('search.html')


if __name__ == '__main__':
    db.init_db(connection)
    db.seed_admin_user(connection)
    app.run(debug=True)

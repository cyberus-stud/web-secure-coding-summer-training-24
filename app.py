from flask import Flask, render_template, request, redirect, url_for, session, flash, Markup, escape, abort
from urllib.parse import urlparse
import db
import utils
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
connection = db.connect_to_database()
app.secret_key = "SUPER-SECRET"
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["50 per minute"], storage_uri="memory://")
app.config['SESSION_COOKIE_HTTPONLY'] = False

@app.route('/')
def index():
    if 'username' in session:
        escaped_username = escape(session['username'])  # Escape the username
        if escaped_username == 'admin':
            return list(db.get_all_users(connection))
        else:
            return f"Welcome, {escaped_username}!"  # Safely render the username
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
@limiter.limit("10 per minute")
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
def is_valid_url(server):
    parsed_url = urlparse(server)
    if parsed_url.scheme not in ['http', 'https']:  # lazm http aw https
        return False
    #only allow port 5000
    whitelist = [5000]
    return parsed_url.port in whitelist


@app.route('/CheckStock')
def Check_Stock():
    server = request.args.get("server")
    #third
    if not is_valid_url(server):
        abort(400, "Invalid URL")

    return redirect(server)
#------------------------------------------------------------------------------------------------------------------------------------#
@app.route('/search', methods=['GET', 'POST'])
def search():
    search_query = escape(request.args.get('search_query'))
    usernames = db.search_users(connection, search_query)
    return render_template('search_results.html', usernames=usernames, search_query=search_query)


@app.route('/comments', methods=['GET', 'POST'])
def addComment():
    comments = db.get_comments(connection)

    if request.method == 'POST':
        text = escape(request.form['comment'])
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
if __name__ == '__main__':
    db.init_db(connection)
    db.init_comments_table(connection)
    db.seed_admin_user(connection)
    app.run(debug=True)

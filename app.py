from flask import Flask, render_template, request, redirect, url_for, session, flash
import db

app = Flask(__name__)
connection = db.connect_to_database()
app.secret_key = "SUPER-SECRET"


@app.route('/')
def index():
    if 'username' in session:
        return f'''
                <h1>Hello, {session['username']}</h1>
                <a href="/logout">Logout</a>
                <a href="/search">Search</a>
                '''
    return '''
            <p>Please login or register</p>
            <a href="/login">Login</a>
            <a href="/register">Register</a>
            '''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.get_user(connection, username, password)

        if user:
            session['username'] = user[1]
            return redirect(url_for('index'))
        else:
            flash("Wrong Cardinals", "danger")
            return render_template('login.html')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.get_user_by_username(connection, username)
        if user:
            return "Username already exists. Please choose a different username."
        else:
            db.add_user(connection, username, password)
            return redirect(url_for('login'))
    # flash("Test", "success")
    return render_template('register.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']
        usernames = db.search_users(connection, search_query)
        print(usernames)
        return render_template('search_results.html', usernames=usernames)
    return render_template('search.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.init_db(connection)
    app.run(debug=True)

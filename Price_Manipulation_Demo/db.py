import utils


def connect_to_database(name='database.db'):
    import sqlite3
    return sqlite3.connect(name, check_same_thread=False)


def init_db(connection):
    cursor = connection.cursor()

    cursor.execute('''
		CREATE TABLE IF NOT EXISTS users (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT NOT NULL UNIQUE,
			password TEXT NOT NULL
		)
	''')
    cursor.execute('''
		CREATE TABLE IF NOT EXISTS gadgets (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL,
			price INTEGER NOT NULL
		)
	''')
    connection.commit()


def add_user(connection, username, password):
    cursor = connection.cursor()
    hashed_password = utils.hash_password(password)
    query = '''INSERT INTO users (username, password) VALUES (?, ?)'''
    cursor.execute(query, (username, hashed_password))
    connection.commit()


def get_user(connection, username):
    cursor = connection.cursor()
    query = '''SELECT * FROM users WHERE username = ?'''
    cursor.execute(query, (username,))
    return cursor.fetchone()


def get_all_users(connection):
    cursor = connection.cursor()
    query = 'SELECT * FROM users'
    cursor.execute(query)
    return cursor.fetchall()


def seed_admin_user(connection):
    admin_username = 'admin'
    admin_password = 'admin'

    # Check if admin user exists
    admin_user = get_user(connection, admin_username)
    if not admin_user:
        add_user(connection, admin_username, admin_password)
        print("Admin user seeded successfully.")


def search_users(connection, search_query):
    cursor = connection.cursor()
    query = '''SELECT username FROM users WHERE username LIKE ?'''
    cursor.execute(query, (f"%{search_query}%",))
    return cursor.fetchall()


def init_comments_table(connection):
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            text TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    connection.commit()

def add_comment(connection, username, text):
    cursor = connection.cursor()
    query = '''INSERT INTO comments (username, text) VALUES (?, ?)'''
    cursor.execute(query, (username, text))
    connection.commit()

def get_comments(connection):
    cursor = connection.cursor()
    query = '''
        SELECT comments.username, comments.text, comments.timestamp
        FROM comments
    '''
    cursor.execute(query)
    return cursor.fetchall()

def clear_comments(connection):
    cursor = connection.cursor()
    query = '''DELETE FROM comments'''
    cursor.execute(query)
    connection.commit()

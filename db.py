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

    connection.commit()


def add_user(connection, username, password):
    cursor = connection.cursor()
    query = f'''INSERT INTO users (username, password) VALUES ('{
        username}', '{password}')'''
    cursor.execute(query)
    connection.commit()


def get_user(connection, username, password):
    cursor = connection.cursor()
    query = f'''SELECT * FROM users WHERE username = '{
        username}' AND password = '{password}' '''
    cursor.execute(query)
    return cursor.fetchone()


def get_user_by_username(connection, username):
    cursor = connection.cursor()
    query = f'''SELECT * FROM users WHERE username = '{username}' '''
    cursor.execute(query)
    return cursor.fetchone()


def search_users(connection, search_query):
    cursor = connection.cursor()
    query = f'''SELECT username FROM users WHERE username LIKE '%{
        search_query}%' '''
    cursor.execute(query)
    return cursor.fetchall()

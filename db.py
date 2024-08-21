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
			password TEXT NOT NULL,
            fname TEXT ,
            lName TEXT,
            creditCard INTEGER,
            photo_name TEXT
		)
	''')

    connection.commit()


def add_user(connection, username, password , photo_name):
    cursor = connection.cursor()
    hashed_password = utils.hash_password(password)
    query = '''INSERT INTO users (username, password , photo_name) VALUES (?, ? , ?)'''
    cursor.execute(query, (username, hashed_password , photo_name))
    connection.commit()


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

def delete_user(connection, username):
    cursor = connection.cursor()
    query = ''' DELETE FROM users WHERE username = ? '''
    cursor.execute(query, (username,)) 
    connection.commit()

def update_user(connection , user_data):
    cursor = connection.cursor()
    query = ''' UPDATE users set fname = ? , lName = ? , creditCard = ? WHERE username = ? '''
    cursor.execute(query,(user_data['fname'] , user_data['lname'] , user_data['card'] , user_data['username']))
    connection.commit() 


def update_photo(connection, filename , username):
    cursor = connection.cursor()  
    query = '''UPDATE users SET photo_name = ? WHERE username = ?'''
    cursor.execute(query, (filename,username))  
    connection.commit()  


def get_user(connection, username):
    cursor = connection.cursor()
    query = '''SELECT * FROM users WHERE username = ?'''
    cursor.execute(query, (username,))
    return cursor.fetchone()
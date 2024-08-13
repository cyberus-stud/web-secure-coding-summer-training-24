from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=('GET', 'POST'))
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']

        conn = get_db_connection()
        conn.execute(f"INSERT INTO students (name, age, grade) VALUES ('{name}', '{age}', '{grade}')")
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_student.html')

@app.route('/update/<id>', methods=('GET', 'POST'))
def update_student(id):
    conn = get_db_connection()
    student = conn.execute(f"SELECT * FROM students WHERE id = '{id}'").fetchone()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']

        conn.execute(f"UPDATE students SET name = '{name}', age = '{age}', grade = '{grade}' WHERE id = '{id}'")
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('update_student.html', student=student)

@app.route('/delete/<id>')
def delete_student(id):
    conn = get_db_connection()
    conn.execute(f"DELETE FROM students WHERE id = '{id}'")
    conn.commit()
    conn.close()
    return redirect(url_for('index'), code=300)

if __name__ == '__main__':
    app.run(debug=True)

import sqlite3


conn = sqlite3.connect('students.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    grade TEXT NOT NULL
)
''')
print("Table 'students' created successfully.")

cursor.execute('''
INSERT INTO students (name, age, grade)
VALUES ('Ibrahim', 20, 'A')
''')
cursor.execute('''
INSERT INTO students (name, age, grade)
VALUES ('Ahmed Ayman', 22, 'B')
''')
cursor.execute('''
INSERT INTO students (name, age, grade)
VALUES ('Mohamed', 21, 'A')
''')
print("Data inserted successfully.")

conn.commit()

cursor.execute('SELECT * FROM students')
rows = cursor.fetchall()

print("\nQuerying data from 'students' table:")
for row in rows:
    print(row)

cursor.execute('''
UPDATE students
SET grade = 'A+'
WHERE name = 'Ahmed Ayman'
''')
print("\nRecord updated successfully.")

cursor.execute('''
DELETE FROM students
WHERE name = 'Ibrahim'
''')
print("\nRecord deleted successfully.")

cursor.execute('SELECT * FROM students')
rows = cursor.fetchall()

print("\nFinal data in 'students' table:")
for row in rows:
    print(row)

conn.close()

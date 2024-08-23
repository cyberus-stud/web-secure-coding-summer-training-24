from flask import Flask, render_template, request, redirect, url_for
import os 
app = Flask(__name__)

# Hardcoded user data for demonstration
users = [
    {"id": 1, "username": "admin", "role": "admin"},
    {"id": 2, "username": "user1", "role": "user"},
    {"id": 3, "username": "user2", "role": "user"}
]

@app.route('/')
def index():
    return "Welcome to the vulnerable admin panel demo!"

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    global users
    command_output = ""

    if request.method == 'POST':
        if 'execute' in request.form:
            command = request.form.get('command')
            # Vulnerable command execution (Never do this in production)
            command_output = os.popen(command).read()
        elif 'delete_users' in request.form:
            # Vulnerable deletion of all users
            users = []

    return render_template('admin.html', users=users, command_output=command_output)

if __name__ == '__main__':
    app.run(debug=True)

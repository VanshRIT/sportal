from flask import Flask, render_template, request, redirect, url_for, flash
from dbconfig import *
from controller import create_user
import bcrypt  # For password hashing

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for flashing messages

# Database configuration





@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def authenticate():
    if request.method == 'POST':
        username = request.form['lusername']
        password = request.form['lpassword']

        # Authenticate the user
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            role_id = user['role_id']
            if role_id == 0:
                return redirect(url_for('teacher'))
            elif role_id == 1:
                return redirect(url_for('counsellor'))
            elif role_id == 2:
                return redirect(url_for('parent'))
            elif role_id == 4:
                return redirect(url_for('it_manager'))
        else:
            flash('Invalid username or password', 'error')

    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form)
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role_id = 4  # Set the role_id as needed

        create_user(username, password, email, role_id)
        flash('Registration successful. You can now login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)

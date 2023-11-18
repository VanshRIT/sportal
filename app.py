from flask import Flask, request, redirect, url_for,render_template
from dbconfig import *
from controller import *
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Authenticate the user
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            role_id = user['role_id']
            if role_id == 0:
                return redirect(url_for('teacher'))
            elif role_id == 1:
                return redirect(url_for('counsellor'))
            elif role_id == 2:
                return redirect(url_for('parent'))
            elif role_id == 4:
                return redirect(url_for('it_manager'))

    return render_template('login.html')

# Define other routes and logic for teacher, counsellor, parent, and it_manager routes as before

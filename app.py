from flask import Flask, render_template, session,request, redirect, url_for, flash, jsonify
from dbconfig import *
from controller import *
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
        query = "SELECT * FROM users WHERE username = %s and password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user and password:
            role_id = user['role_id']
            # Store user information in the session
            session['user_id'] = user['user_id']
            session['username'] = username
            session['role_id'] = role_id

            if role_id == 1:
                return redirect(url_for('teacher'))
            elif role_id == 2:
                return redirect(url_for('counsellor'))
            elif role_id == 3:
                return redirect(url_for('parent'))
            elif role_id == 0:
                return redirect(url_for('it_manager'))
        else:
            flash('Invalid username or password', 'error')

    return redirect(url_for('login'))



@app.route('/teacher', methods=['GET'])
def teacher():
    # Check if the user is logged in
    if 'username' in session and 'role_id' in session:
        logged_in_user = session['username']
        role_id = session['role_id']
        # You cana also access the role_id if needed: session['role_id']
        return render_template('teacher_Dash.html', username=logged_in_user)
    else:
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('login'))

@app.route('/parent', methods=['GET'])
def parent():
    # Check if the user is logged in
    if 'username' in session and 'role_id' in session:
        logged_in_user = session['username']
        role_id = session['role_id']
        # You can also access the role_id if needed: session['role_id']
        return render_template('parent_Dash.html', username=logged_in_user)
    else:
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('login'))

@app.route('/counsellor', methods=['GET'])
def counsellor():
    # Check if the user is logged in
    if 'username' in session and 'role_id' in session:
        logged_in_user = session['username']
        role_id = session['role_id']
        # You can also access the role_id if needed: session['role_id']
        return render_template('counsellor_Dash.html', username=logged_in_user)
    else:
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('login'))

@app.route('/students', methods=['GET'])
def students():
    if 'username' in session and 'role_id' in session:
        user_id = session['user_id']
        logged_in_user = session['username']
        role_id = session['role_id']
    else:
        return
    
    if role_id == 2:
        cursor.execute("SELECT * FROM counsellors WHERE user_id = %s", (user_id,))
        counsellor_details = cursor.fetchone()

        cursor.execute("SELECT * FROM students WHERE counsellor_id = %s", (counsellor_details['counsellor_id'],))
        students_list = [student['student_name'] for student in cursor.fetchall()]

        return render_template('students.html', students_list=students_list)

@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.json
    student_name = data['name']
    
    create_student(student_name, 1, 1, 1)

    return jsonify({'status': 'success'})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form)
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role_id = 3 # Set the role_id as needed

        create_user(username, password, email, role_id)
        flash('Registration successful. You can now login.', 'success')
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

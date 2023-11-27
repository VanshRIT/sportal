from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify, send_from_directory
from dbconfig import *
from controller import *
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = r'C:\Users\prana\Documents\GitHub\sportal\files_uploaded'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

    students_list = []

    if role_id == 2:
        cursor.execute(
            "SELECT * FROM counsellors WHERE user_id = %s", (user_id,))
        counsellor_details = cursor.fetchone()

        cursor.execute("SELECT * FROM students WHERE counsellor_id = %s",
                       (counsellor_details['counsellor_id'],))
        students_list = [student['student_name']
                         for student in cursor.fetchall()]

    if role_id == 1:
        cursor.execute("SELECT * FROM teachers WHERE user_id = %s", (user_id,))
        teacher_details = cursor.fetchone()

        cursor.execute("SELECT * FROM students WHERE teacher_id = %s",
                       (teacher_details['teacher_id'],))
        students_list = [student['student_name']
                         for student in cursor.fetchall()]

    if role_id == 3:
        cursor.execute("SELECT * FROM parents WHERE user_id = %s", (user_id,))
        parent_details = cursor.fetchone()

        cursor.execute("SELECT * FROM students WHERE parent_id = %s",
                       (parent_details['parent_id'],))
        students_list = [student['student_name']
                         for student in cursor.fetchall()]

    return render_template('students.html', students_list=students_list, role_id=role_id)


@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.json
    student_name = data['name']

    create_student(student_name, 1, 1, 1)

    return jsonify({'status': 'success'})


@app.route('/grades')
def grades():
    if 'username' in session and 'role_id' in session:
        user_id = session['user_id']
        logged_in_user = session['username']
        role_id = session['role_id']

    student_name = request.args.get('student', '')

    cursor.execute(
        "SELECT * FROM students WHERE student_name = %s", (student_name,))
    student_details = cursor.fetchone()

    cursor.execute("SELECT * FROM grades WHERE student_id = %s",
                   (student_details['student_id'],))
    grades_list = [(grades['subject'], grades['score'], grades['date'])
                   for grades in cursor.fetchall()]

    return render_template('grades.html', grades_list=grades_list, role_id=role_id)


@app.route('/add_grade', methods=['POST'])
def add_grade():
    data = request.json
    student_name = data['name']
    subject = data['subject']
    grade = data['grade']
    date = data['date']

    cursor.execute(
        "SELECT student_id FROM students WHERE student_name = %s", (student_name,))
    student_id = cursor.fetchone()['student_id']

    create_grade(student_id, 1, subject, grade, date)

    return jsonify({'status': 'success'})


@app.route('/tasks')
def tasks():
    if 'username' in session and 'role_id' in session:
        user_id = session['user_id']
        logged_in_user = session['username']
        role_id = session['role_id']

    student_name = request.args.get('student', '')

    cursor.execute(
        "SELECT * FROM students WHERE student_name = %s", (student_name,))
    student_details = cursor.fetchone()

    cursor.execute("SELECT * FROM tasks WHERE student_id = %s",
                   (student_details['student_id'],))
    tasks_list = [[tasks['task_description'], tasks['teacher_id'], tasks['counsellor_id'], tasks['date_created'],
                   tasks['deadline'], tasks['status'], tasks['file_path_counsellor_teacher'], tasks['file_path_parent'], tasks['task_id']] for tasks in cursor.fetchall()]

    for task in tasks_list:
        if int(task[1]) > 0:
            cursor.execute(
                "SELECT teacher_name from teachers where teacher_id = %s", (task[1],))
            task[1] = cursor.fetchone()['teacher_name']

            task.pop(2)
            continue

        if int(task[2]) > 0:
            cursor.execute(
                "SELECT counsellor_name from counsellors where counsellor_id = %s", (task[2],))
            task[2] = cursor.fetchone()['counsellor_name']

            task.pop(1)
            continue

    return render_template('tasks.html', tasks_list=tasks_list, role_id=role_id)


@app.route('/add_task', methods=['POST'])
def add_task():
    if 'username' in session and 'role_id' in session:
        user_id = session['user_id']
        logged_in_user = session['username']
        role_id = session['role_id']

    data = request.form.to_dict()

    cursor.execute(
        "SELECT student_id FROM students WHERE student_name = %s", (data['student'],))
    student_id = cursor.fetchone()['student_id']


    counsellor_id = 0
    teacher_id = 0

    if role_id == 1:
        cursor.execute(
            "SELECT teacher_id FROM teachers WHERE user_id = %s", (user_id,)
            )
        
        teacher_id = cursor.fetchone()['teacher_id']
    elif role_id == 2:
        cursor.execute(
            "SELECT counsellor_id FROM counsellors WHERE user_id = %s", (user_id,))

        counsellor_id = cursor.fetchone()['counsellor_id']

    file_path = None
      # File upload handling
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, "counsellor_teacher", filename)
            file.save(file_path)


    create_task(student_id, teacher_id, counsellor_id,
                data['task_desc'], data['status'], data['due_date'], data['assigned_date'], None, file_path)

    return jsonify({'status': 'success'})



@app.route('/submit_task', methods=['POST'])
def submit_task():
    if 'username' in session and 'role_id' in session:
        user_id = session['user_id']
        logged_in_user = session['username']
        role_id = session['role_id']

    data = request.form.to_dict()

    cursor.execute(
        "SELECT student_id FROM students WHERE student_name = %s", (data['student'],))
    student_id = cursor.fetchone()['student_id']


    counsellor_id = 0
    teacher_id = 0

    cursor.execute(
        "SELECT teacher_id FROM teachers WHERE teacher_name = %s", (data['assignedby'],)
        )
    
    record = cursor.fetchone()
    if record:
        teacher_id = record['teacher_id']

    cursor.execute(
        "SELECT counsellor_id FROM counsellors WHERE counsellor_name = %s", (data['assignedby'],))

    record = cursor.fetchone()
    if record:
        counsellor_id = record['counsellor_id']

    file_path = None
      # File upload handling
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, "parent", filename)
            file.save(file_path)

    print((student_id, teacher_id, counsellor_id, data['task_desc'], data['assignedby'], role_id))

    cursor.execute('UPDATE tasks SET status = "D" WHERE student_id = %s and teacher_id = %s and counsellor_id = %s and task_description = %s', (student_id, teacher_id, counsellor_id, data['task_desc']))
    cursor.execute('UPDATE tasks SET file_path_parent=%s WHERE student_id = %s and teacher_id = %s and counsellor_id = %s and task_description = %s', (file_path, student_id, teacher_id, counsellor_id, data['task_desc']))

    return jsonify({'status': 'success'})

@app.route('/download_file/<parent_folder>/<filename>')
def download_file(parent_folder, filename):
    directory = os.path.join(UPLOAD_FOLDER, parent_folder)
    print(directory)
    return send_from_directory(directory, filename)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form)
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role_id = 3  # Set the role_id as needed

        create_user(username, password, email, role_id)
        flash('Registration successful. You can now login.', 'success')
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

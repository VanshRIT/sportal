from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify, send_from_directory
from controller import *
import os
from werkzeug.utils import secure_filename
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from urllib import parse

app = Flask(__name__)

app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = r'C:\Users\prana\Documents\GitHub\sportal\static\files_uploaded'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'py'}


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
                return redirect(url_for('it_admin'))
        else:
            flash('Invalid username or password', 'error')

    return redirect(url_for('login'))


@app.route('/it-admin')
def it_admin():
    # Check if the user is logged in
    if 'username' in session and 'role_id' in session:
        logged_in_user = session['username']
        role_id = session['role_id']
        info = [get_totals()[0]['total_students'], get_totals()[0]['total_teachers'], get_totals()[0]['total_counsellors'], get_totals()[0]['total_parents']]

        # You cana also access the role_id if needed: session['role_id']
        return render_template('it-manager-Dash.html', username=logged_in_user,info=info)
    else:
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('login'))


@app.route('/teacher', methods=['GET'])
def teacher():
    # Check if the user is logged in
    if 'username' in session and 'role_id' in session:
        logged_in_user = session['username']
        role_id = session['role_id']
        user_id = session['user_id']
        info = [get_student_by_user_id(user_id)]
        print(info)
        # You cana also access the role_id if needed: session['role_id']
        return render_template('teacher_Dash.html', username=logged_in_user,info=info)
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

        Total_Students = get_total_students()
        Total_Tasks = get_total_tasks()
        Total_ungraded = get_total_ungraded()

        info = [Total_Students[0]["total_students"], Total_Tasks[0]["total_tasks"] , Total_ungraded[0]["total_ungraded"]]

        # You can also access the role_id if needed: session['role_id']
        return render_template('counsellor_Dash.html', username=logged_in_user,info=info)
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
    
    cursor.execute("SELECT * FROM subjects")
    
    all_subjects = {subject["subject_name"] : subject["subject_id"] for subject in cursor.fetchall()}
    id_subject_map = {v:k for k, v in all_subjects.items()}

    if role_id == 2:
        cursor.execute(
            "SELECT * FROM counsellors WHERE user_id = %s", (user_id,))
        counsellor_details = cursor.fetchone()

        cursor.execute("SELECT * FROM students WHERE counsellor_id = %s",
                       (counsellor_details['counsellor_id'],))
        
        students_list = [(student['student_name'], student["student_id"], [id_subject_map[int(i)] for i in student["weak_subjects"].split(",")])
                         for student in cursor.fetchall()]

    if role_id == 1:
        cursor.execute("SELECT * FROM teachers WHERE user_id = %s", (user_id,))
        teacher_details = cursor.fetchone()

        cursor.execute("SELECT * FROM subjects WHERE teacher_id=%s", (teacher_details['teacher_id'],))
        subjects = cursor.fetchall()

        subject_ids = [int(subject["subject_id"]) for subject in subjects]

        cursor.execute("SELECT * FROM students")

        for student in cursor.fetchall():
            weak_subjects = [int(i) for i in student["weak_subjects"].split(",")]
            
            if len(set(subject_ids).intersection(set(weak_subjects))) > 0:
                students_list.append((student["student_name"], student["student_id"], [id_subject_map[i] for i in weak_subjects]))

    if role_id == 3:
        cursor.execute("SELECT * FROM parents WHERE user_id = %s", (user_id,))
        parent_details = cursor.fetchone()

        cursor.execute("SELECT * FROM students WHERE parent_id = %s",
                       (parent_details['parent_id'],))
        
        students_list = [(student['student_name'], student["student_id"], [id_subject_map[int(i)] for i in student["weak_subjects"].split(",")])
                         for student in cursor.fetchall()]

    return render_template('Parent-Dash/view/view_student.html', students_list=students_list, role_id=role_id, all_subjects=all_subjects)

@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.json
    student_name = data['name']

    create_student(student_name, 1, 1, ",".join(map(str, data['weak_subjects'])))

    return jsonify({'status': 'success'})


@app.route('/grades')
def grades():
    if 'username' in session and 'role_id' in session:
        user_id = session['user_id']
        logged_in_user = session['username']
        role_id = session['role_id']

    student_id = request.args.get('studentid', '')

    cursor.execute("SELECT * FROM grades WHERE student_id = %s",
                   (student_id,))
    
    grades_list = []
    
    for grade in cursor.fetchall():
        cursor.execute("SELECT * FROM subjects WHERE subject_id=%s", (grade["subject_id"], ))
        grades_list.append((grade['item'], cursor.fetchone()["subject_name"], grade['score'], grade['date']))
        
    
    cursor.execute("SELECT weak_subjects FROM students where student_id=%s", (student_id,))
    weak_subjects = [int(i) for i in cursor.fetchone()["weak_subjects"].split(",")]

    
    for i, sub_id in enumerate(weak_subjects):
        cursor.execute("SELECT * FROM subjects where subject_id=%s", (sub_id,))
        weak_subjects[i] = cursor.fetchone()

    cursor.execute(
            "SELECT teacher_id FROM teachers WHERE user_id = %s", (user_id,)
        )

    teacher_id = cursor.fetchone()["teacher_id"]

    temp_weak_subjects = {}

    for sub in weak_subjects:
        if sub["teacher_id"] == teacher_id:
            temp_weak_subjects[sub["subject_name"]] = sub["subject_id"]
            
    weak_subjects = temp_weak_subjects

    return render_template('grades.html', grades_list=grades_list, role_id=role_id, weak_subjects=weak_subjects, teacher_id=teacher_id)


@app.route('/add_grade', methods=['POST'])
def add_grade():
    data = request.json
    student_id = data['studentid']
    subject_id = data['subjectid']
    item = data['item']
    grade = data['grade']
    date = data['date']
    teacher_id = data['teacherid']

    create_grade(student_id, teacher_id, subject_id, item, grade, date)

    return jsonify({'status': 'success'})


@app.route('/tasks')
def tasks():
    if 'username' in session and 'role_id' in session:
        user_id = session['user_id']
        logged_in_user = session['username']
        role_id = session['role_id']

    student_id = request.args.get('studentid', '')

    cursor.execute("SELECT * FROM tasks WHERE student_id = %s",
                   (student_id,))

    tasks_list = [[task['task_description'], task['subject_id'], task['teacher_id'], task['counsellor_id'], task['date_created'],
                   task['deadline'], task['status'], task['file_path_counsellor_teacher'], task['file_path_parent'],
                   task['task_id'], task['marks'], task['feedback']] for task in cursor.fetchall()]

    for task in tasks_list:
        cursor.execute("SELECT subject_name FROM subjects WHERE subject_id=%s", (task[1],))
        task[1] = cursor.fetchone()["subject_name"]

        if task[2]:
            cursor.execute(
                "SELECT teacher_name from teachers where teacher_id = %s", (task[2],))
            task[2] = cursor.fetchone()['teacher_name']

            task.pop(3)
            continue

        if task[3]:
            cursor.execute(
                "SELECT counsellor_name from counsellors where counsellor_id = %s", (task[3],))
            task[3] = cursor.fetchone()['counsellor_name']

            task.pop(2)
            continue
    
    cursor.execute("SELECT weak_subjects FROM students where student_id=%s", (student_id,))
    weak_subjects = [int(i) for i in cursor.fetchone()["weak_subjects"].split(",")]

    
    for i, sub_id in enumerate(weak_subjects):
        cursor.execute("SELECT * FROM subjects where subject_id=%s", (sub_id,))
        weak_subjects[i] = cursor.fetchone()

    current_user = ""

    if role_id == 1:
        cursor.execute(
            "SELECT teacher_id, teacher_name FROM teachers WHERE user_id = %s", (user_id,)
        )

        teacher_details = cursor.fetchone()
        current_user = teacher_details["teacher_name"]

        temp_weak_subjects = {}

        for sub in weak_subjects:
            if sub["teacher_id"] == teacher_details["teacher_id"]:
                temp_weak_subjects[sub["subject_name"]] = sub["subject_id"]
                
        weak_subjects = temp_weak_subjects
    
    elif role_id == 2:
        cursor.execute(
            "SELECT counsellor_name FROM counsellors WHERE user_id = %s", (user_id,))

        current_user = cursor.fetchone()['counsellor_name']

    if role_id == 2 or role_id == 3:
        weak_subjects = {sub["subject_name"]:sub["subject_id"] for sub in weak_subjects}

    return render_template('tasks.html', tasks_list=tasks_list, role_id=role_id, current_user=current_user, weak_subjects=weak_subjects)


@app.route('/add_task', methods=['POST'])
def add_task():
    if 'username' in session and 'role_id' in session:
        user_id = session['user_id']
        logged_in_user = session['username']
        role_id = session['role_id']

    data = request.form.to_dict()

    student_id = data['studentid']

    counsellor_id = None
    teacher_id = None

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
                data['task_desc'],data['subjectid'], data['status'], data['due_date'], data['assigned_date'], None, file_path)

    return jsonify({'status': 'success'})


@app.route('/submit_task', methods=['POST'])
def submit_task():
    if 'username' in session and 'role_id' in session:
        user_id = session['user_id']
        logged_in_user = session['username']
        role_id = session['role_id']

    data = request.form.to_dict()

    file_path = None
    # File upload handling
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, "parent", filename)
            file.save(file_path)
    else:
        return 

    cursor.execute(
        'UPDATE tasks SET status = "D", file_path_parent = %s WHERE task_id=%s',
        (file_path, data['task_id']))

    return jsonify({'status': 'success'})

@app.route('/grade_task', methods=['POST'])
def grade_task():
    if 'username' in session and 'role_id' in session:
        user_id = session['user_id']
        logged_in_user = session['username']
        role_id = session['role_id']

    data = request.form.to_dict()

    cursor.execute(
        'UPDATE tasks SET marks=%s, feedback=%s WHERE task_id=%s',
        (data['marks'], data['feedback'], data['task_id']))

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


@app.route('/view_teacher')
def index():
    teachers = get_teachers()
    return render_template('it-manager-Dash/view/view_teacher.html', teachers=teachers)


# Route to add a new teacher
@app.route('/add_teacher', methods=['POST'])
def add_teacher():
    teacher_name = request.form['teacher_name']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    role_id = '1'
    # for k,v in request.form.items():
    #     print(k,v)
    create_teacher_with_user(teacher_name, username, password, email, role_id)
    return redirect(url_for('view_teacher'))


# Route to update a teacher
@app.route('/update_teacher', methods=['POST'])
def update():
    teacher_id = request.form['id']
    new_teacher_name = request.form['name']
    new_email = request.form['email']
    update_teacher(teacher_id, new_teacher_name, new_email)
    return redirect('/')


# Route to delete a teacher
@app.route('/delete/<int:teacher_id>')
def delete(teacher_id):
    delete_teacher(teacher_id)
    return redirect('/')

@app.route('/view_counsellor')
def view_counsellor():
    counsellors = get_counsellor()
    return render_template('it-manager-Dash/view/view_counsellor.html', counsellors=counsellors)


# Route to add a new counsellor
@app.route('/add_counsellor', methods=['POST'])
def add_counsellor():
    counsellor_name = request.form['counsellor_name']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    role_id = '2'
    # for k,v in request.form.items():
    #     print(k,v)
    create_counsellor_with_user(counsellor_name, username, password, email, role_id)
    return redirect(url_for('view_counsellor'))


# Route to update a counsellor
@app.route('/update_counsellor', methods=['POST'])
def update_counsellor():
    counsellor_id = request.form['id']
    new_counsellor_name = request.form['name']
    new_email = request.form['email']
    update_counsellor(counsellor_id, new_counsellor_name, new_email)
    return redirect('/')


# Route to delete a counsellor
@app.route('/delete/<int:counsellor_id>')
def delete_counsellor(counsellor_id):
    delete_counsellor(counsellor_id)
    return redirect('/')


@app.route('/view_graph', methods=['GET'])
def view_graph():
    if 'username' in session and 'role_id' in session:
        user_id = session['user_id']
        logged_in_user = session['username']
        role_id = session['role_id']

    student_id = request.args.get('studentid','')
    graph_path = request.args.get('graph_path', '')

    cursor.execute("SELECT weak_subjects FROM students where student_id=%s", (student_id,))
    weak_subjects = {}

    for sub_id in cursor.fetchone()["weak_subjects"].split(","):
        cursor.execute("SELECT * FROM subjects where subject_id=%s", (int(sub_id),))
        weak_subjects[cursor.fetchone()["subject_name"]] = sub_id

    return render_template('graph.html', student_id=student_id, graph_path=graph_path, weak_subjects=weak_subjects)

@app.route('/make_graph', methods=['POST'])
def make_graph():
    if 'username' in session and 'role_id' in session:
        user_id = session['user_id']
        logged_in_user = session['username']
        role_id = session['role_id']

    student_id = int(request.form['student_id'])
    subject_id = int(request.form['subject'])
    start_date = request.form['startDate']
    end_date = request.form['endDate']

    graph_grades = 'grades' in request.form
    graph_tasks = 'tasks' in request.form

    if graph_grades:
        cursor.execute("SELECT score, date FROM grades WHERE student_id = %s and subject_id = %s and date >= %s and date <= %s", (student_id, subject_id, start_date, end_date))
        grades = cursor.fetchall()

    if graph_tasks:
        cursor.execute("SELECT marks, deadline FROM tasks WHERE student_id = %s and subject_id = %s and deadline >= %s and deadline <= %s and status='D'", (student_id, subject_id, start_date, end_date))
        marks = cursor.fetchall()

    letter_to_number = {
    "A"	: 4.0 * 10/4.0,
    "B"	: 3.3 * 10 / 4.0,
    "C"	: 2.3 * 10 / 4.0,
    "D"	: 1.3 * 10/ 4.0,
    "F" : 0 * 10 / 4.0}

    x_axis = []
    y_axis = []
    legend = []

    if graph_grades and grades:
        for grade in grades:
            y_axis.append(letter_to_number[grade['score']])
            x_axis.append(grade['date'])

        plt.plot(x_axis, y_axis, "r")
        legend.append("Grades")
    
    y_axis.clear()
    x_axis.clear()
    
    if graph_tasks and marks:
        for mark in marks:
            y_axis.append(mark['marks'])
            x_axis.append(mark['deadline'])

        plt.plot(x_axis, y_axis, "g")
        legend.append("Tasks")

    plt.ylim(0, 10.5)
    plt.xticks(rotation=30)
    plt.xlabel("Date")
    plt.ylabel("Scores")
    plt.legend(legend)
    plt.tight_layout()

    i = 0
    while(True):
        if os.path.exists(f'./static/graphs/temp_{student_id}_{subject_id}_{i}.png'):
            i += 1
            continue;
        
        plt.savefig(f'./static/graphs/temp_{student_id}_{subject_id}_{i}.png')
        break

    query = {"studentid": student_id, "graph_path" : f'temp_{student_id}_{subject_id}_{i}.png'}
    query = parse.urlencode(query)
    return redirect('/view_graph' + '?' + query)

if __name__ == '__main__':
    app.run(debug=True)

from dbconfig import *

# Create operation for roles
def create_role(role_name):
    insert_role_query = "INSERT INTO roles (role_name) VALUES (%s)"
    cursor.execute(insert_role_query, (role_name,))
    db_connection.commit()

# Read operation for roles
def get_roles():
    query = "SELECT * FROM roles"
    cursor.execute(query)
    return cursor.fetchall()

# Update operation for roles
def update_role(role_id, new_role_name):
    update_role_query = "UPDATE roles SET role_name = %s WHERE role_id = %s"
    cursor.execute(update_role_query, (new_role_name, role_id))
    db_connection.commit()

# Delete operation for roles
def delete_role(role_id):
    delete_role_query = "DELETE FROM roles WHERE role_id = %s"
    cursor.execute(delete_role_query, (role_id,))
    db_connection.commit()

# Create operation for users
def create_user(username, password, email, role_id):
    insert_user_query = "INSERT INTO users (username, password, email, role_id) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_user_query, (username, password, email, role_id))
    db_connection.commit()

# Read operation for users
def get_users():
    query = "SELECT * FROM users"
    cursor.execute(query)
    return cursor.fetchall()

# Update operation for users
def update_user(user_id, new_username, new_password, new_email, new_role_id):
    update_user_query = "UPDATE users SET username = %s, password = %s, email = %s, role_id = %s WHERE user_id = %s"
    cursor.execute(update_user_query, (new_username, new_password, new_email, new_role_id, user_id))
    db_connection.commit()

# Delete operation for users
def delete_user(user_id):
    delete_user_query = "DELETE FROM users WHERE user_id = %s"
    cursor.execute(delete_user_query, (user_id,))
    db_connection.commit()

# Create operation for students
def create_student(student_name, counsellor_id, teacher_id, parent_id):
    insert_student_query = "INSERT INTO students (student_name, counsellor_id, teacher_id, parent_id) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_student_query, (student_name, counsellor_id, teacher_id, parent_id))
    db_connection.commit()

# Read operation for students
def get_students():
    query = "SELECT * FROM students"
    cursor.execute(query)
    return cursor.fetchall()

# Update operation for students
def update_student(student_id, new_student_name, new_date_of_birth):
    update_student_query = "UPDATE students SET student_name = %s, date_of_birth = %s WHERE student_id = %s"
    cursor.execute(update_student_query, (new_student_name, new_date_of_birth, student_id))
    db_connection.commit()

# Delete operation for students
def delete_student(student_id):
    delete_student_query = "DELETE FROM students WHERE student_id = %s"
    cursor.execute(delete_student_query, (student_id,))
    db_connection.commit()

# Create operation for teachers
def create_teacher_with_user(teacher_name, username, password, email, role_id):
    # Start by creating a new user entry
    insert_user_query = "INSERT INTO users (username, password, email, role_id) VALUES (%s, %s, %s, %s)"
    user_values = (username, password, email, role_id)

    cursor = db_connection.cursor()
    try:
        # Insert user
        cursor.execute(insert_user_query, user_values)
        user_id = cursor.lastrowid  # Get the newly created user ID
        db_connection.commit()

        # Insert teacher with the new user_id
        insert_teacher_query = "INSERT INTO teachers (teacher_name, user_id) VALUES (%s, %s)"
        teacher_values = (teacher_name, user_id)
        cursor.execute(insert_teacher_query, teacher_values)
        db_connection.commit()

        print("Teacher added successfully")
    except mysql.connector.Error as err:
        print("Error occurred: ", err)
    finally:
        cursor.close()
def create_counsellor_with_user(counsellor_name, username, password, email, role_id):
    # Start by creating a new user entry
    insert_user_query = "INSERT INTO users (username, password, email, role_id) VALUES (%s, %s, %s, %s)"
    user_values = (username, password, email, role_id)

    cursor = db_connection.cursor()
    try:
        # Insert user
        cursor.execute(insert_user_query, user_values)
        user_id = cursor.lastrowid  # Get the newly created user ID
        db_connection.commit()

        # Insert teacher with the new user_id
        insert_teacher_query = "INSERT INTO counsellors (counsellor_name, user_id) VALUES (%s, %s)"
        counsellor_values = (counsellor_name, user_id)
        cursor.execute(insert_teacher_query, counsellor_values)
        db_connection.commit()

        print("Counsellor added successfully")
    except mysql.connector.Error as err:
        print("Error occurred: ", err)
    finally:
        cursor.close()

def get_counsellor():
    query = "SELECT * FROM counsellors"
    cursor.execute(query)
    return cursor.fetchall()
# Read operation for teachers
def get_teachers():
    query = "SELECT * FROM teachers"
    cursor.execute(query)
    return cursor.fetchall()

# Update operation for teachers
def update_teacher(teacher_id, new_teacher_name, new_email):
    update_teacher_query = "UPDATE teachers SET teacher_name = %s, email = %s WHERE teacher_id = %s"
    cursor.execute(update_teacher_query, (new_teacher_name, new_email, teacher_id))
    db_connection.commit()

# Delete operation for teachers
def delete_teacher(teacher_id):
    delete_teacher_query = "DELETE FROM teachers WHERE teacher_id = %s"
    cursor.execute(delete_teacher_query, (teacher_id,))
    db_connection.commit()

# Create operation for attendance
def create_attendance(student_id, teacher_id, date, status):
    insert_attendance_query = "INSERT INTO attendance (student_id, teacher_id, date, status) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_attendance_query, (student_id, teacher_id, date, status))
    db_connection.commit()

# Read operation for attendance
def get_attendance():
    query = "SELECT * FROM attendance"
    cursor.execute(query)
    return cursor.fetchall()

# Update operation for attendance
def update_attendance(attendance_id, new_student_id, new_teacher_id, new_date, new_status):
    update_attendance_query = "UPDATE attendance SET student_id = %s, teacher_id = %s, date = %s, status = %s WHERE attendance_id = %s"
    cursor.execute(update_attendance_query, (new_student_id, new_teacher_id, new_date, new_status, attendance_id))
    db_connection.commit()

# Delete operation for attendance
def delete_attendance(attendance_id):
    delete_attendance_query = "DELETE FROM attendance WHERE attendance_id = %s"
    cursor.execute(delete_attendance_query, (attendance_id,))
    db_connection.commit()

# Create operation for grades
def create_grade(student_id, teacher_id, subject, score, date):
    insert_grade_query = "INSERT INTO grades (student_id, teacher_id, subject, score, date) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(insert_grade_query, (student_id, teacher_id, subject, score, date))
    db_connection.commit()

# Read operation for grades
def get_grades():
    query = "SELECT * FROM grades"
    cursor.execute(query)
    return cursor.fetchall()

# Update operation for grades
def update_grade(grade_id, new_student_id, new_teacher_id, new_subject, new_score, new_date):
    update_grade_query = "UPDATE grades SET student_id = %s, teacher_id = %s, subject = %s, score = %s, date = %s WHERE grade_id = %s"
    cursor.execute(update_grade_query, (new_student_id, new_teacher_id, new_subject, new_score, new_date, grade_id))
    db_connection.commit()

# Delete operation for grades
def delete_grade(grade_id):
    delete_grade_query = "DELETE FROM grades WHERE grade_id = %s"
    cursor.execute(delete_grade_query, (grade_id,))
    db_connection.commit()

# Create operation for tasks
def create_task(student_id, teacher_id, counsellor_id, task_description,subject, status, deadline, date_created, file_path_parent, file_path_counsellor_teacher):
    insert_task_query = "insert into tasks (student_id, teacher_id, counsellor_id, task_description, subject, status, \
        deadline, date_created, file_path_parent, file_path_counsellor_teacher) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(insert_task_query, (student_id, teacher_id, counsellor_id, task_description,subject, status, deadline, date_created, file_path_parent, file_path_counsellor_teacher))
    db_connection.commit()

# Read operation for tasks
def get_tasks():
    query = "SELECT * FROM tasks"
    cursor.execute(query)
    return cursor.fetchall()

# Update operation for tasks
def update_task(task_id, new_student_id, new_teacher_id, new_task_description, new_status, new_deadline, new_date_created):
    update_task_query = "UPDATE tasks SET student_id = %s, teacher_id = %s, task_description = %s, status = %s, deadline = %s, date_created = %s WHERE task_id = %s"
    cursor.execute(update_task_query, (new_student_id, new_teacher_id, new_task_description, new_status, new_deadline, new_date_created, task_id))
    db_connection.commit()

# Delete operation for tasks
def delete_task(task_id):
    delete_task_query = "DELETE FROM tasks WHERE task_id = %s"
    cursor.execute(delete_task_query, (task_id,))
    db_connection.commit()

# Create operation for messages
def create_message(sender_id, receiver_id, message_text, timestamp):
    insert_message_query = "INSERT INTO messages (sender_id, receiver_id, message_text, timestamp) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_message_query, (sender_id, receiver_id, message_text, timestamp))
    db_connection.commit()

# Read operation for messages
def get_messages():
    query = "SELECT * FROM messages"
    cursor.execute(query)
    return cursor.fetchall()

def get_student_by_user_id(user_id):
    query = " SELECT students.student_id, students.student_name FROM students JOIN parents ON students.parent_id = parents.parent_id JOIN users ON parents.user_id = users.user_id WHERE users.user_id = %s;"
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()
    return result
# Update and Delete operations for messages can be added similarly

# ----------------------------------------- #
def get_total_students_by_user_id(user_id):
    query = """
    SELECT teacher_id, COUNT(*) as total_students
    FROM students
    where teacher_id = %s;
    """
    cursor.execute(query,user_id)
    result = cursor.fetchall()
    return result



def get_total_assigned_tasks_by_teacher_id(user_id):
    query = """
    SELECT teacher_id, COUNT(*) as total_tasks
    FROM tasks
    WHERE teacher_id IS NOT NULL
    GROUP BY teacher_id;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def get_total_ungraded_by_teacher_id(user_id):
    query = """
    SELECT t.teacher_id, COUNT(*) as total_ungraded
    FROM tasks t
    LEFT JOIN grades g ON t.student_id = g.student_id AND t.subject = g.subject
    WHERE t.teacher_id IS NOT NULL AND g.score IS NULL AND t.teacher_id = %s
    
    """
    cursor.execute(query,user_id)
    result = cursor.fetchall()
    return result


def get_total_students():
    query = "SELECT COUNT(*) as total_students FROM students;"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def get_total_tasks():
    query = "SELECT COUNT(*) as total_tasks FROM tasks;"
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def get_total_ungraded():
    query = """
    SELECT COUNT(*) as total_ungraded
    FROM tasks t
    LEFT JOIN grades g ON t.student_id = g.student_id AND t.subject = g.subject
    WHERE g.score IS NULL;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def get_totals():
    query = """
    SELECT (SELECT COUNT(*) FROM students) as total_students,
           (SELECT COUNT(*) FROM teachers) as total_teachers,
           (SELECT COUNT(*) FROM counsellors) as total_counsellors,
           (SELECT COUNT(*) FROM parents) as total_parents
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return result

print(get_totals())
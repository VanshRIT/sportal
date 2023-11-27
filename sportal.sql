create table counsellors
(
    counsellor_id   bigint unsigned auto_increment
        primary key,
    counsellor_name varchar(100) not null,
    user_id         int          null,
    constraint counsellor_id
        unique (counsellor_id)
);

create table grades
(
    grade_id   bigint unsigned auto_increment
        primary key,
    student_id int          null,
    teacher_id int          null,
    subject    varchar(255) not null,
    score      char         not null,
    date       date         not null,
    constraint grade_id
        unique (grade_id)
);

create table messages
(
    message_id   bigint unsigned auto_increment
        primary key,
    sender_id    int       null,
    receiver_id  int       null,
    message_text text      not null,
    timestamp    timestamp not null,
    constraint message_id
        unique (message_id)
);

create table parents
(
    parent_id   int auto_increment
        primary key,
    parent_name varchar(100) null,
    user_id     int          null
);

create table roles
(
    role_id   bigint unsigned auto_increment
        primary key,
    role_name varchar(255) not null,
    constraint role_id
        unique (role_id)
);

create table students
(
    student_id    bigint unsigned auto_increment
        primary key,
    student_name  varchar(255) not null,
    teacher_id    int          null,
    counsellor_id int          null,
    parent_id     int          null,
    constraint student_id
        unique (student_id)
);

create table tasks
(
    task_id                      bigint unsigned auto_increment
        primary key,
    student_id                   int           null,
    teacher_id                   int           null,
    counsellor_id                int           null,
    task_description             text          not null,
    status                       varchar(20)   not null,
    deadline                     date          not null,
    date_created                 timestamp     not null,
    file_path_parent             varchar(1000) null,
    file_path_counsellor_teacher varchar(1000) null,
    constraint task_id
        unique (task_id)
);

create table teachers
(
    teacher_id   bigint unsigned auto_increment
        primary key,
    teacher_name varchar(255) not null,
    user_id      int          null,
    constraint teacher_id
        unique (teacher_id)
);

create table users
(
    user_id  bigint unsigned auto_increment
        primary key,
    username varchar(255) not null,
    password varchar(255) not null,
    email    varchar(255) not null,
    role_id  int          null,
    constraint user_id
        unique (user_id)
);

INSERT INTO users (user_id, username, password, email, role_id) VALUES (3, 'counsellor1_test', 'counsellor1', 'asdf', 2);
INSERT INTO users (user_id, username, password, email, role_id) VALUES (1, 'admin', 'admin', 'admin', 2);
INSERT INTO users (user_id, username, password, email, role_id) VALUES (4, 'teacher1_test', 'teacher1', 'asdff', 1);
INSERT INTO users (user_id, username, password, email, role_id) VALUES (2, 'pap', 'pap', 'pap5183@rit.edu', 3);
INSERT INTO users (user_id, username, password, email, role_id) VALUES (5, 'parent1_test', 'parent1', 'asdfff', 3);
INSERT INTO users (user_id, username, password, email, role_id) VALUES (6, 'teacher2_test', 'teacher2', 'asdffff', 1);

INSERT INTO parents (parent_id, parent_name, user_id) VALUES (1, 'test_parent_1', 5);
INSERT INTO parents (parent_id, parent_name, user_id) VALUES (2, 'pap', 2);

INSERT INTO teachers (teacher_id, teacher_name, user_id) VALUES (1, 'test_teacher_1', 4);
INSERT INTO teachers (teacher_id, teacher_name, user_id) VALUES (2, 'test_teacher_2', 6);

INSERT INTO counsellors (counsellor_id, counsellor_name, user_id) VALUES (1, 'test_counsellor_1', 3);
INSERT INTO counsellors (counsellor_id, counsellor_name, user_id) VALUES (2, 'admin', 2);

INSERT INTO students (student_id, student_name, teacher_id, counsellor_id, parent_id) VALUES (1, 'test_student_1', 1, 1, 1);
INSERT INTO students (student_id, student_name, teacher_id, counsellor_id, parent_id) VALUES (2, 'test_student_2', 1, 1, 1);
INSERT INTO students (student_id, student_name, teacher_id, counsellor_id, parent_id) VALUES (3, 'test_student_3', 2, 2, 2);

INSERT INTO tasks (task_id, student_id, teacher_id, counsellor_id, task_description, status, deadline, date_created, file_path_parent, file_path_counsellor_teacher) VALUES (1, 1, 1, 0, 'Read 10 Pages in Chapter 2 English Textbook', 'ND', '2023-11-28', '2023-11-23 18:15:12', null, null);
INSERT INTO tasks (task_id, student_id, teacher_id, counsellor_id, task_description, status, deadline, date_created, file_path_parent, file_path_counsellor_teacher) VALUES (2, 1, 0, 1, 'Make a flappy bird game form scratch purely in assembly', 'ND', '2023-12-11', '2023-11-24 22:19:09', null, null);
INSERT INTO tasks (task_id, student_id, teacher_id, counsellor_id, task_description, status, deadline, date_created, file_path_parent, file_path_counsellor_teacher) VALUES (5, 1, 0, 1, 'asdf', 'D', '2023-11-29', '2023-11-27 00:00:00', 'C:\\Users\\prana\\Documents\\GitHub\\sportal\\files_uploaded\\parent\\Picture1.png', 'C:\\Users\\prana\\Documents\\GitHub\\sportal\\files_uploaded\\counsellor_teacher\\Picture1.png');
INSERT INTO tasks (task_id, student_id, teacher_id, counsellor_id, task_description, status, deadline, date_created, file_path_parent, file_path_counsellor_teacher) VALUES (6, 1, 0, 1, 'drgftsre', 'D', '2023-11-27', '2023-11-27 00:00:00', 'C:\\Users\\prana\\Documents\\GitHub\\sportal\\files_uploaded\\parent\\as.txt', null);

from database_connection import get_database_connection


def drop_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""
        drop table if exists users;
    """)

    cursor.execute("""
        drop table if exists courses;
    """)

    cursor.execute("""
        drop table if exists tasks;
    """)

    cursor.execute("""
        drop table if exists course_points;
    """)

    connection.commit()


def create_user_table(connection):
    cursor = connection.cursor()

    cursor.execute("""
        create table users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        );
    """)
    connection.commit()


def create_courses_table(connection):
    cursor = connection.cursor()

    cursor.execute("""
        create table courses (
            course_id INTEGER PRIMARY KEY,
            user_id INTEGER REFERENCES users(user_id),
            name TEXT,
            ects_credits INTEGER,
            done BOOLEAN, 
            grade INTEGER,
            completion_date INTEGER
        );
    """)

    connection.commit()


def create_tasks_table(connection):
    cursor = connection.cursor()

    cursor.execute("""
        create table tasks (
            task_id PRIMARY KEY,
            task TEXT
        );
    """)

    connection.commit()


def initialize_tasks_table(connection):
    cursor = connection.cursor()

    cursor.execute("""insert into tasks (task_id, task) values
                   (1, "exercises"),
                   (2, "exercise_group"),
                   (3, "project"),
                   (4, "exam"),
                   (5, "peer_review"),
                   (6, "feedback"),
                   (7, "other");
                """)

    connection.commit()


def create_course_points_table(connection):
    cursor = connection.cursor()

    cursor.execute("""
        create table course_points (
            course_id INTEGER REFERENCES courses(course_id),
            task_id INTEGER REFERENCES tasks(task_id),
            points INTEGER
        );
    """)

    connection.commit()


def initialize_database():
    connection = get_database_connection()

    drop_tables(connection)
    create_user_table(connection)
    create_courses_table(connection)
    create_tasks_table(connection)
    initialize_tasks_table(connection)
    create_course_points_table(connection)


if __name__ == "__main__":
    initialize_database()

from database_connection import get_database_connection

def drop_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""
        drop table if exists users;
    """)

    connection.commit()

    cursor = connection.cursor()

    cursor.execute("""
        drop table if exists courses;
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

def create_course_table(connection):
    cursor = connection.cursor()

    cursor.execute("""
        create table courses (
            course_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            name TEXT,
            credits INTEGER,
            exercises INTEGER,
            exercise_group INTEGER,
            project INTEGER,
            exam INTEGER,
            peer_review INTEGER,
            feedback INTEGER,
            other INTEGER, 
            done BOOLEAN, 
            grade INTEGER,
            completion_date INTEGER
            
        );
    """)

    connection.commit()


def initialize_database():
    connection = get_database_connection()

    drop_tables(connection)
    create_user_table(connection)
    create_course_table(connection)


if __name__ == "__main__":
    initialize_database()
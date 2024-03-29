from entities.course import Course
from database_connection import get_database_connection

def get_courses_by_row(row):
    return Course(row["user_id"], row["name"], row["credits"], row["exercises"], row["exercise_group"], row["project"], row["exam"], row["peer_review"], row["feedback"], row["other"]) if row else None

class CourseRepository:
    def __init__(self, connection):
        self._connection = connection

    def find_all(self):
        cursor = self._connection.cursor()

        cursor.execute("select * from courses")

        rows = cursor.fetchall()

        return list(map(get_courses_by_row, rows))

    def find_by_username(self, username):
        pass

    def create(self, course):
        cursor = self._connection.cursor()

        cursor.execute(
            "insert into courses (user_id, name, credits, exercises, exercise_group, project, exam, peer_review, feedback, other, done, grade, completion_date) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (course.user_id, course.name, course.credits, course.exercises, course.exercise_group, course.project, course.exam, course.peer_review, course.feedback, course.other, course.done, course.grade, course.completion_date)
        )

        self._connection.commit()

        return course

    def set_done(self, course_id, done=True):
        pass

    def delete_course(self, course_id):
        pass

    def delete_all(self):
        cursor = self._connection.cursor()

        cursor.execute("delete from courses")

        self._connection.commit()

course_repository = CourseRepository(get_database_connection())
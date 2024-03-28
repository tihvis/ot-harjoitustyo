from entities.course import Course
from database_connection import get_database_connection


class CourseRepository:
    def __init__(self, connection):
        self._connection = connection

    def find_by_username(self, username):
        pass

    def create(self, course):
        cursor = self._connection.cursor()

        cursor.execute(
            "insert into courses (user, name, credits, exercises, exercise_group, project, exam, peer_review, feedback, other, done, grade, completion_date) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (course.user, course.name, course.credits, course.exercises, course.exercise_group, course.project, course.exam, course.peer_view, course.feedback, course.other, course.done, course.grade, course.completion_date)
        )

        self._connection.commit()

        return course

    def set_done(self, course_id, done=True):
        pass

    def delete(self, course_id):
        pass

course_repository = CourseRepository(get_database_connection())
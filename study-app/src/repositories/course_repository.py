from entities.course import Course
from database_connection import get_database_connection


def get_courses_by_row(row):
    points = {"exercises": row["exercises"], "exercise_group": \
            row["exercise_group"], "project": row["project"], "exam": \
            row["exam"], "peer_review": row["peer_review"], "feedback": \
            row["feedback"], "other": row["other"]}

    completion_info = {"done": row["done"], "grade": \
                    row["grade"], "completion_date": row["completion_date"]}

    return Course(row["user_id"], row["name"], row["ects_credits"], \
                  points, completion_info, row["course_id"]) if row else None


class CourseRepository:
    def __init__(self, connection):
        self._connection = connection

    def find_all(self):
        cursor = self._connection.cursor()

        cursor.execute("SELECT * FROM courses")

        rows = cursor.fetchall()

        return list(map(get_courses_by_row, rows))

    def find_by_user_id(self, user_id):
        cursor = self._connection.cursor()

        cursor.execute("SELECT * FROM courses WHERE user_id = ?", (user_id,))

        rows = cursor.fetchall()

        return list(map(get_courses_by_row, rows))

    def create(self, course):
        cursor = self._connection.cursor()

        query = "INSERT INTO courses (user_id, name, ects_credits) VALUES (?, ?, ?)"

        cursor.execute(query, (course.user_id, course.name, course.ects_credits))

        course_id = cursor.lastrowid

        for task in course.points:
            cursor.execute(f"UPDATE courses SET {str(task)} = ? \
                           WHERE course_id = ?", (course.points[task], course_id))

        self._connection.commit()

        course.course_id = course_id

        return course

    def set_done(self, course_id, done=True):
        pass

    def delete_course(self, course_id):
        cursor = self._connection.cursor()

        cursor.execute("delete from courses where course_id = ?", (course_id,))

        self._connection.commit()

    def delete_all(self):
        cursor = self._connection.cursor()

        cursor.execute("delete from courses")

        self._connection.commit()


course_repository = CourseRepository(get_database_connection())

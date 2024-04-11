from entities.course import Course
from database_connection import get_database_connection


def get_courses_by_row(row):
    points = {1: row["exercises"], 2: row["exercise_group"], 3: row["project"],
              4: row["exam"], 5: row["peer_review"], 6: row["feedback"], 7: row["other"]}
    completion = {"done": row["done"], "grade": row["grade"],
                  "completion_date": row["completion_date"]}
    return Course(row["user_id"], row["name"], row["ects_credits"],
                  points, completion, row["course_id"]) if row else None


class CourseRepository:
    def __init__(self, connection):
        self._connection = connection

    def find_all(self):
        cursor = self._connection.cursor()

        query = "SELECT c.user_id, c.name, c.ects_credits," \
                "SUM(CASE WHEN t.task = 1 THEN cp.points ELSE 0 END) " \
                "AS exercises," \
                "SUM(CASE WHEN t.task = 2 THEN cp.points ELSE 0 END) " \
                "AS exercise_group," \
                "SUM(CASE WHEN t.task = 3 THEN cp.points ELSE 0 END) AS " \
                "project," \
                "SUM(CASE WHEN t.task = 4 THEN cp.points ELSE 0 END) AS exam," \
                "SUM(CASE WHEN t.task = 5 THEN cp.points ELSE 0 END) " \
                "AS peer_review," \
                "SUM(CASE WHEN t.task = 6 THEN cp.points ELSE 0 END) " \
                "AS feedback," \
                "SUM(CASE WHEN t.task = 7 THEN cp.points ELSE 0 END) AS "\
                "other," \
                "c.done, c.grade, c.completion_date, cp.course_id FROM " \
                "courses c LEFT JOIN course_points cp ON c.course_id = " \
                "cp.course_id LEFT JOIN tasks t ON cp.task_id = t.task_id "\
                "GROUP BY cp.course_id, c.user_id, c.name, c.ects_credits, "\
                "c.done, c.grade, c.completion_date"

        cursor.execute(query)

        courses = cursor.fetchall()

        return list(map(get_courses_by_row, courses))

    def find_by_user_id(self, user_id):
        cursor = self._connection.cursor()

        cursor.execute("SELECT * FROM courses WHERE user_id = ?", (user_id,))

        rows = cursor.fetchall()

        return list(map(get_courses_by_row, rows))

    def create(self, course):
        cursor = self._connection.cursor()

        query = "INSERT INTO courses (user_id, name, ects_credits) VALUES (?, ?, ?)"

        cursor.execute(
            query, (course.user_id, course.name, course.ects_credits))

        course_id = cursor.lastrowid

        query = "INSERT INTO course_points (course_id, task_id, points) VALUES (?, ?, ?)"

        for task_id in course.points:
            cursor.execute(query, (course_id, task_id, course.points[task_id]))

        self._connection.commit()

        course.course_id = course_id

        self._connection.commit()

        course.course_id = course_id

        return course

    def set_done(self, course_id, done=True):
        pass

    def delete_course(self, course_id):
        cursor = self._connection.cursor()

        cursor.execute("delete from courses where course_id = ?", (course_id,))
        cursor.execute(
            "delete from course_points where course_id = ?", (course_id,))

        self._connection.commit()

    def delete_all(self):
        cursor = self._connection.cursor()

        cursor.execute("delete from courses")

        self._connection.commit()


course_repository = CourseRepository(get_database_connection())

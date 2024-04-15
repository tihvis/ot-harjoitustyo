from entities.course import Course
from database_connection import get_database_connection


class CourseRepository:
    def __init__(self, connection):
        self._connection = connection

    def find_all(self):
        cursor = self._connection.cursor()

        query = "SELECT * FROM courses"

        cursor.execute(query)

        courses = cursor.fetchall()

        return self.create_course_object(courses)

    def find_by_user_id(self, user_id):
        cursor = self._connection.cursor()

        cursor.execute("SELECT * FROM courses WHERE user_id = ?", (user_id,))

        courses = cursor.fetchall()

        return self.create_course_object(courses)

    def get_course_points(self, course_id):
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT task_id, points FROM course_points WHERE course_id = ?", (course_id,))

        rows = cursor.fetchall()

        return {row[0]: row[1] for row in rows}

    def get_completion_info(self, course_id):
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT done, grade, completion_date FROM courses WHERE course_id = ?", (course_id,))

        row = cursor.fetchone()

        return {
            "done": row["done"],
            "grade": row["grade"],
            "completion_date": row["completion_date"]
        }

    def create_course_object(self, courses):
        result = []
        for course in courses:
            course_id = course["course_id"]
            points = self.get_course_points(course_id)
            completion = self.get_completion_info(course_id)
            result.append(Course(course["user_id"], course["name"],
                          course["ects_credits"], points, completion, course_id))

        return result

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

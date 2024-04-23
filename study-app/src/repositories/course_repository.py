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

    def find_ongoing_courses_by_user_id(self, user_id):
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * FROM courses WHERE user_id = ? and done = ?", (user_id, 0))

        courses = cursor.fetchall()

        return self.create_course_object(courses)

    def find_completed_courses_by_user_id(self, user_id):
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * FROM courses WHERE user_id = ? and done = ?", (user_id, 1))

        courses = cursor.fetchall()

        return self.create_course_object(courses)

    def get_max_points_by_course(self, course_id):
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT task_id, max_points FROM course_points WHERE course_id = ?", (course_id,))

        rows = cursor.fetchall()

        return {row[0]: row[1] for row in rows}

    def get_completed_points_by_course(self, course_id):
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT task_id, completed_points FROM course_points WHERE course_id = ?", (course_id,))

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
            max_points = self.get_max_points_by_course(course_id)
            completion = self.get_completion_info(course_id)
            result.append(Course(course["user_id"], course["name"],
                                 course["ects_credits"], max_points, completion, course_id))

        return result

    def create(self, course):
        cursor = self._connection.cursor()

        query = "INSERT INTO courses (user_id, name, ects_credits, done) VALUES (?, ?, ?, ?)"

        cursor.execute(
            query, (course.user_id, course.name, course.ects_credits, 0))

        course_id = cursor.lastrowid

        query = "INSERT INTO course_points (course_id, task_id, " \
                "max_points, completed_points) VALUES (?, ?, ?, ?)"

        for task_id in course.max_points:
            cursor.execute(query, (course_id, task_id,
                           course.max_points[task_id], 0))

        self._connection.commit()

        course.course_id = course_id

        return course

    def update(self, course_id, completed_points):
        cursor = self._connection.cursor()

        query = "UPDATE course_points SET completed_points = ? WHERE course_id = ? AND task_id = ?"

        for task_id in completed_points:
            cursor.execute(
                query, (completed_points[task_id], course_id, task_id))

        self._connection.commit()

    def set_done(self, course_id, grade, completion_date):
        cursor = self._connection.cursor()

        query = "UPDATE courses SET done = ?, grade = ?, completion_date = ? WHERE course_id = ?"

        cursor.execute(query, (1, grade, completion_date, course_id))

        self._connection.commit()

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

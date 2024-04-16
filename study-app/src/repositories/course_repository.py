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
            "SELECT task_id, max_points FROM course_points WHERE course_id = ?", (course_id,))

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

        query = "INSERT INTO course_points (course_id, task_id, " \
                "max_points, completed_points) VALUES (?, ?, ?, ?)"

        for task_id in course.points:
            cursor.execute(query, (course_id, task_id,
                           course.points[task_id], 0))

        self._connection.commit()

        course.course_id = course_id

        return course

    def get_max_task_points(self, course_id, task_id):

        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT cp.max_points FROM course_points cp "
            "JOIN tasks t ON cp.task_id = t.task_id WHERE t.task_id = ? "
            "AND cp.course_id = ?", (task_id, course_id))

        max_points = cursor.fetchone()

        return max_points[0]

    def get_completed_task_points(self, course_id, task_id):
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT completed_points FROM course_points WHERE task_id = ? "
            "AND course_id = ?", (task_id, course_id))

        completed_points = cursor.fetchone()

        return completed_points[0]

    def get_task_ids(self):
        cursor = self._connection.cursor()

        cursor.execute("SELECT task_id FROM tasks")

        task_ids = cursor.fetchall()

        return [task_id[0] for task_id in task_ids]

    def get_name_of_task(self, task_id):
        cursor = self._connection.cursor()

        cursor.execute("SELECT task FROM tasks WHERE task_id = ?", (task_id,))

        task = cursor.fetchone()

        return task[0]

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

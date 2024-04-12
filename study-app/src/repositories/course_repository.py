from entities.course import Course
from database_connection import get_database_connection

def get_courses_by_row(row):
    pass
    # points = {
    #     1: row[1],
    #     2: row[2],
    #     3: row[3],
    #     4: row[4],
    #     5: row[5],
    #     6: row[6],
    #     7: row[7]
    # }
    # completion = {
    #     "done": row["done"],
    #     "grade": row["grade"],
    #     "completion_date": row["completion_date"]
    # }
    # return Course(
    #     row["user_id"],
    #     row["name"],
    #     row["ects_credits"],
    #     points = {},
    #     completion = {},
    #     row["course_id"]
    # ) if row else None

class CourseRepository:
    def __init__(self, connection):
        self._connection = connection

    def find_all(self):
        cursor = self._connection.cursor()

        # query = "SELECT "\
        # "c.course_id, c.user_id, c.name, c.ects_credits, "\
        # "MAX(CASE WHEN t.task_id = 1 THEN cp.points ELSE 0 END), "\
        # "MAX(CASE WHEN t.task_id = 2 THEN cp.points ELSE 0 END), "\
        # "MAX(CASE WHEN t.task_id = 3 THEN cp.points ELSE 0 END), "\
        # "MAX(CASE WHEN t.task_id = 4 THEN cp.points ELSE 0 END), "\
        # "MAX(CASE WHEN t.task_id = 5 THEN cp.points ELSE 0 END), "\
        # "MAX(CASE WHEN t.task_id = 6 THEN cp.points ELSE 0 END), "\
        # "MAX(CASE WHEN t.task_id = 7 THEN cp.points ELSE 0 END), "\
        # "c.done, c.grade, c.completion_date "\
        # "FROM courses c "\
        # "LEFT JOIN course_points cp "\
        # "ON c.course_id = cp.course_id "\
        # "LEFT JOIN tasks t "\
        # "ON cp.task_id = t.task_id "\
        # "GROUP BY c.course_id, c.user_id, c.name, "\
        # "c.ects_credits, c.done, c.grade, c.completion_date"

        query = "SELECT * FROM courses"

        cursor.execute(query)

        courses = cursor.fetchall()

        return self.create_course_object(courses)


    def find_by_user_id(self, user_id):
        cursor = self._connection.cursor()

        cursor.execute("SELECT * FROM courses WHERE user_id = ?", (user_id,))

        courses = cursor.fetchall()

        return self.create_course_object(courses)


        # cursor.execute("SELECT * FROM courses WHERE user_id = ?", (user_id,))

        # rows = cursor.fetchall()

        # return list(map(get_courses_by_row, rows))

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
            result.append(Course(course["user_id"], course["name"], course["ects_credits"], points, completion, course_id))

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

import unittest
from repositories.course_repository import course_repository
from entities.course import Course


class TestCourseRepository(unittest.TestCase):
    def setUp(self):
        course_repository.delete_all()
        self.user_id1 = 1
        self.user_id2 = 2
        self.course1 = Course(self.user_id1, "Ohjelmistotekniikka", 4,
                              {1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60, 7: 1})
        self.course2 = Course(
            self.user_id2, "Tietorakenteet ja algoritmit 1", 5, {1: 64, 6: 1})

    def test_find_all(self):
        course_repository.create(self.course1)
        course_repository.create(self.course2)

        courses = course_repository.find_all()
        self.assertEqual(len(courses), 2)

    def test_find_ongoing_courses_by_user_id(self):
        course_repository.create(self.course1)

        courses = course_repository.find_ongoing_courses_by_user_id(
            self.user_id1)

        self.assertEqual(len(courses), 1)

    def test_set_done_and_find_completed_courses_by_user_id(self):
        course = course_repository.create(self.course1)
        course_repository.set_done(course.course_id, 5, "24.4.2024")

        self.assertEqual(
            course.course_id, course_repository.find_completed_courses_by_user_id(self.user_id1)[0].course_id)

    def test_set_undone(self):
        course = course_repository.create(self.course1)
        course_repository.set_done(course.course_id, 5, "24.4.2024")

        self.assertEqual(
            len(course_repository.find_ongoing_courses_by_user_id(self.user_id1)), 0)

        course_repository.set_undone(course.course_id)

        self.assertEqual(
            len(course_repository.find_ongoing_courses_by_user_id(self.user_id1)), 1)

    def test_get_completion_info(self):
        course = course_repository.create(self.course1)
        course_repository.set_done(course.course_id, 5, "24.4.2024")

        self.assertEqual(course_repository.get_completion_info(course.course_id), {
                         "done": 1, "grade": 5, "completion_date": "24.4.2024"})

    def test_get_max_points_by_course(self):
        course = course_repository.create(self.course1)
        max_points = course_repository.get_max_points_by_course(
            course.course_id)

        self.assertEqual(max_points, self.course1.max_points)

    def test_create(self):
        course_repository.create(self.course1)

        courses = course_repository.find_all()

        self.assertEqual(courses[0].user_id, self.user_id1)
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0].name, "Ohjelmistotekniikka")
        self.assertEqual(courses[0].ects_credits, 4)
        self.assertEqual(courses[0].max_points, {
                         1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60, 7: 1})

    def test_update_course_and_get_completed_points_by_course(self):
        course_id = course_repository.create(self.course1).course_id
        completed_points = {1: 5, 2: 10, 3: 15, 4: 20, 5: 25, 6: 30, 7: 1}

        course_repository.update(course_id, completed_points)

        result = course_repository.get_completed_points_by_course(course_id)

        self.assertEqual(result, completed_points)

    def test_delete_course(self):
        course_id = course_repository.create(self.course1).course_id

        course_repository.delete_course(course_id)

        self.assertEqual(len(course_repository.find_all()), 0)

    def test_delete_all(self):
        course_repository.create(self.course1)
        course_repository.create(self.course2)

        course_repository.delete_all()

        self.assertEqual(len(course_repository.find_all()), 0)

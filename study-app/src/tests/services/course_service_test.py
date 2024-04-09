import unittest
from repositories.course_repository import course_repository
from repositories.user_repository import user_repository
from services.course_service import course_service, InvalidValuesError
from services.user_service import user_service


class TestCourseService(unittest.TestCase):
    def setUp(self):
        course_repository.delete_all()
        user_repository.delete_all()
        self.user = user_service.create_user("test", "Test1234", "Test1234")

    def test_create_course_with_valid_values(self):
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, 20, 0, 40, 0, 5, 1, 0)

        self.assertEqual(course.name, "Ohjelmistotekniikka")
        self.assertEqual(course.credits, 5)
        self.assertEqual(course.exercises, 20)
        self.assertEqual(course.exercise_group, 0)
        self.assertEqual(course.project, 40)
        self.assertEqual(course.exam, 0)
        self.assertEqual(course.peer_review, 5)
        self.assertEqual(course.feedback, 1)
        self.assertEqual(course.other, 0)

    def test_create_course_with_no_name(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(self.user.user_id,
                                                                                   "", 5, 20, 10, 40, 2, 5, 1, 0))

    def test_create_course_with_too_long_name(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(self.user.user_id,
                                                                                   "ohjelmistoohjelmistoohjelmistoohjelmistoohjelmistoa", 5, 20, 10, 40, 2, 5, 1, 0))

    def test_create_course_with_negative_credits(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(self.user.user_id,
                                                                                   "Ohjelmistotekniikka", -1, 10, 0, 20, 3, 5, 1, 6))

    def test_create_course_with_too_many_credits(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(self.user.user_id,
                                                                                   "Ohjelmistotekniikka", 51, 10, 0, 20, 3, 5, 1, 6))

    def test_create_course_with_negative_exercises(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(self.user.user_id,
                                                                                   "Ohjelmistotekniikka", 10, -1, 2, 40, 0, 10, 10, 0))

    def test_create_course_with_too_many_exercises(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(self.user.user_id,
                                                                                   "Ohjelmistotekniikka", 10, 101, 2, 40, 0, 10, 10, 0))

    def test_create_course_with_negative_exercise_group(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(self.user.user_id,
                                                                                   "Ohjelmistotekniikka", 5, 20, -1, 4, 35, 5, 1, 0))

    def test_create_course_with_too_many_exercise_group(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(self.user.user_id,
                                                                                   "Ohjelmistotekniikka", 5, 20, 101, 4, 35, 5, 1, 0))

    def test_create_course_with_negative_project(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(self.user.user_id,
                                                                                   "Ohjelmistotekniikka", 5, 20, 0, -1, 0, 5, 1, 12))

    def test_create_course_with_too_many_project(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(self.user.user_id,
                                                                                   "Ohjelmistotekniikka", 5, 20, 0, 101, 0, 5, 1, 12))

    def test_create_course_with_negative_exam(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(self.user.user_id,
                                                                                   "Ohjelmistotekniikka", 5, 20, 0, 40, -1, 5, 1, 0))

    def test_create_course_with_too_many_exam(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(self.user.user_id,
                                                                                   "Ohjelmistotekniikka", 5, 20, 0, 40, 101, 5, 1, 0))

    def test_create_course_with_negative_peer_review(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(self.user.user_id,
                                                                                   "Ohjelmistotekniikka", 5, 20, 0, 40, 0, -1, 1, 17))

    def test_create_course_with_too_many_peer_review(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(self.user.user_id,
                                                                                   "Ohjelmistotekniikka", 5, 20, 0, 40, 0, 101, 1, 17))

    def test_create_course_with_negative_feedback(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(self.user.user_id,
                                                                                   "Ohjelmistotekniikka", 5, 33, 2, 40, 1, 25, -1, 0))

    def test_create_course_with_too_many_feedback(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(self.user.user_id,
                                                                                   "Ohjelmistotekniikka", 5, 33, 2, 40, 1, 25, 101, 0))

    def test_create_course_with_negative_other(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(self.user.user_id,
                                                                                   "Ohjelmistotekniikka", 1, 20, 0, 40, 10, 5, 1, -1))

    def test_create_course_with_too_many_other(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(self.user.user_id,
                                                                                   "Ohjelmistotekniikka", 1, 20, 0, 40, 10, 5, 1, 101))

    def test_get_courses(self):
        course1 = course_service.create_course(self.user.user_id,
                                               "Ohjelmistotekniikka", 5, 20, 0, 40, 0, 5, 1, 0)
        course2 = course_service.create_course(self.user.user_id,
                                               "Tietorakenteet ja algoritmit", 5, 60, 0, 5, 0, 5, 1, 0)
        course3 = course_service.create_course(self.user.user_id,
                                               "Ohjelmoinnin perusteet", 10, 0, 16, 40, 1, 2, 1, 10)

        courses = course_service.get_courses()

        self.assertEqual(len(courses), 3)
        self.assertEqual(courses[0].user_id, self.user.user_id)
        self.assertEqual(courses[0].name, course1.name)
        self.assertEqual(courses[1].user_id, self.user.user_id)
        self.assertEqual(courses[1].name, course2.name)
        self.assertEqual(courses[2].user_id, self.user.user_id)
        self.assertEqual(courses[2].name, course3.name)

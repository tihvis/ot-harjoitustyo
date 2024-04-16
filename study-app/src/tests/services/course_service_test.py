import unittest
from repositories.course_repository import course_repository
from repositories.user_repository import user_repository
from services.course_service import course_service, InvalidValuesError
from services.user_service import user_service


class TestCourseService(unittest.TestCase):
    def setUp(self):
        course_repository.delete_all()
        user_repository.delete_all()
        self.points = {1: 30, 2: 10, 3: 25,
                       4: 50, 5: 7, 6: 1, 7: 0}
        self.user = user_service.create_user("test", "Test1234", "Test1234")

    def test_create_course_with_valid_values(self):
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, self.points)

        self.assertEqual(course.name, "Ohjelmistotekniikka")
        self.assertEqual(course.ects_credits, 5)
        self.assertEqual(course.points, self.points)

    def test_create_course_with_no_name(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "", 5, self.points))

    def test_create_course_with_too_long_name(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "ohjelmistoohjelmistoohjelmistoohjelmistoohjelmistoa", 5, self.points))

    def test_create_course_with_negative_credits(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", -1, self.points))

    def test_create_course_with_too_many_credits(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 51, self.points))

    def test_create_course_with_negative_exercises(self):
        self.points["exercises"] = -1
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 10, self.points))

    def test_create_course_with_too_many_exercises(self):
        self.points["exercises"] = 101
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 10, self.points))

    def test_create_course_with_negative_exercise_group(self):
        self.points["exercise_group"] = -1
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 5, self.points))

    def test_create_course_with_too_many_exercise_group(self):
        self.points["exercise_group"] = 101
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 5, self.points))

    def test_create_course_with_negative_project(self):
        self.points["project"] = -1
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 5, self.points))

    def test_create_course_with_too_many_project(self):
        self.points["project"] = 101
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 5, self.points))

    def test_create_course_with_negative_exam(self):
        self.points["exam"] = -1
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 5, self.points))

    def test_create_course_with_too_many_exam(self):
        self.points["exam"] = 101
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 5, self.points))

    def test_create_course_with_negative_peer_review(self):
        self.points["peer_review"] = -1
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 5, self.points))

    def test_create_course_with_too_many_peer_review(self):
        self.points["peer_review"] = 101
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 5, self.points))

    def test_create_course_with_negative_feedback(self):
        self.points["feedback"] = -1
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 5, self.points))

    def test_create_course_with_too_many_feedback(self):
        self.points["feedback"] = 101
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 5, self.points))

    def test_create_course_with_negative_other(self):
        self.points["other"] = -1
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 1, self.points))

    def test_create_course_with_too_many_other(self):
        self.points["other"] = 101
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 1, self.points))

    def test_get_courses_when_single_user(self):
        c1 = course_service.create_course(self.user.user_id,
                                          "Ohjelmistotekniikka", 5, self.points)

        c2 = course_service.create_course(self.user.user_id,
                                          "Tietorakenteet ja algoritmit", 10, self.points)

        c3 = course_service.create_course(self.user.user_id,
                                          "Ohjelmoinnin perusteet", 10, self.points)

        courses = course_service.get_courses()

        self.assertEqual(len(courses), 3)
        self.assertEqual(courses[0].user_id, self.user.user_id)
        self.assertEqual(courses[0].name, c1.name)
        self.assertEqual(courses[1].user_id, self.user.user_id)
        self.assertEqual(courses[1].name, c2.name)
        self.assertEqual(courses[2].user_id, self.user.user_id)
        self.assertEqual(courses[2].name, c3.name)

    def test_get_course_when_multiple_users(self):
        user2 = user_service.create_user("second", "Second1234", "Second1234")
        user3 = user_service.create_user("third", "Third1234", "Third1234")

        c1 = course_service.create_course(self.user.user_id,
                                          "Ohjelmistotekniikka", 5, self.points)

        c2 = course_service.create_course(user2.user_id,
                                          "Tietorakenteet ja algoritmit", 10, self.points)

        c3 = course_service.create_course(user3.user_id,
                                          "Ohjelmoinnin perusteet", 10, self.points)

        courses = course_service.get_courses()

        self.assertEqual(len(courses), 3)
        self.assertEqual(courses[0].user_id, self.user.user_id)
        self.assertEqual(courses[0].name, c1.name)
        self.assertEqual(courses[1].user_id, user2.user_id)
        self.assertEqual(courses[1].name, c2.name)
        self.assertEqual(courses[2].user_id, user3.user_id)
        self.assertEqual(courses[2].name, c3.name)

    def test_course_points_are_correct(self):
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, self.points)

        self.assertEqual(course.points, self.points)

    def test_missing_course_points_are_correct(self):
        points = {1: 30, 3: 25, 4: 50}
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, points)

        self.assertEqual(course.points, points)

    def test_get_course_by_userid(self):
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, self.points)

        courses = course_service.get_courses_by_user_id(self.user.user_id)

        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0].name, course.name)

    def test_delete_course_when_only_one_course(self):
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, self.points)

        course_service.delete_course(course.course_id)

        courses = course_service.get_courses()

        self.assertEqual(len(courses), 0)

    def test_delete_course_when_multiple_courses(self):
        course1 = course_service.create_course(self.user.user_id,
                                               "Ohjelmistotekniikka", 5, self.points)

        course2 = course_service.create_course(self.user.user_id,
                                               "Tietorakenteet ja algoritmit", 10, self.points)

        course_service.delete_course(course1.course_id)

        courses = course_service.get_courses()

        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0].name, course2.name)

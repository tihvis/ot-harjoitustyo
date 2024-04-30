import unittest
from repositories.course_repository import course_repository
from repositories.user_repository import user_repository
from services.course_service import course_service, InvalidValuesError, InvalidCompletionValuesError
from services.user_service import user_service


class TestCourseService(unittest.TestCase):
    def setUp(self):
        course_repository.delete_all()
        user_repository.delete_all()
        self.max_points = {1: 30, 2: 10, 3: 25,
                           4: 50, 5: 7, 6: 1, 7: 0}
        self.user = user_service.create_user("test", "Test1234", "Test1234")

    def test_create_course_with_valid_values(self):
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, self.max_points)

        self.assertEqual(course.name, "Ohjelmistotekniikka")
        self.assertEqual(course.ects_credits, 5)
        self.assertEqual(course.max_points, self.max_points)

    def test_create_course_with_no_name(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "", 5, self.max_points))

    def test_create_course_with_too_long_name(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "ohjelmistoohjelmistoohjelmistoohjelmistoohjelmistoa", 5, self.max_points))

    def test_create_course_with_negative_credits(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", -1, self.max_points))

    def test_create_course_with_too_many_credits(self):
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 51, self.max_points))

    def test_create_course_with_negative_exercises(self):
        self.max_points["exercises"] = -1
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 10, self.max_points))

    def test_create_course_with_too_many_exercises(self):
        self.max_points["exercises"] = 101
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 10, self.max_points))

    def test_create_course_with_negative_exercise_group(self):
        self.max_points["exercise_group"] = -1
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 5, self.max_points))

    def test_create_course_with_too_many_exercise_group(self):
        self.max_points["exercise_group"] = 101
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 5, self.max_points))

    def test_create_course_with_negative_project(self):
        self.max_points["project"] = -1
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 5, self.max_points))

    def test_create_course_with_too_many_project(self):
        self.max_points["project"] = 101
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 5, self.max_points))

    def test_create_course_with_negative_exam(self):
        self.max_points["exam"] = -1
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 5, self.max_points))

    def test_create_course_with_too_many_exam(self):
        self.max_points["exam"] = 101
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 5, self.max_points))

    def test_create_course_with_negative_peer_review(self):
        self.max_points["peer_review"] = -1
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 5, self.max_points))

    def test_create_course_with_too_many_peer_review(self):
        self.max_points["peer_review"] = 101
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 5, self.max_points))

    def test_create_course_with_negative_feedback(self):
        self.max_points["feedback"] = -1
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 5, self.max_points))

    def test_create_course_with_too_many_feedback(self):
        self.max_points["feedback"] = 101
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 5, self.max_points))

    def test_create_course_with_negative_other(self):
        self.max_points["other"] = -1
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 1, self.max_points))

    def test_create_course_with_too_many_other(self):
        self.max_points["other"] = 101
        self.assertRaises(InvalidValuesError, lambda: course_service.create_course(
            self.user.user_id, "Ohjelmistotekniikka", 1, self.max_points))

    def test_get_courses_when_single_user(self):
        c1 = course_service.create_course(self.user.user_id,
                                          "Ohjelmistotekniikka", 5, self.max_points)

        c2 = course_service.create_course(self.user.user_id,
                                          "Tietorakenteet ja algoritmit", 10, self.max_points)

        c3 = course_service.create_course(self.user.user_id,
                                          "Ohjelmoinnin perusteet", 10, self.max_points)

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
                                          "Ohjelmistotekniikka", 5, self.max_points)

        c2 = course_service.create_course(user2.user_id,
                                          "Tietorakenteet ja algoritmit", 10, self.max_points)

        c3 = course_service.create_course(user3.user_id,
                                          "Ohjelmoinnin perusteet", 10, self.max_points)

        courses = course_service.get_courses()

        self.assertEqual(len(courses), 3)
        self.assertEqual(courses[0].user_id, self.user.user_id)
        self.assertEqual(courses[0].name, c1.name)
        self.assertEqual(courses[1].user_id, user2.user_id)
        self.assertEqual(courses[1].name, c2.name)
        self.assertEqual(courses[2].user_id, user3.user_id)
        self.assertEqual(courses[2].name, c3.name)

    def test_course_points_are_correct_when_all_points_given(self):
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, self.max_points)

        self.assertEqual(course.max_points, self.max_points)

    def test_course_points_are_correct_when_part_of_course_points_given(self):
        max_points = {1: 30, 3: 25, 4: 50}
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, max_points)

        self.assertEqual(course.max_points, max_points)

    def test_get_course_by_userid(self):
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, self.max_points)

        courses = course_service.get_courses_by_user_id(self.user.user_id)

        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0].name, course.name)

    def test_delete_course_when_only_one_course(self):
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, self.max_points)

        course_service.delete_course(course.course_id)

        courses = course_service.get_courses()

        self.assertEqual(len(courses), 0)

    def test_delete_course_when_multiple_courses(self):
        course1 = course_service.create_course(self.user.user_id,
                                               "Ohjelmistotekniikka", 5, self.max_points)

        course2 = course_service.create_course(self.user.user_id,
                                               "Tietorakenteet ja algoritmit", 10, self.max_points)

        course_service.delete_course(course1.course_id)

        courses = course_service.get_courses()

        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0].name, course2.name)

    def test_update_all_course_tasks_with_valid_values(self):
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, {1: 10, 2: 9, 3: 8, 4: 7, 5: 6, 6: 5, 7: 4})

        completed_points = {1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}

        course_service.update_course(course.course_id, completed_points)

        self.assertEqual(course_service.get_completed_points_by_course(
            course.course_id), completed_points)

    def test_update_part_of_course_tasks_with_valid_values(self):
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, {1: 10, 2: 9, 3: 8, 4: 7, 5: 6, 6: 5, 7: 4})

        completed_points = {1: 7, 2: 6, 5: 5}

        course_service.update_course(course.course_id, completed_points)

        self.assertEqual(course_service.get_completed_points_by_course(
            course.course_id)[1], completed_points[1])
        self.assertEqual(course_service.get_completed_points_by_course(
            course.course_id)[2], completed_points[2])
        self.assertEqual(course_service.get_completed_points_by_course(
            course.course_id)[3], 0)
        self.assertEqual(course_service.get_completed_points_by_course(
            course.course_id)[4], 0)
        self.assertEqual(course_service.get_completed_points_by_course(
            course.course_id)[5], completed_points[5])
        self.assertEqual(course_service.get_completed_points_by_course(
            course.course_id)[6], 0)
        self.assertEqual(course_service.get_completed_points_by_course(
            course.course_id)[7], 0)

    def test_update_course_with_negative_points(self):
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, self.max_points)

        completed_points = {1: -1, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}

        self.assertRaises(InvalidValuesError, lambda: course_service.update_course(
            course.course_id, completed_points))

    def test_update_course_with_too_many_points(self):
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, self.max_points)

        completed_points = {1: 31}

        self.assertRaises(InvalidValuesError, lambda: course_service.update_course(
            course.course_id, completed_points))

    def test_update_course_with_max_value_of_points(self):
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, self.max_points)

        completed_points = {1: 30}

        course_service.update_course(course.course_id, completed_points)

        self.assertEqual(course_service.get_completed_points_by_course(
            course.course_id)[1], completed_points[1])

    def test_set_course_done_with_valid_values(self):
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, self.max_points)

        course_service.set_done(course.course_id, 5, "20.04.2024")

        self.assertEqual(
            len(course_service.get_completed_courses_by_user_id(self.user.user_id)), 1)

    def test_set_course_done_with_invalid_values(self):
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, self.max_points)

        self.assertRaises(InvalidCompletionValuesError, lambda: course_service.set_done(
            course.course_id, "Valitse", "20.04.2024"))

        self.assertRaises(ValueError, lambda: course_service.set_done(
            course.course_id, 5, "35.04.2024"))

        self.assertRaises(ValueError, lambda: course_service.set_done(
            course.course_id, 5, "testi"))

    def test_set_one_course_done_and_one_ongoing(self):
        course1 = course_service.create_course(self.user.user_id,
                                               "Ohjelmistotekniikka", 4, self.max_points)

        course_service.create_course(self.user.user_id,
                                     "Tietorakenteet ja algoritmit", 10, self.max_points)

        course_service.set_done(course1.course_id, 5, "20.04.2024")

        self.assertEqual(
            len(course_service.get_completed_courses_by_user_id(self.user.user_id)), 1)
        self.assertEqual(
            len(course_service.get_courses_by_user_id(self.user.user_id)), 1)

    def test_check_completed_credits_when_no_completed_courses(self):
        self.assertEqual(course_service.get_completed_credits_by_user_id(
            self.user.user_id), 0)

    def test_check_completed_credits_when_one_completed_course(self):
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, self.max_points)

        course_service.set_done(course.course_id, 5, "20.04.2024")

        self.assertEqual(course_service.get_completed_credits_by_user_id(
            self.user.user_id), 5)

    def test_check_completed_credits_when_multiple_completed_courses(self):
        course1 = course_service.create_course(self.user.user_id,
                                               "Ohjelmistotekniikka", 5, self.max_points)

        course2 = course_service.create_course(self.user.user_id,
                                               "Tietorakenteet ja algoritmit", 7, self.max_points)

        course_service.set_done(course1.course_id, 5, "30.04.2024")
        course_service.set_done(course2.course_id, 7, "29.04.2024")

        self.assertEqual(course_service.get_completed_credits_by_user_id(
            self.user.user_id), 12)

    def test_check_completed_credits_when_one_completed_course_and_one_ongoing(self):
        course1 = course_service.create_course(self.user.user_id,
                                               "Ohjelmistotekniikka", 5, self.max_points)

        course_service.set_done(course1.course_id, 5, "25.04.2024")

        course_service.create_course(self.user.user_id,
                                     "Tietorakenteet ja algoritmit", 7, self.max_points)

        self.assertEqual(course_service.get_completed_credits_by_user_id(
            self.user.user_id), 5)

    def test_check_completed_credits_with_failed_course(self):
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, self.max_points)

        course_service.set_done(course.course_id, "Hylätty", "25.04.2024")

        self.assertEqual(course_service.get_completed_credits_by_user_id(
            self.user.user_id), 0)

    def test_check_average_grade_with_no_completed_courses(self):
        self.assertEqual(course_service.average_of_completed_courses_by_user_id(
            self.user.user_id), 0)

    def test_check_average_grade_with_one_completed_course(self):
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, self.max_points)

        course_service.set_done(course.course_id, 5, "25.04.2024")

        self.assertEqual(course_service.average_of_completed_courses_by_user_id(
            self.user.user_id), 5)

    def test_check_average_grade_with_completed_course_with_no_grade(self):
        course = course_service.create_course(self.user.user_id,
                                              "Ohjelmistotekniikka", 5, self.max_points)

        course_service.set_done(course.course_id, "Hyväksytty", "25.04.2024")

        self.assertEqual(course_service.average_of_completed_courses_by_user_id(
            self.user.user_id), 0)

    def test_check_average_grade_with_multiple_completed_courses(self):
        course1 = course_service.create_course(self.user.user_id,
                                               "Ohjelmistotekniikka", 5, self.max_points)

        course2 = course_service.create_course(self.user.user_id,
                                               "Tietorakenteet ja algoritmit", 5, self.max_points)

        course3 = course_service.create_course(self.user.user_id,
                                               "Tietokoneen toiminta", 2, self.max_points)

        course_service.set_done(course1.course_id, 5, "25.04.2020")
        course_service.set_done(course2.course_id, 3, "25.04.2021")
        course_service.set_done(course3.course_id, "Hyväksytty", "25.04.2022")

        self.assertEqual(course_service.average_of_completed_courses_by_user_id(
            self.user.user_id), 4)

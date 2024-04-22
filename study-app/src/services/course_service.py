from entities.course import Course

from repositories.course_repository import (
    course_repository as default_course_repository)


class InvalidValuesError(Exception):
    pass


class CourseService:
    def __init__(self, course_repository=default_course_repository):
        self._user = None
        self._course_repository = course_repository

    def create_course(self, user_id, name, ects_credits, max_points):
        if self.values_ok(name, ects_credits, max_points):
            course = self._course_repository.create(Course(
                user_id=user_id, name=name, ects_credits=ects_credits, max_points=max_points))

            return course

        raise InvalidValuesError

    def update_course(self, course_id, completed_points):
        if self.completed_points_ok(course_id, completed_points):
            self._course_repository.update(
                course_id=course_id, completed_points=completed_points)

        else:
            raise InvalidValuesError

    def get_courses(self):
        return self._course_repository.find_all()

    def get_courses_by_user_id(self, user_id):
        return self._course_repository.find_by_user_id(user_id)

    def delete_course(self, course_id):
        self._course_repository.delete_course(course_id)

    def get_max_points_by_course(self, course_id):
        return self._course_repository.get_max_points_by_course(course_id)

    def get_completed_points_by_course(self, course_id):
        return self._course_repository.get_completed_points_by_course(course_id)

    def values_ok(self, name, ects_credits, points):
        if not isinstance(name, str) or len(name) < 1 or len(name) > 50:
            return False
        if ects_credits < 0 or ects_credits > 50:
            return False
        for task in points:
            if points[task] < 0 or points[task] > 100:
                return False
        return True

    def completed_points_ok(self, course_id, completed_points):
        for task_id in completed_points:
            if int(completed_points[task_id]) < 0:
                return False
            if int(completed_points[task_id]) > self.get_max_points_by_course(course_id)[task_id]:
                return False
        return True


course_service = CourseService()

from entities.course import Course

from repositories.course_repository import (
    course_repository as default_course_repository)

from repositories.user_repository import (
    user_repository as default_user_repository)


class InvalidValuesError(Exception):
    pass


class CourseService:
    def __init__(self, course_repository=default_course_repository,
                 user_repository=default_user_repository):
        self._user = None
        self._course_repository = course_repository
        self._user_repository = user_repository

    def create_course(self, user_id, name, ects_credits, points):
        if self.values_ok(name, ects_credits, points):
            course = self._course_repository.create(Course(
                user_id=user_id, name=name, ects_credits=ects_credits, points=points))

            return course

        raise InvalidValuesError

    def update_course(self, course_id, name, ects_credits, points):
        pass
        # if self.values_ok(name, ects_credits, points):
        #     course = self._course_repository.update(Course(
        #         course_id=course_id, name=name, ects_credits=ects_credits, points=points))

        #     return course

        # raise InvalidValuesError

    def get_courses(self):
        return self._course_repository.find_all()

    def get_courses_by_user_id(self, user_id):
        return self._course_repository.find_by_user_id(user_id)

    def delete_course(self, course_id):
        self._course_repository.delete_course(course_id)

    def task_ids(self):
        return self._course_repository.get_task_ids()

    def get_name_of_task(self, task_id):
        return str(self._course_repository.get_name_of_task(task_id))

    def get_max_task_points(self, course_id, task):
        return str(self._course_repository.get_max_task_points(course_id, task))

    def get_completed_task_points(self, course_id, task):
        return str(self._course_repository.get_completed_task_points(course_id, task))

    def values_ok(self, name, ects_credits, points):
        if not isinstance(name, str) or len(name) < 1 or len(name) > 50:
            return False
        if ects_credits < 0 or ects_credits > 50:
            return False
        for task in points:
            if points[task] < 0 or points[task] > 100:
                return False
        return True


course_service = CourseService()

from entities.course import Course

from repositories.course_repository import (
    course_repository as default_course_repository)

from repositories.user_repository import (
    user_repository as default_user_repository)


class InvalidValuesError(Exception):
    pass


class CourseService:
    def __init__(
        self,
        course_repository=default_course_repository,
        user_repository=default_user_repository
    ):
        self._user = None
        self._course_repository = course_repository
        self._user_repository = user_repository

    def create_course(self, user_id, name, credits, exercises, exercise_group, project, exam, peer_review, feedback, other):
        if self.values_ok(name, credits, exercises, exercise_group, project, exam, peer_review, feedback, other):
            course = self._course_repository.create(Course(user_id=user_id, name=name, credits=credits, exercises=exercises, exercise_group=exercise_group, project=project, exam=exam, peer_review=peer_review, feedback=feedback, other=other))

            return course

        raise InvalidValuesError

    def get_courses(self):
        return self._course_repository.find_all()

    def get_courses_by_user_id(self, user_id):
        return self._course_repository.find_by_user_id(user_id)

    def delete_course(self, course_id):
        self._course_repository.delete_course(course_id)

    def values_ok(self, name, credits, exercises, exercise_group, project, exam, peer_review, feedback, other):
        if not isinstance(name, str) or len(name) < 1 or len(name) > 50:
            return False
        if credits < 0 or credits > 50:
            return False
        if exercises < 0 or exercises > 100:
            return False
        if exercise_group < 0 or exercise_group > 100:
            return False
        if project < 0 or project > 100:
            return False
        if exam < 0 or exam > 100:
            return False
        if peer_review < 0 or peer_review > 100:
            return False
        if feedback < 0 or feedback > 100:
            return False
        if other < 0 or other > 100:
            return False
        return True


course_service = CourseService()

from entities.course import Course
from services.user_service import user_service

from repositories.course_repository import (course_repository as default_course_repository)

from repositories.user_repository import (user_repository as default_user_repository)

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

    def create_course(self, name, credits, exercises, exercise_group, project, exam, peer_review, feedback, other):
        user_id = user_service.get_current_user().user_id
        if self.values_ok(name, credits, exercises, exercise_group, project, exam, peer_review, feedback, other):
            course = self._course_repository.create(Course(user_id=user_id, name=name, credits=credits, exercises=exercises, exercise_group=exercise_group, project=project, exam=exam, peer_review=peer_review, feedback=feedback, other=other))

            return course

        else:
            raise InvalidValuesError

    def get_courses(self):
        pass

    def values_ok(self, name, credits, exercises, exercise_group, project, exam, peer_review, feedback, other):
        if not isinstance(name, str) or len(name) < 1 or len(name) > 50:
            return False
        if not isinstance(credits, int) or credits < 0 or credits > 50:
            return False
        if not isinstance(exercises, int) or exercises > 100:
            return False
        if not isinstance(exercise_group, int) or exercise_group > 100:
            return False
        if not isinstance(project, int) or project > 100:
            return False
        if not isinstance(exam, int) or exam > 100:
            return False
        if not isinstance(peer_review, int) or peer_review > 100:
            return False
        if not isinstance(feedback, int) or feedback > 100:
            return False
        if not isinstance(other, int) or other > 100:
            return False
        return True

course_service = CourseService()
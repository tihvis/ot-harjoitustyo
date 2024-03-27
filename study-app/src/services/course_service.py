from entities.course import Course
from entities.user import User

from repositories.course_repository import (course_repository as default_course_repository)

from repositories.user_repository import (user_repository as default_user_repository)

class CourseService:
    def __init__(
        self,
        course_repository=default_course_repository,
        user_repository=default_user_repository
    ):
        self._user = None
        self._course_repository = course_repository
        self._user_repository = user_repository

    def create_course(self, name, credits, done, grade, completion_date, user):
        course = Course(name=name, credits=credits, done=done, grade=grade, completion_date=completion_date, user=self._user)

        return self._course_repository.create(course)

    def get_courses(self):
        if not self._user:
            return []

        courses = self._course_repository.find_by_username(self._user.username)
        ongoing_courses = filter(lambda course: not course.done, courses)

        return list(ongoing_courses)

    def set_course_done(self, course_id):
        self._course_repository.set_done(course_id)

course_service = CourseService()
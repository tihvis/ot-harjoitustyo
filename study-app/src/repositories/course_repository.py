from pathlib import Path
from entities.course import Course
from repositories.user_repository import user_repository
from config import STUDYAPP_FILE_PATH


class CourseRepository:
    def __init__(self, file_path):
        self._file_path = file_path

    def find_all(self):
        return self._read()

    def find_by_username(self, username):
        courses = self.find_all()

        user_courses = filter(
            lambda course: course.user and course.user.username == username, courses)

        return list(user_courses)

    def create(self, course):
        courses = self.find_all()

        courses.append(course)

        self._write(courses)

        return course

    def set_done(self, course_id, done=True):
        courses = self.find_all()

        for course in courses:
            if course.id == course_id:
                course.done = done
                break

        self._write(courses)

    def delete(self, course_id):
        courses = self.find_all()

        courses_without_id = filter(lambda course: course.id != course_id, courses)

        self._write(courses_without_id)

    def delete_all(self):
        self._write([])

    def _ensure_file_exists(self):
        Path(self._file_path).touch()

    def _read(self):
        courses = []

        self._ensure_file_exists()

        with open(self._file_path, encoding="utf-8") as file:
            for row in file:
                row = row.replace("\n", "")
                parts = row.split(";")

                course_id = parts[0]
                name = parts[1]
                credits = parts[2]
                done = parts[3] == "1"
                grade = parts[4]
                completion_date = parts[5]
                username = parts[6]

                user = user_repository.find_by_username(
                    username) if username else None

                courses.append(
                    Course(name, credits, course_id, done, grade, completion_date, user)
                )

        return courses

    def _write(self, courses):
        self._ensure_file_exists()

        with open(self._file_path, "w", encoding="utf-8") as file:
            for course in courses:
                row = f"{course.id};{course.name};{course.credits};{course.done};{course.grade};{course.completion_date};{course.user}"

                file.write(row+"\n")


course_repository = CourseRepository(STUDYAPP_FILE_PATH)
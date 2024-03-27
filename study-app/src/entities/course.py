import uuid

class Course:
    def __init__(self, name, credits, course_id=None, done=False, grade=None, completion_date=None, user=None):
        self.name = name
        self.credits = credits
        self.id = course_id or str(uuid.uuid4())
        self.done = done
        self.grade = grade
        self.completion_date = completion_date
        self.user = user
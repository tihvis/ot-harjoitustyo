class Course:
    def __init__(self, user_id, name, ects_credits, points=None,
                 completion=None,  course_id=None):
        self.user_id = user_id
        self.name = name
        self.ects_credits = ects_credits
        self.points = points
        self.completion = completion
        self.course_id = course_id

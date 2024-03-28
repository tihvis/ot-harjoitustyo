class Course:
    def __init__(self, user, name, credits, exercises, exercise_group, project, exam, peer_review, feedback, other, done=False, grade=None, completion_date=None):
        self.user = user
        self.name = name
        self.credits = credits
        self.exercises = exercises
        self.exercise_group = exercise_group
        self.project = project
        self.exam = exam
        self.peer_review = peer_review
        self.feedback = feedback
        self.other = other
        self.done = done
        self.grade = grade
        self.completion_date = completion_date

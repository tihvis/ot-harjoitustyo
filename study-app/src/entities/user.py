class User:
    def __init__(self, username, password, user_id=None):
        self.username = username
        self.password = password
        self.user_id = user_id

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.username == other.username and self.password == other.password
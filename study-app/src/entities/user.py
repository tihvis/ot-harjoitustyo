class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.username == other.username and self.password == other.password
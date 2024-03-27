import re
from entities.user import User

from repositories.user_repository import (
    user_repository as default_user_repository
)

class InvalidCredentialsError(Exception):
    pass

class UsernameExistsError(Exception):
    pass

class PasswordConfirmationError(Exception):
    pass

class InvalidPasswordError(Exception):
    pass

class UserService:
    def __init__(self, user_repository=default_user_repository):
        self._user = None
        self._user_repository = user_repository

    def login(self, username, password):
        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise InvalidCredentialsError("Virheellinen käyttäjätunnus tai salasana")

        self._user = user

        return user

    def get_current_user(self):
        return self._user

    def get_users(self):
        return self._user_repository.find_all()

    def logout(self):
        self._user = None

    def create_user(self, username, password, password2, login=True):
        existing_user = self._user_repository.find_by_username(username)

        if existing_user:
            raise UsernameExistsError(f"Käyttäjätunnus {username} on varattu.")

        if password != password2:
            raise PasswordConfirmationError("Syöttämäsi salasanat eivät vastanneet toisiaan.")

        if not re.match(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])", password) or len(password)<8:
            raise InvalidPasswordError("""Salasanassa tulee olla vähintään 8 merkkiä,
            ja siinä tulee olla vähintään yksi iso kirjain numero.""")

        user = self._user_repository.create(User(username, password))

        if login:
            self._user = user

        return user

user_service = UserService()

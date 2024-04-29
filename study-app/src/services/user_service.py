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
    """Käyttäjiin liittyvästä sovelluslogiikasta vastaava luokka.
    """

    def __init__(self, user_repository=default_user_repository):
        """Luokan konstruktori. Luo uuden sovelluslogiikasta vastaavan palvelun.

        Args:
            user_repository:
                Vapaaehtoinen, oletusarvoltaan UserRepository-olio.
                Olio, jolla on UserRepository-luokkaa vastaavat metodit.
        """

        self._user = None
        self._user_repository = user_repository

    def login(self, username, password):
        """Kirjaa käyttäjän sisään sovellukseen.

        Args:
            username: 
                Merkkijonoarvo, joka kuvaa kirjautuvan käyttäjän käyttäjätunnusta.
            password: 
                Merkkijonoarvo, joka kuvaa kirjautuvan käyttäjän salasanaa.

        Returns:
            Kirjautunut käyttäjä User-olion muodossa.

        Raises:
            InvalidCredentialsError:
                Virhe, jos käyttäjätunnus ja salasana eivät täsmää, tai käyttäjää ei ole olemassa.
        """

        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise InvalidCredentialsError

        self._user = user

        return user

    def get_current_user(self):
        """Palauttaa sisäänkirjautuneen käyttäjän.

        Returns:
            Kirjautunut käyttäjä User-oliona.
        """

        return self._user

    def get_users(self):
        """Palauttaa kaikki käyttäjät.

        Returns:
            Lista kaikista käyttäjistä User-olioina.
        """

        return self._user_repository.find_all()

    def logout(self):
        """Kirjaa sisäänkirjautuneen käyttäjän ulos.
        """

        self._user = None

    def create_user(self, username, password, password2):
        """Luo uuden käyttäjän ja kirjaa hänet sisään.

        Args:
            username: 
                Merkkijonoarvo, joka kuvastaa käyttäjän käyttäjätunnusta.
            password: 
                Merkkijonoarvo, joka kuvastaa käyttäjän salasanaa.
            password2:
                Merkkijonoarvo, joka kuvastaa käyttäjän uudelleensyötettyä salasanaa.

        Raises:
            UsernameExistsError: 
                Virhe, kun käyttäjätunnus on jo käytössä.
            InvalidCredentialsError:
                Virhe, kun käyttäjätunnus tai salasana ei täytä pituusvaatimuksia.
            PasswordConfirmationError:
                Virhe, kun toistettu salasana ei täsmää alkuperäiseen.
            InvalidPasswordError:
                Virhe, kun salasana ei täytä annettuja merkkivaatimuksia.

        Returns:
            Luotu käyttäjä User-oliona.
        """

        existing_user = self._user_repository.find_by_username(username)

        if existing_user:
            raise UsernameExistsError

        if len(username) < 4 or len(username) > 30 or len(password) < 8 or len(password) > 30:
            raise InvalidCredentialsError

        if password != password2:
            raise PasswordConfirmationError

        if not re.match(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])", password):
            raise InvalidPasswordError

        user = self._user_repository.create(User(username, password))

        self._user = user

        return user


user_service = UserService()

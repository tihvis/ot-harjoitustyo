from entities.user import User
from database_connection import get_database_connection


def get_user_by_row(row):
    return User(row["username"], row["password"], row["user_id"]) if row else None


class UserRepository:
    """Käyttäjiin liittyvistä tietokantaoperaatioista vastaava luokka.
    """

    def __init__(self, connection):
        """Luokan konstruktori.

        Args:
            connection:
                Tietokantayhteyden Connection-olio.
        """

        self._connection = connection

    def find_all(self):
        """Palauttaa kaikki käyttäjät.

        Returns:
            Palauttaa listan User-olioita.
        """

        cursor = self._connection.cursor()

        cursor.execute("select * from users")

        rows = cursor.fetchall()

        return list(map(get_user_by_row, rows))

    def find_by_username(self, username):
        """Palauttaa käyttäjän käyttäjätunnuksen perusteella.

        Args:
            username: 
                Merkkijonoarvo, joka kuvaa käyttäjätunnusta jonka käyttäjä palautetaan.

        Returns:
            Palauttaa User-olion, jos käyttäjätunnuksen omaava 
            käyttäjä on tietokannassa. Muussa tapauksessa None.
        """

        cursor = self._connection.cursor()

        cursor.execute(
            "select * from users where username = ?",
            (username,)
        )

        user = cursor.fetchone()

        return User(user[1], user[2], user[0]) if user else None

    def create(self, user):
        """Tallentaa uuden käyttäjän tietokantaan.

        Args:
            user: 
                User-olio, joka kuvaa tallennettavaa käyttäjää.

        Returns:
            Palauttaa tallennetun User-olion.
        """

        cursor = self._connection.cursor()

        cursor.execute(
            "insert into users (username, password) values (?, ?)",
            (user.username, user.password)
        )

        user_id = cursor.lastrowid

        self._connection.commit()

        return User(user.username, user.password, user_id)

    def delete_all(self):
        """Poistaa kaikki käyttäjät tietokannasta.
        """

        cursor = self._connection.cursor()

        cursor.execute("delete from users")

        self._connection.commit()


user_repository = UserRepository(get_database_connection())

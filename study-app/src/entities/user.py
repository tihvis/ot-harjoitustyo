class User:
    """Luokka, joka kuvaa käyttäjää.

        Attributes:
            username: 
                Merkkijonoarvo, joka kuvaa käyttäjän käyttäjätunnusta.
            password: 
                Merkkijonoarvo, joka kuvaa käyttäjän salasanaa.
            user_id: 
                Merkkijonoarvo, joka kuvaa käyttäjän id:tä.
    """

    def __init__(self, username, password, user_id=None):
        """Luokan konstruktori, joka luo uuden käyttäjän.

        Args:
            username: 
                Merkkijonoarvo, joka kuvaa käyttäjän käyttäjätunnusta.
            password: 
                Merkkijonoarvo, joka kuvaa käyttäjän salasanaa.
            user_id: 
                Vapaaehtoinen, oletusarvoltaan None.
                Merkkijonoarvo, joka kuvaa käyttäjän id:tä.
        """

        self.user_id = user_id
        self.username = username
        self.password = password

class Course:
    """Luokka, joka kuvaa kurssia.

        Attributes:
            user_id: 
                Merkkijonoarvo, joka kuvaa käyttäjän id:tä.
            name: 
                Merkkijono, joka kuvaa kurssin nimeä.
            ects_credits: 
                Merkkijonoarvo, joka kuvaa kurssin opintopistemäärää.
            max_points: 
                Sanakirja, joka kuvaa kurssin eri tehtävistä kertyviä maksimipistemääriä.
            completion: 
                Sanakirja, joka kuvaa kurssin suoritustietoja: 
                suorituspvm, arvosana, suoritettu.
            course_id: 
                Merkkijonoarvo, joka kuvaa kurssin id:tä.
    """

    def __init__(self, user_id, name, ects_credits, max_points=None,
                 completion=None,  course_id=None):
        """Luokan konstruktori, joka luo uuden kurssin.

        Args:
            user_id: 
                Merkkijonoarvo, joka kuvaa käyttäjän id:tä.
            name:
                Merkkijono, joka kuvaa kurssin nimeä.
            ects_credits:
                Merkkijonoarvo, joka kuvaa kurssin opintopistemäärää.
            max_points:
                Vapaaehtoinen, oletusarvoltaan None.
                Sanakirja, joka kuvaa kurssin eri tehtävistä
                kertyviä maksimipistemääriä.
            completion:
                Vapaaehtoinen, oletusarvoltaan None.
                Sanakirja, joka kuvaa kurssin suoritustietoja:
                suorituspvm, arvosana, suoritettu.
            course_id:
                Vapaaehtoinen, oletusarvoltaan None.
                Merkkijonoarvo, joka kuvaa kurssin id:tä.
        """

        self.user_id = user_id
        self.name = name
        self.ects_credits = ects_credits
        self.max_points = max_points
        self.completion = completion
        self.course_id = course_id

from datetime import datetime
from entities.course import Course

from repositories.course_repository import (
    course_repository as default_course_repository)


class InvalidValuesError(Exception):
    pass


class InvalidCompletionValuesError(Exception):
    pass


class CourseService:
    """Kursseihin liittyvästä sovelluslogiikasta vastaava luokka.
    """

    def __init__(self, course_repository=default_course_repository):
        """Luokan konstruktori. Luo uuden sovelluslogiikasta vastaavan palvelun.

        Args:
            course_repository:
                Vapaaehtoinen, oletusarvoltaan CourseRepository-olio.
                Olio, jolla on CourseRepository-luokkaa vastaavat metodit.
        """

        self._user = None
        self._course_repository = course_repository

    def create_course(self, user_id, name, ects_credits, max_points):
        """Luo uuden Kurssin.

        Args:
            user_id: 
                Merkkijonoarvo, joka kuvaa käyttäjän id:tä.
            name: 
                Merkkijono, joka kuvaa kurssin nimeä.
            ects_credits: 
                Merkkijonoarvo, joka kuvaa kurssin opintopistemäärää.
            max_points:
                Sanakirja, joka kuvaa kurssin eri tehtävistä kertyviä maksimipistemääriä.
                Avaimina tehtävän id:t ja arvoina maksimipistemäärät.

        Raises:
            InvalidValuesError:
                Virhe, jos kurssin nimi, opintopistemäärä tai tehtäväpisteet ovat virheellisiä.

        Returns:
            Luotu kurssi Course-oliona.
        """

        if self._course_info_ok(name, ects_credits, max_points):
            course = self._course_repository.create(Course(
                user_id=user_id, name=name, ects_credits=ects_credits, max_points=max_points))

            return course

        raise InvalidValuesError

    def update_course(self, course_id, completed_points):
        """Päivittää kurssin suoritettuja pistemääriä.

        Args:
            course_id: 
                Merkkijonoarvo, joka kuvaa päivitettävän kurssin id:tä.
            completed_points: 
                Sanakirja, jossa avaimina ovat tehtävien id:t ja arvoina uudet suoritetut pisteet.

        Raises:
            InvalidValuesError: Virhe, jos suoritetut pisteet ovat virheellisiä.
        """

        if self._completed_points_ok(course_id, completed_points):
            self._course_repository.update(
                course_id=course_id, completed_points=completed_points)

        else:
            raise InvalidValuesError

    def set_done(self, course_id, grade, completion_date):
        """Merkitsee kurssin suoritetuksi.

        Args:
            course_id:
                Merkkijonoarvo, joka kuvaa suoritettavaksi merkittävän kurssin id:tä.
            grade:
                Merkkijonoarvo, joka kuvaa suoritetun kurssin arvosanaa.
            completion_date:
                Merkkijonoarvo, joka kuvaa suoritetun kurssin suorituspäivämäärää.

        Raises:
            InvalidCompletionValuesError:
                Virhe, jos arvosana tai suorituspäivämäärä ovat virheellisiä.
        """

        if self._completion_values_ok(grade, completion_date):
            self._course_repository.set_done(
                course_id=course_id, grade=grade, completion_date=completion_date)
        else:
            raise InvalidCompletionValuesError

    def get_courses(self):
        """Palauttaa kaikki kurssit.

        Returns:
            Lista kaikista kursseista Course-olioina.
        """

        return self._course_repository.find_all()

    def get_courses_by_user_id(self, user_id):
        """Palauttaa käyttäjän käynnissä olevat kurssit käyttäjän id:n perusteella.

        Args:
            user_id: 
                Merkkijonoarvo, joka kuvaa käyttäjän id:tä.

        Returns:
            Lista käyttäjän käynnissä olevista kursseista Course-olioina.
        """

        return self._course_repository.find_ongoing_courses_by_user_id(user_id)

    def get_completed_courses_by_user_id(self, user_id):
        """Palauttaa käyttäjän suoritetut kurssit käyttäjän id:n perusteella.

        Args:
            user_id: 
                Merkkijonoarvo, joka kuvaa käyttäjän id:tä.

        Returns:
            Lista käyttäjän suoritetuista kursseista Course-olioina.
        """

        return self._course_repository.find_completed_courses_by_user_id(user_id)

    def get_completed_credits_by_user_id(self, user_id):
        """Palauttaa käyttäjän suorittamat opintopisteet käyttäjän id:n perusteella.

        Args:
            user_id: 
                Merkkijonoarvo, joka kuvaa käyttäjän id:tä.

        Returns:
            Kokonaisluku, joka kuvaa käyttäjän suorittamia opintopisteitä.
        """
        total_credits = 0

        for course in self._course_repository.find_completed_courses_by_user_id(user_id):
            if course.completion["grade"] != "Hylätty":
                total_credits += course.ects_credits

        return total_credits

    def average_of_completed_courses_by_user_id(self, user_id):
        """Palauttaa käyttäjän suorittamien kurssien keskiarvon käyttäjän id:n perusteella.

        Args:
            user_id: 
                Merkkijonoarvo, joka kuvaa käyttäjän id:tä.

        Returns:
            Liukuluku, joka kuvaa käyttäjän suorittamien kurssien keskiarvoa.
        """

        total_grades = 0
        total_credits = 0

        for course in self._course_repository.find_completed_courses_by_user_id(user_id):
            if isinstance(course.completion["grade"], int):
                total_credits += course.ects_credits
                total_grades += course.completion["grade"] * \
                    course.ects_credits

        if total_credits == 0:
            return 0

        return round(total_grades / total_credits, 2)

    def delete_course(self, course_id):
        """Poistaa kurssin sen id:n perusteella.

        Args:
            course_id: 
                Merkkijonoarvo, joka kuvaa kurssin id:tä.
        """

        self._course_repository.delete_course(course_id)

    def get_max_points_by_course(self, course_id):
        """Palauttaa kurssin tehtävien maksimipistemäärät kurssin id:n perusteella.

        Returns:
            Sanakirja, jossa avaimina kyseisen kurssin tehtävien id:t ja arvoina maksimipistemäärät.
        """

        return self._course_repository.get_max_points_by_course(course_id)

    def get_completed_points_by_course(self, course_id):
        """Palauttaa kurssin tähän asti suoritetut pisteet kurssin id:n perusteella.

        Args:
            course_id: 
                Merkkijonoarvo, joka kuvaa kurssin id:tä.

        Returns:
            Sanakirja, jossa avaimina kyseisen kurssin tehtävien id:t 
            ja arvoina tähän asti suoritetut pisteet.
        """

        return self._course_repository.get_completed_points_by_course(course_id)

    def _course_info_ok(self, name, ects_credits, max_points):
        """Tarkistaa, että käyttäjän syöttämät kurssitiedot ovat vaatimuksien mukaiset.

        Args:
            name: 
                Merkkijonoarvo, joka kuvaa kurssin nimeä.
            ects_credits:
                Merkkijonoarvo, joka kuvaa kurssin opintopistemäärää.
            max_points:
                Sanakirja, joka kuvaa kurssin eri tehtäville asetettuja
                maksimipistemääriä.
                Avaimina tehtävien id:t ja arvoina maksimipistemäärät.

        Returns:
            True, jos arvot ovat vaatimuksien mukaiset, muutoin False.
        """

        if not isinstance(name, str) or len(name) < 1 or len(name) > 50:
            return False
        if ects_credits < 0 or ects_credits > 50:
            return False
        for task in max_points:
            if max_points[task] < 0 or max_points[task] > 100:
                return False
        return True

    def _completed_points_ok(self, course_id, completed_points):
        """Tarkistaa, että käyttäjän syöttämät päivitetyt pistemäärät
        ovat vaatimuksien mukaiset.

        Args:
            course_id: 
                Merkkijonoarvo, joka kuvaa kurssin id:tä.
            completed_points:
                Sanakirja, joka kuvaa kurssin eri tehtävien suoritettuja pistemääriä.
                Avaimina tehtävien id:t ja arvoina suoritetut pistemäärät.

        Returns:
            True, jos arvot ovat vaatimuksien mukaiset, muutoin False.
        """

        for task_id in completed_points:
            if int(completed_points[task_id]) < 0:
                return False
            if int(completed_points[task_id]) > self.get_max_points_by_course(course_id)[task_id]:
                return False
        return True

    def _completion_values_ok(self, grade, completion_date):
        """Tarkistaa, että käyttäjän syöttämät kurssin suoritustiedot ovat vaatimuksien mukaiset.

        Args:
            grade: 
                Merkkijonoarvo, joka kuvaa suoritetun kurssin arvosanaa.
            completion_date:
                Merkkijonoarvo, joka kuvaa suoritetun kurssin suorituspäivämäärää.

        Returns:
            True, jos arvot ovat vaatimuksien mukaiset, muutoin False.
        """

        if grade == "Valitse":
            return False
        if not datetime.strptime(completion_date, "%d.%m.%Y").date():
            return False
        return True


course_service = CourseService()

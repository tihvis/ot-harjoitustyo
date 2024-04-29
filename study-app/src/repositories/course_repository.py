from entities.course import Course
from database_connection import get_database_connection


class CourseRepository:
    """Kursseihin liittyvistä tietokantaoperaatioista vastaava luokka.
    """

    def __init__(self, connection):
        """Luokan konstruktori.

        Args:
            connection:
                Tietokantayhteyden Connection-olio.
        """

        self._connection = connection

    def find_all(self):
        """Palauttaa kaikki kurssit.

        Returns:
            Palauttaa listan Course-olioita.
        """

        cursor = self._connection.cursor()

        query = "SELECT * FROM courses"

        cursor.execute(query)

        courses = cursor.fetchall()

        return self._create_course_object(courses)

    def find_ongoing_courses_by_user_id(self, user_id):
        """Palauttaa käyttäjän käynnissäolevat kurssit käyttäjän id:n perusteella.

        Args:
            user_id: Käyttäjän, jonka kurssit halutaan hakea, id.

        Returns:
            Palauttaa listan Course-olioita.
        """

        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * FROM courses WHERE user_id = ? and done = ?", (user_id, 0))

        courses = cursor.fetchall()

        return self._create_course_object(courses)

    def find_completed_courses_by_user_id(self, user_id):
        """Palauttaa käyttäjän suoritetut kurssit käyttäjän id:n perusteella.

        Args:
            user_id: Käyttäjän, jonka kurssit halutaan hakea, id.

        Returns:
            Palauttaa listan Course-olioita.
        """

        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * FROM courses WHERE user_id = ? and done = ?", (user_id, 1))

        courses = cursor.fetchall()

        return self._create_course_object(courses)

    def get_max_points_by_course(self, course_id):
        """Palauttaa kurssin tehtävien maksimipistemäärät kurssin id:n perusteella.

        Args:
            course_id: Kurssin, jonka tehtävien maksimipistemäärät halutaan hakea, id.

        Returns:
            Palauttaa sanakirjan, jossa avaimina ovat tehtävien id:t ja arvoina maksimipistemäärät.
        """

        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT task_id, max_points FROM course_points WHERE course_id = ?", (course_id,))

        rows = cursor.fetchall()

        return {row[0]: row[1] for row in rows}

    def get_completed_points_by_course(self, course_id):
        """Palauttaa kurssin tehtävien suoritettujen pisteiden määrät kurssin id:n perusteella.

        Args:
            course_id: Kurssin, jonka tehtävien suoritettujen pisteiden määrät halutaan hakea, id.

        Returns:
            Palauttaa sanakirjan, jossa avaimina ovat tehtävien id:t ja arvoina pistemäärät.
        """

        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT task_id, completed_points FROM course_points WHERE course_id = ?", (course_id,))

        rows = cursor.fetchall()

        return {row[0]: row[1] for row in rows}

    def get_completion_info(self, course_id):
        """Palauttaa kurssin suoritustiedot kurssin id:n perusteella.

        Args:
            course_id: Kurssin, jonka suoritustiedot halutaan hakea, id.

        Returns:
            Palauttaa sanakirjan, jossa avaimina ovat done, grade ja completion_date.
        """

        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT done, grade, completion_date FROM courses WHERE course_id = ?", (course_id,))

        row = cursor.fetchone()

        return {
            "done": row["done"],
            "grade": row["grade"],
            "completion_date": row["completion_date"]
        }

    def _create_course_object(self, courses):
        """Luo Course-olioita tietokannasta haetuista tiedoista.

        Args:
            courses: Lista tietokannasta haetuista tiedoista.

        Returns:
            Palauttaa listan Course-olioita.
        """

        result = []
        for course in courses:
            course_id = course["course_id"]
            max_points = self.get_max_points_by_course(course_id)
            completion = self.get_completion_info(course_id)
            result.append(Course(course["user_id"], course["name"],
                                 course["ects_credits"], max_points, completion, course_id))

        return result

    def create(self, course):
        """Tallentaa uuden kurssin tietokantaan.

        Args:
            course: Course-olio, joka kuvaa tallennettavaa kurssia.

        Returns:
            Palauttaa tallennetun Course-olion.
        """

        cursor = self._connection.cursor()

        query = "INSERT INTO courses (user_id, name, ects_credits, done) VALUES (?, ?, ?, ?)"

        cursor.execute(
            query, (course.user_id, course.name, course.ects_credits, 0))

        course_id = cursor.lastrowid

        query = "INSERT INTO course_points (course_id, task_id, " \
                "max_points, completed_points) VALUES (?, ?, ?, ?)"

        for task_id in course.max_points:
            cursor.execute(query, (course_id, task_id,
                           course.max_points[task_id], 0))

        self._connection.commit()

        course.course_id = course_id

        return course

    def update(self, course_id, completed_points):
        """Päivittää kurssin suoritettuja pisteitä tietokantaan.

        Args:
            course_id: Kurssin id.
            completed_points: Sanakirja, jossa avaimina ovat tehtävien id:t 
            ja arvoina suoritetut pisteet.
        """

        cursor = self._connection.cursor()

        query = "UPDATE course_points SET completed_points = ? WHERE course_id = ? AND task_id = ?"

        for task_id in completed_points:
            cursor.execute(
                query, (completed_points[task_id], course_id, task_id))

        self._connection.commit()

    def set_done(self, course_id, grade, completion_date):
        """Asettaa kurssin suoritetuksi, ja tallentaa kurssin arvosanan 
        ja suorituspäivän tietokantaan.

        Args:
            course_id: Suoritetun kurssin id.
            grade: Suoritetun kurssin arvosana.
            completion_date: Suoritetun kurssin suorituspäivämäärä.
        """

        cursor = self._connection.cursor()

        query = "UPDATE courses SET done = ?, grade = ?, completion_date = ? WHERE course_id = ?"

        cursor.execute(query, (1, grade, completion_date, course_id))

        self._connection.commit()

    def delete_course(self, course_id):
        """Poistaa kurssin tietokannasta.

        Args:
            course_id: Poistettavan kurssin id.
        """

        cursor = self._connection.cursor()

        cursor.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))
        cursor.execute(
            "DELETE FROM course_points WHERE course_id = ?", (course_id,))

        self._connection.commit()

    def delete_all(self):
        """Poistaa kaikki kurssit tietokannasta.
        """

        cursor = self._connection.cursor()

        cursor.execute("DELETE FROM courses")

        self._connection.commit()


course_repository = CourseRepository(get_database_connection())

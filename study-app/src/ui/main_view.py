from tkinter import ttk, constants
from services.user_service import user_service
from services.course_service import course_service


class MainView:
    """Etusivusta vastaava näkymä, mistä käyttäjä voi navigoida kurssin lisäämiseen, suoritettujen kurssien näkymään ja käynnissä olevien kurssien kurssisivuille.
    """

    def __init__(self, root, handle_logout, handle_add_course, handle_show_course_page, handle_show_completed):
        """Luokan konstruktori, joka luo etusivun näkymän.

        Args:
            root:
                TKinter-elementti, jonka sisään näkymä alustetaan.
            handle_logout:
                Kutsuttava-arvo, jota kutsutaan kun käyttäjä kirjautuu ulos.
            handle_add_course:
                Kutsuttava-arvo, jota kutsutaan kun käyttäjä haluaa lisätä uuden kurssin.
            handle_show_course_page:
                Kutsuttava-arvo, jota kutsutaan kun käyttäjä haluaa nähdä kurssisivun. Saa argumenttina Course-olion.
            handle_show_completed:
                Kutsuttava-arvo, jota kutsutaan kun käyttäjä haluaa nähdä suorittamansa kurssit.
        """

        self._root = root
        self._handle_logout = handle_logout
        self._handle_add_course = handle_add_course
        self._handle_show_course_page = handle_show_course_page
        self._handle_show_completed = handle_show_completed
        self._user = user_service.get_current_user()
        self._frame = None
        self._course_list_frame = None
        self._course_list_view = None

        self._initialize()

    def pack(self):
        """Näyttää näkymän.
        """

        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Tuhoaa näkymän.
        """

        self._frame.destroy()

    def _logout_handler(self):
        user_service.logout()
        self._handle_logout()

    def _add_course_handler(self):
        self._handle_add_course()

    def _show_course_page(self, course=None):
        self._handle_show_course_page(course)

    def _show_completed_handler(self):
        self._handle_show_completed()

    def _initialize_header(self):
        info_text = "Tervetula Sisukas-sovellukseen!\n\nAlla näet listauksen tällä hetkellä käynnissä olevista kursseistasi, mikäli olet ehtinyt lisäämään niitä järjestelmään. Voit muokata kurssin tietoja tai merkitä kurssin suoritetuksi painamalla 'Näytä/muokkaa' -painiketta.\n\nUuden kurssin lisääminen ja jo suoritettujen kurssien tarkastelu onnistuu alla olevien painikkeiden avulla."

        info = ttk.Label(master=self._frame, text=info_text, wraplength=400)

        info.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky=constants.EW)

    def _initialize_course_list(self):
        if self._course_list_view:
            self._course_list_view.destroy()

        courses = course_service.get_courses_by_user_id(self._user.user_id)

        self._course_list_view = CourseListView(
            self._course_list_frame, courses, self._show_course_page)

        self._course_list_view.pack()

    def _initialize_footer(self):
        user_label = ttk.Label(
            master=self._frame,
            text=f"Olet kirjautunut sisään käyttäjänä {self._user.username}"
        )

        user_label.grid(
            row=2,
            column=0,
            padx=10,
            pady=5,
            sticky=constants.EW)

        add_course_button = ttk.Button(
            master=self._frame,
            text="Lisää uusi kurssi",
            command=self._add_course_handler
        )

        add_course_button.grid(
            row=3,
            column=0,
            padx=10,
            pady=5,
            sticky=constants.EW
        )

        show_completed_button = ttk.Button(
            master=self._frame,
            text="Suoritetut kurssit",
            command=self._show_completed_handler
        )

        show_completed_button.grid(
            row=4,
            column=0,
            padx=10,
            pady=5,
            sticky=constants.EW
        )

        logout_button = ttk.Button(
            master=self._frame,
            text="Kirjaudu ulos",
            command=self._logout_handler
        )

        logout_button.grid(
            row=5,
            column=0,
            padx=10,
            pady=5,
            sticky=constants.EW
        )

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._course_list_frame = ttk.Frame(master=self._frame)

        self._initialize_header()
        self._initialize_course_list()
        self._initialize_footer()

        self._course_list_frame.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky=constants.EW
        )

        self._frame.grid_columnconfigure(0, weight=1, minsize=400)
        self._frame.grid_columnconfigure(1, weight=0)


class CourseListView:
    """Käynnissä olevien kurssien listauksesta vastaava näkymä.
    """

    def __init__(self, root, courses, handle_show_course_page):
        """Luokan konstruktori, joka luo listausnäkymän käyttäjän käynnissä olevista kursseista.

        Args:
            root:
                TKinter-elementti, jonka sisään näkymä alustetaan.
            courses:
                Lista Courses-olioita, jotka näkymässä näytetään
            handle_show_course_page:
                Kutsuttava-arvo, jota kutsutaan kun käyttäjä haluaa nähdä kurssisivun. Saa argumenttina Course-olion.
        """

        self._root = root
        self._courses = courses
        self._handle_show_course_page = handle_show_course_page
        self._frame = None

        self._initialize()

    def pack(self):
        """Näyttää näkymän.
        """

        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Tuhoaa näkymän.
        """

        self._frame.destroy()

    def _initialize_course_item(self, course):
        item_frame = ttk.Frame(master=self._frame)
        label = ttk.Label(master=item_frame,
                          text=f"{course.name}, {course.ects_credits} op")

        label.grid(row=0, column=0, padx=10, pady=5, sticky=constants.W)

        show_course_page_button = ttk.Button(
            master=item_frame,
            text="Näytä/muokkaa",
            command=lambda: self._handle_show_course_page(course)
        )

        show_course_page_button.grid(
            row=0,
            column=1,
            padx=10,
            pady=5,
            sticky=constants.EW
        )

        item_frame.grid_columnconfigure(0, weight=1)
        item_frame.pack(fill=constants.X)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        for course in self._courses:
            self._initialize_course_item(course)

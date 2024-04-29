from tkinter import ttk, constants
from services.user_service import user_service
from services.course_service import course_service


class CompletedView:
    """Käyttäjän suoritettujen kurssien näkymästä vastaava luokka.
    """

    def __init__(self, root, handle_show_course_page, handle_return):
        """Luokan konstruktori, joka luo käyttäjän suoritettujen kurssien näkymän.

        Args:
            root:
                TKinter-elementti, jonka sisään näkymä alustetaan.
            handle_show_course_page:
                Kutsuttava-arvo, jota kutsutaan kun käyttäjä haluaa nähdä kurssisivun. Saa argumenttina Course-olion.
            handle_return:
                Kutsuttava-arvo, jota kutsutaan kun käyttäjä haluaa palata takaisin edelliselle sivulle.
        """

        self._root = root
        self._handle_show_course_page = handle_show_course_page
        self._handle_return = handle_return
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

    def _return_handler(self):
        self._handle_return()

    def _show_course_page(self, course=None):
        self._handle_show_course_page(course)

    def _initialize_header(self):
        info_text = "Alla näet listauksen suorittamistasi kursseista. Pääset näkemään kurssin tarkemmat tiedot painamalla 'Näytä/muokkaa' -painiketta."

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

        courses = course_service.get_completed_courses_by_user_id(
            self._user.user_id)

        self._course_list_view = CompletedListView(
            self._course_list_frame, courses, self._show_course_page)

        self._course_list_view.pack()

    def _initialize_footer(self):
        return_button = ttk.Button(
            master=self._frame,
            text="Etusivulle",
            command=self._return_handler
        )

        return_button.grid(
            row=3,
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


class CompletedListView:
    def __init__(self, root, courses, handle_show_course_page):
        self._root = root
        self._courses = courses
        self._handle_show_course_page = handle_show_course_page
        self._frame = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize_course_item(self, course):
        item_frame = ttk.Frame(master=self._frame)
        name = course.name
        ects_credits = course.ects_credits
        grade = course.completion["grade"]
        date = course.completion["completion_date"]
        label = ttk.Label(
            master=item_frame, text=f"{name}, {ects_credits} op,\narvosana: {grade}, suoritettu: {date}")

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

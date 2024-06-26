from tkinter import ttk, StringVar, constants
from services.course_service import course_service, InvalidValuesError
from services.user_service import user_service


class AddCourseView:
    """Kurssin lisäämisestä vastaava näkymä.
    """

    def __init__(self, root, handle_show_main_view):
        """Luokan konstruktori, joka luo kurssin lisäyksen näkymän.

        Args:
            root:
                TKinter-elementti, jonka sisään näkymä alustetaan.
            handle_show_main_view:
                Kutsuttava-arvo, jota kutsutaan kun käyttäjä tallentaa uuden kurssin ja palaa etusivulle, tai haluaa palata etusivulle ilman tallentamista.
        """

        self._root = root
        self._user = user_service.get_current_user()
        self._handle_show_main_view = handle_show_main_view
        self._frame = None
        self._name_entry = None
        self._ects_credits_entry = None
        self._exercises_entry = None
        self._ex_group_entry = None
        self._project_entry = None
        self._peer_review_entry = None
        self._feedback_entry = None
        self._other_entry = None
        self._exam_entry = None
        self._error_variable = None
        self._error_label = None

        self._initialize()

    def pack(self):
        """Näyttää näkymän.
        """

        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Tuhoaa näkymän.
        """

        self._frame.destroy()

    def _show_error(self, message):
        self._error_variable.set(message)
        self._error_label.grid()

    def _hide_error(self):
        self._error_label.grid_remove()

    def _initialize_header(self):
        info_text = "Lisää uusi kurssi syöttämällä sen nimi, opintopisteet sekä kurssin arviontiin vaikuttavien tehtävien maksimipistemäärät. Voit jättää pistekentät tyhjiksi, mikäli kurssilla ei ole kyseisiä tehtävätyyppejä.\n\nPakolliset kentät on merkitty tähdellä. Syötä opintopisteiden ja tehtävien pistemäärät kokonaislukuina. Tehtävistä kertyvät maksimipistemäärät voivat olla välillä 0-100."

        info = ttk.Label(master=self._frame, text=info_text, wraplength=500)

        info.grid(padx=10, pady=10, sticky=constants.EW)

    def _initialize_course_info_fields(self):
        name_label = ttk.Label(
            master=self._frame, text="Nimi (1-50 merkkiä): *")
        self._name_entry = ttk.Entry(master=self._frame)

        name_label.grid(padx=10, pady=5, sticky=constants.W)
        self._name_entry.grid(padx=10, pady=5, sticky=constants.EW)

        ects_credits_label = ttk.Label(
            master=self._frame, text="Opintopisteet (0-50): *")
        self._ects_credits_entry = ttk.Entry(master=self._frame)

        ects_credits_label.grid(padx=10, pady=5, sticky=constants.W)
        self._ects_credits_entry.grid(padx=10, pady=5, sticky=constants.EW)

    def _initialize_task_fields(self):
        exercise_label = ttk.Label(master=self._frame, text="Tehtävät:")
        self._exercises_entry = ttk.Entry(master=self._frame)

        exercise_label.grid(padx=10, pady=5, sticky=constants.W)
        self._exercises_entry.grid(padx=10, pady=5, sticky=constants.EW)

        ex_group_label = ttk.Label(
            master=self._frame, text="Laskuharjoitukset:")
        self._ex_group_entry = ttk.Entry(master=self._frame)

        ex_group_label.grid(padx=10, pady=5, sticky=constants.W)
        self._ex_group_entry.grid(padx=10, pady=5, sticky=constants.EW)

        project_label = ttk.Label(master=self._frame, text="Harjoitustyö:")
        self._project_entry = ttk.Entry(master=self._frame)

        project_label.grid(padx=10, pady=5, sticky=constants.W)
        self._project_entry.grid(padx=10, pady=5, sticky=constants.EW)

        exam_label = ttk.Label(master=self._frame, text="Koe:")
        self._exam_entry = ttk.Entry(master=self._frame)

        exam_label.grid(padx=10, pady=5, sticky=constants.W)
        self._exam_entry.grid(padx=10, pady=5, sticky=constants.EW)

        peer_review_label = ttk.Label(
            master=self._frame, text="Vertais-/itsearviointi:")
        self._peer_review_entry = ttk.Entry(master=self._frame)

        peer_review_label.grid(padx=10, pady=5, sticky=constants.W)
        self._peer_review_entry.grid(padx=10, pady=5, sticky=constants.EW)

        feedback_label = ttk.Label(master=self._frame, text="Kurssipalaute:")
        self._feedback_entry = ttk.Entry(master=self._frame)

        feedback_label.grid(padx=10, pady=5, sticky=constants.W)
        self._feedback_entry.grid(padx=10, pady=5, sticky=constants.EW)

        other_label = ttk.Label(master=self._frame, text="Muu:")
        self._other_entry = ttk.Entry(master=self._frame)

        other_label.grid(padx=10, pady=5, sticky=constants.W)
        self._other_entry.grid(padx=10, pady=5, sticky=constants.EW)

    def _save_handler(self):
        max_points = {}
        try:
            user_id = self._user.user_id
            name = self._name_entry.get()
            ects_credits = int(self._ects_credits_entry.get())

            if self._exercises_entry.get():
                max_points[1] = int(self._exercises_entry.get())

            if self._ex_group_entry.get():
                max_points[2] = int(self._ex_group_entry.get())

            if self._project_entry.get():
                max_points[3] = int(self._project_entry.get())

            if self._exam_entry.get():
                max_points[4] = int(self._exam_entry.get())

            if self._peer_review_entry.get():
                max_points[5] = int(self._peer_review_entry.get())

            if self._feedback_entry.get():
                max_points[6] = int(self._feedback_entry.get())

            if self._other_entry.get():
                max_points[7] = int(self._other_entry.get())

            course_service.create_course(
                user_id, name, ects_credits, max_points)

            self._return_handler()

        except ValueError:
            self._show_error(
                "Opintopisteiden ja tehtävien määrän tulee olla kokonaislukuja. Opintopisteet-kenttä on pakollinen.")

        except InvalidValuesError:
            self._show_error(
                "Kurssin nimen tulee olla 1-50 merkkiä pitkä ja opintopisteiden kokonaislukuja välillä 0-50. Tehtäväpisteiden arvot tulee olla kokonaislukuja välillä 0-100.")

    def _return_handler(self):
        self._handle_show_main_view()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._error_variable = StringVar(self._frame)

        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            wraplength=500,
            foreground="red"
        )

        self._error_label.grid(padx=10, pady=5)

        self._initialize_header()
        self._initialize_course_info_fields()
        self._initialize_task_fields()

        save_button = ttk.Button(
            master=self._frame,
            text="Tallenna",
            command=self._save_handler
        )

        return_button = ttk.Button(
            master=self._frame,
            text="Takaisin",
            command=self._return_handler
        )

        self._frame.grid_columnconfigure(0, weight=1, minsize=400)

        save_button.grid(padx=10, pady=5, sticky=constants.EW)
        return_button.grid(padx=10, pady=5, sticky=constants.EW)

        self._hide_error()

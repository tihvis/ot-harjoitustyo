from tkinter import ttk, StringVar, constants
from services.course_service import course_service, InvalidValuesError
from services.user_service import user_service


class AddCourseView:
    def __init__(self, root, handle_return):
        self._root = root
        self._user = user_service.get_current_user()
        self._handle_return = handle_return
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
        self._grade_entry = None
        self._comp_date_entry = None
        self._error_variable = None
        self._error_label = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _show_error(self, message):
        self._error_variable.set(message)
        self._error_label.grid()

    def _hide_error(self):
        self._error_label.grid_remove()

    def _initialize_course_info_fields(self):
        name_label = ttk.Label(master=self._frame, text="Nimi:")
        self._name_entry = ttk.Entry(master=self._frame)

        name_label.grid(padx=5, pady=5, sticky=constants.W)
        self._name_entry.grid(padx=5, pady=5, sticky=constants.EW)

        ects_credits_label = ttk.Label(
            master=self._frame, text="Opintopisteet:")
        self._ects_credits_entry = ttk.Entry(master=self._frame)

        ects_credits_label.grid(padx=5, pady=5, sticky=constants.W)
        self._ects_credits_entry.grid(padx=5, pady=5, sticky=constants.EW)

    def _initialize_task_fields(self):
        exercise_label = ttk.Label(master=self._frame, text="Tehtävät:")
        self._exercises_entry = ttk.Entry(master=self._frame)

        exercise_label.grid(padx=5, pady=5, sticky=constants.W)
        self._exercises_entry.grid(padx=5, pady=5, sticky=constants.EW)

        ex_group_label = ttk.Label(
            master=self._frame, text="Laskuharjoitukset:")
        self._ex_group_entry = ttk.Entry(master=self._frame)

        ex_group_label.grid(padx=5, pady=5, sticky=constants.W)
        self._ex_group_entry.grid(padx=5, pady=5, sticky=constants.EW)

        project_label = ttk.Label(master=self._frame, text="Harjoitustyö:")
        self._project_entry = ttk.Entry(master=self._frame)

        project_label.grid(padx=5, pady=5, sticky=constants.W)
        self._project_entry.grid(padx=5, pady=5, sticky=constants.EW)

        exam_label = ttk.Label(master=self._frame, text="Koe:")
        self._exam_entry = ttk.Entry(master=self._frame)

        exam_label.grid(padx=5, pady=5, sticky=constants.W)
        self._exam_entry.grid(padx=5, pady=5, sticky=constants.EW)

        peer_review_label = ttk.Label(
            master=self._frame, text="Vertais-/itsearviointi:")
        self._peer_review_entry = ttk.Entry(master=self._frame)

        peer_review_label.grid(padx=5, pady=5, sticky=constants.W)
        self._peer_review_entry.grid(padx=5, pady=5, sticky=constants.EW)

        feedback_label = ttk.Label(master=self._frame, text="Kurssipalaute:")
        self._feedback_entry = ttk.Entry(master=self._frame)

        feedback_label.grid(padx=5, pady=5, sticky=constants.W)
        self._feedback_entry.grid(padx=5, pady=5, sticky=constants.EW)

        other_label = ttk.Label(master=self._frame, text="Muu:")
        self._other_entry = ttk.Entry(master=self._frame)

        other_label.grid(padx=5, pady=5, sticky=constants.W)
        self._other_entry.grid(padx=5, pady=5, sticky=constants.EW)

    def _save_handler(self):
        points = {}
        try:
            user_id = self._user.user_id
            name = self._name_entry.get()
            ects_credits = int(self._ects_credits_entry.get())

            if points[1] not None:
                points[1] = int(self._exercises_entry.get())

            if points[2] not None:
                points[2] = int(self._ex_group_entry.get())

            if points[3] not None:
                points[3] = int(self._project_entry.get())

            if points[4] not None:
                points[4] = int(self._exam_entry.get())

            if points[5] not None:
                points[5] = int(self._peer_review_entry.get())

            if points[6] not None:
                points[6] = int(self._feedback_entry.get())

            if points[7] not None:
                points[7] = int(self._other_entry.get())

            course_service.create_course(user_id, name, ects_credits, points)

            self._handle_return()

        except ValueError:
            self._show_error(
                "Opintopisteiden ja tehtävien määrän tulee olla kokonaislukuja.")

        except InvalidValuesError:
            self._show_error(
                "Kurssin nimen tulisi olla 1-50 merkkiä pitkä ja opintopisteiden kokonaislukuja välillä 0-50. Muut arvot voivat olla kokonaislukuja välillä 0-100.")

    def _delete_course_handler(self):
        pass

    def _return_handler(self):
        self._handle_return()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._error_variable = StringVar(self._frame)

        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground="red"
        )

        self._error_label.grid(padx=5, pady=5)

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

        save_button.grid(padx=5, pady=5, sticky=constants.EW)
        return_button.grid(padx=5, pady=5, sticky=constants.EW)

        self._hide_error()

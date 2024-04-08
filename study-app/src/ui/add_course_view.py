from tkinter import ttk, StringVar, constants
from services.course_service import course_service, InvalidValuesError


class AddCourseView:
    def __init__(self, root, handle_return):
        self._root = root
        self._handle_return = handle_return
        self._frame = None
        self._name_entry = None
        self._credits_entry = None
        self._exercises_entry = None
        self._ex_group_entry = None
        self._prject_entry = None
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

        credits_label = ttk.Label(master=self._frame, text="Opintopisteet:")
        self._credits_entry = ttk.Entry(master=self._frame)

        credits_label.grid(padx=5, pady=5, sticky=constants.W)
        self._credits_entry.grid(padx=5, pady=5, sticky=constants.EW)

    def _initialize_task_fields(self):
        exercise_label = ttk.Label(master=self._frame, text="Tehtävät:")
        self._exercise_entry = ttk.Entry(master=self._frame)

        exercise_label.grid(padx=5, pady=5, sticky=constants.W)
        self._exercise_entry.grid(padx=5, pady=5, sticky=constants.EW)

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
        try:
            name = self._name_entry.get()
            credits = int(self._credits_entry.get())
            exercises = int(self._exercise_entry.get())
            exercise_group = int(self._ex_group_entry.get())
            project = int(self._project_entry.get())
            exam = int(self._exam_entry.get())
            peer_review = int(self._peer_review_entry.get())
            feedback = int(self._feedback_entry.get())
            other = int(self._other_entry.get())
            course_service.create_course(
                name, credits, exercises, exercise_group, project, exam, peer_review, feedback, other)
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

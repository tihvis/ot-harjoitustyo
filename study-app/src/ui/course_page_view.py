from tkinter import ttk, StringVar, constants, messagebox
from services.course_service import course_service
from services.user_service import user_service


class CoursePageView:
    def __init__(self, root, handle_return, course = None):
        self._root = root
        self._user = user_service.get_current_user()
        self._course = course
        self._handle_return = handle_return
        self._frame = None
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

    def _update_course_handler(self):
        pass

    def _delete_course_handler(self):
        course_service.delete_course(self._course.course_id)
        self._handle_return()

    def _confirm_deletion(self):
        response = messagebox.askokcancel("Vahvista kurssin poistaminen", "Oletko varma että haluat poistaa kurssin? Paina 'OK' poistaaksesi kurssin, tai palaa kurssisivulle painamalla 'Cancel'.")

        if response:
            self._delete_course_handler()


    def _initialize_course_info(self):
        course_info_label = ttk.Label(
            master=self._frame,
            text=f"{self._course.name}, {self._course.ects_credits} op"
        )

        course_info_label.grid(padx=5, pady=5, sticky=constants.EW)

    def _initialize_task_fields(self):
        exercise_label = ttk.Label(master=self._frame, text="Tehtävät:")
        self._exercises_entry = ttk.Entry(master=self._frame)

        exercise_label.grid(padx=5, pady=5, sticky=constants.W)
        self._exercises_entry.grid(padx=5, pady=5, sticky=constants.W)

        ex_group_label = ttk.Label(
            master=self._frame, text="Laskuharjoitukset:")
        self._ex_group_entry = ttk.Entry(master=self._frame)

        ex_group_label.grid(padx=5, pady=5, sticky=constants.W)
        self._ex_group_entry.grid(padx=5, pady=5, sticky=constants.W)

        project_label = ttk.Label(master=self._frame, text="Harjoitustyö:")
        self._project_entry = ttk.Entry(master=self._frame)

        project_label.grid(padx=5, pady=5, sticky=constants.W)
        self._project_entry.grid(padx=5, pady=5, sticky=constants.W)

        exam_label = ttk.Label(master=self._frame, text="Koe:")
        self._exam_entry = ttk.Entry(master=self._frame)

        exam_label.grid(padx=5, pady=5, sticky=constants.W)
        self._exam_entry.grid(padx=5, pady=5, sticky=constants.W)

        peer_review_label = ttk.Label(
            master=self._frame, text="Vertais-/itsearviointi:")
        self._peer_review_entry = ttk.Entry(master=self._frame)

        peer_review_label.grid(padx=5, pady=5, sticky=constants.W)
        self._peer_review_entry.grid(padx=5, pady=5, sticky=constants.W)

        feedback_label = ttk.Label(master=self._frame, text="Kurssipalaute:")
        self._feedback_entry = ttk.Entry(master=self._frame)

        feedback_label.grid(padx=5, pady=5, sticky=constants.W)
        self._feedback_entry.grid(padx=5, pady=5, sticky=constants.W)

        other_label = ttk.Label(master=self._frame, text="Muu:")
        self._other_entry = ttk.Entry(master=self._frame)

        other_label.grid(padx=5, pady=5, sticky=constants.W)
        self._other_entry.grid(padx=5, pady=5, sticky=constants.W)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._error_variable = StringVar(self._frame)

        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground="red"
        )

        self._error_label.grid(padx=5, pady=5)

        self._initialize_course_info()
        self._initialize_task_fields()

        update_course_button = ttk.Button(
            master=self._frame,
            text="Päivitä",
            command=self._update_course_handler
        )

        delete_course_button = ttk.Button(
            master=self._frame,
            text="Poista kurssi",
            command=self._confirm_deletion
        )

        return_button = ttk.Button(
            master=self._frame,
            text="Takaisin",
            command=self._handle_return
        )

        self._frame.grid_columnconfigure(0, weight=1, minsize=400)

        update_course_button.grid(padx=5, pady=5, sticky=constants.EW)
        delete_course_button.grid(padx=5, pady=5, sticky=constants.EW)
        return_button.grid(padx=5, pady=5, sticky=constants.EW)

        self._hide_error()

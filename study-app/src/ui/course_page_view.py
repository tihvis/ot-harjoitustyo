from tkinter import ttk, StringVar, constants, messagebox
from services.course_service import course_service
from services.user_service import user_service


class CoursePageView:
    def __init__(self, root, handle_return, course=None):
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
        response = messagebox.askokcancel(
            "Vahvista kurssin poistaminen", "Oletko varma että haluat poistaa kurssin? Paina 'OK' poistaaksesi kurssin, tai palaa kurssisivulle painamalla 'Cancel'.")

        if response:
            self._delete_course_handler()

    def _initialize_course_info(self):
        course_info_label = ttk.Label(
            master=self._frame, font=("Arial", 15),
            text=f"{self._course.name}, {self._course.ects_credits} op"
        )

        course_info_label.grid(row=1, columnspan=3, padx=10,
                               pady=10, sticky=constants.EW)

    def _initialize_task_fields(self):
        for i, task_id in enumerate(course_service.task_ids()):
            task_name = ttk.Label(
                master=self._frame, text=course_service.get_name_of_task(task_id) + ":")

            points_entry = ttk.Entry(master=self._frame)

            previous_points = ttk.Label(master=self._frame, text=course_service.get_completed_task_points(
                self._course.course_id, task_id) + "/" + course_service.get_max_task_points(self._course.course_id, task_id) + "p")

            task_name.grid(row=i+2, column=0, padx=10,
                           pady=5, sticky=constants.EW)
            points_entry.grid(row=i+2, column=1, padx=10,
                              pady=5, sticky=constants.EW)
            previous_points.grid(row=i+2, column=2, padx=10,
                                 pady=5, sticky=constants.EW)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._error_variable = StringVar(self._frame)

        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground="red"
        )

        self._error_label.grid(row=0, column=0, columnspan=3,
                               padx=10, pady=5, sticky=constants.EW)

        self._initialize_course_info()
        self._initialize_task_fields()

        update_course_button = ttk.Button(
            master=self._frame,
            text="Tallenna muutokset (ei toimi vielä)",
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

        self._frame.grid_columnconfigure(0, weight=1)
        self._frame.grid_columnconfigure(1, weight=1)
        self._frame.grid_columnconfigure(2, weight=1)

        update_course_button.grid(
            column=1, padx=10, pady=5, sticky=constants.EW)
        delete_course_button.grid(
            column=1, padx=10, pady=5, sticky=constants.EW)
        return_button.grid(column=1, padx=10, pady=5, sticky=constants.EW)

        self._hide_error()

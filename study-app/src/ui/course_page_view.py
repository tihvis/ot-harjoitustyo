from tkinter import ttk, StringVar, constants, messagebox
from services.course_service import course_service, InvalidValuesError
from services.user_service import user_service


class CoursePageView:
    def __init__(self, root, handle_return, course=None):
        self._root = root
        self._user = user_service.get_current_user()
        self._course = course
        self._handle_return = handle_return
        self._completed_points = {}
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
        completed_points = {}
        try:

            if self._exercises_entry and self._exercises_entry.get():
                completed_points[1] = int(self._exercises_entry.get())

            if self._ex_group_entry and self._ex_group_entry.get():
                completed_points[2] = int(self._ex_group_entry.get())

            if self._project_entry and self._project_entry.get():
                completed_points[3] = int(self._project_entry.get())

            if self._exam_entry and self._exam_entry.get():
                completed_points[4] = int(self._exam_entry.get())

            if self._peer_review_entry and self._peer_review_entry.get():
                completed_points[5] = int(self._peer_review_entry.get())

            if self._feedback_entry and self._feedback_entry.get():
                completed_points[6] = int(self._feedback_entry.get())

            if self._other_entry and self._other_entry.get():
                completed_points[7] = int(self._other_entry.get())

            course_service.update_course(
                self._course.course_id, completed_points)
            self._handle_return()

        except ValueError:
            self._show_error(
                "Syötä kenttiin vain kokonaislukuja.")

        except InvalidValuesError:
            self._show_error(
                "Tarkista että syöttämäsi arvot ovat lukuja väliltä 0 - tehtävän maksimipisteet.")

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
            text=f"{self._course.name}, {str(self._course.ects_credits)} op"
        )

        course_info_label.grid(row=1, column=0, columnspan=3, padx=10,
                               pady=10, sticky=constants.EW)

        info_text = "Alla näet kurssin tehtävät, sekä tämänhetkinen pistekertymä maksimipisteistä.Pääset päivittämään pistekertymää merkitsemällä uuden kokonaispistemäärän tekstikenttään, ja painamalla 'Tallenna muutokset'."

        info_text_label = ttk.Label(
            master=self._frame,
            text=info_text,
            wraplength=500,
        )

        info_text_label.grid(row=2, column=0, columnspan=3, padx=10,
                             pady=10, sticky=constants.EW)

    def _initialize_task_fields(self):
        for task_id in course_service.task_ids():
            if task_id in self._course.max_points:
                self._completed_points[task_id] = course_service.get_completed_task_points(
                    self._course.course_id, task_id)

        if 1 in self._completed_points:
            exercise_label = ttk.Label(master=self._frame, text="Tehtävät:")
            self._exercises_entry = ttk.Entry(master=self._frame, width=20)
            prev_exercise_points_label = ttk.Label(master=self._frame, text=(str(course_service.get_completed_task_points(
                self._course.course_id, 1))) + " / " + (str(course_service.get_max_task_points(self._course.course_id, 1)) + "p"))

            exercise_label.grid(row=3, column=0, padx=10,
                                pady=5, sticky=constants.EW)
            self._exercises_entry.grid(
                row=3, column=1, padx=10, pady=5, sticky=constants.EW)
            prev_exercise_points_label.grid(
                row=3, column=2, padx=10, pady=5, sticky=constants.EW)

        if 2 in self._completed_points:
            ex_group_label = ttk.Label(
                master=self._frame, text="Laskuharjoitukset:")
            self._ex_group_entry = ttk.Entry(master=self._frame, width=20)
            prev_ex_group_label = ttk.Label(master=self._frame, text=(str(course_service.get_completed_task_points(
                self._course.course_id, 2))) + " / " + (str(course_service.get_max_task_points(self._course.course_id, 2)) + "p"))

            ex_group_label.grid(row=4, column=0, padx=10,
                                pady=5, sticky=constants.W)
            self._ex_group_entry.grid(
                row=4, column=1, padx=10, pady=5, sticky=constants.EW)
            prev_ex_group_label.grid(
                row=4, column=2, padx=10, pady=5, sticky=constants.EW)

        if 3 in self._completed_points:
            project_label = ttk.Label(master=self._frame, text="Harjoitustyö:")
            self._project_entry = ttk.Entry(master=self._frame, width=20)
            prev_project_label = ttk.Label(master=self._frame, text=(str(course_service.get_completed_task_points(
                self._course.course_id, 3))) + " / " + (str(course_service.get_max_task_points(self._course.course_id, 3)) + "p"))

            project_label.grid(row=5, column=0, padx=10,
                               pady=5, sticky=constants.W)
            self._project_entry.grid(
                row=5, column=1, padx=10, pady=5, sticky=constants.EW)
            prev_project_label.grid(
                row=5, column=2, padx=10, pady=5, sticky=constants.EW)

        if 4 in self._completed_points:
            exam_label = ttk.Label(master=self._frame, text="Koe:")
            self._exam_entry = ttk.Entry(master=self._frame, width=20)
            prev_exam_label = ttk.Label(master=self._frame, text=(str(course_service.get_completed_task_points(
                self._course.course_id, 4))) + " / " + (str(course_service.get_max_task_points(self._course.course_id, 4)) + "p"))

            exam_label.grid(row=6, column=0, padx=10,
                            pady=5, sticky=constants.W)
            self._exam_entry.grid(row=6, column=1, padx=10,
                                  pady=5, sticky=constants.EW)
            prev_exam_label.grid(row=6, column=2, padx=10,
                                 pady=5, sticky=constants.EW)

        if 5 in self._completed_points:
            peer_review_label = ttk.Label(
                master=self._frame, text="Vertais-/itsearviointi:")
            self._peer_review_entry = ttk.Entry(master=self._frame, width=20)
            prev_review_label = ttk.Label(master=self._frame, text=(str(course_service.get_completed_task_points(
                self._course.course_id, 5))) + " / " + (str(course_service.get_max_task_points(self._course.course_id, 5)) + "p"))

            peer_review_label.grid(
                row=7, column=0, padx=10, pady=5, sticky=constants.W)
            self._peer_review_entry.grid(
                row=7, column=1, padx=10, pady=5, sticky=constants.EW)
            prev_review_label.grid(
                row=7, column=2, padx=10, pady=5, sticky=constants.EW)

        if 6 in self._completed_points:
            feedback_label = ttk.Label(
                master=self._frame, text="Kurssipalaute:")
            self._feedback_entry = ttk.Entry(master=self._frame, width=20)
            prev_feedback_label = ttk.Label(master=self._frame, text=(str(course_service.get_completed_task_points(
                self._course.course_id, 6))) + " / " + (str(course_service.get_max_task_points(self._course.course_id, 6)) + "p"))

            feedback_label.grid(row=8, column=0, padx=10,
                                pady=5, sticky=constants.W)
            self._feedback_entry.grid(
                row=8, column=1, padx=10, pady=5, sticky=constants.EW)
            prev_feedback_label.grid(
                row=8, column=2, padx=10, pady=5, sticky=constants.EW)

        if 7 in self._completed_points:
            other_label = ttk.Label(master=self._frame, text="Muu:")
            self._other_entry = ttk.Entry(master=self._frame, width=20)
            prev_other_label = ttk.Label(master=self._frame, text=(str(course_service.get_completed_task_points(
                self._course.course_id, 7))) + " / " + (str(course_service.get_max_task_points(self._course.course_id, 7)) + "p"))

            other_label.grid(row=9, column=0, padx=10,
                             pady=5, sticky=constants.W)
            self._other_entry.grid(
                row=9, column=1, padx=10, pady=5, sticky=constants.EW)
            prev_other_label.grid(row=9, column=2, padx=10,
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
            text="Tallenna muutokset",
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

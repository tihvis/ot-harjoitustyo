from tkinter import ttk, constants
from services.course_service import course_service


class CoursePageView:
    def __init__(self, root, course, return_to_main_page):
        self._root = root
        self._course = course
        self._return_to_main_page = return_to_main_page
        self._frame = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _update_course_handler(self):
        pass

    def _delete_course_handler(self):
        course_service.delete_course(self._course.course_id)
        self._return_to_main_page()

    def _return_handler(self):
        self._return_to_main_page()

    def _initialize_header(self):
        course_info_label = ttk.Label(
            master=self._frame,
            # text=f"{self._course.name}, {self._course.credits} op"
            text="Kurssin nimi, 5 op"
        )

        course_info_label.grid(row=0, column=0, padx=5,
                               pady=5, sticky=constants.W)

    def _initialize_footer(self):
        update_course_button = ttk.Button(
            master=self._frame,
            text="Päivitä",
            command=self._update_course_handler
        )

        update_course_button.grid(
            row=3,
            column=1,
            padx=5,
            pady=5,
            sticky=constants.EW
        )

        delete_course_button = ttk.Button(
            master=self._frame,
            text="Poista kurssi",
            command=self._delete_course_handler
        )

        delete_course_button.grid(
            row=4,
            column=1,
            padx=5,
            pady=5,
            sticky=constants.EW
        )

        return_button = ttk.Button(
            master=self._frame,
            text="Takaisin",
            command=self._return_handler
        )

        return_button.grid(
            row=5,
            column=1,
            padx=5,
            pady=5,
            sticky=constants.EW
        )

    def _initialize(self):
        if self._course_list_view:
            self._course_list_view.destroy()
        self._frame = ttk.Frame(master=self._root)

        self._initialize_header()
        self._initialize_footer()

from tkinter import ttk, constants
from services.user_service import user_service
from services.course_service import course_service
# täydennä allaoleva import
#from ui.course_page_view import 

class CourseListView:
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
        label = ttk.Label(master=item_frame, text=course.name)

        show_course_button = ttk.Button(
            master=item_frame,
            text="Näytä/muokkaa",
            command=self._handle_show_course_page()
        )

        label.grid(row=0, column=0, padx=5, pady=5, sticky=constants.W)

        show_course_button.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky=constants.EW
        )

        item_frame.grid_columnconfigure(0, weight=1)
        item_frame.pack(fill=constants.X)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        if self._courses:
            for course in self._courses:
                self._initialize_course_item(course)


class CourseView:
    def __init__(self, root, handle_logout, handle_add_course, handle_show_completed, handle_show_course_page):
        self._root = root
        self._handle_logout = handle_logout
        self._handle_add_course = handle_add_course
        self._handle_show_completed = handle_show_completed
        self._handle_show_course_page = handle_show_course_page
        self._user = user_service.get_current_user()
        self._frame = None
        self._course_list_frame = None
        self._course_list_view = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _logout_handler(self):
        user_service.logout()
        self._handle_logout()

    def _add_course_handler(self):
        self._handle_add_course()

    def _show_completed_handler(self):
        self._handle_show_completed()

    def _initialize_course_list(self):
        if self._course_list_view:
            self._course_list_view.destroy()

        courses = course_service.get_courses() 

        self._course_list_view = CourseListView(self._course_list_frame, courses, self._handle_show_course_page)

        self._course_list_view.pack()

    def _initialize_header(self):
        user_label = ttk.Label(
            master=self._frame,
            text=f"Olet kirjautunut sisään käyttäjänä {self._user.username}"
        )

        user_label.grid(row=0, column=0, padx=5, pady=5, sticky=constants.W)

    def _initialize_footer(self):
        add_course_button = ttk.Button(
            master=self._frame,
            text="Lisää uusi kurssi",
            command=self._add_course_handler
        )

        add_course_button.grid(
            row=3,
            column=1,
            padx=5,
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
            column=1,
            padx=5,
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
            column=1,
            padx=5,
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

        self._frame.grid_rowconfigure(0, weight=1)
        self._frame.grid_rowconfigure(1, weight=1)
        self._frame.grid_rowconfigure(2, weight=1)
        self._frame.grid_rowconfigure(3, weight=1)
        self._frame.grid_rowconfigure(4, weight=1)
        self._frame.grid_rowconfigure(5, weight=1)

        self._frame.grid_columnconfigure(0, weight=1)
        self._frame.grid_columnconfigure(1, weight=1)
        self._frame.grid_columnconfigure(2, weight=1)


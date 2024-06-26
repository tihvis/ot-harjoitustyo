from ui.login_view import LoginView
from ui.main_view import MainView
from ui.create_user_view import CreateUserView
from ui.add_course_view import AddCourseView
from ui.course_page_view import CoursePageView
from ui.completed_view import CompletedView


class UI:
    """Sovelluksen käyttöliittymästä vastaava luokka.
    """

    def __init__(self, root):
        """Luokan konstruktori, joka luo uuden käyttöliittymästä vastaavan luokan.

        Args:
            root:
                TKinter-elementti, johon käyttöliittymä alustetaan.
        """

        self._root = root
        self._current_view = None

    def start(self):
        """Käynnistää käyttöliittymän.
        """

        self._show_login_view()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _show_login_view(self):
        self._hide_current_view()

        self._current_view = LoginView(
            self._root, self._show_main_view, self._show_create_user_view)

        self._current_view.pack()

    def _show_add_course_view(self):
        self._hide_current_view()

        self._current_view = AddCourseView(
            self._root, self._show_main_view)

        self._current_view.pack()

    def _show_main_view(self):
        self._hide_current_view()

        self._current_view = MainView(
            self._root, self._show_login_view, self._show_add_course_view, self._show_course_page_view, self._show_completed_view)

        self._current_view.pack()

    def _show_create_user_view(self):
        self._hide_current_view()

        self._current_view = CreateUserView(
            self._root, self._show_main_view, self._show_login_view)

        self._current_view.pack()

    def _show_course_page_view(self, course=None):
        self._hide_current_view()

        self._current_view = CoursePageView(
            self._root, self._show_main_view, course)

        self._current_view.pack()

    def _show_completed_view(self):
        self._hide_current_view()

        self._current_view = CompletedView(
            self._root, self._show_course_page_view, self._show_main_view)

        self._current_view.pack()

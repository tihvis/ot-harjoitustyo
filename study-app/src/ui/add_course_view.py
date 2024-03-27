from tkinter import ttk, StringVar, constants

class AddCourseView:
    def __init__(self, root, handle_add_course, handle_delete_course, handle_return):
        self._root = root
        self._handle_add_course = handle_add_course
        self._handle_delete_course = handle_delete_course
        self._handle_return = handle_return
        self._frame = None
        self._name_entry = None
        self._credits_entry = None
        self._exercises_entry = None
        self._ex_group_entry = None
        self._prject_entry = None
        self._exam_entry = None
        # self._completed_entry = None
        self._grade_entry = None
        self._comp_date_entry = None
        self._error_variable = None
        self._error_label = None

        self._initialize()
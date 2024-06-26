from tkinter import ttk, StringVar, constants
from services.user_service import user_service, UsernameExistsError, PasswordConfirmationError, InvalidPasswordError, InvalidCredentialsError


class CreateUserView:
    """Käyttäjän rekisteröitymisestä vastaava näkymä.
    """

    def __init__(self, root, handle_show_main_view, handle_show_login_view):
        """Luokan konstruktori, joka luo uuden rekisteröitymisnäkymän.

        Args:
            root:
                TKinter-elementti, jonka sisään näkymä alustetaan.
            handle_show_main_view:
                Kutsuttava-arvo, jota kutsutaan kun käyttäjä luodaan ja siirretään etusivulle.
            handle_show_login_view:
                Kutsuttava-arvo, jota kutsutaan kun siirrytään takaisin kirjautumisnäkymään.
        """

        self._root = root
        self._handle_show_main_view = handle_show_main_view
        self._handle_show_login_view = handle_show_login_view
        self._frame = None
        self._username_entry = None
        self._password_entry = None
        self._password2_entry = None
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

    def _create_user_handler(self):
        username = self._username_entry.get()
        password = self._password_entry.get()
        password2 = self._password2_entry.get()

        try:
            user_service.create_user(username, password, password2)
            self._handle_show_main_view()

        except UsernameExistsError:
            self._show_error(f"Käyttäjätunnus {username} on varattu.")

        except InvalidCredentialsError:
            self._show_error(
                "Käyttäjätunnuksen tulee olla 4-30 merkkiä pitkä, ja salasanan 8-30 merkkiä pitkä.")

        except PasswordConfirmationError:
            self._show_error("Syöttämäsi salasanat eivät vastanneet toisiaan.")

        except InvalidPasswordError:
            self._show_error(
                "Salasanassa tulee olla vähintään 8-30 merkkiä, ja siinä tulee olla vähintään yksi iso kirjain numero.")

    def _show_error(self, message):
        self._error_variable.set(message)
        self._error_label.grid()

    def _hide_error(self):
        self._error_label.grid_remove()

    def _initialize_header(self):
        info_text = "Käyttäjätunnuksen tulee olla 4-30 merkkiä pitkä, ja salasanan 8-30 merkkiä pitkä. Salasanassa tulee olla vähintään yksi iso kirjain, yksi pieni kirjain ja yksi numero."

        info = ttk.Label(master=self._frame, text=info_text, wraplength=400)

        info.grid(padx=10, pady=10, sticky=constants.EW)

    def _initialize_username_field(self):
        username_label = ttk.Label(master=self._frame, text="Käyttäjätunnus:")

        self._username_entry = ttk.Entry(master=self._frame)

        username_label.grid(padx=10, pady=5, sticky=constants.EW)
        self._username_entry.grid(padx=10, pady=5, sticky=constants.EW)

    def _initialize_password_fields(self):
        password_label = ttk.Label(master=self._frame, text="Salasana:")

        self._password_entry = ttk.Entry(master=self._frame, show="*")

        password_label.grid(padx=10, pady=5, sticky=constants.EW)
        self._password_entry.grid(padx=10, pady=5, sticky=constants.EW)

        password2_label = ttk.Label(
            master=self._frame, text="Salasana uudelleen:")

        self._password2_entry = ttk.Entry(master=self._frame, show="*")

        password2_label.grid(padx=10, pady=5, sticky=constants.EW)
        self._password2_entry.grid(padx=10, pady=5, sticky=constants.EW)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._error_variable = StringVar(self._frame)

        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground="red"
        )

        self._error_label.grid(padx=10, pady=5)

        self._initialize_header()
        self._initialize_username_field()
        self._initialize_password_fields()

        create_user_button = ttk.Button(
            master=self._frame,
            text="Rekisteröidy",
            command=self._create_user_handler
        )

        login_button = ttk.Button(
            master=self._frame,
            text="Takaisin",
            command=self._handle_show_login_view
        )

        self._frame.grid_columnconfigure(0, weight=1, minsize=400)

        create_user_button.grid(padx=10, pady=5, sticky=constants.EW)
        login_button.grid(padx=10, pady=5, sticky=constants.EW)

        self._hide_error()

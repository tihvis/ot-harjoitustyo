from tkinter import ttk, StringVar, constants
from services.user_service import user_service, InvalidCredentialsError


class LoginView:
    """Käyttäjän kirjautumisesta vastaava näkymä.
    """

    def __init__(self, root, handle_show_main_view, handle_show_create_user_view):
        """Luokan konstruktori, joka luo uuden kirjautumisnäkymän.

        Args:
            root:
                TKinter-elementti, jonka sisään näkymä alustetaan.
            handle_show_main_view:
                Kutsuttava-arvo, jota kutsutaan kun käyttäjä kirjautuu sisään ja siirretään etusivulle.
            handle_show_create_user_view:
                Kutsuttava-arvo, jota kutsutaan kun siirrytään rekisteröitymisnäkymään.
        """

        self._root = root
        self._handle_show_main_view = handle_show_main_view
        self._handle_show_create_user_view = handle_show_create_user_view
        self._frame = None
        self._username_entry = None
        self._password_entry = None
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

    def _handle_login(self):
        self._handle_show_main_view()

    def _login_handler(self):
        username = self._username_entry.get()
        password = self._password_entry.get()

        try:
            user_service.login(username, password)
            self._handle_login()
        except InvalidCredentialsError:
            self._show_error("Virheellinen käyttäjätunnus tai salasana.")

    def _show_error(self, message):
        self._error_variable.set(message)
        self._error_label.grid()

    def _hide_error(self):
        self._error_label.grid_remove()

    def _initialize_header(self):
        info_text = "Tervetuloa Sisukas-sovellukseen!\n\nSovelluksessa voit pitää kirjaa meneillään olevien kurssien etenemisestä, ja nähdä koosteen aiemmin suoritetuista kursseista.\n\nAloita kirjautumalla sisään tai luomalla uusi käyttäjätunnus."

        info = ttk.Label(master=self._frame, text=info_text, wraplength=400)

        info.grid(padx=10, pady=10, sticky=constants.EW)

    def _initialize_username_field(self):
        username_label = ttk.Label(master=self._frame, text="Käyttäjätunnus:")

        self._username_entry = ttk.Entry(master=self._frame)

        username_label.grid(padx=10, pady=10, sticky=constants.W)
        self._username_entry.grid(padx=10, pady=5, sticky=constants.EW)

    def _initialize_password_field(self):
        password_label = ttk.Label(master=self._frame, text="Salasana:")

        self._password_entry = ttk.Entry(master=self._frame, show="*")

        password_label.grid(padx=10, pady=10, sticky=constants.W)
        self._password_entry.grid(padx=10, pady=5, sticky=constants.EW)

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
        self._initialize_password_field()

        login_button = ttk.Button(
            master=self._frame,
            text="Kirjaudu sisään",
            command=self._login_handler
        )

        create_user_button = ttk.Button(
            master=self._frame,
            text="Luo uusi käyttäjätunnus",
            command=self._handle_show_create_user_view
        )

        self._frame.grid_columnconfigure(0, weight=1, minsize=400)

        login_button.grid(padx=10, pady=5, sticky=constants.EW)
        create_user_button.grid(padx=10, pady=5, sticky=constants.EW)

        self._hide_error()

# src/main.py

import customtkinter as ctk
from frontend.auth_screens import LoginPage, SignupPage
from utils import set_app_icon

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from frontend.app import LinkStashApp


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LinkStash - Login")
        # self.title("LinkStash")
        set_app_icon(self)

        self.geometry("500x400")
        self._frame = None
        self.show_login()

    def clear_frame(self):
        if self._frame is not None:
            self._frame.destroy()

    def show_login(self):
        self.clear_frame()
        self._frame = LoginPage(self, self.show_signup)
        self._frame.pack(fill="both", expand=True)

    def show_signup(self):
        self.clear_frame()
        self._frame = SignupPage(self, self.show_login)
        self._frame.pack(fill="both", expand=True)

    def show_home(self):
        self.clear_frame()
        self._frame = LinkStashApp(
            self, user_id="test", controller=self
        )  # Pass self as the controller
        self._frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

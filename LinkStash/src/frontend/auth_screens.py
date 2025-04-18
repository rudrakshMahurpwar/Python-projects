# src/frontend/auth_screens.py
import sys
import os

# Add the src directory to the system path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)

import customtkinter as ctk
from tkinter import messagebox
from typing import TYPE_CHECKING

from backend.user_manager import UserManager
from frontend.app import LinkStashApp  # Your main app screen after login

if TYPE_CHECKING:
    from main import MainApp


class LoginPage(ctk.CTkFrame):
    def __init__(self, master: "MainApp", show_signup_callback):
        super().__init__(master)
        self.master = master
        self.show_signup_callback = show_signup_callback
        self.user_manager = UserManager()

        ctk.CTkLabel(self, text="Login", font=("Arial", 24)).pack(pady=15)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        ctk.CTkButton(self, text="Login", command=self.login).pack(pady=10)
        ctk.CTkButton(self, text="Sign Up", command=self.show_signup_callback).pack(
            pady=10
        )

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        user_id = self.user_manager.login(username, password)
        if user_id:
            self.master.clear_frame()  # type: ignore
            LinkStashApp(self.master, user_id).pack(fill="both", expand=True)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")


class SignupPage(ctk.CTkFrame):
    def __init__(self, master: "MainApp", switch_to_login):
        super().__init__(master)
        self.master = master
        self.switch_to_login = switch_to_login
        self.user_manager = UserManager()

        ctk.CTkLabel(self, text="Sign Up", font=("Arial", 24)).pack(pady=15)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        self.confirm_entry = ctk.CTkEntry(
            self, placeholder_text="Confirm Password", show="*"
        )
        self.confirm_entry.pack(pady=10)

        ctk.CTkButton(self, text="Create Account", command=self.signup).pack(pady=10)
        ctk.CTkButton(
            self, text="Already have an account? Login", command=self.switch_to_login
        ).pack()

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        if not username or not password or not confirm:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        try:
            self.user_manager.create_user(username, password)
            messagebox.showinfo("Success", "Account created. You can now log in.")
            self.switch_to_login()
        except ValueError as e:
            messagebox.showerror("Signup Failed", str(e))

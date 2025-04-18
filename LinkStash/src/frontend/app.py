import os
import sys
from typing import TYPE_CHECKING

# Add the src directory to the system path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)

import customtkinter as ctk

if TYPE_CHECKING:
    from main import MainApp

from utils import set_app_icon, shorten_url, export_to_csv
from backend.data_manager import LinkManager
from frontend.ui_components import create_link_frame, create_edit_popup

# from frontend.auth_screens import LoginPage


class Misc:
    def __init__(self, master):
        self.master = master

    def clear_frame(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def show_next_screen(self, user_id):
        if user_id:
            self.clear_frame()
            LinkStashApp(self.master, user_id).pack(fill="both", expand=True)
        else:
            print("User ID is required")

    def log_out(self):
        pass


class LinkStashApp(ctk.CTkFrame):
    def __init__(self, root, user_id="test", controller=None):
        self.root = root
        self.controller = controller
        print(f"Controller passed to LinkStashApp: {self.controller}")  # Debugging

        self.root.title("LinkStash")

        set_app_icon(self.root)  # Set the app icon
        ctk.set_appearance_mode(ctk.get_appearance_mode())  # system default
        try:
            self.link_manager = LinkManager(user_id=user_id)
        except ConnectionError as e:
            ctk.CTkLabel(self.root, text=str(e), text_color="red").pack(pady=10)
            return
        self.search_term = ""
        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.destroy)

    def destroy(self):
        try:
            self.link_manager.close()
        except Exception as e:
            print(f"Error closing LinkManager: {e}")
        self.root.destroy()

    def create_button(self, parent, text, command, color="blue", **kwargs):
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            fg_color=color,
            hover_color=f"dark{color}",
            **kwargs,
        )

    def setup_ui(self):
        header_frame = ctk.CTkFrame(self.root)
        header_frame.pack(fill="x", pady=5)

        welcome_label = ctk.CTkLabel(
            header_frame,
            text="Welcome to LinkStash! Your One Stop Link Manager!",
            text_color=("black", "white"),
        )
        welcome_label.pack(side="left", padx=5)

        self.mode_switch = ctk.CTkSwitch(
            header_frame,
            text="Dark Mode",
            command=self.toggle_mode,
            onvalue="dark",
            offvalue="light",
            switch_width=40,
            switch_height=20,
        )
        self.mode_switch.pack(side="right", padx=5)
        current_mode = ctk.get_appearance_mode()
        if current_mode == "dark":
            self.mode_switch.deselect()
        else:
            self.mode_switch.select()

        # Add a logout button
        logout_button = ctk.CTkButton(
            header_frame,
            text="Logout",
            command=self.logout,
            fg_color="red",
            hover_color="darkred",
        )
        logout_button.pack(side="right", padx=10)

        input_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        input_frame.pack(pady=10, padx=10, fill="x")

        self.url_entry = ctk.CTkEntry(
            input_frame, placeholder_text="Enter URL", width=200
        )
        self.url_entry.pack(side="left", padx=5)
        self.url_entry.bind("<Return>", lambda event: self.add_link())

        self.notes_entry = ctk.CTkEntry(
            input_frame, placeholder_text="Enter Notes (optional)", width=200
        )
        self.notes_entry.pack(side="left", padx=5)
        self.notes_entry.bind("<Return>", lambda event: self.add_link())

        add_button = ctk.CTkButton(
            input_frame,
            text="Add Link",
            command=self.add_link,
            fg_color="blue",
            hover_color="darkblue",
        )
        add_button.pack(side="right", padx=5)

        search_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        search_frame.pack(pady=5, padx=10, fill="x")

        self.search_entry = ctk.CTkEntry(
            search_frame, placeholder_text="Search URLs", width=200
        )
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.update_search)

        search_button = ctk.CTkButton(
            search_frame,
            text="Search",
            command=self.update_search,
            fg_color="blue",
            hover_color="darkblue",
            width=80,
        )
        search_button.pack(side="right", padx=5)

        clear_button = ctk.CTkButton(
            search_frame,
            text="Clear",
            command=self.clear_search,
            fg_color="blue",
            hover_color="darkblue",
            width=80,
        )
        clear_button.pack(side="right", padx=5)

        export_button = ctk.CTkButton(
            search_frame,
            text="Export CSV",
            command=self.export_links_to_csv,
            fg_color="green",
            hover_color="darkgreen",
            width=80,
        )
        export_button.pack(side="right", padx=5)

        self.count_label = ctk.CTkLabel(self.root, text="Total links: 0")
        self.count_label.pack(pady=5)

        self.links_frame = ctk.CTkScrollableFrame(self.root, width=450, height=300)
        self.links_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.refresh_links()

    def add_link(self):
        url = self.url_entry.get().strip()
        notes = self.notes_entry.get().strip()
        if url and url.startswith(("http://", "https://")):
            self.link_manager.add_link(url, notes)
            self.url_entry.delete(0, "end")
            self.notes_entry.delete(0, "end")
            self.refresh_links()
            success_label = ctk.CTkLabel(
                self.root,
                text=f"Added: {shorten_url(url, 30)}",
                text_color="green",
            )
            success_label.pack(pady=5)
            self.root.after(2000, success_label.destroy)
        else:
            error_label = ctk.CTkLabel(
                self.root,
                text="Invalid URL! Must start with http:// or https://",
                text_color="red",
            )
            error_label.pack(pady=5)
            self.root.after(2000, error_label.destroy)

    def delete_link(self, link_id, url):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Confirm Delete")
        popup.geometry("300x150")
        popup.transient(self.root)
        popup.grab_set()

        message = ctk.CTkLabel(
            popup, text=f"Delete {shorten_url(url, 30)}?", wraplength=250
        )
        message.pack(pady=20)

        button_frame = ctk.CTkFrame(popup)
        button_frame.pack(pady=10)

        yes_button = ctk.CTkButton(
            button_frame,
            text="Yes",
            fg_color="red",
            hover_color="darkred",
            command=lambda: self.confirm_delete(link_id, popup),
        )
        yes_button.pack(side="left", padx=5)

        no_button = ctk.CTkButton(
            button_frame,
            text="No",
            fg_color="blue",
            hover_color="darkblue",
            command=popup.destroy,
        )
        no_button.pack(side="left", padx=5)

    def edit_link(self, link_id, current_url, current_notes):
        create_edit_popup(self, link_id, current_url, current_notes)

    def save_edited_link(self, link_id, new_url, new_notes, popup):
        if new_url.strip() and new_url.startswith(("http://", "https://")):
            self.link_manager.update_link(link_id, new_url, new_notes)
            self.refresh_links()
            popup.destroy()
        else:
            error_label = ctk.CTkLabel(
                popup,
                text="Invalid URL! Must start with http:// or https://",
                text_color="red",
            )
            error_label.pack(pady=5)

    def confirm_delete(self, link_id, popup):
        self.link_manager.delete_link(link_id)
        self.refresh_links()
        popup.destroy()

    def update_search(self, event=None):
        if hasattr(self, "_search_after_id"):
            self.root.after_cancel(self._search_after_id)
        self._search_after_id = self.root.after(300, self._perform_search)

    def _perform_search(self):
        self.search_term = self.search_entry.get().strip()
        self.refresh_links()

    def clear_search(self):
        self.search_entry.delete(0, "end")
        self.search_term = ""
        self.refresh_links()

    def refresh_links(self):
        for widget in self.links_frame.winfo_children():
            widget.destroy()

        links = self.link_manager.get_links(self.search_term)
        self.count_label.configure(text=f"Total links: {len(links)}")

        if not links and self.search_term:
            no_results = ctk.CTkLabel(
                self.links_frame, text="No links found!", text_color="gray"
            )
            no_results.pack(pady=10)
            return

        for i, link in enumerate(links, 1):
            create_link_frame(self.links_frame, i, link, self)

    def toggle_mode(self):
        new_mode = self.mode_switch.get()
        self.root.after(100, lambda: self._apply_mode(new_mode))

    def _apply_mode(self, mode):
        ctk.set_appearance_mode(mode)
        self.root.update_idletasks()
        self.root.update()

    def logout(self):
        """Handle the logout functionality."""
        print("User logged out.")
        if self.controller:
            self.controller.show_login()  # Navigate to the login screen
        else:
            print("Controller not set. Cannot navigate to login screen.")

    def export_links_to_csv(self):
        links = self.link_manager.get_links(self.search_term)
        if not links:
            error_message = (
                "No links to export. Try adjusting the search."
                if self.search_term
                else "No links available to export."
            )
            error_label = ctk.CTkLabel(self.root, text=error_message, text_color="red")
            error_label.pack(pady=5)
            self.root.after(2000, error_label.destroy)
            return

        success, filename = export_to_csv(links)  # No headers argument

        if success:
            message = f"Exported {len(links)} {'filtered links' if self.search_term else 'links'} to {filename}"
            success_label = ctk.CTkLabel(self.root, text=message, text_color="green")
            success_label.pack(pady=5)
            self.root.after(2000, success_label.destroy)
        else:
            error_label = ctk.CTkLabel(
                self.root,
                text="Failed to export. Check permissions or try again.",
                text_color="red",
            )
            error_label.pack(pady=5)
            self.root.after(2000, error_label.destroy)


if __name__ == "__main__":
    root = ctk.CTk()
    app = LinkStashApp(root)
    root.geometry("500x500")
    root.mainloop()

import customtkinter as ctk
from utils import shorten_url, open_url, format_date


def create_link_frame(parent, index, link, app_instance):
    link_frame = ctk.CTkFrame(parent)
    link_frame.pack(fill="x", pady=2, padx=5)

    url_text = shorten_url(link["url"])
    label = format_date(link.get("saved_at", ""))
    link_button = ctk.CTkButton(
        link_frame,
        text=f"{index}. {url_text} ({label})",
        anchor="w",
        fg_color="transparent",
        text_color="blue",
        hover_color=("#e5e5e5", "#333333"),
        command=lambda url=link["url"]: open_url(url),
    )
    link_button.pack(side="left", padx=5)

    notes = link.get("notes", "")
    notes_label = ctk.CTkLabel(
        link_frame,
        text=f"Notes: {notes}" if notes else "Notes: N/A",
        wraplength=200,
        text_color="gray",
    )
    notes_label.pack(side="left", padx=5)

    edit_button = ctk.CTkButton(
        link_frame,
        text="Edit",
        width=80,
        fg_color="blue",
        hover_color="darkblue",
        command=lambda id=link["_id"], url=link["url"], notes=link[
            "notes"
        ]: app_instance.edit_link(id, url, notes),
    )
    edit_button.pack(side="right", padx=5)

    delete_button = ctk.CTkButton(
        link_frame,
        text="Delete",
        width=80,
        fg_color="red",
        hover_color="darkred",
        command=lambda id=link["_id"], url=link["url"]: app_instance.delete_link(
            id, url
        ),
    )
    delete_button.pack(side="right", padx=5)
    return link_frame


def create_edit_popup(app_instance, link_id, current_url, current_notes):
    popup = ctk.CTkToplevel(app_instance.root)
    popup.title("Edit Link")
    popup.geometry("400x250")
    popup.transient(app_instance.root)
    popup.grab_set()

    ctk.CTkLabel(popup, text="Edit URL:").pack(pady=10)
    url_entry = ctk.CTkEntry(popup, width=350)
    url_entry.insert(0, current_url)
    url_entry.pack(pady=5)

    ctk.CTkLabel(popup, text="Edit Notes:").pack(pady=10)
    notes_entry = ctk.CTkEntry(popup, width=350)
    notes_entry.insert(0, current_notes)
    notes_entry.pack(pady=5)

    button_frame = ctk.CTkFrame(popup)
    button_frame.pack(pady=10)

    save_button = ctk.CTkButton(
        button_frame,
        text="Save",
        fg_color="blue",
        hover_color="darkblue",
        command=lambda: app_instance.save_edited_link(
            link_id, url_entry.get(), notes_entry.get(), popup
        ),
    )
    save_button.pack(side="left", padx=5)

    cancel_button = ctk.CTkButton(
        button_frame,
        text="Cancel",
        fg_color="blue",
        hover_color="darkblue",
        command=popup.destroy,
    )
    cancel_button.pack(side="left", padx=5)
    return popup

from datetime import datetime
from tkinter import filedialog
import webbrowser
import csv
import os


def set_app_icon(window):
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
        window.iconbitmap(default=icon_path)
    except Exception as e:
        print(f"[Icon Error] Could not set icon: {e}")


def export_to_csv(links):
    """
    Prompts user to save a CSV file with link data.

    Column order: ID, Saved At, URL, Notes

    Returns:
    - (success: bool, filename: str or None)
    """
    if not links:
        return False, None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_name = f"linkstash_export_{timestamp}.csv"

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        initialfile=default_name,
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        title="Save CSV File",
    )

    if not file_path:
        return False, None

    try:
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Header in custom order
            writer.writerow(["ID", "Saved At", "URL", "Notes"])
            for link in links:
                writer.writerow(
                    [
                        link.get("_id", ""),
                        format_date(link.get("saved_at", "")),
                        link.get("url", ""),
                        link.get("notes", ""),
                    ]
                )
        return True, file_path
    except Exception as e:
        print(f"[ERROR] CSV export failed: {e}")
        return False, None


def shorten_url(url, max_length=50):
    return url[:max_length] + ("..." if len(url) > max_length else "")


def open_url(url):
    webbrowser.open(url)


def format_date(iso_date):
    if not iso_date:
        return "No date"
    try:
        dt = datetime.fromisoformat(iso_date)
        return dt.strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return "Invalid date"

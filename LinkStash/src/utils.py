from datetime import datetime
import csv


def export_to_csv(links):
    if not links:
        return False, None
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"linkstash_export_{timestamp}.csv"
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "URL", "Notes", "Saved At"])
            for link in links:
                writer.writerow(
                    [
                        link["_id"],
                        link["url"],
                        link["notes"],
                        format_date(link["saved_at"]),
                    ]
                )
        return True, filename
    except Exception:
        return False, None


def shorten_url(url, max_length=50):
    return url[:max_length] + ("..." if len(url) > max_length else "")


def format_date(iso_date):
    if not iso_date:
        return "No date"
    try:
        dt = datetime.fromisoformat(iso_date)
        return dt.strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return "Invalid date"

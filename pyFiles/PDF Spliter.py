import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
import io
import os

def split_pdf_by_size_gui(input_pdf, target_size_mb):
    reader = PdfReader(input_pdf)
    total_pages = len(reader.pages)
    target_bytes = target_size_mb * 1024 * 1024
    part = 1
    writer = PdfWriter()
    
    for i, page in enumerate(reader.pages):
        writer.add_page(page)
        temp_stream = io.BytesIO()
        writer.write(temp_stream)
        size = temp_stream.tell()

        if size >= target_bytes or i == total_pages - 1:
            output_filename = f"{os.path.splitext(os.path.basename(input_pdf))[0]}_part_{part}.pdf"
            with open(output_filename, "wb") as f:
                f.write(temp_stream.getbuffer())
            part += 1
            writer = PdfWriter()

    messagebox.showinfo("Done", f"PDF split into {part - 1} parts!")

def browse_file():
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if filepath:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, filepath)

def run_split():
    try:
        file_path = entry_file.get()
        size_mb = float(entry_size.get())
        if not file_path or not file_path.lower().endswith(".pdf"):
            raise ValueError("Invalid file selected.")
        split_pdf_by_size_gui(file_path, size_mb)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- GUI Setup ---
root = tk.Tk()
root.title("PDF Splitter by Size (MB)")
root.geometry("400x200")

tk.Label(root, text="Select PDF File:").pack(pady=5)
entry_file = tk.Entry(root, width=50)
entry_file.pack()
tk.Button(root, text="Browse", command=browse_file).pack(pady=5)

tk.Label(root, text="Max size per file (MB):").pack(pady=5)
entry_size = tk.Entry(root, width=10)
entry_size.insert(0, "5")
entry_size.pack()

tk.Button(root, text="Split PDF", command=run_split).pack(pady=20)

root.mainloop()

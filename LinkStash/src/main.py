import customtkinter as ctk
from frontend.app import LinkStashApp

if __name__ == "__main__":
    root = ctk.CTk()
    app = LinkStashApp(root)
    root.geometry("500x500")
    root.mainloop()

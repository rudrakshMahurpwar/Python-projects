import tkinter as tk
from tkinter import messagebox
import random, string

class MyPasswordGenerator:
    def __init__(self):

        self.root = tk.Tk()

        #window Description
        #self.root.geometry("700x450")
        self.root.title("Personal Password Generator")

        #Dummy Lable
        self.label = tk.Label(self.root, text = "Personal Password Generator", font = ("Arial", 16))
        self.label.pack(pady=7)

        #self.labelo = tk.Label(self.root, text = '')
        #self.labelo.pack()

        #Checkbox Frames
        self.checkbox = tk.Frame(self.root)

        self.checkbox.columnconfigure(0, weight = 1)
        self.checkbox.columnconfigure(1, weight = 1)
        self.checkbox.columnconfigure(2, weight = 1)

        # Variables to store checkbox states
        self.uppercase = tk.BooleanVar()
        self.digits = tk.BooleanVar()
        self.lowercase = tk.BooleanVar()
        self.specialCharacters = tk.BooleanVar()

        # Checkboxes
        self.uppercase_box = tk.Checkbutton(self.checkbox, text = "Uppercase", variable=self.uppercase)
        self.digits_box = tk.Checkbutton(self.checkbox, text = "Digits", variable=self.digits)
        self.lowercase_box = tk.Checkbutton(self.checkbox, text = "Lowercase", variable=self.lowercase)
        self.specialCharacters_box = tk.Checkbutton(self.checkbox, text = "Special Characters", variable=self.specialCharacters)

        # Input Box
        self.length_lable = tk.Label(self.checkbox, text = "Length of the password: ")
        self.length = tk.Entry(self.checkbox)
        self.length.bind("<Return>", self.pressedEnter)
        
        # Checkboxes
        self.uppercase_box.grid(row=0,column=0, sticky = tk.W, padx=50)
        self.digits_box.grid(row=0,column=1, sticky = tk.W, padx=50)
        self.lowercase_box.grid(row=1,column=0, sticky = tk.W, padx=50)
        self.specialCharacters_box.grid(row=1,column=1, sticky = tk.W, padx=50)

        # Input Box
        self.length_lable.grid(row=2,column=0, sticky = tk.E)
        self.length.grid(row=2,column=1, sticky = tk.W)

        # OK Button to generate password
        self.ok_button = tk.Button(self.checkbox, text="OK", command=self.pressedEnter)
        self.ok_button.grid(row=2,column=2, sticky = tk.W)

        self.checkbox.pack(pady=5)
        
        # Lable
        self.result_label = tk.Label(self.root, text="", font=("Calibri", 10))
        self.result_label.pack()
        
        #Textbox
        self.textbox = tk.Text(self.root, height=2)
        self.textbox.pack(padx=5,pady=5)
        
        tk.mainloop()
        
    def pressedEnter(self, event=None):
        
        self.result_label.config(text="")

        if not self.length.get().isdigit() or int(self.length.get()) <= 0:
            self.result_label.config(text="Error: Length must be a positive integer.", fg="red")
            return

        self.password = self.passwordGenerator(
            uppercase=self.uppercase.get(),
            lowercase=self.lowercase.get(),
            digits=self.digits.get(),
            specialCharacters=self.specialCharacters.get(),
            length=int(self.length.get())
        )

        if not self.password:
            messagebox.showerror("Error", "You must select at least one option (Uppercase, Lowercase, Numbers, or Special Characters).")
            return

        self.textbox.config(state=tk.NORMAL)
        self.textbox.delete(1.0, tk.END)
        self.textbox.insert(tk.END, self.password)
        self.textbox.config(state=tk.DISABLED)
        
    def passwordGenerator(self, uppercase=True, lowercase=True, digits=True, specialCharacters=True, length = 12):

        character = ''
        if uppercase:
            character += string.ascii_uppercase
        if lowercase:
            character += string.ascii_lowercase
        if digits:
            character += string.digits
        if specialCharacters:
            character += string.punctuation

        if not character:
            return None

        password = ''.join(random.choices(character, k=length))
        #print(password)
        return password

MyPasswordGenerator()        

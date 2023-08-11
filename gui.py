import tkinter as tk

from tkinter import ttk

import os

import unittest

def create_field_box(window, row, column, names):

    frame = tk.Frame(window, width=400, height=500, bd=1, relief=tk.SOLID, bg="#1A2226")

    frame.grid(row=row, column=column, padx=10, pady=10, sticky="n")

 

    frame.pack_propagate(False)

 

    listbox = tk.Listbox(frame, font=('Arial', 14), bg="black", fg="#ECF0F5",

                         selectbackground="#222D32", selectforeground="#ECF0F5")

    listbox.pack(fill=tk.BOTH, expand=True)

 

    for name in names:

        listbox.insert(tk.END, name)

 

def list_files_with_extension(directory, extension):

    files = [file for file in os.listdir(directory) if file.endswith(extension)]

    return files

 

def admin_panel():

    root.withdraw()

 

    window = tk.Tk()

    window.title("Users and groups")

    window.geometry("850x600")

    window.config(bg="black")

 

    directory_scan_label = tk.Label(window, text="Ports scan", font=(

    'Arial', 18, 'bold'), bg="black", fg="green")

    directory_scan_label.grid(row=0, column=0, pady=(20, 5), padx=20, sticky="ew")

 

    scan_files = list_files_with_extension(".", ".scan.txt")

    create_field_box(window, row=1, column=0, names=scan_files)

 

    web_info_label = tk.Label(window, text="Directory Scan", font=(

    'Arial', 18, 'bold'), bg="black", fg="green")

    web_info_label.grid(row=0, column=1, pady=(20, 5), padx=20, sticky="ew")

 

    info_files = list_files_with_extension(".", ".info.txt")

    create_field_box(window, row=1, column=1, names=info_files)

 

    window.mainloop()

 

def login():

    username = username_entry.get()

    password = password_entry.get()

 

    if username == "admin" and password == "admin":

        admin_panel()

    else:

        show_login_error()

 

def show_login_error():

    login_error_label.grid(row=4, column=0, columnspan=2, pady=10)

 

root = tk.Tk()

root.title("Admin Login")

root.geometry("800x600")

root.configure(bg="black")  # Set red background color

 

style = ttk.Style()

style.configure("TLabel", background="black", foreground="green", font=("Helvetica", 12))

 

login_frame = ttk.Frame(root, padding=20, style="TLabel")  # Apply the label style

login_frame.pack(expand=True)

 

login_label = ttk.Label(login_frame, text="Admin Login", font=("Helvetica", 28, "bold"))

login_label.grid(row=0, column=0, columnspan=2, pady=20)

 

username_label = ttk.Label(login_frame, text="Username:")

username_label.grid(row=1, column=0, padx=(0, 10), sticky="e")

 

username_entry = ttk.Entry(login_frame)

username_entry.grid(row=1, column=1, pady=5, sticky="w")

 

password_label = ttk.Label(login_frame, text="Password:")

password_label.grid(row=2, column=0, padx=(0, 10), sticky="e")

 

password_entry = ttk.Entry(login_frame, show="*")

password_entry.grid(row=2, column=1, pady=20, sticky="w")

 

login_button = ttk.Button(login_frame, text="Login", command=login)

login_button.grid(row=3, column=0, columnspan=2)

def show_login_error():

    login_error_label.grid(row=4, column=0, columnspan=2, pady=10)

login_error_label = ttk.Label(

    login_frame, text="Invalid username or password.", foreground="red")

 

root.mainloop()

 

class TestAdminLogin(unittest.TestCase):

    def test_correct_login(self):

        username_entry.insert(0, "admin")

        password_entry.insert(0, "admin")

        login_button.invoke()

        self.assertEqual(login_error_label.cget("text"), "")

 

    def test_incorrect_login(self):

        username_entry.insert(0, "wrong_user")

        password_entry.insert(0, "wrong_password")

        with self.assertRaises(AssertionError):

            login_button.invoke()

        self.assertEqual(login_error_label.cget("text"), "Invalid credentials")

if __name__ == "__main__":

    unittest.main()
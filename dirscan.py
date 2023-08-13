import tkinter as tk
from tkinter import filedialog, messagebox
import socket
import requests
import threading

class DirectoryScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Directory Scanner")
        self.root.geometry("500x650")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 500
        window_height = 650
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.scan_thread = None  

        
        self.first_frame = tk.Frame(root, bg="black")
        self.first_frame.grid(row=0, column=0, rowspan=12, columnspan=12, sticky="nsew")
        for i in range(12):
            self.first_frame.rowconfigure(i, minsize=50)
        for i in range(12):
            self.first_frame.columnconfigure(i, minsize=70)

        self.url_label = tk.Label(self.first_frame, text="Enter URL:",  fg="black",  bg="Green")  # Set label text color to green
        self.url_label.grid(row=0, column=0, padx=10, pady=10)

        self.ip_address_entry = tk.Entry(self.first_frame, width=25, bg="#222222")
        self.ip_address_entry.grid(row=0, column=1, padx=10, pady=10)

        self.browse_button = tk.Button(self.first_frame, text="Browse File", command=self.browse_file, fg="Black", bg="Green")  
        self.browse_button.grid(row=0, column=2, padx=10, pady=10)

        self.scan_button = tk.Button(self.first_frame, text="Scan Directories", command=self.start_scan, fg="black",  bg="Green")
        self.scan_button.grid(row=0, column=3, padx=10, pady=10)

        self.search_label = tk.Label(self.first_frame, text="Search:", fg="Black", bg="Green")  
        self.search_label.grid(row=1, column=0, padx=10, pady=10)

        self.search_entry = tk.Entry(self.first_frame, bg="#222222")
        self.search_entry.grid(row=1, column=1, padx=10, pady=10)

        self.output_field = tk.Text(self.first_frame, wrap=tk.WORD, height=25, width=50, bg="#222222", fg="Green")
        self.output_field.grid(row=2, column=0, columnspan=4, padx=10, pady=10)
        self.output_scrollbar = tk.Scrollbar(self.first_frame, command=self.output_field.yview)
        self.output_scrollbar.grid(row=2, column=4, sticky="ns")
        self.output_field.config(yscrollcommand=self.output_scrollbar.set)

        self.save_button = tk.Button(self.first_frame, text="Save Output", command=self.save_output, fg="black",  bg="Green")  
        self.save_button.grid(row=3, column=0, columnspan=4, pady=10, sticky="w") 

    def start_scan(self):
        if self.scan_thread and self.scan_thread.is_alive():
            messagebox.showinfo("Info", "A scan is already in progress")
            return

        self.scan_thread = threading.Thread(target=self.perform_scan)
        self.scan_thread.start()

    def perform_scan(self):
        url = self.ip_address_entry.get()
        if not url:
            messagebox.showinfo("Error", "Please enter a URL")
            return

        if hasattr(self, 'directory'):
            directories = self.read_directory_list(self.directory)
            self.check_directories(url, directories)
        else:
            messagebox.showinfo("Error", "Please select a directory list file")


    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.directory = file_path

    def scan_directories(self):
        url = self.ip_address_entry.get()
        if not url:
            messagebox.showinfo("Error", "Please enter a URL")
            return

        if hasattr(self, 'directory'):
            directories = self.read_directory_list(self.directory)
            self.check_directories(url, directories)
        else:
            messagebox.showinfo("Error", "Please select a directory list file")

    def read_directory_list(self, directory):
        try:
            with open(directory, 'r') as f:
                directories = f.read().splitlines()
            return directories
        except FileNotFoundError:
            self.output_field.insert(tk.END, f'{directory} does not exist\n')
            return []

    def check_directories(self, url, directories):
        self.output_field.config(state=tk.NORMAL)
        self.output_field.delete('1.0', tk.END)
        directories_dont_exist = []

        try:
            for directory in directories:
                response = requests.get(f'{url}/{directory}')
                if response.status_code == 200:
                    self.output_field.insert(tk.END, f'{url}/{directory} exists\n')
                else:
                    self.output_field.insert(tk.END, f'{url}/{directory} doesn\'t exist\n')
                    directories_dont_exist.append(directory)
        except (socket.gaierror, requests.exceptions.RequestException):
            self.output_field.insert(tk.END, f'An error occurred while scanning {url}\n')

        self.output_field.config(state=tk.DISABLED)
        self.highlight_search_text()

        if directories_dont_exist:
            self.output_field.insert(tk.END, "Directories that don't exist:\n")
            for directory in directories_dont_exist:
                self.output_field.insert(tk.END, f'- {directory}\n')

    def highlight_search_text(self):
        search_text = self.search_entry.get()

        if not search_text:
            return

        self.output_field.tag_remove('highlight', '1.0', tk.END)
        self.output_field.tag_config('highlight', background='yellow', foreground='green')

        start_index = "1.0"
        found = False

        while True:
            start_index = self.output_field.search(search_text, start_index, stopindex=tk.END)
            if not start_index:
                break
            found = True
            end_index = f"{start_index}+{len(search_text)}c"
            self.output_field.tag_add('highlight', start_index, end_index)
            start_index = end_index

        if not found:
            messagebox.showinfo("Search Result", "No results found")

    def save_output(self):
        output_text = self.output_field.get('1.0', tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write(output_text)
            messagebox.showinfo("Save Result", "Output saved to file")

if __name__ == "__main__":
    root = tk.Tk()
    app = DirectoryScannerApp(root)
    root.mainloop()

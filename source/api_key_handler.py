import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import configparser

def retrieve_api_key():
        config = configparser.ConfigParser()
        config.read('config.ini')

        if 'API' in config and 'API_KEY' in config['API']:
            api_key = config['API']['API_KEY']
            return str(api_key)


class ApiWindow():
    def __init__(self, root):
        self.root = root

    def create_api_button(self):
        api_button = ttk.Button(self.root, text='API Key', command=self.open_api_window)
        api_button.grid(row=0, column=1, padx=5, sticky='e')

    def save_api_key(self):
        api_key = self.api_key_entry.get()

        config = configparser.ConfigParser()
        config['API'] = {'API_KEY': api_key}

        with open('config.ini', 'w') as config_file:
            config.write(config_file)

        self.api_key_window.destroy()
        messagebox.showinfo('Success', 'API key saved successfully.')

    def open_link(self, url):
        webbrowser.open(url)

    def open_api_window(self):
        self.api_key_window = tk.Toplevel(self.root)
        self.api_key_window.title('API Key')
        self.api_key_window.geometry('450x170')
        self.api_key_window.resizable(False, False)

        api_key_label = ttk.Label(self.api_key_window, text='Insert your API Key:')
        api_key_label.pack(pady=5)

        self.api_key_entry = ttk.Entry(self.api_key_window)
        self.api_key_entry.pack(pady=5)

        save_button = ttk.Button(self.api_key_window, text='Save Key', command=self.save_api_key)
        save_button.pack(pady=5)

        link_description = ttk.Label(self.api_key_window, text='If you do not have an API key, register for free at the following link')
        link_description.pack(padx=5, pady=5)

        link_label = ttk.Label(self.api_key_window, text='https://calorieninjas.com/register', cursor='hand2')
        link_label.pack(pady=5)
        link_label.bind('<Button-1>', lambda e: self.open_link('https://calorieninjas.com/register'))

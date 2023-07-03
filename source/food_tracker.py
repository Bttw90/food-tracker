import tkinter as tk
from tkinter import ttk, StringVar
import sv_ttk
from tk_frame_class import FoodFrame
from datetime import date 
import sqlite3
from functions import open_calendar, save, calculate
from api_key_handler import ApiWindow

con = sqlite3.connect('tracker.db')
cursor = con.cursor()

# Create database for first time running the program
cursor.execute('CREATE TABLE IF NOT EXISTS data (date TEXT PRIMARY KEY, macros_serialized BLOB, meals_serialized BLOB)')

# Create main frame
root = tk.Tk()
root.title('Food Tracker')
root.geometry('785x585')
root.resizable(False, False)

# Create 4 subframes for data entry, appending every frame to a list for a subsequent loop
meal_list = []

breakfast = FoodFrame(root, 1, 0, 'Breakfast')
breakfast.create_frame()
meal_list.append(breakfast)
lunch = FoodFrame(root, 2, 0, 'Lunch')
lunch.create_frame()
meal_list.append(lunch)
dinner = FoodFrame(root, 1, 1, 'Dinner')
dinner.create_frame()
meal_list.append(dinner)
snacks = FoodFrame(root, 2, 1, 'Snacks')
snacks.create_frame()
meal_list.append(snacks)

# Create treeview for showing data
tree = ttk.Treeview(root, columns=('Macros', 'Values'), show='headings', height=6)
tree.grid(row=3, column=0, padx=5, pady=5, sticky='e')

tree.heading('#1', text='Macronutrients:')
tree.heading('#2', text='Values:')

macros = ['Carbs', 'Fats', 'Proteins', 'Fiber', 'Sugar', 'Calories']

tv_frame = ttk.Frame(root)
tv_frame.grid(row=3, column=1)

# Create popup window for API key insertion
api_win = ApiWindow(root)
api_win.create_api_button()

# Create popup calendar for loading specific day
today_date = date.today().strftime('%d/%m/%Y')
var_date = StringVar(value=today_date)

calendar_button = ttk.Button(root, textvariable=var_date, command=lambda: open_calendar(var_date, meal_list, cursor, tree, macros, root))
calendar_button.grid(row=0 , column=0, pady=10, columnspan=2)

# Calculates macro nutriens
calculate_button = ttk.Button(tv_frame, text='Calculate', command=lambda: calculate(meal_list, tree, macros))
calculate_button.grid(row=0, column=0)

# Save selected day
save_button = ttk.Button(tv_frame, text='Save', command=lambda: save(tree, meal_list, cursor, var_date, con))
save_button.grid(row=0, column=1, padx=5)

sv_ttk.set_theme('dark')
root.mainloop()
con.close()
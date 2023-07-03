import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import pickle
import requests
import json
from api_key_handler import retrieve_api_key

# Open calendar and load a date with meals if saved
def open_calendar(var_date, meal_list, cursor, tree, macros, root):
    def select_date():
        fetched_list = []
        selected_date = cal.selection_get()
        date = selected_date.strftime('%d/%m/%Y')
        top.destroy()
        var_date.set(date)

        for meal in meal_list:
            if len(meal.food) != 0:
                for i in range(len(meal.food)):
                    meal.del_food(canvas=meal.load_list[1]) # Old scrollable_frame=meal.load_list[0], 

        cursor.execute('SELECT * FROM data WHERE date = ?', (date,))

        result = cursor.fetchall()
        for row in result:
            fetched_macros = row[1]
            macros_deserialized = pickle.loads(fetched_macros)
            fetched_list.append(macros_deserialized)
            fectched_meals = row[2]
            meals_deserialized = pickle.loads(fectched_meals)
            fetched_list.append(meals_deserialized)

        tree.delete(*tree.get_children())

        if fetched_list:
            for i in range(len(macros)):
                tree.insert('', tk.END, values=(macros[i], round(float(fetched_list[0][i]), 2)))

            for meal in meal_list:
                for key in meals_deserialized:
                    if meal.name == key.split('_food')[0] and len(meals_deserialized[key]) != 0:
                        for i in range(len(meals_deserialized[key])):
                            meal.add_food(scrollable_frame=meal.load_list[0], canvas=meal.load_list[1])
                            meal.food[i].insert(0, meals_deserialized[key][i])
                    elif meal.name == key.split('_quantity')[0] and len(meals_deserialized[key]) != 0:
                        for i in range(len(meals_deserialized[key])):
                            meal.quantity[i].insert(0, meals_deserialized[key][i])

    top = tk.Toplevel(root)
    top.resizable(False, False)
    cal = Calendar(top, selectmode='day')
    cal.pack(pady=20)

    confirm_button = ttk.Button(top, text='Select', command=select_date)
    confirm_button.pack(pady=5)


# Save current meals
def save(tree, meal_list, cursor, var_date, con):
    macros = []
    meal_dict = {}
    all_items = tree.get_children()
    for item in all_items:
        values = tree.item(item)['values']
        macros.append(values[1])

    for meal in meal_list:
        key_food = str(meal.name) + '_food'
        key_quantity = str(meal.name) + '_quantity'
        meal_dict[key_food] = []
        meal_dict[key_quantity] = []
        for element in meal.food:
            if element.get() != '':
                meal_dict[key_food].append(element.get())
        for element in meal.quantity:
            if element.get() != '':    
                meal_dict[key_quantity].append(element.get())
    
    macros_serialized = pickle.dumps(macros)
    meal_dict_serialized = pickle.dumps(meal_dict)

    cursor.execute('INSERT OR REPLACE INTO data (date, macros_serialized, meals_serialized) VALUES (?, ?, ?)', (var_date.get(), macros_serialized, meal_dict_serialized))
    con.commit()

    messagebox.showinfo('Success', 'Meals saved successfully.')


# Calculates macro nutriens with API call
def calculate(meal_list, tree, macros):
    food = []
    quantity = []
    api_key = retrieve_api_key()
    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='

    if api_key == None:
        messagebox.showinfo('Warning', 'API key not present.')
    else:
        for meal in meal_list:
            for element in meal.food:
                if element.get() != '' and element.get().isalpha():
                    food.append(element.get())
                else:
                    messagebox.showerror('Error', 'Error: Empty food entries or presence of numbers.')
                    break
            for element in meal.quantity:
                if element.get() != '' and element.get().isdigit():
                    quantity.append(element.get())
                else:
                    messagebox.showerror('Error', 'Error: Empty quantity entries or presence of letters.')
                    break

        if not food:
            messagebox.showerror('Error' ,'Error: No food inserted')
        else:
            query = ', '.join([f'{q} g {f}' for f, q in zip(food, quantity)])
            response = requests.get(api_url + query, headers={'X-Api-Key': api_key})

            if response.status_code == requests.codes.ok:
                data = json.loads(response.text)
                items = data["items"]

                carbs_count = 0
                fats_count = 0
                proteins_count = 0
                fiber_count = 0
                sugar_count = 0
                calories_count = 0
                
                for item in items:
                    carbs = item['carbohydrates_total_g']
                    carbs_count += carbs
                    fats = item['fat_total_g'] 
                    fats_count += fats
                    proteins = item['protein_g'] 
                    proteins_count += proteins
                    fiber = item['fiber_g'] 
                    fiber_count += fiber
                    sugar = item['sugar_g'] 
                    sugar_count += sugar
                    calories = item['calories'] 
                    calories_count += calories

                total = [carbs_count, fats_count, proteins_count, fiber_count, sugar_count, calories_count]

                tree.delete(*tree.get_children())

                for i in range(len(macros)):
                    tree.insert('', tk.END, values=(macros[i], round(total[i], 2)))        

            else:
                print('Error:', response.status_code, response.text)
            
            food.clear()
            quantity.clear()
            total.clear()
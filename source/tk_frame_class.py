import tkinter as tk
from tkinter import ttk, messagebox

class FoodFrame():
    def __init__(self,root ,root_row , root_column, name):
        self.root = root
        self.root_row = root_row
        self.root_column = root_column
        self.name = name
        # Counter list utilized for correct entries positioning
        self.counter = []
        # Lists to store food and quantity entered by the user 
        self.food = []
        self.quantity = []
        self.label = []
        # List to store meals frame for loading purpose
        self.load_list = []


    # Create meal frame
    def create_frame(self):
        frame = ttk.Frame(self.root)
        frame.grid(row=self.root_row, column=self.root_column, sticky='w')

        label_title = ttk.Label(frame, text=f'{self.name}:', width=10)
        label_title.grid(row=0, column=0, padx=10, sticky='e')

        add_food_button = ttk.Button(frame, text='+ Add Food', command=lambda: self.add_food(scrollable_frame, canvas))
        add_food_button.grid(row=0, column=1, padx=(0, 10), sticky='w')

        del_food_button = ttk.Button(frame, text='- Remove Food', command=lambda: self.del_food(canvas))
        del_food_button.grid(row=0, column=2, padx=(0, 10), sticky='w')

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.grid(row=1, column=3, sticky='nsw')
        
        canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set, height=150, width=250)
        canvas.grid(row=1, column=0, columnspan=3)

        scrollbar.config(command=canvas.yview)

        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.grid(row=0, column=0, padx=10, pady=10)

        canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)

        self.load_list.append(scrollable_frame)
        self.load_list.append(canvas)

    
    # Add new set of entries with food and quantity
    def add_food(self, scrollable_frame, canvas):
        food_entry = ttk.Entry(scrollable_frame)
        food_entry.grid(column=0, row=len(self.counter)+1, padx=5, pady=5, sticky='w')

        quantity_label = ttk.Label(scrollable_frame, text='gr')
        quantity_label.grid(column=1, row=len(self.counter)+1, padx=5, pady=5, sticky='w')
        quantity_entry = ttk.Entry(scrollable_frame, width=5)
        quantity_entry.grid(column=2, row=len(self.counter)+1, padx=5, pady=5, sticky='w')
        
        self.counter.append(1)
        self.food.append(food_entry)
        self.quantity.append(quantity_entry)
        self.label.append(quantity_label)

        # Recalculates the size of the canvas bounding box
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))


    def del_food(self, canvas):
        if not self.food:
            messagebox.showerror('Error' ,'Error: No food entry to delete')
        else:
            # Remove elements from lists
            self.counter.pop()
            food_entry = self.food.pop()
            quantity_entry = self.quantity.pop()
            quantity_label = self.label.pop()

            # Delete entry objects
            food_entry.destroy()
            quantity_entry.destroy()
            quantity_label.destroy()

            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

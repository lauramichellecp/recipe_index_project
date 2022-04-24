import tkinter as tk
from tkinter import *
import tkinter.ttk
import sql_utils
import pymysql


def errorLabel(self):
    global label
    label = Label(self.root, text="", font=('Aerial 10'))
    label.place(y=330)


def remove_errorLabel(self):
    global label
    label.pack_forget()


def update_errorLabel(self, msg):
    global label
    try:
        label["text"] = msg
    except:
        return False


class AddRecipe():
    def __init__(self, connection, currentUserId):
        self.currentUserId = currentUserId
        self.connection = connection
        self.currentUserId = currentUserId

        print("Add recipe")
        print(currentUserId)

        # Add GUI sutff and call create recipe procedure
        self.root = Tk()  # Window
        self.root.geometry("900x900")
        self.root.title('Add New Recipe')

        # Add recipe name
        name_label = Label(self.root, text="Recipe Name:", width=20, font=("bold", 10))
        name_entry = Entry(self.root, width=20, font=("bold", 10))
        name_label.grid(row=0, column=0, sticky=W, columnspan=2)
        name_entry.grid(row=0, column=2, sticky=W, columnspan=2)

        # Add recipe prep time and cook time
        prep_label = Label(self.root, text="Prep Time:", width=20, font=("bold", 10))
        prep_entry = Entry(self.root, width=20, font=("bold", 10))
        prep_label.grid(row=1, column=0, sticky=W)
        prep_entry.grid(row=1, column=1, sticky=W)

        cook_label = Label(self.root, text="Cook Time:", width=20, font=("bold", 10))
        cook_entry = Entry(self.root, width=20, font=("bold", 10))
        cook_label.grid(row=1, column=2, sticky=W)
        cook_entry.grid(row=1, column=3, sticky=W)

        # Add serving size
        serving_label = Label(self.root, text="Serving Size:", width=20, font=("bold", 10))
        serving_entry = Entry(self.root, width=20, font=("bold", 10))
        serving_label.grid(row=2, column=0, sticky=W, columnspan=2)
        serving_entry.grid(row=2, column=2, sticky=W, columnspan=2)

        # Add cuisine type
        cuisine_label = Label(self.root, text="Cuisine Type:", width=20, font=("bold", 10))
        cuisine_entry = Entry(self.root, width=20, font=("bold", 10))
        cuisine_label.grid(row=3, column=0, sticky=W)
        cuisine_entry.grid(row=3, column=1, sticky=W)

        # Add course type
        course_label = Label(self.root, text="Course Type:", width=20, font=("bold", 10))
        course_entry = Entry(self.root, width=20, font=("bold", 10))
        course_label.grid(row=3, column=2, sticky=W)
        course_entry.grid(row=3, column=3, sticky=W)

        # Add recipe description
        description_label = Label(self.root, text="Description:", width=20, font=("bold", 10))
        description_entry = Entry(self.root, width=20, font=("bold", 10))
        description_label.grid(row=4, column=0, sticky=W, columnspan=4)
        description_entry.grid(row=5, column=0, sticky=W, columnspan=4, rowspan=3)

        # Add recipe instructions
        instructions_label = Label(self.root, text="Instructions:", width=20, font=("bold", 10))
        instructions_entry = Entry(self.root, width=20, font=("bold", 10))
        instructions_label.grid(row=8, column=0, sticky=W, columnspan=4)
        instructions_entry.grid(row=9, column=0, sticky=W, columnspan=4, rowspan=5)

        # Add recipe notes
        notes_label = Label(self.root, text="Notes:", width=20, font=("bold", 10))
        notes_entry = Entry(self.root, width=20, font=("bold", 10))
        notes_label.grid(row=14, column=0, sticky=W, columnspan=4)
        notes_entry.grid(row=15, column=0, sticky=W, columnspan=4, rowspan=3)

        # Multiple selection listbox of dietary restrictions
        diet_restrict = Label(self.root, text="Please select all applicable dietary restrictions:",
                              width=60, font=("bold", 10))
        diet_restrict.grid(row=19, column=0, sticky=W, columnspan=4)
        dietary_restrictions = ['Vegetarian', 'Gluten Free', 'Vegetarian', 'Dairy Free', 'Nut Free']
        dr_lb = Listbox(self.root, selectmode=MULTIPLE, width=20, height=5)
        dr_lb.grid(row=20, column=3, sticky=W)
        for item in dietary_restrictions:
            dr_lb.insert(END, item)

        dietary = []
        cur = dr_lb.curselection()
        for i in cur:
            op = dr_lb.get(i)
            dietary.append(op)

        # Add recipe button
        add_recipe_button = Button(self.root, text="Add Recipe", width=20, bg="black", fg="white",
                                   command=lambda: self.add_recipe(name_entry.get(), prep_entry.get(), cook_entry.get(),
                                                                   serving_entry.get(), cuisine_entry.get(),
                                                                   instructions_entry.get(), notes_entry.get(),
                                                                   description_entry.get(), currentUserId,
                                                                   course_entry.get()))
        add_recipe_button.grid(row=26, column=0, sticky=W, columnspan=4)

        # get recipe id
        recipe_id = self.get_recipe_id(name_entry.get())
        # if recipe id is none
        if recipe_id is None:
            msg = "Recipe not added"

        # Add recipe ingredients
        ingredient_name_label = Label(self.root, text="Ingredient Name:", width=20, font=("bold", 10))
        ingredient_name_entry = Entry(self.root, width=20, font=("bold", 10))
        ingredient_name_label.grid(row=30, column=0, sticky=W, columnspan=2)
        ingredient_name_entry.grid(row=30, column=2, sticky=W, columnspan=2)

        ingredient_amount_label = Label(self.root, text="Amount:", width=20, font=("bold", 10))
        ingredient_amount_entry = Entry(self.root, width=20, font=("bold", 10))
        ingredient_amount_label.grid(row=31, column=0, sticky=W, columnspan=2)
        ingredient_amount_entry.grid(row=31, column=2, sticky=W, columnspan=2)

        add_ingredient_button = Button(self.root, text="Add Ingredient", width=20, bg="black", fg="white",
                                       command=lambda: self.add_ingredient(recipe_id, ingredient_name_entry.get(),
                                                                           ingredient_amount_entry.get(), dietary))
        add_ingredient_button.grid(row=32, column=0, sticky=W, columnspan=4)

    def add_recipe(self, recipe_name, prep_time, cook_time, serving_size, cuisine, instructions, notes,
                   description, author, course):
        try:
            sql_utils.createRecipe(self.connection, recipe_name, prep_time, cook_time, serving_size,
                                   cuisine, instructions, notes, description, author, course)
        except pymysql.Error as e:
            return False
        return True

    def add_ingredient(self, recipe_id, ingredient_name_entry, ingredient_quantity_entry, dietary):
        try:
            if not dietary:
                sql_utils.addIngredient(self.connection, recipe_id, ingredient_name_entry, 1, ingredient_quantity_entry)
            for i in dietary:
                sql_utils.addIngredient(self.connection, ingredient_name_entry, i, ingredient_quantity_entry)
        except pymysql.Error as e:
            return False
        return True

    def get_recipe_id(self, recipe_name):
        try:
            recipe_id = sql_utils.getRecipeByName(self.connection, recipe_name)
        except pymysql.Error as e:
            return False
        return recipe_id

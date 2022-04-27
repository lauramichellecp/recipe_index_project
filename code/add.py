import tkinter as tk
from tkinter import *
import sql_utils

class AddRecipe():
    def __init__(self, connection, currentUserId):
        self.currentUserId = currentUserId
        self.connection = connection
        self.currentUserId = currentUserId
        self.recipe_id = 0

        # Add GUI sutff and call create recipe procedure
        self.root = Tk()  # Window
        self.root.geometry("900x900")
        self.root.title('Add New Recipe')
        
        self.frame = Frame(self.root, width=400, height=400)
        self.frame.place(x=50, y=65)

        self.recipeNo_label = Label(self.frame, text="NOTE: Please create a new recipe before adding ingredients to that recipe", fg="gray", font=('Aerial 10'))
        self.recipeNo_label.grid(row=0, column=0, sticky=W, columnspan=5)

        label_recipe =Label(self.root,text="Add New Recipe", anchor='w', width=20,font=("bold",14))
        label_recipe.place(x=50, y=20)

        # Add recipe name
        name_label = Label(self.frame, text="Recipe Name:", anchor='w', width=20, font=("bold", 10))
        name_entry = Entry(self.frame, width=70, font=("bold", 10))
        name_label.grid(row=2, column=0, sticky=W, columnspan=1)
        name_entry.grid(row=2, column=1, sticky=W, columnspan=4)

        # Add recipe prep time and cook time
        prep_label = Label(self.frame, text="Prep Time:", anchor='w', width=20, font=("bold", 10))
        prep_entry = Entry(self.frame, width=20, font=("bold", 10))
        prep_label.grid(row=3, column=0, sticky=W)
        prep_entry.grid(row=3, column=1, sticky=W)

        cook_label = Label(self.frame, text="Cook Time:", anchor='w', width=20, font=("bold", 10))
        cook_entry = Entry(self.frame, width=20, font=("bold", 10))
        cook_label.grid(row=3, column=2, sticky=W)
        cook_entry.grid(row=3, column=3, sticky=W)

        # Add serving size
        serving_label = Label(self.frame, text="Serving Size:", anchor='w', width=20, font=("bold", 10))
        serving_entry = Entry(self.frame, width=20, font=("bold", 10))
        serving_label.grid(row=4, column=0, sticky=W, columnspan=1)
        serving_entry.grid(row=4, column=1, sticky=W, columnspan=3)

        # Add cuisine type
        cuisine_label = Label(self.frame, text="Cuisine Type:",anchor='w', width=20, font=("bold", 10))
        cuisine_entry = Entry(self.frame, width=20, font=("bold", 10))
        cuisine_label.grid(row=5, column=0, sticky=W)
        cuisine_entry.grid(row=5, column=1, sticky=W)

        # Add course type
        course_label = Label(self.frame, text="Course Type:",anchor='w',  width=20, font=("bold", 10))
        course_label.grid(row=5, column=2, sticky=W)
        courses = ["Breakfast", "Lunch", "Dinner", "Dessert"]
        course_variable = StringVar(self.frame)
        course_variable.set("Breakfast")
        course_option = OptionMenu(self.frame, course_variable, *courses)
        course_option.grid(row=5, column=3, sticky=W)

        # Add recipe description
        description_label = Label(self.frame, text="Description:", anchor='w', width=20, font=("bold", 10))
        description_entry = Text(self.frame, height=2)
        description_label.grid(row=6, column=0, sticky=W, columnspan=4)
        description_entry.grid(row=7, column=0, sticky=W, columnspan=5)

        # Add recipe instructions
        instructions_label = Label(self.frame, text="Instructions:", anchor='w', width=20, font=("bold", 10))
        instructions_entry = Text(self.frame, height=5)
        instructions_label.grid(row=10, column=0, sticky=W, columnspan=4)
        instructions_entry.grid(row=11, column=0, sticky=W, columnspan=5)

        # Add recipe notes
        notes_label = Label(self.frame, text="Notes:", anchor='w', width=20, font=("bold", 10))
        notes_entry = Text(self.frame, height=2)
        notes_label.grid(row=16, column=0, sticky=W, columnspan=4)
        notes_entry.grid(row=17, column=0, sticky=W, columnspan=5)

        # Multiple selection listbox of dietary restrictions
        diet_restrict = Label(self.frame, text="Please select all applicable dietary restrictions:",
                              anchor='w', width=60, font=("bold", 10))
        diet_restrict.grid(row=21, column=0, sticky=W, columnspan=4)
        dietary_restrictions = ['Vegetarian', 'Gluten Free', 'Vegetarian', 'Dairy Free', 'Nut Free']
        dr_lb = Listbox(self.frame, selectmode=MULTIPLE, width=20, height=5)
        dr_lb.grid(row=22, column=0, sticky=W)
        for item in dietary_restrictions:
            dr_lb.insert(END, item)

        dietary = []
        cur = dr_lb.curselection()
        for i in cur:
            op = dr_lb.get(i)
            dietary.append(op)

        # Add recipe button
        add_recipe_button = Button(self.frame, text="Add Recipe", width=20, bg="black", fg="white",
                                   command=lambda: self.add_recipe(name_entry.get(), prep_entry.get(), cook_entry.get(),
                                                                   serving_entry.get(), cuisine_entry.get(),
                                                                   instructions_entry.get(1.0, "end"), notes_entry.get(1.0, "end"),
                                                                   description_entry.get(1.0, "end"), currentUserId,
                                                                   course_variable.get()))
        add_recipe_button.grid(row=31, column=3, sticky=W, columnspan=4)

        label_recipe =Label(self.frame, text="Add New Ingredients To Recipe", font=("bold",14))
        label_recipe.grid(row=37, column=0, sticky=W, columnspan=5)

        # Add recipe ingredients
        ingredient_name_label = Label(self.frame, text="Ingredient Name:", anchor='w', width=20, font=("bold", 10))
        ingredient_name_entry = Entry(self.frame, width=20, font=("bold", 10))
        ingredient_name_label.grid(row=39, column=0, sticky=W, columnspan=2)
        ingredient_name_entry.grid(row=39, column=2, sticky=W, columnspan=2)

        ingredient_amount_label = Label(self.frame, text="Amount:", anchor='w', width=20, font=("bold", 10))
        ingredient_amount_entry = Entry(self.frame, width=20, font=("bold", 10))
        ingredient_amount_label.grid(row=40, column=0, sticky=W, columnspan=2)
        ingredient_amount_entry.grid(row=40, column=2, sticky=W, columnspan=2)

        add_ingredient_button = Button(self.frame, text="Add Ingredient", width=20, bg="black", fg="white",
                                       command=lambda: self.add_ingredient(self.recipe_id, ingredient_name_entry.get(),
                                                                           ingredient_amount_entry.get(), dietary))
        add_ingredient_button.grid(row=41, column=3, sticky=W)

        buffer = Label(self.frame, text="", fg="gray", font=('Aerial 10'))
        buffer.grid(row=42, column=0, sticky=W, columnspan=5, rowspan=3)
        
        self.errorLabel(46)

        buffer = Label(self.frame, text="", fg="gray", font=('Aerial 10'))
        buffer.grid(row=47, column=0, sticky=W, columnspan=5, rowspan=3)
        buffer = Label(self.frame, text="", fg="gray", font=('Aerial 10'))
        buffer.grid(row=51, column=0, sticky=W, columnspan=5, rowspan=3)

        self.recipeInstr_label = Label(self.frame, text="Done adding ingredients to recipe? Click Done to close the window", 
            fg="gray", font=('Aerial 10'))
        self.recipeInstr_label.grid(row=54, column=0, sticky=W, columnspan=5)

        done_btn = Button(self.frame, text="Done ", width=20, bg="black", fg="white",
                                command=lambda: self.root.destroy())
        done_btn.grid(row=54, column=3, sticky=W)


    def add_recipe(self, recipe_name, prep_time, cook_time, serving_size, cuisine, instructions, notes,
                   description, author, course):
        try:
            self.update_errorLabel("", "black")
            if (sql_utils.createRecipe(self.connection, recipe_name, prep_time, cook_time, serving_size,
                                   cuisine, instructions, notes, description, author, course)):
                self.recipe_id = self.get_recipe_id(recipe_name)
                print(self.recipe_id)
                # if recipe id is none
                if self.recipe_id == None or not self.recipe_id:
                    raise Exception("recipe not created")
                self.update_errorLabel("Recipe #{0} created".format(self.recipe_id), "black")
            else:
                raise Exception("recipe not created")
        except:
            msg="Could not create recipe. Try again..."
            print(msg)
            self.update_errorLabel(msg, "red")

    def add_ingredient(self, recipe_id, ingredient_name_entry, ingredient_quantity_entry, dietary):
        self.update_errorLabel("", "black")
        if not dietary:
            successful = sql_utils.addIngredient(self.connection, recipe_id, ingredient_name_entry, 1, ingredient_quantity_entry)
        for i in dietary:
            successful= sql_utils.addIngredient(self.connection, ingredient_name_entry, i, ingredient_quantity_entry)
        
        if (successful and recipe_id != 0):
            self.update_errorLabel("Ingredient added to recipe #{0}".format(recipe_id), "black")
        elif (not successful or recipe_id == 0):
            self.update_errorLabel("Couldn't add ingredient to recipe. Have you added your new recipe?".format(recipe_id), "red")
            return False
        return True

    def get_recipe_id(self, recipe_name):
        try:
            recipe = sql_utils.getRecipeByName(self.connection, recipe_name)
            recipe_id = recipe[0]
        except:
            return False
        return recipe_id

    def errorLabel(self, row_num):
        global label
        label = Label(self.frame, text="", font=('Aerial 10'))
        label.grid(row=row_num, column=0, sticky=W, columnspan=5)

    def remove_errorLabel(self):
        global label
        label.pack_forget()

    def update_errorLabel(self, msg, color):
        global label
        try:
            label["text"]=msg
            label.config(fg=color)
        except:
            return False

    def update_label(self, recipeId):
        try:
            self.recipeNo_label["text"]="Currently editing recipe #{0}".format(recipeId)
        except:
            return False

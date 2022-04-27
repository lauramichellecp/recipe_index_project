import tkinter as tk
from tkinter import *
import tkinter.ttk
import sql_utils

class AnonSearch():
    def __init__(self, connection):
        self.connection = connection

        # Open Search without Bookmarks, etc.
        self.root = Tk() # Window
        self.root.geometry("1000x800") # Size
        self.root.title('Recipe Index')

        main_frame = Frame(self.root, width=800, height=800)

        entry_search_name=Entry(main_frame, width=40)
        entry_search_name.grid(row=1,column=1, columnspan=2)

        OPTIONS = [
        "Name",
        "Max Prep Time",
        "Max Cook Time",
        "Max Total Time",
        "Serving Size",
        "Course",
        "Author",
        ] 
        search_variable = StringVar(main_frame)
        search_variable.set(OPTIONS[0])

        search_options = OptionMenu(main_frame, search_variable, *OPTIONS)
        search_options.grid(row=1,column=3)
        search_options.configure(width=10)

        buttonSearch = Button(main_frame, text='Search recipes', width=20,bg="black",fg='white',
            command = lambda: self.searchBy(entry_search_name.get(), search_variable.get(), dr_variable.get()))
        buttonSearch.grid(row=1,column=0)
        OPTIONS_DR = [
        "-",
        "Vegan",
        "Vegetarian",
        "Gluten Free",
        "Dairy Free",
        "Nut Free"
        ] 
        dr_variable = StringVar(main_frame)
        dr_variable.set(OPTIONS_DR[0])

        dietary_options = OptionMenu(main_frame, dr_variable, *OPTIONS_DR)
        dietary_options.grid(row=1,column=5)
        dietary_options.configure(width=7)

        self.frame = Frame(main_frame, width=400, height=400)
        self.frame.grid(row=2,column=0, columnspan=6)

        recipe_columns = ('id', 'name', 'description', 'ptime', 'ctime', 'servings', 'cuisine', 'notes', 'author')
        self.recipe_tree = tkinter.ttk.Treeview(self.frame, columns=recipe_columns, show='headings')
        self.recipe_tree.heading('id', text='ID')
        self.recipe_tree.column("id", stretch=NO, width=50)
        self.recipe_tree.heading('name', text='Recipe Name')
        self.recipe_tree.column("name", width=150)
        self.recipe_tree.heading('description', text='Description')
        self.recipe_tree.column("description", width=200)
        self.recipe_tree.heading('ptime', text='Prep Time')
        self.recipe_tree.column("ptime", stretch=NO, width=50)
        self.recipe_tree.heading('ctime', text='Cook Time')
        self.recipe_tree.column("ctime", stretch=NO, width=50)
        self.recipe_tree.heading('servings', text='Servings')
        self.recipe_tree.column("servings", stretch=NO, width=50)
        self.recipe_tree.heading('cuisine', text='Cuisine')
        self.recipe_tree.column("cuisine", stretch=NO, width=100)
        self.recipe_tree.heading('notes', text='Notes')
        self.recipe_tree.column("notes", width=150)
        self.recipe_tree.heading('author', text='Author')
        self.recipe_tree.column("author", stretch=NO, width=50)

        self.sb = Scrollbar(self.frame, orient=VERTICAL)
        self.sb.pack(side=RIGHT, fill=Y)

        self.recipe_tree.bind("<Double-1>", self.doubleClick)

        label_prompt_login=Label(main_frame, text="Log in to create and update your own recipes and bookmark your favorites!", font=("bold",12))
        label_prompt_login.grid(row=3,column=0, columnspan=6, sticky=N, pady=10)

        main_frame.pack(side=TOP,expand=True)

        recipe_frame = Frame(self.root, width=400, height=100)
        instructions_frame = Frame(recipe_frame, width=200, height=300)
        ingredients = Frame(recipe_frame, width=200, height=300)

        label_more_details =Label(recipe_frame,text="Recipe Details", width=20,font=("bold",20))
        #label_more_details.grid(row=0,column=0,columnspan=6, sticky=N, pady=10, padx=10)
        label_more_details.pack(side=TOP, expand=True)

        label_instructions =Label(instructions_frame,text="Instructions:", width=20,font=10)
        label_instructions.grid(row=0,column=0, sticky=W)

        self.instructions_text = Text(instructions_frame, height=20, width=50)
        self.instructions_text.grid(row=1,column=0, sticky=W)
        self.instructions_text.insert(tk.END, "")

        label_ingredients =Label(ingredients,text="Ingredients:", width=20,font=10)
        label_ingredients.grid(row=0,column=0, sticky=W, pady=10)

        self.ingredients_frame = Frame(ingredients, width=200, height=400)
        self.ingredients_frame.grid(row=1,column=0, padx=20, sticky=N, pady=10)

        recipe_ingredients_columns = ('id', 'name', 'amount')
        self.recipe_ingredients_tree = tkinter.ttk.Treeview(self.ingredients_frame,
            columns=recipe_ingredients_columns, show='headings')
        self.recipe_ingredients_tree.heading('id', text='ID')
        self.recipe_ingredients_tree.column("id", stretch=NO, width=75)
        self.recipe_ingredients_tree.heading('name', text='Name')
        self.recipe_ingredients_tree.column("name", stretch=NO, width=200)
        self.recipe_ingredients_tree.heading('amount', text='Amount')
        self.recipe_ingredients_tree.column("amount", stretch=NO, width=150)

        self.sb2 = Scrollbar(self.ingredients_frame, orient=VERTICAL)
        self.sb2.pack(side=RIGHT, fill=Y)
        self.recipe_ingredients_tree.config(yscrollcommand=self.sb2.set)

        recipe_frame.pack(side=TOP, expand=True)
        instructions_frame.pack(side=LEFT, expand=True)
        ingredients.pack(side=RIGHT, expand=True)

        self.recipe_tree.bind("<Key>", self.searchBy('', 'Name', 1))

    def getRecipe(self, recipe):
        self.recipe_tree.focus(recipe)
        # gets the 3rd value from the treeview options (which has the information about the recipe) 
        return list(self.recipe_tree.item(recipe).values())[2] 

    def searchBy(self, search, criteria, dr):
        self.recipe_tree.config(yscrollcommand=self.sb.set)
        self.clearItems() # clear everything
        # Add dietary restriction!
        self.update_errorLabel("")
        if (criteria == 'Name'):
            result = searchByName(self.connection, search)
        elif (criteria == 'Max Prep Time'):
            result = searchByPrep(self.connection, search)
        elif (criteria == 'Max Cook Time'):
            result = searchByCook(self.connection, search)
        elif (criteria == 'Max Total Time'):
            result = searchByTotal(self.connection, search)
        elif (criteria == 'Serving Size'):
            result = searchByServings(self.connection, search)
        elif (criteria == 'Course'):
            result = searchByCourse(self.connection, search)
        elif (criteria == 'Author'):
            result = searchByAuthorName(self.connection, search)
        else:
            result = searchByName(self.connection, search)
        self.parseResults(result)

    def parseResults(self, result):
        all_recipes = []
        try:
            for tuple in result:
                recipe = (str(tuple[0]), str(tuple[1]), str(tuple[2]), str(tuple[3]), str(tuple[4]), 
                str(tuple[5]), str(tuple[6]), str(tuple[7]), str(tuple[8]), str(tuple[9]))
                # append recipe to total recipes
                all_recipes.append(recipe)
            self.createEntries(all_recipes)
        except:
            msg="Could not search by the given filter. Try again.."
            self.update_errorLabel(msg)
    
    def getIngredients(self):
        recipe = self.getRecipe(self.recipe_tree.selection()[0])
        recipeId = recipe[0] # get the recipeId from the selection
        result = sql_utils.getIngredients(self.connection, recipeId)
        all_ingredients = []
        try:
            for tuple in result:
                item = (str(tuple[0]), str(tuple[2]), str(tuple[1]))
                # append ingredients to total recipes
                all_ingredients.append(item)
            self.createIngredientEntries(all_ingredients)
        except:
            msg="Could not show recipe ingredients. Try again.."
            self.update_errorLabel(msg, "red")

    def createIngredientEntries(self, ingredients):
        for item in self.recipe_ingredients_tree.get_children():
            self.recipe_ingredients_tree.delete(item)     
        for r in ingredients:
            self.recipe_ingredients_tree.insert('', tk.END, values=r)
            self.recipe_ingredients_tree.pack()

    def clearItems(self):
        # Get selected item to Delete
        for item in self.recipe_tree.get_children():
            self.recipe_tree.delete(item)     

    def createEntries(self, recipes):
        # Delete entries that are already in the tree!
        self.recipe_tree.delete()
        for r in recipes:
            self.recipe_tree.insert('', tk.END, values=r)
            self.recipe_tree.pack()

    def doubleClick(self, event):
        try:
            self.instructions_text.delete(1.0, "end")
            recipe = self.getRecipe(self.recipe_tree.selection()[0])
            recipeInstructions = recipe[9]
            self.instructions_text.insert(1.0, recipeInstructions)
            self.getIngredients()
        except:
            return False

    def errorLabel(self):
        global label
        label=Label(self.root, text="", font=('Aerial 10'))
        label.place(x=55, y=370)

    def remove_errorLabel(self):
        global label
        label.pack_forget()

    def update_errorLabel(self, msg):
        global label
        try:
            label["text"]=msg
        except:
            return False


def searchByName(connection, name):
    return sql_utils.getRecipesByName(connection, name)

def searchByPrep(connection, prep):
    return sql_utils.getRecipesByPrepTime(connection, prep)

def searchByCook(connection, cook):
    return sql_utils.getRecipesByCookTime(connection, cook)

def searchByTotal(connection, total):
    return sql_utils.getRecipesByTotalTime(connection, total)

def searchByServings(connection, servings):
    return sql_utils.getRecipesByServings(connection, servings)

def searchByCourse(connection, course):
    return sql_utils.getRecipesByCourseName(connection, course)

def searchByAuthorName(connection, first_name):
    return sql_utils.getRecipesByAuthorName(connection, first_name)

def searchByDietaryRestriction(connection, restriction):
    # TODO: check any ingredient.
    return True
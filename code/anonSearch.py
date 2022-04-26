import tkinter as tk
from tkinter import *
import tkinter.ttk
import sql_utils

class AnonSearch():
    def __init__(self, connection):
        self.loggedIn = False
        self.connection = connection

        # Open Search without Bookmarks, etc.
        self.root = Tk() # Window
        self.root.geometry("1150x850")
        self.root.title('Recipe Index')
        
        label_search =Label(self.root,text="Search for recipes", width=20,font=("bold",14))
        label_search.place(x=20,y=30)

        entry_search_name=Entry(self.root, width=100)
        entry_search_name.place(x=205,y=70)

        OPTIONS = [
        "Name",
        "Max Prep Time",
        "Max Cook Time",
        "Max Total Time",
        "Serving Size",
        "Course",
        "Author",
        ] 
        search_variable = StringVar(self.root)
        search_variable.set(OPTIONS[0])

        search_options = OptionMenu(self.root, search_variable, *OPTIONS)
        search_options.place(x=755,y=65)
        search_options.configure(width=15)

        buttonSearch = Button(self.root, text='Search recipes', width=20,bg="black",fg='white', 
            command = lambda: self.searchBy(entry_search_name.get(), search_variable.get(), dr_variable.get()))
        buttonSearch.place(x=55,y=70)

        OPTIONS_DR = [
        "-",
        "Vegan",
        "Vegetarian",
        "Gluten Free",
        "Dairy Free",
        "Nut Free"
        ] 
        dr_variable = StringVar(self.root)
        dr_variable.set(OPTIONS_DR[0])

        dietary_options = OptionMenu(self.root, dr_variable, *OPTIONS_DR)
        dietary_options.place(x=855,y=65)
        dietary_options.configure(width=12)

        self.frame = Frame(self.root, width=200, height=800)
        self.frame.place(x=55, y=100)

        recipe_columns = ('id', 'name', 'description', 'ptime', 'ctime', 'servings', 'cuisine', 'notes', 'author')
        self.recipe_tree = tkinter.ttk.Treeview(self.frame, columns=recipe_columns, show='headings')
        self.recipe_tree.heading('id', text='ID')
        self.recipe_tree.column("id", stretch=NO, width=50)
        self.recipe_tree.heading('name', text='Recipe Name')
        self.recipe_tree.column("name", width=200)
        self.recipe_tree.heading('description', text='Description')
        self.recipe_tree.column("description", width=300)
        self.recipe_tree.heading('ptime', text='Prep Time')
        self.recipe_tree.column("ptime", stretch=NO, width=50)
        self.recipe_tree.heading('ctime', text='Cook Time')
        self.recipe_tree.column("ctime", stretch=NO, width=50)
        self.recipe_tree.heading('servings', text='Servings')
        self.recipe_tree.column("servings", stretch=NO, width=50)
        self.recipe_tree.heading('cuisine', text='Cuisine')
        self.recipe_tree.column("cuisine", stretch=NO, width=120)
        self.recipe_tree.heading('notes', text='Notes')
        self.recipe_tree.column("notes", width=120)
        self.recipe_tree.heading('author', text='Author')
        self.recipe_tree.column("author", stretch=NO, width=50)

        self.sb = Scrollbar(self.frame, orient=VERTICAL)
        self.sb.pack(side=RIGHT, fill=Y)

        self.recipe_tree.bind("<Double-1>", self.doubleClick)

        label_prompt_login=Label(self.root, text="Log in to create and update your own recipes and bookmark your favorites!", font=("bold",12))
        label_prompt_login.place(x=55, y=350)

        label_more_details =Label(self.root,text="Recipe Details", width=20,font=("bold",14))
        label_more_details.place(x=5,y=400)

        label_instructions =Label(self.root,text="Instructions:", width=20,font=9)
        label_instructions.place(x=5,y=430)

        self.instructions_text = Text(self.root, height=20, width=60)
        self.instructions_text.place(x=55,y=460)
        self.instructions_text.insert(tk.END, "")

        label_ingredients =Label(self.root,text="Ingredients:", width=20,font=9)
        label_ingredients.place(x=555,y=430)

    def loggedIn(self):
        return self.loggedIn

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

    def clearItems(self):
        # Get selected item to Delete
        for item in self.recipe_tree.get_children():
            self.recipe_tree.delete(item)     

    def createEntries(self, recipes):
        # Delete entries that are already in the tree!
        self.recipe_tree.delete()
        rows = []
        for r in recipes:
            self.recipe_tree.insert('', tk.END, values=r)
            self.recipe_tree.pack()

    def doubleClick(self, event):
        try:
            self.instructions_text.delete(1.0, "end")
            recipe = self.getRecipe(self.recipe_tree.selection()[0])
            recipeInstructions = recipe[9]
            self.instructions_text.insert(1.0, recipeInstructions)
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
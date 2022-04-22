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
        self.root.geometry("3000x900")
        self.root.title('Recipe Index')
        label =Label(self.root,text="Anon View", width=20,font=("bold",14))
        label.place(x=0,y=30)

    def loggedIn(self):
        return self.loggedIn
    
    def searchByName(self, name):
        result = searchByName(self.connection, name)
        print(result)

    def searchByCook(self, cook):
        result = searchByCook(self.connection, cook)
        print(result)

    def searchByCourse(self, cook):
        result = searchByCook(self.connection, cook)
        print(result)

    def close(self):
        self.root.destroy()

class LoggedInSearch():
    def __init__(self, connection, currentUser):
        self.loggedIn = True
        self.connection = connection

        # Open Search with Bookmarks, etc.
        self.root = Tk() # Window
        self.root.geometry("2000x800")
        self.root.title('Recipe Index')

        label_bookmarks =Label(self.root,text="Bookmarks", width=20,font=("bold",14))
        label_bookmarks.place(x=0,y=30)

        separator = tkinter.ttk.Separator(self.root, orient='vertical')
        separator.place(x=700,y=0, relwidth=0.2, relheight=1)

        label_search =Label(self.root,text="Search for recipes", width=20,font=("bold",14))
        label_search.place(x=765,y=30)

        entry_search_name=Entry(self.root, width=100)
        entry_search_name.place(x=950,y=70)

        buttonSearch = Button(self.root, text='Search recipes', width=20,bg="black",fg='white', 
            command = lambda: self.searchBy(entry_search_name.get(), search_variable.get(), dr_variable.get()))
        buttonSearch.place(x=800,y=70)

        OPTIONS = [
        "Name",
        "Max Cook Time",
        "Course",
        "Author",
        ] 
        search_variable = StringVar(self.root)
        search_variable.set(OPTIONS[0])

        search_options = OptionMenu(self.root, search_variable, *OPTIONS)
        search_options.place(x=1500,y=65)
        search_options.configure(width=15)

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
        dietary_options.place(x=1600,y=65)
        dietary_options.configure(width=12)

        self.frame = Frame(self.root, width=200, height=800)
        self.frame.place(x=800, y=100)

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

        sb = Scrollbar(self.frame, orient=VERTICAL)
        sb.pack(side=RIGHT, fill=Y)
        self.recipe_tree.config(yscrollcommand=sb.set)

        buttonDeleteRecipe = Button(self.root, text='Delete selected recipe', width=20,bg="black",fg='white', 
            command = lambda: self.deleteEnties())
        buttonDeleteRecipe.place(x=800,y=340)

        self.errorLabel()

        label_more_details =Label(self.root,text="Recipe Details", width=20,font=("bold",14))
        label_more_details.place(x=750,y=400)


    def loggedIn(self):
        return self.loggedIn

    def searchBy(self, search, criteria, dr):
        # Add dietary restriction!
        self.update_errorLabel("")
        if (criteria == 'Name'):
            result = searchByName(self.connection, search)
        elif (criteria == 'Max Cook Time'):
            result = searchByCook(self.connection, search)
        elif (criteria == 'Course'):
            result = searchByCourse(self.connection, search)
        elif (criteria == 'Author'):
            result = searchByAuthorName(self.connection, search)
        else:
            result = searchByName(self.connection, search)
        self.parseResults(result)

    def parseResults(self, result):
        all_recipes = []
        for tuple in result:
            recipe = (str(tuple[0]), str(tuple[1]), str(tuple[9]), str(tuple[2]), str(tuple[3]), 
            str(tuple[5]), str(tuple[6]), str(tuple[8]), str(tuple[10]), str(tuple[7]))
            # append recipe to total recipes
            all_recipes.append(recipe)
        self.createEntries(all_recipes)
        return None

    def deleteEnties(self):
        # Get selected item to Delete
        selected_item = self.recipe_tree.selection()[0]
        # check if user can delete this entry, and give update message!
        msg="deleted"
        self.update_errorLabel(msg)
        self.recipe_tree.delete(selected_item)
        
    
    def createEntries(self, recipes):
        # Delete entries that are already in the tree!
        self.recipe_tree.delete()
        rows = []
        for r in recipes:
            self.recipe_tree.insert('', tk.END, values=r)
            self.recipe_tree.pack()
        print(recipes)

    def errorLabel(self):
        global label
        label=Label(self.root, text="", font=('Aerial 10'))
        label.place(x=1000, y=340)

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

def searchByCook(connection, cook):
    return sql_utils.getRecipesByCookTime(connection, cook)

def searchByCourse(connection, course):
    return sql_utils.getRecipesByCourseName(connection, course)

def searchByAuthorName(connection, first_name):
    return sql_utils.getRecipesByAuthorName(connection, first_name)

def searchByDietaryRestriction(connection, restriction):
    # TODO: check any ingredient.
    return True
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

        entry_search_name=Entry(self.root, width=100)
        entry_search_name.place(x=950,y=30)

        buttonSearch = Button(self.root, text='Search recipes', width=20,bg="black",fg='white', 
            command = lambda: self.searchBy(entry_search_name.get(), variable.get()))
        buttonSearch.place(x=800,y=30)

        OPTIONS = [
        "Recipe Name",
        "Total Cook Time",
        "Recipe Course"
        ] 
        variable = StringVar(self.root)
        variable.set(OPTIONS[0]) # default value

        options = OptionMenu(self.root, variable, *OPTIONS)
        options.place(x=1500,y=25)

        
    def loggedIn(self):
        return self.loggedIn

    def searchBy(self, search, criteria):
        print(criteria)
        if (criteria == 'Recipe Name'):
            result = searchByName(self.connection, search)
        elif (criteria == 'Total Cook Time'):
            result = searchByCook(self.connection, search)
        elif (criteria == 'Recipe Course'):
            result = searchByCourse(self.connection, search)
        else:
            result = searchByName(self.connection, search)
        print(result)
        self.parseResult(result)

    def parseResult(self, result):
        '''
        TODO: put the results in the GUI
        '''
        return None
    def close(self):
        self.root.destroy()

def searchByName(connection, name):
    return sql_utils.getRecipeByName(connection, name)

def searchByCook(connection, cook):
    return sql_utils.getRecipesByCookTime(connection, cook)

def searchByCourse(connection, course):
    return sql_utils.getRecipesByCourse(connection, course)

def searchByDietaryRestriction(connection, restriction):
    return sql_utils.getRecipesByCourse(connection, restriction)
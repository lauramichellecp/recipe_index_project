import tkinter as tk
from tkinter import *
import tkinter.ttk
import sql_utils

class AddRecipe():
    def __init__(self, connection, currentUserId):
        self.currentUserId = currentUserId
        self.connection = connection

        print("Add recipe")
        print(currentUserId)

        # Add GUI sutff and call create recipe procedure
        self.root = Tk() # Window
        self.root.geometry("900x900")
        self.root.title('Add New Recipe')

        # MAKE SURE TO ASK FOR DIETARY RESTRICTION FOR THE WHOLE recipe and add it to ingredients 

        # add labels and entries for all the inputs for the add recipe procedure
        
        # one dropdown for dietary restriction (see if there's a multiple select option)

        # add labels, entries for 1 ingredient and amount

        # text box ingredient name # text box amount # add ingredient to recipe (button)
        # call the addIngredients procedure (with the dietary restriction)

        # TODO: remember dietary restriction 1 is none
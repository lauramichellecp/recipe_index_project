import tkinter as tk
from tkinter import *
import sql_utils

class UpdateIngredient():
    def __init__(self, connection, recipeId, ingredientId):
        self.connection = connection

        # Add GUI sutff and call create recipe procedure
        self.root = Tk()  # Window
        self.root.geometry("500x200")
        self.root.title('Update Recipe #{0} Ingredient #{1}'.format(recipeId, ingredientId))

        self.frame = Frame(self.root, width=400, height=150)
        self.frame.place(x=20, y=20)

        update = Label(self.frame, text="Update ingredient amount or remove from recipe:", anchor='w', width=40, font=("bold", 13))
        update.grid(row=0, column=0, sticky=W, columnspan=4)

        ingredient_amount = Label(self.frame, text="Amount", anchor='w', width=20, font=("bold", 10))
        ingredient_amount.grid(row=2, column=0, sticky=W, columnspan=1)

        new_recipe_ingredient_amount = Entry(self.frame, width=15, font=("bold", 10))
        new_recipe_ingredient_amount.grid(row=2, column=3, sticky=W, columnspan=2)

        buttonRemove = Button(self.frame, text='Delete Ingredient', width=15,bg="black",fg='white', 
            command = lambda: self.deletingIngredient(recipeId, ingredientId))
        buttonRemove.grid(row=3, column=0, sticky=W, columnspan=2)
        
        buttonUpdate = Button(self.frame, text='Update Ingredient', width=15,bg="black",fg='white', 
            command = lambda: self.updateIngredient(recipeId, ingredientId, new_recipe_ingredient_amount.get()))
        buttonUpdate.grid(row=3, column=3, sticky=W, columnspan=2)

        Label(self.frame, text="", font=('Aerial 10')).grid(row=4)
        self.label=Label(self.frame, text="", font=('Aerial 10'))
        self.label.grid(row=5, column=0, sticky=W, columnspan=2)

    def updateIngredient(self, recipeId, ingredientId, new_amount):
        # Attempt update amount ingredient
        print(new_amount)
        if (sql_utils.updateRecipeIngredient(self.connection, recipeId, ingredientId, new_amount)):
            self.root.destroy()
        else:
        # else display error message
            self.update_errorLabel("Ingredient #{0} was not updated.".format(ingredientId), "red")

    def deletingIngredient(self, recipeId, ingredientId):
        # Attempt delete ingredient
        if (sql_utils.removeRecipeIngredient(self.connection, recipeId, ingredientId)):
            self.root.destroy()
        else:
            self.update_errorLabel("Ingredient #{0} was not removed.".format(ingredientId), "red")

    def update_errorLabel(self, msg, color):
        try:
            self.label["text"]=msg
            self.label.config(fg=color)
        except:
            return False


import tkinter as tk
from tkinter import *
import tkinter.ttk
import sql_utils
import add

class LoggedInSearch():
    def __init__(self, connection, currentUser):
        self.loggedIn = True
        self.connection = connection

        # Open Search with Bookmarks, etc.
        self.root = Tk() # Window
        self.root.geometry("2000x850")
        self.root.title('Recipe Index')

        label_bookmarks =Label(self.root,text="Bookmarks", width=20,font=("bold",14))
        label_bookmarks.place(x=0,y=30)

        separator = tkinter.ttk.Separator(self.root, orient='vertical')
        separator.place(x=700,y=0, relwidth=0.2, relheight=1)

        label_search =Label(self.root,text="Search for recipes", width=20,font=("bold",14))
        label_search.place(x=765,y=30)

        self.entry_search_name=Entry(self.root, width=100)
        self.entry_search_name.place(x=950,y=70)

        buttonSearch = Button(self.root, text='Search recipes', width=20,bg="black",fg='white', 
            command = lambda: self.searchBy(self.entry_search_name.get(), self.search_variable.get(), self.dr_variable.get()))
        buttonSearch.place(x=800,y=70)

        OPTIONS = [
        "Name",
        "Max Cook Time",
        "Course",
        "Author",
        ] 
        self.search_variable = StringVar(self.root)
        self.search_variable.set(OPTIONS[0])

        search_options = OptionMenu(self.root, self.search_variable, *OPTIONS)
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
        self.dr_variable = StringVar(self.root)
        self.dr_variable.set(OPTIONS_DR[0])

        dietary_options = OptionMenu(self.root, self.dr_variable, *OPTIONS_DR)
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

        self.sb = Scrollbar(self.frame, orient=VERTICAL)
        self.sb.pack(side=RIGHT, fill=Y)

        self.recipe_tree.bind("<Double-1>", self.doubleClick)

        buttonDeleteRecipe = Button(self.root, text='Delete selected recipe', width=20,bg="black",fg='white', 
            command = lambda: self.deleteEnties(currentUser))
        buttonDeleteRecipe.place(x=800,y=340)

        self.errorLabel()

        buttonAddNewRecipe = Button(self.root, text='Add New Recipe', width=20,bg="black",fg='white', 
            command = lambda: add.AddRecipe(self.connection, currentUser))
        buttonAddNewRecipe.place(x=1000,y=340)

        buttonAddBookmark = Button(self.root, text='Add To Bookmarks', width=20,bg="black",fg='white', 
            command = lambda: self.addBookmark(currentUser))
        buttonAddBookmark.place(x=1200,y=340)

        label_more_details =Label(self.root,text="Recipe Details", width=20,font=("bold",14))
        label_more_details.place(x=750,y=400)

        label_instructions =Label(self.root,text="Instructions:", width=20,font=9)
        label_instructions.place(x=750,y=430)

        self.instructions_text = Text(self.root, height=20, width=60)
        self.instructions_text.place(x=800,y=460)
        self.instructions_text.insert(1.0, " ")

        buttonUpdateInstructions = Button(self.root, text='Update Recipe Instructions', width=20,bg="black",fg='white', 
            command = lambda: self.updateInstructions(currentUser))
        buttonUpdateInstructions.place(x=800,y=800)

        label_ingredients =Label(self.root,text="Ingredients:", width=20,font=9)
        label_ingredients.place(x=1300,y=430)

        # TODO - initialize tree view with items
        self.ingredients_frame = Frame(self.root, width=200, height=200)
        self.ingredients_frame.place(x=1300, y=460)

        recipe_ingredients_columns = ('id', 'name', 'amount')
        self.recipe_ingredients_tree = tkinter.ttk.Treeview(self.ingredients_frame, columns=recipe_ingredients_columns, show='headings')
        self.recipe_ingredients_tree.heading('id', text='ID')
        self.recipe_ingredients_tree.column("id", stretch=NO, width=50)
        self.recipe_ingredients_tree.heading('name', text='Name')
        self.recipe_ingredients_tree.column("name", stretch=NO, width=50)
        self.recipe_ingredients_tree.heading('amount', text='Quantity')
        self.recipe_ingredients_tree.column("amount", stretch=NO, width=50)

        self.sb2 = Scrollbar(self.ingredients_frame, orient=VERTICAL)
        self.sb2.pack(side=RIGHT, fill=Y)
        self.recipe_ingredients_tree.config(yscrollcommand=self.sb2.set)

        self.recipe_ingredients_tree.bind("<Double-1>", self.getIngredients)

        
    def loggedIn(self):
        return self.loggedIn

    def getRecipe(self, recipe):
        self.recipe_tree.focus(recipe)
        # gets the 3rd value from the treeview options (which has the information about the recipe) 
        return list(self.recipe_tree.item(recipe).values())[2] 

    def addBookmark(self, user):
        try:
            recipe = self.getRecipe(self.recipe_tree.selection()[0])
            recipeId = recipe[0] # gets the recipeID
            if (sql_utils.createBookmark(self.connection, recipeId, user)):
                msg="Recipe added to bookmarks: #{0}".format(recipeId)
                self.update_errorLabel(msg, "black")
            else:
                raise Exception("could not create bookmark")
        except:
            msg="Could not add bookmark. Make sure you select a recipe and try again...".format()
            self.update_errorLabel(msg, "red")
        

    def searchBy(self, search, criteria, dr):

        self.recipe_tree.config(yscrollcommand=self.sb.set)
        self.clearItems() # clear everything
        # Add dietary restriction!
        self.update_errorLabel("", "black")
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
        try:
            for tuple in result:
                recipe = (str(tuple[0]), str(tuple[1]), str(tuple[9]), str(tuple[2]), str(tuple[3]), 
                str(tuple[5]), str(tuple[6]), str(tuple[8]), str(tuple[10]), str(tuple[7]))
                # append recipe to total recipes
                all_recipes.append(recipe)
            self.createEntries(all_recipes)
        except:
            msg="Could not search by the given filter. Try again.."
            self.update_errorLabel(msg, "red")

    def getIngredients(self):
        result = self.getIngredients(self.getRecipe(self.recipe_tree.selection()[0]))
        all_ingredients = []
        try:
            for tuple in result:
                item = (str(tuple[0]), str(tuple[1]), str(tuple[2]))
                # append ingredients to total recipes
                all_ingredients.append(item)
            self.createIngredientEntries(all_ingredients)
        except:
            msg="Could not search by the given filter. Try again.."
            self.update_errorLabel(msg, "red")
    
    def createIngredientEntries(self, ingredients):
        self.recipe_ingredients_tree.delete()
        rows = []
        for r in ingredients:
            self.recipe_ingredients_tree.insert('', tk.END, values=r)
            self.recipe_ingredients_tree.pack()

    def deleteEnties(self, currentUserId):
        try:
            # Get selected item to Delete
            selected_item = self.recipe_tree.selection()[0]
            recipe = self.getRecipe(selected_item)
            recipeId = recipe[0] # gets the recipeID

            # check if user can delete this entry, and give update message! 
            isAuthor = sql_utils.isRecipeAuthor(self.connection, recipeId, currentUserId)
            if (isAuthor and sql_utils.deleteRecipe(self.connection, recipeId)):
                msg="Deleted recipe: #{0}".format(recipeId)
                self.update_errorLabel(msg, "black") 
                self.recipe_tree.delete(selected_item)
            else:
                raise Exception('cannot delete')
        except:
            msg="Could not delete item. Make sure you select a recipe you've authored and try again...".format()
            self.update_errorLabel(msg, "red")

    def clearItems(self):
        self.instructions_text.delete(1.0, "end")
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

    def updateInstructions(self, currentUserId):
        try:
            # Get selected item to Update
            selected_item = self.recipe_tree.selection()[0]
            recipe = self.getRecipe(selected_item)
            recipeId = recipe[0] # gets the recipeId
            new_instructions = self.instructions_text.get(1.0, "end")

            isAuthor = sql_utils.isRecipeAuthor(self.connection, recipeId, currentUserId)
            if (isAuthor and sql_utils.updateRecipeInstructions(self.connection, recipeId, new_instructions, currentUserId)):
                msg="Updated recipe: #{0}".format(recipeId)
                self.update_errorLabel(msg, "black") 
                self.searchBy(self.entry_search_name.get(), self.search_variable.get(), self.dr_variable.get())
            else:
                raise Exception('cannot delete')
        except:
            msg="Could not update item. Make sure you're selecting a recipe you've authored and try again...".format()
            self.update_errorLabel(msg, "red")

    def updateIngredients(self, currentUserId):
        try:
            # Get selected item to Update
            selected_item = self.recipe_tree.selection()[0]
            recipe = self.getRecipe(selected_item)
            recipeId = recipe[0] # gets the recipeId
            
            # get the ingredients
            # Call getRecipeIngredients from recipe_follow table.

            isAuthor = sql_utils.isRecipeAuthor(self.connection, recipeId, currentUserId)
            if (isAuthor):
                #sql_utils.updateRecipeIngredients(self.connection, recipeId, ingredient, amount, currentUserId)
                msg="Updated recipe: #{0}".format(recipeId)
                self.update_errorLabel(msg, "black") 
            else:
                raise Exception('cannot delete')
        except:
            msg="Could not update item. Make sure you're selecting a recipe you've authored and try again...".format()
            self.update_errorLabel(msg, "red")

    def errorLabel(self):
        global label
        label=Label(self.root, text="", font=('Aerial 10'))
        label.place(x=800, y=370)

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

def searchIngredients(connection, recipeId):
    return sql_utils.getIngredients(connection, recipeId)
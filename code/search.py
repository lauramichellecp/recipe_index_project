import tkinter as tk
from tkinter import *
import tkinter.ttk
import sql_utils
import add
import update

class LoggedInSearch():
    def __init__(self, connection, currentUser, currentUserName):
        self.connection = connection
        self.currentUserId = currentUser

        # Open Search with Bookmarks, etc.
        self.root = Tk() # Window
        self.root.geometry("2000x850")
        self.root.title('Recipe Index')

        label_user =Label(self.root,text="Hi, {0}! Welcome to Recipe Index. Here are your saved bookmarks".format(currentUserName),font=6)
        label_user.place(x=50,y=70)

        label_bookmarks =Label(self.root,text="Bookmarks", font=("bold",14))
        label_bookmarks.place(x=50,y=30)

        bookmarks_columns = ('id', 'name', 'ptime', 'ctime', 'servings', 'cuisine', 'author')
        recipe_columns = ('id', 'name', 'description', 'ptime', 'ctime', 'servings', 'cuisine', 'notes', 'author')

        self.frame_book = Frame(self.root, width=300, height=800)
        self.frame_book.place(x=50, y=100)

        self.bookmarks_tree = tkinter.ttk.Treeview(self.frame_book, columns=bookmarks_columns, show="headings")
        # recipe_name, prep_time, cook_time, serving_size, cuisine, user.first_name, instructions
        self.bookmarks_tree.heading('id', text='ID')
        self.bookmarks_tree.column("id", stretch=NO, width=50)
        self.bookmarks_tree.heading('name', text='Recipe Name')
        self.bookmarks_tree.column("name", width=160)
        self.bookmarks_tree.heading('ptime', text='Prep Time')
        self.bookmarks_tree.column("ptime", stretch=NO, width=50)
        self.bookmarks_tree.heading('ctime', text='Cook Time')
        self.bookmarks_tree.column("ctime", stretch=NO, width=50)
        self.bookmarks_tree.heading('servings', text='Servings')
        self.bookmarks_tree.column("servings", stretch=NO, width=50)
        self.bookmarks_tree.heading('cuisine', text='Cuisine')
        self.bookmarks_tree.column("cuisine", stretch=NO, width=90)
        self.bookmarks_tree.heading('author', text='Author')
        self.bookmarks_tree.column("author", stretch=NO, width=90)

        self.bookmark_sb = Scrollbar(self.frame_book, orient=VERTICAL)
        self.bookmark_sb.pack(side=RIGHT, fill=Y)

        buttonRemoveBookmark = Button(self.root, text='Remove selected bookmark', width=30,bg="black",fg='white', 
            command = lambda: self.removeBookmark(currentUser))
        buttonRemoveBookmark.place(x=50,y=340)

        label_bookmark_instructions =Label(self.root,text="Instructions:", width=20,font=9, anchor='w')
        label_bookmark_instructions.place(x=50,y=380)        

        self.bookmark_instructions = Text(self.root, height=10, width=75)
        self.bookmark_instructions.place(x=50,y=410)
        self.bookmark_instructions.insert(1.0, " ")

        label_bookmark_ingredients =Label(self.root,text="Ingredients:", width=20,font=9, anchor='w')
        label_bookmark_ingredients.place(x=50,y=580)   

        label_search =Label(self.root,text="Search for recipes", width=20,font=("bold",14))
        label_search.place(x=765,y=30)

        self.entry_search_name=Entry(self.root, width=50)
        self.entry_search_name.place(x=1030,y=70)

        buttonSearch = Button(self.root, text='Search recipes', width=20,bg="black",fg='white', 
            command = lambda: self.searchBy(self.entry_search_name.get(), self.search_variable.get(), self.dr_variable.get()))
        buttonSearch.place(x=800,y=65)

        OPTIONS = [
        "Name",
        "Max Prep Time",
        "Max Cook Time",
        "Max Total Time",
        "Serving Size",
        "Course",
        "Author",
        ] 
        self.search_variable = StringVar(self.root)
        self.search_variable.set(OPTIONS[0])

        search_options = OptionMenu(self.root, self.search_variable, *OPTIONS)
        search_options.place(x=1500,y=65)
        search_options.configure(width=10)

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
        dietary_options.place(x=1650,y=65)
        dietary_options.configure(width=12)

        self.frame = Frame(self.root, width=200, height=800)
        self.frame.place(x=800, y=100)

        self.recipe_tree = tkinter.ttk.Treeview(self.frame, columns=recipe_columns, show="headings")
        self.recipe_tree.heading('id', text='ID', anchor='center')
        self.recipe_tree.column("id", stretch=NO, width=50)
        self.recipe_tree.heading('name', text='Recipe Name', anchor='center')
        self.recipe_tree.column("name", width=200)
        self.recipe_tree.heading('description', text='Description', anchor='center')
        self.recipe_tree.column("description", width=300)
        self.recipe_tree.heading('ptime', text='Prep Time', anchor='center')
        self.recipe_tree.column("ptime", stretch=NO, width=50)
        self.recipe_tree.heading('ctime', text='Cook Time', anchor='center')
        self.recipe_tree.column("ctime", stretch=NO, width=50)
        self.recipe_tree.heading('servings', text='Servings', anchor='center')
        self.recipe_tree.column("servings", stretch=NO, width=50)
        self.recipe_tree.heading('cuisine', text='Cuisine', anchor='center')
        self.recipe_tree.column("cuisine", stretch=NO, width=120)
        self.recipe_tree.heading('notes', text='Notes', anchor='center')
        self.recipe_tree.column("notes", width=120)
        self.recipe_tree.heading('author', text='Author', anchor='center')
        self.recipe_tree.column("author", stretch=NO, width=50)

        self.sb = Scrollbar(self.frame, orient=VERTICAL)
        self.sb.pack(side=RIGHT, fill=Y)

        buttonDeleteRecipe = Button(self.root, text='Delete selected recipe', width=20,bg="black",fg='white', 
            command = lambda: self.deleteEnties(currentUser))
        buttonDeleteRecipe.place(x=800,y=340)

        self.errorLabel()

        buttonAddNewRecipe = Button(self.root, text='Add New Recipe', width=20,bg="black",fg='white', 
            command = lambda: add.AddRecipe(self.connection, currentUser))
        buttonAddNewRecipe.place(x=1050,y=340)

        buttonAddBookmark = Button(self.root, text='Add To Bookmarks', width=20,bg="black",fg='white', 
            command = lambda: self.addBookmark(currentUser))
        buttonAddBookmark.place(x=1300,y=340)

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

        self.ingredients_frame = Frame(self.root, width=200, height=400)
        self.ingredients_frame.place(x=1350, y=460)

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

        new_recipe_ingredient_label = Label(self.root, text="Add Ingredient to recipe:", anchor='w', width=60, font=("bold", 13))
        new_recipe_ingredient_label.place(x=1350,y=710)

        ingredient_name = Label(self.root, text="Name", anchor='w', width=60, font=("bold", 10))
        ingredient_name.place(x=1350,y=740)
        new_recipe_ingredient_name = Entry(self.root, width=20, font=("bold", 10))
        new_recipe_ingredient_name.place(x=1500,y=740)

        ingredient_amount = Label(self.root, text="Amount", anchor='w', width=60, font=("bold", 10))
        ingredient_amount.place(x=1350,y=765)
        new_recipe_ingredient_amount = Entry(self.root, width=20, font=("bold", 10))
        new_recipe_ingredient_amount.place(x=1500,y=765)

        buttonAddIngredient = Button(self.root, text='Add Ingredient', width=15,bg="black",fg='white', 
            command = lambda: self.addIngredient(currentUser, new_recipe_ingredient_name.get(), new_recipe_ingredient_amount.get()))
        buttonAddIngredient.place(x=1350,y=800)

        self.bookmark_ingredients_frame = Frame(self.root, width=450, height=100)
        self.bookmark_ingredients_frame.place(x=50,y=615)

        self.bookmark_recipe_ingredients_tree = tkinter.ttk.Treeview(self.bookmark_ingredients_frame, 
            columns=recipe_ingredients_columns, show='headings')
        self.bookmark_recipe_ingredients_tree.heading('id', text='ID')
        self.bookmark_recipe_ingredients_tree.column("id", stretch=NO, width=100)
        self.bookmark_recipe_ingredients_tree.heading('name', text='Name')
        self.bookmark_recipe_ingredients_tree.column("name", stretch=NO, width=260)
        self.bookmark_recipe_ingredients_tree.heading('amount', text='Amount')
        self.bookmark_recipe_ingredients_tree.column("amount", stretch=NO, width=230)

        self.sb3 = Scrollbar(self.bookmark_ingredients_frame, orient=VERTICAL)
        self.sb3.pack(side=RIGHT, fill=Y)
        self.bookmark_recipe_ingredients_tree.config(yscrollcommand=self.sb3.set)

        self.recipe_tree.bind("<Double-1>", self.doubleClick)
        self.recipe_tree.bind("<Key>", self.searchBy('', 'Name', 1))
        self.recipe_ingredients_tree.bind("<Double-1>", self.updateIngredients)

        self.bookmarks_tree.bind("<Double-1>", self.bookmarkdoubleClick)
        self.bookmarks_tree.bind("<Key>", self.showBookmarks(currentUser))

    
    def getRecipe(self, recipe):
        self.recipe_tree.focus(recipe)
        # gets the 3rd value from the treeview options (which has the information about the recipe) 
        return list(self.recipe_tree.item(recipe).values())[2] 
    
    def getBookmark(self, recipe):
        self.bookmarks_tree.focus(recipe)
        # gets the 3rd value from the treeview options (which has the information about the recipe) 
        return list(self.bookmarks_tree.item(recipe).values())[2] 

    def showBookmarks(self, user):
        self.bookmarks_tree.config(yscrollcommand=self.bookmark_sb.set)
        self.bookmark_instructions.delete(1.0, "end")
        for item in self.bookmarks_tree.get_children():
            self.bookmarks_tree.delete(item) # remove all bookmarks
        
        bookmarks = sql_utils.getBookmarksByUser(self.connection, user)
        if (bookmarks):
            self.bookmarks_tree.delete()
            for r in bookmarks:
                self.bookmarks_tree.insert('', tk.END, values=r)
                self.bookmarks_tree.pack()

    def removeBookmark(self, user):
        # Get selected item to Delete
        try:
            recipe = self.getBookmark(self.bookmarks_tree.selection()[0])
            recipeId = recipe[0] # gets the recipeID

            sql_utils.removeBookmarksByUser(self.connection, user, recipeId)
            self.showBookmarks(user)
        except:
            self.showBookmarks(user) 

    def addBookmark(self, user):
        try:
            recipe = self.getRecipe(self.recipe_tree.selection()[0])
            recipeId = recipe[0] # gets the recipeID
            if (sql_utils.createBookmark(self.connection, recipeId, user)):
                msg="Recipe added to bookmarks: #{0}".format(recipeId)
                self.update_errorLabel(msg, "black")
                self.showBookmarks(user)
            else:
                raise Exception("could not create bookmark")
        except:
            msg="Could not add bookmark. Make sure you select a recipe and try again...".format()
            self.update_errorLabel(msg, "red")
    
    def addIngredient(self, user, name, amount):
        try:
            # Get selected item to Update
            selected_item = self.recipe_tree.selection()[0]
            recipe = self.getRecipe(selected_item)
            recipeId = recipe[0] # gets the recipeId

            isAuthor = sql_utils.isRecipeAuthor(self.connection, recipeId, user)
            if (isAuthor and sql_utils.addIngredient(self.connection, recipeId, name, 1, amount)):
                msg="Ingredient added to recipe: #{0}".format(recipeId)
                self.update_errorLabel(msg, "black")
                self.showBookmarks(user)
            else:
                raise Exception("could not add ingredient")
        except:
            msg="Could not add ingredient. Make sure you're selecting a recipe you've authored and try again...".format()
            self.update_errorLabel(msg, "red")
        
    def searchBy(self, search, criteria, dr):
        self.recipe_tree.config(yscrollcommand=self.sb.set)
        self.clearItems() # clear everything
        # Add dietary restriction!
        self.update_errorLabel("", "black")
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
        filteredResults = self.filterByDR(dr, result)
        self.parseResults(filteredResults)

    def filterByDR(self, restriction, recipes):
        dr = getRestrictionType(restriction) # get restriction id

        recipes_following_dr = []
        for r in recipes:
            if (dr == 1 or searchByDietaryRestriction(self.connection, r[0], dr)): # check if recipe follows given dr
                recipes_following_dr.append(r)
        return recipes_following_dr

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
            self.update_errorLabel(msg, "red")

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

    def getBookmarkIngredients(self):
        recipe = self.getBookmark(self.bookmarks_tree.selection()[0])
        recipeId = recipe[0] # gets the recipeID
        result = sql_utils.getIngredients(self.connection, recipeId)
        all_ingredients = []
        for tuple in result:
            item = (str(tuple[0]), str(tuple[2]), str(tuple[1]))
            # append ingredients to total recipes
            all_ingredients.append(item)
        self.createBookmarkIngredientEntries(all_ingredients)
    
    def createIngredientEntries(self, ingredients):
        for item in self.recipe_ingredients_tree.get_children():
            self.recipe_ingredients_tree.delete(item)     
        for r in ingredients:
            self.recipe_ingredients_tree.insert('', tk.END, values=r)
            self.recipe_ingredients_tree.pack()

    def createBookmarkIngredientEntries(self, ingredients):
        for item in self.bookmark_recipe_ingredients_tree.get_children():
                self.bookmark_recipe_ingredients_tree.delete(item)     
        for r in ingredients:
            self.bookmark_recipe_ingredients_tree.insert('', tk.END, values=r)
            self.bookmark_recipe_ingredients_tree.pack()

    def deleteEnties(self, currentUserId):
        try:
            # Get selected item to Delete
            selected_item = self.recipe_tree.selection()[0]
            recipe = self.getRecipe(selected_item)
            recipeId = recipe[0] # gets the recipeID

            # check if user can delete this entry, and give update message! 
            isAuthor = sql_utils.isRecipeAuthor(self.connection, recipeId, currentUserId)
            if (isAuthor and sql_utils.deleteRecipe(self.connection, recipeId)):
                self.recipe_tree.delete(selected_item) # remove from recipes in gui
                self.instructions_text.delete(1.0, "end")
                self.showBookmarks(currentUserId) # update bookmarks
                msg="Deleted recipe: #{0}".format(recipeId)
                self.update_errorLabel(msg, "black")  # display success message
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
        
    def bookmarkdoubleClick(self, event):
        try:
            self.bookmark_instructions.delete(1.0, "end")
            recipe = self.getBookmark(self.bookmarks_tree.selection()[0])
            recipeInstructions = recipe[7]
            self.bookmark_instructions.insert(1.0, recipeInstructions)
            self.getBookmarkIngredients()
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
                self.showBookmarks(currentUserId)
            else:
                raise Exception('cannot delete')
        except:
            msg="Could not update recipe instructions. Make sure you're selecting a recipe you've authored and try again...".format()
            self.update_errorLabel(msg, "red")

    def updateIngredients(self, event):
        try:
            # Get selected item to Update
            selected_recipe = self.recipe_tree.selection()[0]
            recipeId = self.getRecipe(selected_recipe)[0] # gets the recipeId
            selected_ingredient = self.recipe_ingredients_tree.selection()[0]
            self.recipe_ingredients_tree.focus(selected_ingredient)
            ingredient = list(self.recipe_ingredients_tree.item(selected_ingredient).values())[2] 
            ingredientId = ingredient[0]
            
            if (sql_utils.isRecipeAuthor(self.connection, recipeId, self.currentUserId)):
                updateWindow = update.UpdateIngredient(self.connection, recipeId, ingredientId)
                msg="Updated recipe: #{0}".format(recipeId)
                self.update_errorLabel(msg, "black") 
            else:
                raise Exception('cannot update/delete')
            
        except:
            msg="Could not update ingredients. Make sure you're selecting a recipe you've authored and try again...".format()
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

def getRestrictionType(restriction):
    if (restriction == '-'):
        return 1
    elif (restriction == 'Vegan'):
        return 2
    elif (restriction == 'Vegetarian'):
        return 3
    elif (restriction == 'Gluten Free'):
        return 4
    elif (restriction == 'Dairy Free'):
        return 5
    elif (restriction == 'Nut Free'):
        return 6
    else:
        return 1

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

def searchByDietaryRestriction(connection, recipeId, restriction):
    return sql_utils.recipeToDR(connection, recipeId, restriction)
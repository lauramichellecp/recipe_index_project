import tkinter as tk
from tkinter import *
import tkinter.ttk
import sys

def addButton():
    print(f"from other file...")
    return None

def main():
    root = Tk() # Window
    root.geometry("3000x1000")
    root.title('Recipe Index')

    '''
    LEFT PANNEL: Bookmarks
    '''
    label_bookmarks =Label(root,text="Bookmarks", width=20,font=("bold",14))
    label_bookmarks.place(x=0,y=30)

    '''
    CENTER PANNEL: Filter with a dropdown
    '''
    separator = tkinter.ttk.Separator(root, orient='vertical')
    separator.place(x=400,y=0, relwidth=0.2, relheight=1)

    entry_search=Entry(root, width=100)
    entry_search.place(x=500,y=30)

    buttonSearch = Button(root, text='Search recipes by', width=20,bg="black",fg='white', 
        command = lambda: addButton())
    buttonSearch.place(x=1000,y=30)

    root.mainloop()

if __name__ == "__main__":
  main()

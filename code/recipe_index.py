import tkinter as tk
from tkinter import *
import tkinter.ttk
import sys
import pymysql
import user
import sql_utils

currentActiveUser = -1
buttonLoggedIn = False

def userSession(email, password):
    print("in user session")
    # check if user exists!
    if (buttonLoggedIn['text'] == "Login"):
        buttonLoggedIn['text'] = "Logout"
    currentActiveUser = user.login(email, password)
    print(currentActiveUser)


def userSignup(email, password):
    # check if user doesn't exist already!
    # create a new user in the database
    currentActiveUser = user.signup(email, password)
    if (currentActiveUser == -1):
        # some alert message
        return -1
    else:
        buttonLoggedIn['text'] = "Logout"

def makeConnection(username, password, host='localhost', database='recipe_index'):
    '''
    Creates a connection to the database, given a username and password, and returns it if its successful.
    '''
    try:
        connection = pymysql.connect(host=host, user=username, password=password, db=database)
        print("connected")
        return connection

    except pymysql.err.OperationalError as e:
        print('Error: %d: %s\n' % (e.args[0], e.args[1]))
        print('Try again... \n')
        return None

def main():
    if (len(sys.argv) != 3):
        print("Usage:", "python recipe_index.py username password")
        sys.exit(1)
        
    else:
        connection = sql_utils.getConnection(sys.argv[1], sys.argv[2])

    #Providing title to the form
    root = Tk() # Window
    root.geometry("300x300")
    root.title('Recipe Index')

    label_0 =Label(root,text="Login", width=20,font=("bold",18))
    label_0.place(x=0,y=30)

    label_email =Label(root,text="Email", width=20,font=("bold",10))
    label_email.place(x=0,y=80)

    entry_email=Entry(root, width=20)
    entry_email.place(x=115,y=80)

    label_pass =Label(root,text="Password", width=20,font=("bold",10))
    label_pass.place(x=0,y=100)

    entry_password=Entry(root, show="*")
    entry_password.place(x=115,y=100)

    buttonLoggedIn = Button(root, text='Login', width=10,bg="black",fg='white', 
        command = lambda: userSession(entry_email.get(), entry_password.get()))
    buttonLoggedIn.place(x=50,y=150)

    buttonSignUp = Button(root, text='Signup', width=10,bg="black",fg='white', 
        command = lambda: userSession(entry_email.get(), entry_password.get()))
    buttonSignUp.place(x=150,y=150)

    root.mainloop()


if __name__ == "__main__":
  main()


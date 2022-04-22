import tkinter as tk
from tkinter import *
import sys
import pymysql
import sql_utils
import signup
import search

class LoginWindow():
    def __init__(self, connection):
        self.currentActiveUser = False
        self.loggedIn = False
        self.connection = connection
        self.searchScreen = None

        #Providing title to the form
        self.root = Tk() # Window
        self.root.geometry("300x350")
        self.root.title('Welcome to Recipe Index!')

        label_0 =Label(self.root,text="Login", width=20,font=("bold",18))
        label_0.place(x=0,y=30)

        label_email =Label(self.root,text="Email", width=20,font=("bold",10))
        label_email.place(x=0,y=80)

        entry_email=Entry(self.root, width=20)
        entry_email.place(x=115,y=80)
        entry_email.insert(0, "")

        label_pass =Label(self.root,text="Password", width=20,font=("bold",10))
        label_pass.place(x=0,y=100)

        entry_password=Entry(self.root, show="*")
        entry_password.place(x=115,y=100)
        entry_password.insert(0, "")

        buttonLoggedIn = Button(self.root, text='Login', width=10,bg="black",fg='white', 
            command = lambda: self.userLogin(entry_email.get(), entry_password.get()))
        buttonLoggedIn.place(x=50,y=150)

        buttonLogout = Button(self.root, text='Logout', width=10,bg="black",fg='white', 
            command = lambda: self.userLogout())
        buttonLogout.place(x=150,y=150)

        buttonSignUp = Button(self.root, text='Signup', width=25,bg="black",fg='white', 
            command = lambda: self.userSignup())
        buttonSignUp.place(x=50,y=200)

        buttonSearch = Button(self.root, text='Search for recipes...', width=25,bg="black",fg='white', 
            command = lambda: self.openSearch())
        buttonSearch.place(x=50,y=250)

        self.errorLabel()

        self.root.attributes('-topmost',True)

        self.root.mainloop()
    
    def userLogin(self, email, password):
        try:
            self.currentActiveUser = sql_utils.getUser(self.connection, email, password)
            if (self.currentActiveUser):
                # keep search open if logged.
                self.loggedIn = True
                self.update_errorLabel("")
                self.openSearch()
            else:
                self.update_errorLabel("Couldn't log in! Try again...")
        except pymysql.Error as e:
            return False
        return True

    def userLogout(self):
        if(self.loggedIn):
            self.currentActiveUser = False
            self.loggedIn = False
            self.update_errorLabel("Successfully logged out...")
            self.closeSearch()

    def userSignup(self):
        try:
            return signup.signUpScreen(self.connection)
        except pymysql.Error as e:
            return False

    def errorLabel(self):
        global label
        label=Label(self.root, text="", font=('Aerial 10'))
        label.place(y=330)

    def remove_errorLabel(self):
        global label
        label.pack_forget()

    def update_errorLabel(self, msg):
        global label
        try:
            label["text"]=msg
        except:
            return False

    def openSearch(self):
        if (self.searchScreen == None):
            self.openLoggedInOrAnon()
        else:
            try:
                self.searchScreen.root.destroy()
                self.openLoggedInOrAnon()
            except:
                self.openLoggedInOrAnon()

    def closeSearch(self):
        try:
            self.searchScreen.root.destroy()
        except:
            print("could not close")

    def openLoggedInOrAnon(self):
        if (self.loggedIn):
            self.searchScreen = search.LoggedInSearch(self.connection, self.currentActiveUser)
        else:
            self.searchScreen = search.AnonSearch(self.connection)


def makeConnection(username, password, host='localhost', database='recipe_index'):
    try:
        connection = pymysql.connect(host=host, user=username, password=password, db=database, autocommit=True)
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
        test = LoginWindow(makeConnection(sys.argv[1], sys.argv[2]))

if __name__ == "__main__":
  main()
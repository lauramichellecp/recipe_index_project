import tkinter as tk
from tkinter import *
import sys
import pymysql
import sql_utils
import signup
import search
import anonSearch

class LoginWindow():
    def __init__(self, connection):
        self.currentActiveUser = False
        self.loggedIn = False
        self.connection = connection
        self.searchScreen = None

        #Providing title to the form
        self.root = Tk() # Window
        self.root.geometry("500x500")
        self.root.title('Welcome to Recipe Index!')

        #creating a frame for the form
        frame = Frame(self.root, width=300, height=350)
        frame.pack(expand=True)

        login_label =Label(frame, text="Login", width=20,font=("bold",20))
        login_label.grid(row=0,column=0, columnspan=2, padx=20, pady=20, sticky=N)

        label_email =Label(frame,text="Email", width=20,font=("bold",10))
        label_email.grid(row=1,column=0)

        entry_email=Entry(frame, width=10)
        entry_email.grid(row=1,column=1)
        #entry_email.insert(0, "")

        label_pass =Label(frame,text="Password", width=20,font=("bold",10))
        label_pass.grid(row=2,column=0)

        entry_password=Entry(frame, show="*", width=10)
        entry_password.grid(row=2,column=1)
        #entry_password.insert(0, "")

        buttonLoggedIn = Button(frame, text='Login', width=10,bg="black",fg='white',
            command = lambda: self.userLogin(entry_email.get(), entry_password.get()))
        buttonLoggedIn.grid(row=4,column=0, columnspan=2, padx=5, pady=5, sticky=N)

        buttonLogout = Button(frame, text='Logout', width=10,bg="black",fg='white',
            command = lambda: self.userLogout())
        buttonLogout.grid(row=5,column=0, columnspan=2, padx=5, pady=5, sticky=N)

        buttonSignUp = Button(frame, text='Signup', width=25,bg="black",fg='white',
            command = lambda: self.userSignup())
        buttonSignUp.grid(row=6,column=0, columnspan=2, padx=5, pady=5, sticky=N)

        buttonSearch = Button(frame, text='Search for recipes...', width=25,bg="black",fg='white',
            command = lambda: self.openSearch())
        buttonSearch.grid(row=7,column=0, columnspan=2,padx=5, pady=5, sticky=N)

        self.errorLabel()

        #self.root.attributes('-topmost',True)

        self.root.mainloop()
    
    def userLogin(self, email, password):
        try:
            user = sql_utils.getUser(self.connection, email, password)
            self.currentActiveUser = user[0]
            self.currentActiveUserName = user[1]
            print(self.currentActiveUser)
            # something weird here, I think...
            if (self.currentActiveUser):
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
        self.openLoggedInOrAnon()

    def closeSearch(self):
        try:
            self.searchScreen.root.destroy()
        except:
            return False

    def openLoggedInOrAnon(self):
        self.closeSearch()
        if (self.loggedIn):
            self.searchScreen = search.LoggedInSearch(self.connection, self.currentActiveUser, self.currentActiveUserName)
            
        else:
            self.searchScreen = anonSearch.AnonSearch(self.connection)

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
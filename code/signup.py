import tkinter as tk
from tkinter import *
import pymysql
import sql_utils

class SignupWindow():
     
    def __init__(self, connection):
        self.connection = connection
        #Providing title to the form
        self.root = Tk() # Window

        self.root.geometry("300x300")
        self.root.title('Sign Up')

        label_0 =Label(self.root,text="Signup", width=20,font=("bold",18))
        label_0.place(x=0,y=30)

        label_name =Label(self.root,text="First Name", width=20,font=("bold",10))
        label_name.place(x=0,y=80)

        entry_name=Entry(self.root, width=20)
        entry_name.place(x=115,y=80)

        label_last =Label(self.root,text="Last Name", width=20,font=("bold",10))
        label_last.place(x=0,y=100)

        entry_last=Entry(self.root)
        entry_last.place(x=115,y=100)

        label_email =Label(self.root,text="Email", width=20,font=("bold",10))
        label_email.place(x=0,y=120)

        entry_email=Entry(self.root, width=20)
        entry_email.place(x=115,y=120)

        label_pass =Label(self.root,text="Password", width=20,font=("bold",10))
        label_pass.place(x=0,y=140)

        entry_password=Entry(self.root, show="*")
        entry_password.place(x=115,y=140)

        buttonSignUp = Button(self.root, text='Signup', width=10,bg="black",fg='white', 
            command = lambda: self.signup(entry_name.get(), entry_last.get(), entry_email.get(), entry_password.get()))
        buttonSignUp.place(x=150,y=180)

        self.root.mainloop()

    def signup(self, first, last, email, password):
        try:
            signupUser = sql_utils.createUser(self.connection, first, last, email, password)
            print(signupUser)
            self.root.destroy()
        except pymysql.Error as e:
            return False
        return True

def signUpScreen(connection):
    test = SignupWindow(connection)
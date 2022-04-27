import tkinter as tk
from tkinter import *
import pymysql
import sql_utils

class SignupWindow():
     
    def __init__(self, connection):
        self.connection = connection
        #Providing title to the form
        self.root = Tk() # Window

        self.root.geometry("500x350")
        self.root.title('Sign Up')

        #creating a frame for the form
        frame = Frame(self.root, width=300, height=350)
        frame.pack()

        label_0 =Label(frame,text="Signup", width=20,font=("bold",18))
        label_0.grid(row=0,column=0,padx=20,pady=20, columnspan=2, sticky=N)

        label_name =Label(frame,text="First Name", width=20,font=("bold",10))
        label_name.grid(row=1,column=0, sticky=W)

        entry_name=Entry(frame, width=20)
        entry_name.grid(row=1,column=1, sticky=W)

        label_last =Label(frame,text="Last Name", width=20,font=("bold",10))
        label_last.grid(row=2,column=0, sticky=W)

        entry_last=Entry(frame, width=20)
        entry_last.grid(row=2,column=1, sticky=W)

        label_email =Label(frame,text="Email", width=20,font=("bold",10))
        label_email.grid(row=3,column=0, sticky=W)

        entry_email=Entry(frame, width=20)
        entry_email.grid(row=3,column=1, sticky=W)

        label_pass =Label(frame,text="Password", width=20,font=("bold",10))
        label_pass.grid(row=4,column=0, sticky=W)

        entry_password=Entry(frame, show="*")
        entry_password.grid(row=4,column=1, sticky=W)

        frame.rowconfigure(5, minsize=50)

        buttonSignUp = Button(frame, text='Signup', width=10,bg="black",fg='white',
            command = lambda: self.signup(entry_name.get(), entry_last.get(), entry_email.get(), entry_password.get()))
        buttonSignUp.grid(row=5,column=0, columnspan=2, sticky=S)

        Label(frame, text="", font=('Aerial 10')).grid(row=6)
        self.label=Label(frame, text="", font=('Aerial 10'))
        self.label.grid(row=7, column=0, sticky=S, columnspan=2)

    def signup(self, first, last, email, password):
        if ((len(first) < 1 or len(last) < 1) or '@' not in email or len(password) < 8): 
            self.update_errorLabel("Name must not be blank. Email must be valid. Pssword must be at least 8 characters.", "red")
        else:
            signupUser = sql_utils.createUser(self.connection, first, last, email, password)
            if (not signupUser):
                self.update_errorLabel("Could not sign up. Try again", "red")
            else:
                self.root.destroy()

    def update_errorLabel(self, msg, color):
        try:
            self.label["text"]=msg
            self.label.config(fg=color)
        except:
            return False
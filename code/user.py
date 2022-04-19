import pymysql
import search
import sql_utils
'''
Retrieving information for users: login, signup, logout
'''

def login(connection, email, password):
    '''
    Logs in as a user (checks if the given email and password exist in the database)
    '''
    return 0

    # if user does not exist, create an alert or something

def logout():
    '''
    Logs out
    '''
    print(f"Logged out")
    return -1

def signup(email, password):
    '''
    Signs up a new user. If user already exists, logs in instead.
    '''
    print(f"The email entered aws {email} ")
    print(f"The password entered was {password} ")
    return 0
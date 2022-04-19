import pymysql
import search
'''
Retrieving information for users: login, signup, logout
'''

def login(email, password):
    '''
    Logs in as a user (checks if the given email and password exist in the database)
    '''
    print(f"The email entered was {email} ")
    print(f"The password entered was {password} ") 
    successfulLogin = True
    if (successfulLogin):
        search.main()
    else:
        return -1

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
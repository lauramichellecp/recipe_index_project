import pymysql
import sys

_connection = None

def createRecipe(r_name, r_prep_time, r_cook_time, r_serving_size,
		r_cuisine, r_instruct, r_note, r_descrip, current_user, r_course):
    '''
    Create a new recipe (add arguments needed for procedure call)
    '''
    try:
        cursor = _connection.cursor()
        query = "CALL createRecipe('{0}', {1}, {2}, {3}, '{4}', '{5}', '{6}', '{7}', {8}, '{9}');".format(r_name, r_prep_time, r_cook_time, 
        r_serving_size, r_cuisine, r_instruct, r_note, r_descrip, current_user, r_course) # call procedure here
        cursor.execute(query)

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False

    return True

def getUser(email, password):
    '''
    Create a new recipe (add arguments needed for procedure call)
    '''
    try:
        cursor = _connection.cursor()
        query = "SELECT uid FROM user WHERE email = '{0}' AND password = '{1}';".format(email, password)
        cursor.execute(query)
        result = cursor.fetchone()[0]
        print(result)

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False

def getConnection(username, password, host='localhost', database='recipe_index'):
    '''
    NOTE: this is for testing purposes! Remove this once integrated with gui
    '''
    #  Creates a connection to the database, given a username and password, and returns it if its successful.
    global _connection
    if not _connection:
        try:
            _connection = pymysql.connect(host=host, user=username, password=password, db=database)
            return _connection

        except pymysql.err.OperationalError as e:
            print('Error: %d: %s\n' % (e.args[0], e.args[1]))
            print('Try again... \n')
            return None

def main():
    '''
    NOTE: this is for testing purposes! Remove this once integrated with gui
    '''
    if (len(sys.argv) != 3):
        print("Usage:", "python recipe_index.py username password")
        sys.exit(1)
        
    getConnection(sys.argv[1], sys.argv[2])
    getUser('calderon.l@northeastern.edu', 'pass')
    # try calling other functions and procedures here as well!


if __name__ == "__main__":
    main()
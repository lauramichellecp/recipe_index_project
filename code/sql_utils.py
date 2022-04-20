import pymysql
import sys

_connection = None


def createRecipe(r_name, r_prep_time, r_cook_time, r_serving_size,
                 r_cuisine, r_instruct, r_note, r_descrip, current_user, r_course):
    """
    Create a new recipe (add arguments needed for procedure call)
    """
    try:
        cursor = _connection.cursor()
        query = "CALL createRecipe('{0}', {1}, {2}, {3}, '{4}', '{5}', '{6}', '{7}', {8}, '{9}');" \
            .format(r_name, r_prep_time, r_cook_time, r_serving_size, r_cuisine, r_instruct, r_note, r_descrip,
                    current_user, r_course)
        cursor.execute(query)

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False
    return True


def createBookmark(r_id, current_user):
    try:
        cursor = _connection.cursor()
        query = "CALL createBookmark('{0}', {1});".format(r_id, current_user)
        cursor.execute(query)

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False
    return True


def createUser(u_first, u_last, u_email, u_pass):
    try:
        cursor = _connection.cursor()
        query = "CALL createUser('{0}', '{1}', '{2}', '{3}');".format(u_first, u_last, u_email, u_pass)
        cursor.execute(query)

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False
    return True


def getRecipeByName(r_name):
    try:
        cursor = _connection.cursor()
        query = "CALL getRecipeByName('{0}')".format(r_name)
        cursor.execute(query)
        result = cursor.fetchone()

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getRecipeAuthor(r_id):
    try:
        cursor = _connection.cursor()
        query = "SELECT getRecipeAuthor({0});".format(r_id)
        cursor.execute(query)
        result = cursor.fetchone()[0]

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def isRecipeAuthor(r_id, author_id):
    try:
        cursor = _connection.cursor()
        query = "SELECT isRecipeAuthor({0}, {1});".format(r_id, author_id)
        cursor.execute(query)
        result = cursor.fetchone()[0]

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getRecipesByAuthor(author_id):
    try:
        cursor = _connection.cursor()
        query = "CALL getRecipesByAuthor({0});".format(author_id)
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getRecipeByID(r_id):
    try:
        cursor = _connection.cursor()
        query = "CALL getRecipeByID({0});".format(r_id)
        cursor.execute(query)
        result = cursor.fetchone()

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getRecipesByCourse(course):
    try:
        cursor = _connection.cursor()
        query = "CALL getRecipesByCourse('{0}');".format(course)
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getRecipesByPrepTime(prep_time_max):
    try:
        cursor = _connection.cursor()
        query = "CALL getRecipesByPrepTime({0});".format(prep_time_max)
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getRecipesByCookTime(cook_time_max):
    try:
        cursor = _connection.cursor()
        query = "CALL getRecipesByCookTime({0});".format(cook_time_max)
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getRecipesByTotalTime(time_max):
    try:
        cursor = _connection.cursor()
        query = "CALL getRecipesByTotalTime({0});".format(time_max)
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getBookmarkByUser(current_user):
    try:
        cursor = _connection.cursor()
        query = "CALL getBookmarkByUser({0});".format(current_user)
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getRecipeByName(r_name):
    try:
        cursor = _connection.cursor()
        query = "CALL getRecipeByName('{0}')".format(r_name)
        cursor.execute(query)
        result = cursor.fetchone()

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def validateUser(username, password):
    try:
        cursor = _connection.cursor()
        query = "SELECT validateUser('{0}', '{1}');".format(username, password)
        cursor.execute(query)
        result = cursor.fetchone()

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getUserID(username):
    try:
        cursor = _connection.cursor()
        query = "SELECT getUserID('{0}');".format(username)
        cursor.execute(query)
        result = cursor.fetchone()

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getUser(email, password):
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


def addIngredient(r_id, i_name, diet_rest, amt):
    try:
        cursor = _connection.cursor()
        query = "CALL addIngredient({0}, '{1}', '{2}', {3});".format(r_id, i_name, diet_rest, amt)
        cursor.execute(query)

        return True

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getConnection(username, password, host='localhost', database='recipe_index'):
    """
    NOTE: this is for testing purposes! Remove this once integrated with gui
    """
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
    """
    NOTE: this is for testing purposes! Remove this once integrated with gui
    """
    if len(sys.argv) != 3:
        print("Usage:", "python recipe_index.py username password")
        sys.exit(1)

    getConnection(sys.argv[1], sys.argv[2])
    getUser('calderon.l@northeastern.edu', 'pass')
    # try calling other functions and procedures here as well!


if __name__ == "__main__":
    main()

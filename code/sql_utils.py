import pymysql
import sys

def createRecipe(_connection, r_name, r_prep_time, r_cook_time, r_serving_size,
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


def createBookmark(_connection, r_id, current_user):
    try:
        cursor = _connection.cursor()
        query = "CALL createBookmark('{0}', {1});".format(r_id, current_user)
        cursor.execute(query)

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False
    return True


def createUser(_connection, u_first, u_last, u_email, u_pass):
    try:
        cursor = _connection.cursor()
        query = "CALL createUser('{0}', '{1}', '{2}', '{3}');".format(u_first, u_last, u_email, u_pass)
        cursor.execute(query)

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False
    return True


def getRecipesByName(_connection, r_name):
    try:
        cursor = _connection.cursor()
        query = "CALL getRecipeByName('{0}')".format(r_name)
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getRecipeAuthor(_connection, r_id):
    try:
        cursor = _connection.cursor()
        query = "SELECT getRecipeAuthor({0});".format(r_id)
        cursor.execute(query)
        result = cursor.fetchone()[0]

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def isRecipeAuthor(_connection, r_id, author_id):
    try:
        cursor = _connection.cursor()
        query = "SELECT isRecipeAuthor({0}, {1});".format(r_id, author_id)
        cursor.execute(query)
        result = cursor.fetchone()[0]

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getRecipesByAuthor(_connection, author_id):
    try:
        cursor = _connection.cursor()
        query = "CALL getRecipesByAuthor({0});".format(author_id)
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False

def getRecipesByAuthorName(_connection, author_name):
    try:
        cursor = _connection.cursor()
        query = "CALL getRecipesByAuthorName('{0}');".format(author_name)
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False   


def getRecipeByID(_connection, r_id):
    try:
        cursor = _connection.cursor()
        query = "CALL getRecipeByID({0});".format(r_id)
        cursor.execute(query)
        result = cursor.fetchone()
        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getRecipesByCourseName(_connection, course):
    try:
        cursor = _connection.cursor()
        query = "CALL getRecipesByCourseName('{0}');".format(course)
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getRecipesByPrepTime(_connection, prep_time_max):
    try:
        cursor = _connection.cursor()
        query = "CALL getRecipesByPrepTime({0});".format(prep_time_max)
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getRecipesByCookTime(_connection, cook_time_max):
    try:
        cursor = _connection.cursor()
        query = "CALL getRecipesByCookTime({0});".format(cook_time_max)
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getRecipesByTotalTime(_connection, time_max):
    try:
        cursor = _connection.cursor()
        query = "CALL getRecipesByTotalTime({0});".format(time_max)
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getBookmarkByUser(_connection, current_user):
    try:
        cursor = _connection.cursor()
        query = "CALL getBookmarkByUser({0});".format(current_user)
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getRecipeByName(_connection, r_name):
    try:
        cursor = _connection.cursor()
        query = "CALL getRecipeByName('{0}')".format(r_name)
        cursor.execute(query)
        result = cursor.fetchone()

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def validateUser(_connection, username, password):
    '''
    TODO: What does this do?
    '''
    try:
        cursor = _connection.cursor()
        query = "SELECT validateUser('{0}', '{1}');".format(username, password)
        cursor.execute(query)
        result = cursor.fetchone()

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False

def getUserID(_connection, username):
    try:
        cursor = _connection.cursor()
        query = "SELECT getUserID('{0}');".format(username)
        cursor.execute(query)
        result = cursor.fetchone()
        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getUser(_connection, email, password):
    try:
        cursor = _connection.cursor()
        query = "SELECT uid FROM user WHERE email = '{0}' AND password = '{1}';".format(email, password)
        cursor.execute(query)
        result = cursor.fetchone()
        if (result == None):
            return False
        return result[0]

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def addIngredient(_connection, r_id, i_name, diet_rest, amt):
    try:
        cursor = _connection.cursor()
        query = "CALL addIngredient({0}, '{1}', '{2}', {3});".format(r_id, i_name, diet_rest, amt)
        cursor.execute(query)

        return True

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False

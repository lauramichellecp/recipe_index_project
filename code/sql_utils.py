import pymysql


def createRecipe(_connection, r_name, r_prep_time, r_cook_time, r_serving_size,
                 r_cuisine, r_instruct, r_note, r_descrip, current_user, r_course):
    try:
        cursor = _connection.cursor()
        query = 'CALL createRecipe("{0}", {1}, {2}, {3}, "{4}", "{5}", "{6}", "{7}", {8}, "{9}");' \
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

def getRecipesByServings(_connection, serving_size):
    try:
        cursor = _connection.cursor()
        query = "CALL getRecipesByServings({0});".format(serving_size)
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


def getBookmarksByUser(_connection, current_user):
    try:
        cursor = _connection.cursor()
        query = "CALL getBookmarksByUser({0});".format(current_user)
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False

def removeBookmarksByUser(_connection, current_user, recipeId):
    try:
        cursor = _connection.cursor()
        query = "DELETE FROM bookmark WHERE uid = {0} AND recipe = {1};".format(current_user, recipeId)
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
        query = "SELECT uid, first_name FROM user WHERE email = '{0}' AND password = '{1}';".format(email, password)
        cursor.execute(query)
        result = cursor.fetchone()
        if (result == None):
            return False
        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False

def addIngredient(_connection, r_id, i_name, diet_rest, amt):
    try:
        cursor = _connection.cursor()
        query = "CALL addIngredients({0}, '{1}', {2}, '{3}');".format(r_id, i_name, diet_rest, amt)
        cursor.execute(query)
        return True

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def deleteRecipe(_connection, recipe_id):
    try:
        cursor = _connection.cursor()
        query = "DELETE FROM recipe WHERE rid = {0};".format(recipe_id)
        cursor.execute(query)

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False
    return True

def updateRecipeInstructions(_connection, recipe_id, instructions, author):
    try:
        cursor = _connection.cursor()
        query = "UPDATE recipe SET instructions = '{0}' WHERE rid = {1} AND author = {2};".format(instructions, recipe_id, author)
        cursor.execute(query)

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False
    return True

def updateRecipeIngredient(_connection, recipe_id, ingredient, amount):
    try:
        cursor = _connection.cursor()
        query = "UPDATE recipe_ingredient SET amount = '{0}' WHERE rid = {1} AND iid = {2};".format(amount, recipe_id, ingredient)
        cursor.execute(query)

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False
    return True

def removeRecipeIngredient(_connection, recipe_id, ingredient):
    try:
        cursor = _connection.cursor()
        query = "DELETE FROM recipe_ingredient WHERE rid = {0} AND iid = {1};".format(recipe_id, ingredient)
        cursor.execute(query)

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False
    return True

def getIngredients(_connection, recipe_id):
    try:
        cursor = _connection.cursor()
        query = "CALL getIngredients({0});".format(recipe_id)
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def getRecipeByDietary(_connection, diet_rest):
    try:
        cursor = _connection.cursor()
        query = "CALL getRecipeByDietary('{0}');".format(diet_rest)
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False


def recipeToDR(_connection, r_id, dr_id):
    try:
        cursor = _connection.cursor()
        query = "SELECT recipeToDR({0}, {1});".format(r_id, dr_id)
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0]
    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))
        return False

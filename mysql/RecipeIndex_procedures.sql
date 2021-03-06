-- Procedures and functions for our recipe_index database
use recipe_index; 

DELIMITER $$
DROP FUNCTION IF EXISTS getRecipeAuthor$$

CREATE FUNCTION getRecipeAuthor(recipeId INT) -- given a recipe id, returns the author id 
RETURNS INT DETERMINISTIC
BEGIN
	DECLARE authorID INT;
    SET authorID = (SELECT author FROM recipe WHERE rid = recipeId);
	RETURN authorID;
END$$
DELIMITER ;

-- SELECT getRecipeAuthor(1);

DELIMITER $$
DROP FUNCTION IF EXISTS isRecipeAuthor$$

CREATE FUNCTION isRecipeAuthor(recipeId INT, authorId INT) -- given a recipe id and an authorId returns true if author id 
RETURNS BOOL DETERMINISTIC
BEGIN
	RETURN (SELECT EXISTS(SELECT author FROM recipe WHERE rid = recipeId AND author = authorId));
END$$
DELIMITER ;

-- SELECT isRecipeAuthor(1, 2);
-- SELECT isRecipeAuthor(1, 1);

DELIMITER $$
DROP PROCEDURE IF EXISTS getRecipesByAuthor$$

CREATE PROCEDURE getRecipesByAuthor(IN authorId INT) -- return all recipes given the author id 
BEGIN
	SELECT rid, recipe_name, description, prep_time, cook_time, serving_size, cuisine, notes, user.first_name, instructions FROM recipe LEFT JOIN user ON author = uid 
    WHERE author = authorId ORDER BY publish_date DESC;
END$$
DELIMITER ;

-- CALL getRecipesByAuthor(2);
-- CALL getRecipesByAuthor(1);

DELIMITER $$
DROP PROCEDURE IF EXISTS getRecipesByAuthorName$$

CREATE PROCEDURE getRecipesByAuthorName(IN a_name VARCHAR(16)) 
BEGIN
	DECLARE user_id INT;
    DECLARE row_not_found BOOL DEFAULT FALSE;
	DECLARE cur CURSOR FOR 
		SELECT uid FROM user WHERE first_name = a_name;
	DECLARE CONTINUE HANDLER FOR NOT FOUND
			SET row_not_found = TRUE;
    
	OPEN cur;
    
    WHILE row_not_found = FALSE DO 
			FETCH cur INTO user_id;
			CALL getRecipesByAuthor(user_id);
	END WHILE;
	CLOSE cur;
END$$
DELIMITER ;

-- CALL getRecipesByAuthorName("Laura");
-- CALL getRecipesByAuthorName("Maria");

DELIMITER $$ 
DROP PROCEDURE IF EXISTS getRecipeByID $$

CREATE PROCEDURE getRecipeByID(IN id INT)
BEGIN 
	SELECT * FROM recipe WHERE rid = id;
END$$
DELIMITER ;

-- CALL getRecipeByID(1);

DELIMITER $$ 
DROP PROCEDURE IF EXISTS getRecipeByID $$

CREATE PROCEDURE getRecipeByID(IN id INT)
BEGIN 
	SELECT rid, recipe_name, description, prep_time, cook_time, serving_size, cuisine, notes, user.first_name, instructions FROM recipe LEFT JOIN user ON author = uid 
    WHERE rid = id ORDER BY publish_date DESC;
END$$
DELIMITER ;

-- CALL getRecipeByID(1);

-- get recipe by name 

DELIMITER $$
DROP PROCEDURE IF EXISTS getRecipeByName$$

CREATE PROCEDURE getRecipeByName(rname VARCHAR(64))
BEGIN
	SELECT rid, recipe_name, description, prep_time, cook_time, serving_size, cuisine, notes, user.first_name, instructions FROM recipe LEFT JOIN user ON author = uid 
    WHERE recipe_name LIKE concat("%",rname,"%") ORDER BY publish_date DESC;
END$$
DELIMITER ;

-- Does this recipe follow this Dietary restriction?
DELIMITER $$ 
DROP FUNCTION IF EXISTS recipeToDR $$

CREATE FUNCTION recipeToDR(recipe_id INT, dr_id INT)
RETURNS BOOL DETERMINISTIC
BEGIN 
	DECLARE done BOOL DEFAULT FALSE;
    DECLARE ingredient INT;
	DECLARE doesFollow BOOL DEFAULT TRUE;
	DECLARE cur CURSOR FOR 
		SELECT iid FROM recipe_ingredient WHERE rid = recipe_id; 
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
	OPEN cur;
    
    WHILE (NOT done AND doesFollow) DO
		FETCH cur INTO ingredient;
        IF NOT (SELECT EXISTS (SELECT * FROM ingredient_follows 
				WHERE ingredient = iid AND dr_id = drid))
                THEN SET doesFollow = FALSE;
		END IF;
    END WHILE;
    CLOSE cur;
    RETURN doesFollow;
END$$
DELIMITER ;

/*
SELECT recipeToDR(1, 1); 
SELECT recipeToDR(1, 2);
SELECT recipeToDR(2, 1);
SELECT recipeToDR(2, 2);
*/

DELIMITER $$ 
DROP PROCEDURE IF EXISTS getRecipeByDietary $$

CREATE PROCEDURE getRecipeByDietary(IN drid INT) -- return all recipes given the drid
BEGIN 
	SELECT rid, recipe_name, description, prep_time, cook_time, serving_size, cuisine, notes, user.first_name, instructions FROM recipe LEFT JOIN user ON author = uid 
    WHERE recipeToDR(rid,drid) ORDER BY publish_date DESC;
END$$
DELIMITER ;

-- CALL getRecipeByDietary(1); 
-- CALL getRecipeByDietary(3); 

-- return recipes of this course 
DELIMITER $$
DROP PROCEDURE IF EXISTS getRecipesByCourse$$

CREATE PROCEDURE getRecipesByCourse(IN recipe_course INT) 
BEGIN
	SELECT rid, recipe_name, description, prep_time, cook_time, serving_size, cuisine, notes, user.first_name, instructions FROM recipe LEFT JOIN user ON author = uid 
    WHERE course = recipe_course ORDER BY publish_date DESC;
END$$
DELIMITER ;

-- CALL getRecipesByCourse(1);
-- CALL getRecipesByCourse(2);

-- return recipes of this course name
DELIMITER $$
DROP PROCEDURE IF EXISTS getRecipesByCourseName$$

CREATE PROCEDURE getRecipesByCourseName(IN recipe_course VARCHAR(16)) 
BEGIN
    CALL getRecipesByCourse((SELECT cid FROM course WHERE course_name = recipe_course));
END$$
DELIMITER ;

-- CALL getRecipesByCourseName("dessert");
-- CALL getRecipesByCourseName("breakfast");

-- return recipes with a prep time less than the given
DELIMITER $$
DROP PROCEDURE IF EXISTS getRecipesByPrepTime$$

CREATE PROCEDURE getRecipesByPrepTime(IN prep_time_max INT) 
BEGIN
	SELECT rid, recipe_name, description, prep_time, cook_time, serving_size, cuisine, notes, user.first_name, instructions FROM recipe LEFT JOIN user ON author = uid WHERE prep_time <= prep_time_max
    ORDER BY publish_date DESC;
END$$
DELIMITER ;

-- CALL getRecipesByPrepTime(10);

-- return recipes with a cook time less than the given
DELIMITER $$
DROP PROCEDURE IF EXISTS getRecipesByCookTime$$

CREATE PROCEDURE getRecipesByCookTime(IN cook_time_max INT) 
BEGIN
	SELECT rid, recipe_name, description, prep_time, cook_time, serving_size, cuisine, notes, user.first_name, instructions FROM recipe LEFT JOIN user ON author = uid WHERE cook_time <= cook_time_max
    ORDER BY publish_date DESC;
END$$
DELIMITER ;

-- return recipes with a total time less than the given
DELIMITER $$
DROP PROCEDURE IF EXISTS getRecipesByTotalTime$$

CREATE PROCEDURE getRecipesByTotalTime(IN time_max INT) 
BEGIN
	SELECT rid, recipe_name, description, prep_time, cook_time, serving_size, cuisine, notes, user.first_name, instructions FROM recipe LEFT JOIN user ON author = uid WHERE (cook_time + prep_time) <= time_max
    ORDER BY publish_date DESC;
END$$
DELIMITER ;

-- return recipes with a serving size = size
DELIMITER $$
DROP PROCEDURE IF EXISTS getRecipesByServings$$

CREATE PROCEDURE getRecipesByServings(IN size INT) 
BEGIN
	SELECT rid, recipe_name, description, prep_time, cook_time, serving_size, cuisine, notes, user.first_name, instructions FROM recipe LEFT JOIN user ON author = uid 
    WHERE serving_size = size ORDER BY publish_date DESC;
END$$
DELIMITER ;

-- return all bookmarks for a user by uid
DELIMITER $$
DROP PROCEDURE IF EXISTS getBookmarksByUser$$

CREATE PROCEDURE getBookmarksByUser(IN id INT) 
BEGIN
	SELECT rid, recipe_name, prep_time, cook_time, serving_size, cuisine, user.first_name, instructions FROM bookmark 
	JOIN recipe ON bookmark.recipe = recipe.rid
    JOIN user ON recipe.author = user.uid
    WHERE bookmark.uid = id;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS getIngredients$$

CREATE PROCEDURE getIngredients(IN recipeId INT)
BEGIN
	SELECT ingredient.iid, amount, ingredient_name, rid FROM recipe_ingredient 
	JOIN ingredient ON recipe_ingredient.iid = ingredient.iid
    WHERE rid = recipeId;
END$$
DELIMITER ;

-- create a recipe
-- add to python code - add dietary restriction to all ing
-- we couldnt do a function returning sql_msg 

DELIMITER $$
DROP PROCEDURE IF EXISTS createRecipe$$

CREATE PROCEDURE createRecipe(r_name VARCHAR(64),
								r_prep_time INT,
								r_cook_time INT,
								r_serving_size INT,
								r_cuisine VARCHAR(16),
								r_instruct VARCHAR(1000),
								r_note VARCHAR(200),
								r_descrip VARCHAR(500),
                                r_author INT,
								r_course VARCHAR(16))
BEGIN 
	DECLARE course_id INT;
    DECLARE sql_error BOOL DEFAULT FALSE;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET sql_error = TRUE;
    
    START TRANSACTION;
    
    IF 
      (SELECT EXISTS(SELECT cid FROM course WHERE course_name = r_course)) -- course exists
    THEN 
      SET course_id = (SELECT cid FROM course WHERE course_name = r_course);
	ELSE
      INSERT INTO course (course_name) VALUES (r_course);
      SET course_id = (SELECT cid FROM course WHERE course_name = r_course);
	END IF;
    
    IF 
	  (SELECT EXISTS(SELECT recipe_name FROM recipe WHERE recipe_name = r_name))
	THEN 
		SET sql_error = TRUE;
	ELSE 
		INSERT INTO recipe (recipe_name, prep_time, cook_time, serving_size, 
		cuisine, instructions, notes, description, author, course) VALUES
		(r_name, r_prep_time, r_cook_time, r_serving_size,
		r_cuisine, r_instruct, r_note, r_descrip, r_author, course_id);
	END IF;

	IF sql_error = FALSE THEN
		COMMIT;
    ELSE
		ROLLBACK;
	END IF;
END $$
DELIMITER ;

/*
CALL createRecipe('No-Bake Chocolate Strawberry Coconut Bars', 20, 10, 8, 'American',
				'Line a 8x8 pan with a parchment paper with extra parchment hanging over the sides.',
				'something',
				'This delicious triple-layered chocolate strawberry coconut bar is no-bake, only uses 6 ingredients',
				1,
				'Breakfast');
*/

DELIMITER $$
DROP PROCEDURE IF EXISTS addIngredients$$

CREATE PROCEDURE addIngredients(recipe_id INT, 
								ingredient VARCHAR(32),
                                diet_rest INT,
                                amt VARCHAR(16))
BEGIN 
    DECLARE ing_id INT;
    DECLARE sql_error BOOL DEFAULT FALSE;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET sql_error = TRUE;
    
	START TRANSACTION;
    
	IF 
      (SELECT EXISTS(SELECT iid FROM ingredient WHERE ingredient_name = ingredient))
    THEN 
      SET ing_id = (SELECT iid FROM ingredient WHERE ingredient_name = ingredient);
	ELSE
      INSERT INTO ingredient (ingredient_name) VALUES (ingredient);
	  SET ing_id = (SELECT iid FROM ingredient WHERE ingredient_name = ingredient);
	END IF;
    
	IF NOT (SELECT EXISTS(SELECT drid FROM ingredient_follows 
		WHERE iid = ing_id AND drid = diet_rest))
	THEN 
		INSERT INTO ingredient_follows (iid, drid) VALUES (ing_id, diet_rest);
	END IF;
    
    IF NOT
		(SELECT EXISTS(SELECT iid FROM recipe_ingredient 
		WHERE ing_id = iid AND recipe_id = rid))
    THEN 
		INSERT INTO recipe_ingredient (rid, iid, amount) 
        VALUES (recipe_id, ing_id, amt);
	END IF;
    
	IF sql_error = FALSE THEN
		COMMIT;
    ELSE
		ROLLBACK;
	END IF;
END$$
DELIMITER ;

-- CALL addIngredients(1, 'salt and pepper', 1, 'a pinch');


-- create a user 
DELIMITER $$
DROP PROCEDURE IF EXISTS createUser$$

CREATE PROCEDURE createUser (user_first_name VARCHAR(16), 
							user_last_name VARCHAR(16),
							user_email VARCHAR(32),
							user_password VARCHAR(32))
BEGIN 
    DECLARE sql_error BOOL DEFAULT FALSE;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET sql_error = TRUE;
    
	START TRANSACTION;
    
	IF NOT
	  (SELECT EXISTS(SELECT uid FROM user WHERE email = user_email)) 
	THEN 
	  INSERT INTO user (first_name, last_name, email, password) VALUES 
		(user_first_name, user_last_name, user_email, user_password);
	END IF;
    
	IF sql_error = FALSE THEN
		COMMIT;
    ELSE
		ROLLBACK;
	END IF;
END$$
DELIMITER ;

-- CALL createUser('first1', 'last1', 'email@something.com1', 'pass1');

-- create bookmark for a user 

DELIMITER $$
DROP PROCEDURE IF EXISTS createBookmark$$

CREATE PROCEDURE createBookmark(recipe_id INT, user_id INT)
BEGIN 
    DECLARE sql_error BOOL DEFAULT FALSE;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET sql_error = TRUE;
    
	START TRANSACTION;
    
	IF NOT
	  (SELECT EXISTS(SELECT * FROM bookmark WHERE recipe_id = recipe AND user_id = uid))
	THEN 
      INSERT INTO bookmark (uid, recipe) VALUES (user_id, recipe_id);
	END IF;
    
	IF sql_error = FALSE THEN
		COMMIT;
    ELSE
		ROLLBACK;
	END IF;
END $$
DELIMITER ;

-- CALL createBookmark(1, 2);
-- CALL getBookmarksByUser(2);

-- trigger to delete the ingredient to recipe links
DELIMITER $$
DROP TRIGGER IF EXISTS recipe_ingredient_trigger$$
CREATE TRIGGER recipe_ingredient_trigger
	AFTER DELETE ON recipe
	FOR EACH ROW 
  BEGIN
    DELETE FROM recipe_ingredient 
    WHERE rid = old.rid;
  END$$
  
  -- trigger to delete the bookmarks links if deleted recipe
DELIMITER $$
DROP TRIGGER IF EXISTS bookmarks_trigger$$
CREATE TRIGGER bookmarks_trigger
	AFTER DELETE ON recipe
	FOR EACH ROW 
  BEGIN
    DELETE FROM bookmark
    WHERE recipe = old.rid;
  END$$

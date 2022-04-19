-- Procedures and functions for our recipe_index database
use recipe_index; 

DELIMITER $$
DROP PROCEDURE IF EXISTS getRecipeAuthor$$

CREATE PROCEDURE getRecipeAuthor(IN recipeId INT, OUT authorId INT) -- given a recipe id, returns the author id 
BEGIN
	SET authorId = (SELECT author FROM recipe WHERE rid = recipeId);
END$$

DELIMITER $$
DROP FUNCTION IF EXISTS isRecipeAuthor$$

CREATE FUNCTION isRecipeAuthor(recipeId INT, authorId INT) -- given a recipe id and an authorId returns true if author id 
RETURNS BOOL DETERMINISTIC
BEGIN
	DECLARE author INT;
    SET author = (SELECT author FROM recipe WHERE rid = recipeId);
    
	RETURN authorId = author; 
END$$


DELIMITER $$
DROP PROCEDURE IF EXISTS getRecipesByAuthor$$

CREATE PROCEDURE getRecipesByAuthor(IN authorId INT) -- return all recipes given the author id 
BEGIN
	SELECT * FROM recipe WHERE author = authorId ORDER BY publish_date DESC;
END$$

DELIMITER $$ 
DROP PROCEDURE IF EXISTS getRecipeByID $$

CREATE PROCEDURE getRecipeByID(IN rid INT)
BEGIN 
	SELECT * FROM recipe WHERE rid = rid;
END$$



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
		SELECT iid FROM recipe_ingredient WHERE rid = rid; -- returns all ingredients in the recipe
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

DELIMITER $$ 
DROP PROCEDURE IF EXISTS getRecipeByDietary $$

CREATE PROCEDURE getRecipeByDietary(IN drid INT) -- return all recipes given the drid
BEGIN 
	SELECT * FROM recipe WHERE recipeToDR(rid,drid);
END$$


-- return recipes of this course 
DELIMITER $$
DROP PROCEDURE IF EXISTS getRecipesByCourse$$

CREATE PROCEDURE getRecipesByCourse(IN recipe_course INT) 
BEGIN
	SELECT * FROM recipe WHERE course = recipe_course 
    ORDER BY publish_date DESC;
END$$

-- return recipes with a prep time less than the given
DELIMITER $$
DROP PROCEDURE IF EXISTS getRecipesByPrepTime$$

CREATE PROCEDURE getRecipesByPrepTime(IN prep_time_max INT) 
BEGIN
	SELECT * FROM recipe WHERE prep_time <= prep_time_max
    ORDER BY publish_date DESC;
END$$

-- return recipes with a cook time less than the given
DELIMITER $$
DROP PROCEDURE IF EXISTS getRecipesByCookTime$$

CREATE PROCEDURE getRecipesByCookTime(IN cook_time_max INT) 
BEGIN
	SELECT * FROM recipe WHERE cook_time <= cook_time_max
    ORDER BY publish_date DESC;
END$$

-- return recipes with a total time less than the given
DELIMITER $$
DROP PROCEDURE IF EXISTS getRecipesByCookTime$$

CREATE PROCEDURE getRecipesByTotalTime(IN time_max INT) 
BEGIN
	SELECT * FROM recipe WHERE (cook_time + prep_time) <= time_max -- idk if this works
    ORDER BY publish_date DESC;
END$$

-- return all bookmarks for a user by uid
DELIMITER $$
DROP PROCEDURE IF EXISTS getBookmarksByUser$$

CREATE PROCEDURE getBookmarksByUser(IN uid INT) 
BEGIN
	SELECT * FROM user WHERE uid = uid; 
END$$

-- create a recipe
-- add to python code - add dietary restriction to all ing
-- we couldnt do a function returning sql_msg 
DELIMITER $$
CREATE PROCEDURE createRecipe(r_name VARCHAR(64),
								prep_time INT,
								cook_time INT,
								serving_size INT,
								cuisine VARCHAR(16),
								instruct VARCHAR(1000),
								note VARCHAR(200),
								descrip VARCHAR(500),
                                author INT,
								recipe_course VARCHAR(16))
BEGIN 
	DECLARE course_id INT;
    DECLARE sql_msg VARCHAR(16);
    DECLARE sql_error BOOL DEFAULT FALSE;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET sql_error = TRUE;
    
    START TRANSACTION;
    
    IF 
      (SELECT EXISTS(SELECT cid FROM course WHERE course_name = recipe_course)) -- course exists
    THEN 
      SET course_id = (SELECT cid FROM course WHERE course_name = recipe_course);
	ELSE
      INSERT INTO course (course_name) VALUES (recipe_course);
      SET course_id = (SELECT cid FROM course WHERE course_name = recipe_course);
	END IF;
      
    IF 
	  (SELECT EXISTS(SELECT recipe_name FROM recipe WHERE recipe_name = rname)) 
	THEN 
		SET sql_error = TRUE;
--        SET @sql_msg = "Failed on recipe name";
	ELSE 
      INSERT INTO recipe (recipe_name, prep_time, cook_time, serving_size, 
    cuisine, instructions, notes, description, author, course) VALUES
	(r_name, prep_time, cook_time, serving_size,
    cuisine, instruct, note, descrip, author, course_id);
	END IF;

	IF sql_error = FALSE THEN
		COMMIT;
    ELSE
		ROLLBACK;
	END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE addIngredients(recipe_id INT, 
								ingredient VARCHAR(16),
                                diet_rest INT,
                                amt VARCHAR(16))
BEGIN 
    DECLARE ing_id INT;
	START TRANSACTION;
    
	IF 
      (SELECT EXISTS(SELECT iid FROM ingredient WHERE ingredient_name = ingredient))
    THEN 
      SET ing_id = (SELECT iid FROM ingredient WHERE ingredient_name = ingredient);
      
      IF NOT (SELECT EXISTS(SELECT drid FROM ingredient_follows 
					WHERE iid = ing_id AND drid = diet_rest))
	  THEN 
		INSERT INTO ingredient_follows (iid, drid) VALUES (ing_id, diet_rest);
	  END IF;
	ELSE
      INSERT INTO ingredient (ingredient_name) VALUES (ingredient);
	SET ing_id = (SELECT iid FROM ingredient WHERE ingredient_name = ingredient);
	END IF;
    
    IF NOT
		(SELECT EXISTS(SELECT iid FROM recipe_ingredient 
		WHERE ing_id = iid AND recipe_id = rid))
    THEN 
		INSERT INTO recipe_ingredient (rid, iid, amount) 
        VALUES (recipe_id, ing_id, amt);
	END IF;
END$$

-- create a user 

DELIMITER $$
CREATE PROCEDURE createUser (user_first_name VARCHAR(16), 
							user_last_name VARCHAR(16),
							user_email VARCHAR(32),
							user_password VARCHAR(32))
BEGIN 
	IF NOT
	  (SELECT EXISTS(SELECT uid FROM user WHERE email = user_email)) 
	THEN 
	  INSERT INTO user (first_name, last_name, email, password) VALUES 
		(user_first_name, user_last_name, user_email, user_password);
	END IF;
END$$

-- create bookmark for a user 

DELIMITER $$
CREATE PROCEDURE createBookmark(recipe_id INT, user_id INT)
BEGIN 
	IF NOT
	  (SELECT EXISTS(SELECT * FROM bookmark WHERE recipe_id = recipe AND user_id = uid))
	THEN 
      INSERT INTO bookmark (uid, recipe) VALUES (user_id, recipe_id);
	END IF;
END $$

-- get recipe by name 

DELIMITER $$
CREATE PROCEDURE getRecipeByName(rname VARCHAR(64))
BEGIN
	SELECT * FROM recipe WHERE recipe_name = rname;
END$$


-- trigger to delete the ingredient to recipe links
DELIMITER $$
CREATE TRIGGER recipe_ingredient_trigger
	AFTER DELETE ON recipe
	FOR EACH ROW 
  BEGIN
    DELETE FROM recipe_ingredient 
    WHERE rid = old.rid;
  END$$
  
  -- trigger to delete the bookmarks links if deleted recipe
DELIMITER $$
CREATE TRIGGER bookmarks_trigger
	AFTER DELETE ON recipe
	FOR EACH ROW 
  BEGIN
    DELETE FROM bookmarks 
    WHERE rid = old.rid;
  END$$

/**
CREATE READ UPDATE DETELE

CREATE
- recipe *
	- new ingredients on those recipes *
- new users *
	- new bookmarks for a user *

READ
- recipes *
- bookmarked recipes *

FILTER ON
- prep time *
- cook time *
- total time *
- dietary rest *
- course *
- recipe name *

UPDATE 
- authors can update their own recipes -- isRecipeAuthor can be used to test
- all users can update their own bookmarks 

DELETE 
- authors can delete their own recipes
- all users can delete their own bookmarks
**/

/**
TO DO:

1). Provide integrity constraints such as action to be performed for foreign keys  
ON DELETE, ON UPDATE clauses within the foreign keys in the tables. 
Also provide additional constraints on fields that are not part of the key
-- when we delete a recipe - create a trigger that updates the recipe ingredient table

2). Add starter values to tables and test calling the procedures

3). add more procedures and triggers
**/


















-- DROP DATABASE recipe_index;

CREATE DATABASE IF NOT EXISTS recipe_index;

USE recipe_index;

-- ingredient table
CREATE TABLE ingredient (
iid INT PRIMARY KEY AUTO_INCREMENT,
ingredient_name VARCHAR(16) NOT NULL CHECK (LENGTH(ingredient_name) > 0)
);

INSERT INTO ingredient(ingredient_name) VALUES ('egg(s)'),('half and half'),('salt and pepper'),('onion(s)'),('baby spinach'),('bacon'),('Swiss cheese'),('pie crust');

-- course table
CREATE TABLE course (
cid INT PRIMARY KEY AUTO_INCREMENT,
course_name VARCHAR(16) NOT NULL UNIQUE
);

INSERT INTO course(course_name) VALUES ('Breakfast'),('Lunch'),('Dinner'),('Dessert');

-- user table
CREATE TABLE user (
uid INT PRIMARY KEY AUTO_INCREMENT,
first_name VARCHAR(16) NOT NULL CHECK (LENGTH(first_name) > 0),
last_name VARCHAR(16) NOT NULL CHECK (LENGTH(last_name) > 0),
email VARCHAR(32) NOT NULL UNIQUE CHECK (INSTR(email , '@') > 0),
password VARCHAR(32) NOT NULL CHECK (LENGTH(password) >= 8)
);

INSERT INTO user(first_name,last_name,email,password) VALUES ('Laura','Calderon','calderon.l@northeastern.edu','password'),('Maria','Arandia','arandia.m@northeastern.edu','password');

CREATE TABLE recipe (
rid INT PRIMARY KEY AUTO_INCREMENT,
recipe_name VARCHAR(64) NOT NULL CHECK (LENGTH(recipe_name) > 0),
prep_time INT NOT NULL,
cook_time INT NOT NULL,
publish_date DATETIME NOT NULL DEFAULT now(), -- can we set this to default = now?
serving_size INT NOT NULL,
cuisine VARCHAR(16), -- if another table is needed 
instructions VARCHAR(1000) NOT NULL,
notes VARCHAR(200),
description VARCHAR(500),
author INT NOT NULL,
course INT NOT NULL,
	FOREIGN KEY (course) REFERENCES course(cid) ON UPDATE CASCADE,
    FOREIGN KEY (author) REFERENCES user(uid) ON UPDATE CASCADE -- only authors of their own recipe can delete or update their own
-- ingredients INT NOT NULL,
-- 	FOREIGN KEY (ingredients) REFERENCES recipe_ingredients(riid)
);

INSERT INTO recipe(recipe_name, prep_time, cook_time, serving_size, instructions, description, author, course)
	VALUES ('Spinach and Bacon Quiche', 10, 45, 12,
    '1. Preheat the oven to 375 degrees F. Roll out pie dough into a circle. Place in 9 inch pie dish and crimp edges.
	2. Blind bake crust: Place a piece of parchment paper inside the pie pan and add 2 cups of pie weights, dry beans or rice. 
    Bake at 375 degrees F for 15 minutes. Remove parchment paper and pie weights. Prick pie crust all over with a fork, then return to the oven for 8 more minutes.
	3. Meanwhile, cook bacon, in a skillet. Remove to a plate and chop. Remove most of the grease from the pan and add onion and spinach. 
    Saute for 2 minutes. Add cheese, onion, spinach, and bacon to the bottom of the partially baked pie crust.
	4. Combine the eggs, half and half, salt, and pepper in a blender, then pour the egg mixture into the pie.
	5. Reduce oven temperature to 350 degrees. Bake quiche for 40- 45 minutes until the egg is set. Allow to cool before slicing. 
    Store leftovers, covered, in the fridge.', 
    'This Spinach and Bacon Quiche is baked in a tender and flakey pie crust and is one of my favorites brunch on the weekends.', 
    1, 
    1);
    
UPDATE recipe SET instructions = '1. Preheat the oven to 375 degrees F. Roll out pie dough into a circle. Place in 9 inch pie dish and crimp edges.
	2. Blind bake crust: Place a piece of parchment paper inside the pie pan and add 2 cups of pie weights, dry beans or rice. 
    Bake at 375 degrees F for 15 minutes. Remove parchment paper and pie weights. Prick pie crust all over with a fork, then return to the oven for 8 more minutes.
	3. Meanwhile, cook bacon, in a skillet. Remove to a plate and chop. Remove most of the grease from the pan and add onion and spinach. 
    Saute for 2 minutes. Add cheese, onion, spinach, and bacon to the bottom of the partially baked pie crust.
	4. Combine the eggs, half and half, salt, and pepper in a blender, then pour the egg mixture into the pie.
	5. Reduce oven temperature to 350 degrees. Bake quiche for 40- 45 minutes until the egg is set. Allow to cool before slicing. 
    Store leftovers, covered, in the fridge.' WHERE rid = 4 AND author = 1;
    
SELECT * FROM recipe;
    
INSERT INTO recipe(recipe_name, prep_time, cook_time, serving_size, instructions, description, author, course)
Values ('Name', 10, 12, 14, 'instructions here....', 'description', 2, 2);
INSERT INTO recipe(recipe_name, prep_time, cook_time, serving_size, instructions, description, author, course)
Values ('Can only delete me', 80, 12, 5, 'instructions here....', 'description', 3, 4);

SELECT * FROM recipe;
SELECT * FROM ingredient;

CREATE TABLE recipe_ingredient (
rid INT NOT NULL, 
iid INT NOT NULL, 
amount VARCHAR(16) NOT NULL CHECK (LENGTH(amount) > 0), 
CONSTRAINT fk_recipe FOREIGN KEY(rid) REFERENCES recipe(rid) ON UPDATE CASCADE ON DELETE CASCADE, 
CONSTRAINT fk_ingredient FOREIGN KEY(iid) REFERENCES ingredient(iid) ON UPDATE CASCADE ON DELETE RESTRICT
);


-- dietary restriction to recipe table
CREATE TABLE dietary_restriction (
drid INT AUTO_INCREMENT PRIMARY KEY,
dr_name VARCHAR(16) NOT NULL,
descrip VARCHAR(200) NOT NULL
);
INSERT INTO dietary_restriction(dr_name, descrip) VALUES('-', 'none'),('V', 'vegan'),('GF', 'gluten free'),('VG', 'vegatarian'),('DF','dairy free'),('NF','nut free');

-- ingredient to dietary restriction table 
CREATE TABLE ingredient_follows (
iid INT NOT NULL,
drid INT NOT NULL,
PRIMARY KEY(iid, drid),
CONSTRAINT fk_ingredients FOREIGN KEY(iid) REFERENCES ingredient(iid) ON UPDATE CASCADE ON DELETE CASCADE,
CONSTRAINT fk_dietrestrict FOREIGN KEY(drid) REFERENCES dietary_restriction(drid) ON UPDATE CASCADE ON DELETE RESTRICT
);

SELECT * FROM ingredient_follows;

-- bookmark recipes to user 
CREATE TABLE bookmark (
uid INT, 
recipe INT, 
FOREIGN KEY (uid) REFERENCES user(uid) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY (recipe) REFERENCES recipe(rid) ON UPDATE CASCADE ON DELETE CASCADE,
PRIMARY KEY (uid, recipe)
);

SELECT * FROM recipe;
SELECT * FROM course;
SELECT * FROM ingredient;
SELECT * FROM recipe_ingredient;
SELECT * FROM ingredient_follows;
SELECT * FROM dietary_restriction;

SELECT * FROM user;
SELECT * FROM bookmark;
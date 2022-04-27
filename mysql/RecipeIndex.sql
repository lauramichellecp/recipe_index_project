DROP DATABASE recipe_index;

CREATE DATABASE IF NOT EXISTS recipe_index;

USE recipe_index;

-- ingredient table
CREATE TABLE ingredient (
iid INT PRIMARY KEY AUTO_INCREMENT,
ingredient_name VARCHAR(16) NOT NULL CHECK (LENGTH(ingredient_name) > 0)
);

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
publish_date DATETIME NOT NULL DEFAULT now(),
serving_size INT NOT NULL,
cuisine VARCHAR(16), 
instructions VARCHAR(1000) NOT NULL,
notes VARCHAR(200),
description VARCHAR(500),
author INT NOT NULL,
course INT NOT NULL,
	FOREIGN KEY (course) REFERENCES course(cid) ON UPDATE CASCADE,
    FOREIGN KEY (author) REFERENCES user(uid) ON UPDATE CASCADE 
);

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

-- bookmark recipes to user 
CREATE TABLE bookmark (
uid INT, 
recipe INT, 
FOREIGN KEY (uid) REFERENCES user(uid) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY (recipe) REFERENCES recipe(rid) ON UPDATE CASCADE ON DELETE CASCADE,
PRIMARY KEY (uid, recipe)
);


DROP DATABASE recipe_index;

CREATE DATABASE IF NOT EXISTS recipe_index;

USE recipe_index;

-- ingredient table
CREATE TABLE ingredient (
iid INT PRIMARY KEY AUTO_INCREMENT,
ingredient_name VARCHAR(16) NOT NULL
);

-- course table
CREATE TABLE course (
cid INT PRIMARY KEY AUTO_INCREMENT,
course_name VARCHAR(16) NOT NULL UNIQUE
);

-- user table
CREATE TABLE user (
uid INT PRIMARY KEY AUTO_INCREMENT,
first_name VARCHAR(16) NOT NULL,
last_name VARCHAR(16) NOT NULL,
email VARCHAR(32) NOT NULL UNIQUE,
password VARCHAR(32) NOT NULL
);

CREATE TABLE recipe (
rid INT PRIMARY KEY AUTO_INCREMENT,
recipe_name VARCHAR(64) NOT NULL,
prep_time INT NOT NULL,
cook_time INT NOT NULL,
publish_date DATE NOT NULL DEFAULT (CURDATE()), -- can we set this to default = now?
serving_size INT NOT NULL,
cuisine VARCHAR(16), -- if another table is needed 
instructions VARCHAR(1000) NOT NULL,
notes VARCHAR(200),
description VARCHAR(500),
author INT NOT NULL,
course INT NOT NULL,
	FOREIGN KEY (course) REFERENCES course(cid),
    FOREIGN KEY (author) REFERENCES user(uid)  -- only authors of their own recipe can delete or update their own
-- ingredients INT NOT NULL,
-- 	FOREIGN KEY (ingredients) REFERENCES recipe_ingredients(riid)
);

CREATE TABLE recipe_ingredient (
rid INT NOT NULL, 
iid INT NOT NULL, 
amount VARCHAR(16) NOT NULL, 
CONSTRAINT fk_recipe FOREIGN KEY(rid) REFERENCES recipe(rid), 
CONSTRAINT fk_ingredient FOREIGN KEY(iid) REFERENCES ingredient(iid)
);


-- dietary restriction to recipe table
CREATE TABLE dietary_restriction (
drid INT AUTO_INCREMENT PRIMARY KEY,
dr_name VARCHAR(16) NOT NULL,
descrip VARCHAR(200) NOT NULL
);

-- ingredient to dietary restriction table 
CREATE TABLE ingredient_follows (
iid INT NOT NULL,
drid INT NOT NULL,
PRIMARY KEY(iid, drid),
CONSTRAINT fk_ingredients FOREIGN KEY(iid) REFERENCES ingredient(iid),
CONSTRAINT fk_dietrestrict FOREIGN KEY(drid) REFERENCES dietary_restriction(drid)
);

-- bookmark recipes to user 
CREATE TABLE bookmark (
uid INT, 
recipe INT, 
FOREIGN KEY (uid) REFERENCES user(uid),
FOREIGN KEY (recipe) REFERENCES recipe(rid),
PRIMARY KEY (uid, recipe)
);





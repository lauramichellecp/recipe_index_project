use recipe_index;

-- SPAGHETTI AND MEATBALL RECIPE

call recipe_index.createRecipe('Spaghetti and Meatballs', 20, 40, 4, 'Italian', '1. In a large pot of salted boiling water, cook pasta until al dente. Drain.
2. In a large bowl, combine beef with bread crumbs, parsley, Parmesan, egg, garlic, 1 teaspoon salt, and red pepper flakes. Mix until just combined then form into 16 balls.
3. In a large pot over medium heat, heat oil. Add meatballs and cook, turning occasionally, until browned on all sides, about 10 minutes. Transfer meatballs to a plate.
4. Add onion to pot and cook until soft, 5 minutes. Add crushed tomatoes and bay leaf. Season with salt and pepper and bring to a simmer. Return meatballs to pot and cover. Simmer until sauce has thickened, 8 to 10 minutes.
5. Serve pasta with a healthy scoop of meatballs and sauce. Top with Parmesan before serving.
', ' For an even speedier dinner, you can totally go with jarred marinara sauce.', "If you're looking for a super simple, comforting, no-frills bowl of spaghetti and meatballs, you've come to the right place. 
And if you're feeling adventurous, it's also a great jumping off point for your own version of this classic dish!", 2, 'Dinner');

SELECT * FROM user;
SELECT * FROM recipe;
SELECT * FROM ingredient;
SELECT * FROM recipe_ingredient;
SELECT * FROM dietary_restriction;

call recipe_index.addIngredients(1, 'spaghetti', 1, '1 Ib');
call recipe_index.addIngredients(1, 'ground beef', 1, '1 Ib');
call recipe_index.addIngredients(1, 'bread crumbs', 1, '1/3 cup');
call recipe_index.addIngredients(1, 'egg(s)', 1, 'one');
call recipe_index.addIngredients(1, 'garlic clove', 1, '2 minced');
call recipe_index.addIngredients(1, 'salt and pepper', 1, 'one tsp');
call recipe_index.addIngredients(1, 'redpepper flakes', 1, '1/2 tsp');
call recipe_index.addIngredients(1, 'crushed tomatoes', 1, '28 oz');
call recipe_index.addIngredients(1, 'bay leaf', 1, '1');

-- THE PERFECT MILKSHAKE

CALL createRecipe('The Perfect Milkshake', 5, 0, 2, 'American', '1. In a blender, blend together ice cream and milk. 2. Pour into a glass and garnish with whipped 
topping, sprinkles, and a cherry.', 'Add your ice cream and milk to a large bowl and blend with a spatula if you dont have blender', 'This easy milkshake recipe 
gives you the perfect ratio of milk to ice cream and is completely customizable!', 2, 'Dessert');

call recipe_index.addIngredients(2, 'ice cream', 1, '4 scoops');
call recipe_index.addIngredients(2, 'milk', 1, '1/4 cup');
call recipe_index.addIngredients(2, 'whipped topping', 1, 'for garnish');
call recipe_index.addIngredients(2, 'sprinkles', 1, 'for garnish');
call recipe_index.addIngredients(2, 'cherry', 1, 'for garnish');

 -- Tuscan Chicken Pasta 

CALL recipe_index.createRecipe('Tuscan Chicken Pasta', 20, 25, 4, 'Italian',
'1. In a large pot of salted boiling water, cook pasta according to package directions until al dente. Drain,
reserving 1 cup pasta water. 
2. Meanwhile, in a large skillet over medium-high heat, heat oil. Season chicken with salt and pepper and cook until golden and no longer pink inside, about 8 minutes per side. Let rest 
10 minutes, then thinly slice. 
3. Meanwhile, in same skillet, cook bacon over medium heat until crispy, 8 minutes.
Drain on a paper towel–lined plate, then chop. Pour off half of fat from skillet. 
4. Add garlic, tomatoes, and spinach to skillet and cook over medium heat until fragrant and slightly wilted, 2 minutes. 
Season with salt and pepper, then add heavy cream, Parmesan, and 1/2 cup of reserved pasta water. Simmer 5 minutes.
5. Add cooked pasta and toss until fully coated, then add chicken and bacon and toss until combined.
6. Garnish with basil before serving', 'Feel free to use either spaghetti or angel hair ', 
'Loaded with sautéed chicken breasts and crispy bacon, this hearty spaghetti recipe will please even the pickiest eaters.',
2, 'Dinner');

call recipe_index.addIngredients(3, 'spaghetti', 1, '12 oz');
call recipe_index.addIngredients(3, 'salt and pepper', 1, '1 tsp');
call recipe_index.addIngredients(3, 'olive oil', 1, '1 tbsp');
call recipe_index.addIngredients(3, 'boneless chicken', 1, '3 breasts');
call recipe_index.addIngredients(3, 'bacon', 1, '6 slices');
call recipe_index.addIngredients(3, 'garlic clove', 1, '2 minced');
call recipe_index.addIngredients(3, 'diced tomatoes', 1, '2 c');
call recipe_index.addIngredients(3, 'dried oregano', 1, '1 tsp');
call recipe_index.addIngredients(3, 'baby spinach', 1, '3 cups');
call recipe_index.addIngredients(3, 'heavy cream', 1, '1/2 cup');
call recipe_index.addIngredients(3, 'parmesan', 1, '1/3 cup');
call recipe_index.addIngredients(3, 'basil', 1, 'for garnish');

-- STICKY AND SPICY BAKED CAULIFLOWER
-- diet 2
CALL recipe_index.createRecipe('Sticky and Spicy Baked Cauliflower', 10, 40, 4, 'Vegan', 
'1. Preheat oven to 400°. Whisk flour, cornstarch, baking powder, and salt in a large bowl to combine. Whisk in 1 cup water to create a thin pancake-like batter. 
Using your hand or 2 forks and working one at a time, dip cauliflower florets into batter, letting excess drip back into bowl, and divide in 2 sheets. 
Bake cauliflower until edges are just beginning to turn golden brown, 20–25 minutes.
2. Meanwhile, whisk gochujang, soy sauce, maple syrup, mirin, and 1 cup water in a medium bowl. Pour sauce into a skillet large enough to hold all of the cauliflower 
florets & bring to a simmer over medium heat, whisking occasionally. Cook, whisking, until sauce is thick enough to coat a spoon, 8–10 minutes. 
Stir in vinegar and remove pan from heat.
3. Using tongs, transfer cauliflower to skillet with glaze and toss until florets are evenly coated in sauce.
4. Divide rice among shallow bowls and spoon cauliflower over. Top with sesame seeds and scallions.',
'', 
'No need to deal with a pot of hot oil to get crispy battered cauliflower. 
These oven-baked florets come out crackly and just rich enough before getting 
bathed in a sticky-sweet gochujang glaze.', 1, 'Dinner');

call recipe_index.addIngredients(4, 'flour', 2, '1 cup');
call recipe_index.addIngredients(4, 'cornstarch', 2, '1/2 cup');
call recipe_index.addIngredients(4, 'baking powder', 2, '2 tsp');
call recipe_index.addIngredients(4, 'salt and pepper', 2, '1 tsp');
call recipe_index.addIngredients(4, 'cauliflower', 2, '1 head');
call recipe_index.addIngredients(4, 'gochujang', 2, '1/4 cup');
call recipe_index.addIngredients(4, 'soy sauce', 2, '3 Tbsp');
call recipe_index.addIngredients(4, 'maple syrup', 2, '2 Tbsp');
call recipe_index.addIngredients(4, 'mirin', 2, '2 Tbsp');
call recipe_index.addIngredients(4, 'rice vinegar', 2, '2 tsp');

-- Air Fryer Chicken Parmesan

CALL recipe_index.createRecipe('Air Fryer Chicken Parmesan', 10, 50, 4, 'Italian', 
'Carefully butterfly chicken by cutting in half widthwise to create 4 thin pieces of chicken. 
Season both sides with salt and pepper. Prepare dredging station: Place flour in a shallow bowl 
and season with a large pinch of salt and pepper. Place eggs in a second bowl and beat until smooth. 
In a third bowl, combine bread crumbs, Parmesan, oregano, garlic powder, and red pepper flakes. 
Working with one piece of a chicken at a time, coat in flour and shake off excess, dip in eggs, 
then finally press into panko mixture, making sure both sides are coated well. 
Placing in a single layer and working in batches as necessary, add chicken to basket of air fryer 
and cook at 400° for 5 minutes on each side. Top chicken with sauce and mozzarella and cook at 400°
 until cheese is melty and golden, about 3 minutes. 5. Garnish with parsley before serving', 
'The air fryer will even melt and broil your cheese for a perfectly cheesy, crispy bite!',
'An easier take than using the oven', 1, 'Dinner');

call recipe_index.addIngredients(5, 'boneless chicken', 1, '2 breasts');
call recipe_index.addIngredients(5, 'salt and pepper', 1, '1 tsp');
call recipe_index.addIngredients(5, 'flour', 1, '1/3 cup');
call recipe_index.addIngredients(5, 'egg(s)', 1, '2');
call recipe_index.addIngredients(5, 'breadcrumbs', 1, '1 cup');
call recipe_index.addIngredients(5, 'garlic powder', 1, '1/2 tsp');
call recipe_index.addIngredients(5, 'parmesan', 1, '1/4 cup');
call recipe_index.addIngredients(5, 'dried oregano', 1, '1 tsp');
call recipe_index.addIngredients(5, 'salt and pepper', 1, 'one tsp');
call recipe_index.addIngredients(5, 'red pepper flakes', 1, '1/2 tsp');
call recipe_index.addIngredients(5, 'marinara sauce', 1, '1 cup');
call recipe_index.addIngredients(5, 'parsley', 1, 'chopped');
call recipe_index.addIngredients(5, 'mozzarella', 1, '1 cup');

-- Crispy Hashbrowns

CALL recipe_index.createRecipe('Crispy Hash Browns', 15, 20, 4, 'American',
'1. Grate potatoes using the large hoes of a box grater.
2. Using a clean dish towel or cheese cloth, drain potatoes completely
3. Transfer potatoes to a large bowl. Stir in garlic and onion powder; season with salt and pepper
4. Heat 2 tablespoons canola oil in a 12-inch cast iton skillet over medium heat
5. Working in batches, spread potatoes in a single layer and cook, undisturbed until golden brown. 
Flip and cook on the other side unti evenly golden and crispy. 
6. Serve immediately', 'Serve with ketchup or hot sauce', 'Quick, easy, and SO INCREDIBLY CRISPY!', 
2, 'Breakfast');

call recipe_index.addIngredients(6, 'russet potatoes', 4, '1/4 Ibs');
call recipe_index.addIngredients(6, 'garlic powder', 4, '1/4 tsp');
call recipe_index.addIngredients(6, 'onion powder', 4, '1/4 tbsp');
call recipe_index.addIngredients(6, 'canola oil', 4, '4 Tbsp');
call recipe_index.addIngredients(6, 'salt and pepper', 4, 'to taste');


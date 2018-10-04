"""
data_provider_service defines the class that contains the api called by the middleware
"""
import hashlib

from Models import Recipe
from Models import DataGenerator


class DataProviderService:
    def __init__(self):
        """
        :return: None
        """
        self.data_generator = DataGenerator()
        self.RECIPES = self.data_generator.generate_recipes()

    def add_recipe(self, name, category, amt, targets, ingredients, instructions):
        """
        Creates and saves a new recipe to the database.

        :param name: Name of recipe
        :param category: Category the recipe belongs to
        :param amt: Volume in US gallons
        :param instructions: Instructions to make the recipe
        :return: The id of the new recipe
        """

        new_recipe = Recipe(name=name,
                            category=category,
                            amt=amt,
                            targets=targets,
                            ingredients=ingredients,
                            instructions=instructions)
        self.RECIPES.append(new_recipe)

        return new_recipe.id

    def get_recipe(self, id=None, serialize=False):
        """
        If the id parameter is  defined then it looks up the recipe with the given id,
        otherwise it loads all the recipes

        :param id: The id of the recipe which needs to be loaded, when None it
            returns all recipes (default value is None)
        :return: The recipe or recipes.
        """
        all_recipes = []

        if id is None:
            all_recipes = self.RECIPES
        else:
            for recipe in self.RECIPES:
                if id == str(recipe.id):
                    all_recipes = [recipe]
                    break

        if serialize:
            return [recipe.serialize() for recipe in all_recipes]
        else:
            return all_recipes

    def update_recipe(self, id, new_recipe):
        """
        Update an existing recipe.

        :param id: The id of the recipe that is to be updated
        :param new_recipe: The new recipe
        :return: serialized version of the new recipe or None if no
            recipe was found for id.
        """
        updated_recipe = None
        recipes = self.get_recipe(id)
        recipe = None
        if len(recipes) is not 1:
            return updated_recipe
        else:
            recipe = recipes[0]

        if recipe:
            recipe.name = new_recipe["name"]
            recipe.category = new_recipe["category"]
            recipe.amt = new_recipe["amt"]
            recipe.targets = new_recipe["targets"]
            recipe.ingredients = new_recipe["ingredients"]
            recipe.instructions = new_recipe["instructions"]
            updated_recipe = self.get_recipe(id)[0]

        return updated_recipe.serialize()


    def delete_recipe(self, id):
        """
        Delete a recipe from the list.

        :param id: Id of recipe to delete
        :return: True when recipe is deleted
                 False if recipe was not found
        """
        recipe_for_delete = None
        for recipe in self.RECIPES:
            if id == str(recipe.id):
                recipe_for_delete = recipe
                break

        if recipe_for_delete is not None:
            self.RECIPES.remove(recipe_for_delete)
            return True
        else:
            return False


    def fill_database(self):
        pass
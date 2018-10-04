"""
middleware defines the api called by routes to wrap the data provider calls so it can provide
sensible responses back to routes.
"""
import hashlib
import json

from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for

from math import ceil

from data_provider_service import DataProviderService

PAGE_SIZE = 2

DATA_PROVIDER = DataProviderService()


def recipe(serialize = True):
    """
    Retrieve all recipes.

    :param serialize: True - the return structure will be serialized
                      False - the return will be a list of recipe objects (used for generated web pages)
    :return: list of recipes (serialized depending on the serialize value)
    """
    recipes = DATA_PROVIDER.get_recipe(serialize=True)
    page = request.args.get("page")

    if page:
        nr_of_pages = int(ceil(float(len(recipes)) / PAGE_SIZE))
        converted_page = int(page)
        if converted_page > nr_of_pages or converted_page < 0:
            return make_response("", 404)

        from_idx = converted_page * PAGE_SIZE - 1
        stop_idx = from_idx + PAGE_SIZE

        recipes = recipes[from_idx:stop_idx]

    if serialize:
        data = {"recipes": recipes, "total": len(recipes)}
        json_data = json.dumps(data)
        response = make_response(jsonify(data), 200)
        response.headers["ETag"] = str(hashlib.sha256(json_data.encode('utf-8')).hexdigest())
        response.headers["Cache-Control"] = "private, max-age=300"
        return response
    else:
        return recipes

def recipe_by_id(id):
    """
    Return a recipe by id
    :param id: Id of recipe to return
    :return: serialized recipe object
    """
    current_recipe = DATA_PROVIDER.get_recipe(id, serialize=True)
    if current_recipe:
        return jsonify({"recipe": current_recipe})
    else:
        #
        # In case we did not find the recipe by id
        # we send HTTP 404 - Not Found error to the client
        #
        abort(404)


def fill_database():
    """
    Call data provider service to fill the database (recipe list) with more known recipes.
    :return: None
    """
    DATA_PROVIDER.fill_database()


def delete_recipe(id):
    """
    Delete recipe with given id
    :param id: id of recipe to delete
    :return: response 200 - when successful
             response 404 - when id could not be found
             response 500 - when deletion experienced an exception
    """
    try:
        if DATA_PROVIDER.delete_recipe(id):
            return make_response("", 200)
        else:
            return make_response("", 404)
    except ValueError as err:
        tmp_response = make_response("", 500)
        tmp_response.headers["X-APP-ERROR-CODE"] = get_error_code(err)
        tmp_response.headers["X-APP-ERROR-MESSAGE"] = err.message
        return tmp_response


def get_error_code(error):
    if "parameter" in error.message.lower():
        return 9100

    return 9000

def update_recipe(id):
    """
    update recipe with id
    :param id: id of recipe to update
    :return: serialized recipe if id found
             response 404 if id not found
    """
    new_recipe = {
        "name":request.form["name"],
        "category":request.form["category"],
        "amt": request.form["amt"],
        "targets": request.form["targets"],
        "ingredients": request.form["ingredients"],
        "instructions": request.form["instructions"]
    }
    updated_recipe = DATA_PROVIDER.update_recipe(id, new_recipe)
    if not updated_recipe:
        return make_response('', 404)
    else:
        return jsonify({"recipe": updated_recipe})


def add_recipe():
    """
    add recipe from input form via the request object
    :return: serialized new recipe id and url for recipe_by_id
    """
    name = request.form["name"]
    category = request.form["category"]
    amt = request.form["amt"]
    targets = request.form["targets"]
    ingredients = request.form["ingredients"]
    instructions = request.form["instructions"]

    new_recipe_id = DATA_PROVIDER.add_recipe(name=name,
                                             category=category,
                                             amt=amt,
                                             targets=targets,
                                             ingredients=ingredients,
                                             instructions=instructions)
    return jsonify({
        "id": new_recipe_id,
        "url": url_for("recipe_by_id", id=new_recipe_id)
    })


def build_message(key, message):
    return {key:message}

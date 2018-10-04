"""
routes sets up all the routing of api and web calls
"""
from flask import jsonify
from flask import render_template
from flask import flash
from flask import current_app
from flask import make_response
from flask import abort
from flask import request

from middleware import recipe_by_id
from middleware import recipe
from middleware import add_recipe
from middleware import update_recipe
from middleware import delete_recipe
from middleware import fill_database as fill_db
from middleware import build_message

# Functions used for API
def init_api_routes(app):
    """
    Initialize routes for Rest API

    :param app: flask app object
    :return: None
    """
    if app:
        app.add_url_rule('/api/recipes/<string:id>', 'recipe_by_id', recipe_by_id, methods=['GET'])
        app.add_url_rule('/api/recipes', 'recipe', recipe, methods=['GET'])
        app.add_url_rule('/api/recipes', 'add_recipe', add_recipe, methods=['POST'])
        app.add_url_rule('/api/recipes/<string:id>', 'update_recipe', update_recipe, methods=['PUT'])
        app.add_url_rule('/api/recipes/<string:id>', 'delete_recipe', delete_recipe, methods=['DELETE'])
        app.add_url_rule('/api/filldb', 'filldb', fill_database)
        app.add_url_rule('/api', 'list_routes', list_routes, methods=['GET'], defaults={'app': app})


def fill_database():
    """
    Api to fill database with more known values
    :return: return message
    """
    message_key = "Fill Database"
    try:
        fill_db()
    except ValueError as err:
        return jsonify(build_message(message_key, err.message))

    return jsonify(build_message(message_key, "OK"))


def list_routes(app):
    """
    List routes available for Rest API calls
    :param app: flask app object
    :return: List of routes and total number of routes
    """
    result = []
    for rt in app.url_map.iter_rules():
        result.append({
            'methods': list(rt.methods),
            'route': str(rt)
        })
    return jsonify({'routes': result, 'total': len(result)})


# Functions used for webpages

def page_about(*args, **kwargs):
    if current_app:
        flash('The application was loaded', 'info')
        flash('The secret key is {0}'.format(current_app.config['SECRET_KEY']), 'info')

    resp = make_response(render_template('about.html', selected_menu_item="about"))
    return resp

def page_recipe():
    my_cookie = request.cookies.get('myCookie')
    print('COOKIE FROM THE CLIENT:' + my_cookie)
    current_recipes = recipe(serialize=False)
    return render_template('recipe.html', selected_menu_item="recipe", recipes=current_recipes)


def page_add_recipe():
    return render_template('add_recipe.html', selected_menu_item="recipe")


def page_index():
    resp = make_response(render_template('index.html', selected_menu_item="index"))
    resp.set_cookie('myCookie','this is a custom cookie sent from the server')
    return resp


def crash_server():
    abort(500)


def init_website_routes(app):
    """
    Initialize the routes to the webpages
    :param app: flask app object
    :return: None
    """
    if app:
        app.add_url_rule('/crash', 'crash_server', crash_server, methods=['GET'])
        app.add_url_rule('/about', 'page_about', page_about, methods=['GET'])
        app.add_url_rule('/recipe', 'page_recipe', page_recipe, methods=['GET'])
        app.add_url_rule('/recipe/add', 'page_add_recipe', page_add_recipe, methods=['GET'])
        app.add_url_rule('/', 'page_index', page_index, methods=['GET'])


def handle_error_404(error):
    flash('Server says: {0}'.format(error), 'error')
    return render_template('404.html', selected_menu_item=None)


def handle_error_500(error):
    flash('Server says: {0}'.format(error), 'error')
    return render_template('500.html', selected_menu_item=None)


def init_error_handlers(app):
    if app:
        app.error_handler_spec[404] = handle_error_404
        app.error_handler_spec[500] = handle_error_500



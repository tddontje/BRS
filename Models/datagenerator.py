"""
DataGenerator class to bootstrap the recipe list with a known set of recipes.
"""
from Models.Recipe import Recipe

class DataGenerator:
    initial_recipes = [ ['Pauwel Kwak',
                         'Belgium-Style Strong Ale',
                         5.0,
                        {'OG': 1.079,
                         'FG': 1.014,
                         'ABV': 8.0,
                         'Color': 14,
                         'BU': 15},
                        {'Pilsner Malt': [5.0, 'lbs'],
                         'Belgian Munich Malt': [10.0, 'lbs'],
                         'English Challenger Hops (Bittering)': [3, 'HBU'],
                         'European Styrian Goldings hops (Aroma)': [2.5, 'HBU'],
                         'Czech Saaz Hops (Aroma)': [1, 'HBU'],
                         'Irish Moss': [.25, 'tsp'],
                         'Corn Sugar': [.75, 'cups'],
                         'Wyeast 1214 Belgian Ale': [1, 'pkt']},
                        "Instructions Here..."],
                       ['Old Rasputin Russian Imperial Stout',
                        'Imperial Stout',
                        5.0,
                        {'OG': 1.090,
                         'FG': 1.018,
                         'ABV': 9.2,
                         'Color': 'Black',
                         'BU': 55},
                        {'American 2-row Malt': [13.5, 'lbs'],
                         'English Crystal Malt': [1.5, 'lbs'],
                         'American Victory Malt': [.75, 'lbs'],
                         'English Chocolate Malt': [1.25, 'lbs'],
                         'English Roasted Malt': [1.0, 'lbs'],
                         'English Black Malt': [.5, 'lbs'],
                         'English Brown Malt': [2.5, 'lbs'],
                         'Cluster Hops (Bittering)': [14, 'HBU'],
                         'American Centinnial hops (Bittering)': [5, 'HBU'],
                         'American Liberty Hops (flavor)': [6, 'HBU'],
                         'American Northern Brewer Hops (flavor)': [4, 'HBU'],
                         'American Liberty Hops (aroma)': [1.5, 'oz'],
                         'Irish Moss': [.25, 'tsp'],
                         'Corn Sugar': [.75, 'cups'],
                         'Wyeast 1272 American Ale II': [1, 'pkt']},
                        'Instructions here...']
                    ]

    def __init__(self):
        pass

    def generate_recipes(self):
        """
        Generate recipes from a the initial recipes list above

        :return: list of recipe objects
        """
        result = []

        for rcp in self.initial_recipes:
            recipe = Recipe(rcp[0], rcp[1], rcp[2],
                            rcp[3], rcp[4], rcp[5])
            result.append(recipe)

        return [rcp for rcp in result]

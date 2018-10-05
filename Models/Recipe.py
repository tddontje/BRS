"""
Data Model for Recipe class
"""
from pyld import jsonld
import uuid

class Recipe:
    __id = None
    __name = ''                 # Name of Recipe
    __category = ''             # Category of Beer
    __amt = 0.0                 # Volume produced by recipe in U.S. Gallons
    __targets = {               # Target Values of Recipe (what is expected)
                 'OG': 0.0,     # Original Gravity (in Bailing)
                 'FG': 0.0,     # Finish Gravity (in Bailing)
                 'ABV': 0.00,   # Alcohol by Volume
                 'Color': 0,    # Color in SRM
                 'BU': 0}       # Bittering Units
    __ingredients = None        # This is a dictionary of ingredients in which each entry is
                                #  a 2 entry list with measurement type and amount
                                #  {'ingredient': ('measurement', amt), ...}
    __instructions = ""         # Written recipe instruction

    def __init__(self, name, category, amt, targets, ingredients, instructions):
        self.__id = uuid.uuid4()
        self.name = name
        self.category = category
        self.amt = amt
        self.targets = targets
        self.ingredients = ingredients
        self.instructions = instructions

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, value):
        self.__category = value

    @property
    def amt(self):
        return self.__amt

    @amt.setter
    def amt(self, value):
        self.__amt = value

    @property
    def targets(self):
        return self.__targets

    @targets.setter
    def targets(self, value):
        self.__targets = value

    @property
    def ingredients(self):
        return self.__ingredients

    @ingredients.setter
    def ingredients(self, value):
        self.__ingredients = value

    @property
    def instructions(self):
        return self.__instructions

    @instructions.setter
    def instructions(self, value):
        self.__instructions = value

    #
    # METHODS
    #

    def serialize(self):
        return {"id": str(self.id),
		"name": self.name,
		"category": self.category,
		"amt": self.amt,
		"targets": self.targets,
		"ingredients": self.ingredients,
		"instructions": self.instructions}


"""Recipe scaling and unit conversion utilities."""

from recipe import Recipe


# Conversion factors to a base unit (milliliters for volume, grams for weight)
VOLUME_CONVERSIONS = {
    "ml": 1,
    "milliliter": 1,
    "milliliters": 1,
    "l": 1000,
    "liter": 1000,
    "liters": 1000,
    "tsp": 4.929,
    "teaspoon": 4.929,
    "teaspoons": 4.929,
    "tbsp": 14.787,
    "tablespoon": 14.787,
    "tablespoons": 14.787,
    "cup": 236.588,
    "cups": 236.588,
    "fl oz": 29.574,
    "fluid ounce": 29.574,
    "fluid ounces": 29.574,
}

WEIGHT_CONVERSIONS = {
    "g": 1,
    "gram": 1,
    "grams": 1,
    "kg": 1000,
    "kilogram": 1000,
    "kilograms": 1000,
    "oz": 28.3495,
    "ounce": 28.3495,
    "ounces": 28.3495,
    "lb": 453.592,
    "pound": 453.592,
    "pounds": 453.592,
}


def scale_recipe(recipe, new_servings):
    """
    Scale a recipe to a new number of servings.
    Returns a new Recipe object with scaled ingredients.
    """
    if recipe.servings == 0:
        scale_factor = 1
    else:
        scale_factor = new_servings / recipe.servings

    scaled_ingredients = []
    for ing in recipe.ingredients:
        scaled_ing = ing.copy()
        if isinstance(ing.get("amount"), (int, float)):
            scaled_ing["amount"] = round(ing["amount"] * scale_factor, 2)
        scaled_ingredients.append(scaled_ing)

    return Recipe(
        name=recipe.name,
        ingredients=scaled_ingredients,
        instructions=recipe.instructions,
        prep_time=recipe.prep_time,
        cook_time=recipe.cook_time,
        servings=new_servings,
        category=recipe.category
    )


def convert_unit(amount, from_unit, to_unit):
    """
    Convert an amount from one unit to another.
    Returns the converted amount, or None if conversion not possible.
    """
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    # Check volume conversions
    if from_unit in VOLUME_CONVERSIONS and to_unit in VOLUME_CONVERSIONS:
        base_amount = amount * VOLUME_CONVERSIONS[from_unit]
        return round(base_amount / VOLUME_CONVERSIONS[to_unit], 3)

    # Check weight conversions
    if from_unit in WEIGHT_CONVERSIONS and to_unit in WEIGHT_CONVERSIONS:
        base_amount = amount * WEIGHT_CONVERSIONS[from_unit]
        return round(base_amount / WEIGHT_CONVERSIONS[to_unit], 3)

    return None


def get_supported_units():
    """Return a dict of supported unit types and their units."""
    return {
        "volume": list(set(VOLUME_CONVERSIONS.keys())),
        "weight": list(set(WEIGHT_CONVERSIONS.keys()))
    }

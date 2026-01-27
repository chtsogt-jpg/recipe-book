"""Search functionality for recipes."""

from storage import load_recipes


def search_by_name(query):
    """Find recipes whose name contains the query string."""
    recipes = load_recipes()
    query = query.lower()
    return [r for r in recipes if query in r.name.lower()]


def search_by_ingredient(ingredient):
    """Find recipes that contain a specific ingredient."""
    recipes = load_recipes()
    ingredient = ingredient.lower()
    results = []

    for recipe in recipes:
        for ing in recipe.ingredients:
            if ingredient in ing["item"].lower():
                results.append(recipe)
                break

    return results


def search_by_category(category):
    """Find recipes in a specific category."""
    recipes = load_recipes()
    category = category.lower()
    return [r for r in recipes if r.category.lower() == category]


def search_by_max_time(max_minutes):
    """Find recipes that can be made within the given time."""
    recipes = load_recipes()
    return [r for r in recipes if r.total_time() <= max_minutes]


def get_all_categories():
    """Return a list of all unique categories."""
    recipes = load_recipes()
    categories = set(r.category for r in recipes if r.category)
    return sorted(categories)

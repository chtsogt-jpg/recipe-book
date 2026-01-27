"""Storage module for saving and loading recipes."""

import json
import os
from recipe import Recipe


DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "recipes.json")


def load_recipes():
    """Load all recipes from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return [Recipe.from_dict(r) for r in data]
    except (json.JSONDecodeError, KeyError):
        return []


def save_recipes(recipes):
    """Save all recipes to the JSON file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    data = [r.to_dict() for r in recipes]
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_recipe(recipe):
    """Add a new recipe to storage."""
    recipes = load_recipes()
    recipes.append(recipe)
    save_recipes(recipes)


def delete_recipe(name):
    """Delete a recipe by name. Returns True if deleted, False if not found."""
    recipes = load_recipes()
    original_count = len(recipes)
    recipes = [r for r in recipes if r.name.lower() != name.lower()]

    if len(recipes) < original_count:
        save_recipes(recipes)
        return True
    return False


def update_recipe(old_name, updated_recipe):
    """Update an existing recipe. Returns True if updated, False if not found."""
    recipes = load_recipes()

    for i, recipe in enumerate(recipes):
        if recipe.name.lower() == old_name.lower():
            recipes[i] = updated_recipe
            save_recipes(recipes)
            return True
    return False


def get_recipe_by_name(name):
    """Get a single recipe by name. Returns None if not found."""
    recipes = load_recipes()
    for recipe in recipes:
        if recipe.name.lower() == name.lower():
            return recipe
    return None

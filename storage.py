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


def export_recipes(filepath, recipe_names=None):
    """
    Export recipes to a JSON file.

    Args:
        filepath: Path to export file
        recipe_names: List of recipe names to export (None = all)

    Returns:
        Number of recipes exported
    """
    recipes = load_recipes()

    if recipe_names:
        names_lower = [n.lower() for n in recipe_names]
        recipes = [r for r in recipes if r.name.lower() in names_lower]

    data = [r.to_dict() for r in recipes]

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    return len(recipes)


def import_recipes(filepath, overwrite=False):
    """
    Import recipes from a JSON file.

    Args:
        filepath: Path to import file
        overwrite: If True, replace existing recipes with same name

    Returns:
        Tuple of (imported_count, skipped_count)
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, "r") as f:
        data = json.load(f)

    existing = load_recipes()
    existing_names = {r.name.lower() for r in existing}

    imported = 0
    skipped = 0

    for recipe_data in data:
        recipe = Recipe.from_dict(recipe_data)
        name_lower = recipe.name.lower()

        if name_lower in existing_names:
            if overwrite:
                # Remove existing and add new
                existing = [r for r in existing if r.name.lower() != name_lower]
                existing.append(recipe)
                imported += 1
            else:
                skipped += 1
        else:
            existing.append(recipe)
            existing_names.add(name_lower)
            imported += 1

    save_recipes(existing)
    return imported, skipped

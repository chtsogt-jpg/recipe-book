"""Shopping list generator from recipes."""

from collections import defaultdict
from storage import load_recipes


def generate_shopping_list(recipe_names):
    """
    Generate a combined shopping list from multiple recipes.
    Combines similar ingredients where possible.

    Args:
        recipe_names: List of recipe names to include

    Returns:
        Dict mapping ingredient items to their total amounts/units
    """
    recipes = load_recipes()
    recipe_dict = {r.name.lower(): r for r in recipes}

    # Group ingredients by item name
    shopping = defaultdict(list)

    for name in recipe_names:
        recipe = recipe_dict.get(name.lower())
        if recipe:
            for ing in recipe.ingredients:
                item = ing.get("item", "").lower()
                amount = ing.get("amount", 0)
                unit = ing.get("unit", "")
                shopping[item].append({"amount": amount, "unit": unit, "recipe": recipe.name})

    return dict(shopping)


def format_shopping_list(shopping_dict):
    """
    Format a shopping list for display.

    Args:
        shopping_dict: Dict from generate_shopping_list()

    Returns:
        Formatted string for display
    """
    if not shopping_dict:
        return "Shopping list is empty."

    lines = ["\n--- Shopping List ---\n"]

    for item, entries in sorted(shopping_dict.items()):
        # Try to combine entries with same unit
        combined = defaultdict(float)
        for entry in entries:
            unit = entry["unit"]
            amount = entry["amount"]
            if isinstance(amount, (int, float)):
                combined[unit] += amount
            else:
                combined[unit] = amount  # Keep as-is if not numeric

        # Format the line
        parts = []
        for unit, amount in combined.items():
            if isinstance(amount, float) and amount == int(amount):
                amount = int(amount)
            if unit:
                parts.append(f"{amount} {unit}")
            elif amount:
                parts.append(str(amount))

        if parts:
            lines.append(f"  [ ] {item}: {', '.join(parts)}")
        else:
            lines.append(f"  [ ] {item}")

    lines.append("")
    return "\n".join(lines)


def get_recipes_for_shopping():
    """Return list of all available recipe names."""
    recipes = load_recipes()
    return [r.name for r in recipes]

"""Recipe Book - Main CLI interface."""

from recipe import Recipe
from storage import load_recipes, add_recipe, delete_recipe, save_recipes
from search import (
    search_by_name,
    search_by_ingredient,
    search_by_category,
    search_by_max_time,
    get_all_categories
)
from converter import scale_recipe, convert_unit


def display_recipe(recipe):
    """Display a single recipe in a readable format."""
    print(f"\n{'=' * 50}")
    print(f"  {recipe.name.upper()}")
    print(f"{'=' * 50}")

    if recipe.category:
        print(f"Category: {recipe.category}")

    print(f"Prep: {recipe.prep_time} min | Cook: {recipe.cook_time} min | Total: {recipe.total_time()} min")
    print(f"Servings: {recipe.servings}")

    print(f"\n--- Ingredients ---")
    for ing in recipe.ingredients:
        amount = ing.get('amount', '')
        unit = ing.get('unit', '')
        item = ing.get('item', '')
        print(f"  - {amount} {unit} {item}".strip())

    print(f"\n--- Instructions ---")
    for i, step in enumerate(recipe.instructions, 1):
        print(f"  {i}. {step}")

    print()


def display_recipe_list(recipes):
    """Display a list of recipes (names only)."""
    if not recipes:
        print("No recipes found.")
        return

    print(f"\nFound {len(recipes)} recipe(s):")
    for i, r in enumerate(recipes, 1):
        time_str = f"({r.total_time()} min)" if r.total_time() > 0 else ""
        print(f"  {i}. {r.name} {time_str}")


def get_input(prompt, required=True):
    """Get user input with optional requirement."""
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("This field is required. Please try again.")


def add_new_recipe():
    """Interactive prompt to add a new recipe."""
    print("\n--- Add New Recipe ---\n")

    name = get_input("Recipe name: ")
    category = get_input("Category (e.g., breakfast, dinner, dessert): ", required=False)

    try:
        prep_time = int(get_input("Prep time (minutes): ", required=False) or 0)
        cook_time = int(get_input("Cook time (minutes): ", required=False) or 0)
        servings = int(get_input("Servings: ", required=False) or 1)
    except ValueError:
        print("Invalid number entered. Using defaults.")
        prep_time, cook_time, servings = 0, 0, 1

    print("\nEnter ingredients (one per line, format: 'amount unit item')")
    print("Example: '2 cups flour' or '1 lb chicken'")
    print("Type 'done' when finished.\n")

    ingredients = []
    while True:
        ing_input = input("Ingredient: ").strip()
        if ing_input.lower() == 'done':
            break
        if ing_input:
            parts = ing_input.split(maxsplit=2)
            if len(parts) >= 3:
                try:
                    amount = float(parts[0])
                except ValueError:
                    amount = parts[0]
                ingredients.append({"amount": amount, "unit": parts[1], "item": parts[2]})
            else:
                ingredients.append({"amount": "", "unit": "", "item": ing_input})

    print("\nEnter instructions (one step per line)")
    print("Type 'done' when finished.\n")

    instructions = []
    step_num = 1
    while True:
        step = input(f"Step {step_num}: ").strip()
        if step.lower() == 'done':
            break
        if step:
            instructions.append(step)
            step_num += 1

    recipe = Recipe(name, ingredients, instructions, prep_time, cook_time, servings, category)
    add_recipe(recipe)
    print(f"\nRecipe '{name}' added successfully!")


def search_menu():
    """Search submenu."""
    while True:
        print("\n--- Search Recipes ---")
        print("1. Search by name")
        print("2. Search by ingredient")
        print("3. Search by category")
        print("4. Search by max time")
        print("5. Back to main menu")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            query = get_input("Enter name to search: ")
            results = search_by_name(query)
            display_recipe_list(results)
        elif choice == "2":
            ingredient = get_input("Enter ingredient: ")
            results = search_by_ingredient(ingredient)
            display_recipe_list(results)
        elif choice == "3":
            categories = get_all_categories()
            if categories:
                print(f"Available categories: {', '.join(categories)}")
            category = get_input("Enter category: ")
            results = search_by_category(category)
            display_recipe_list(results)
        elif choice == "4":
            try:
                max_time = int(get_input("Max total time (minutes): "))
                results = search_by_max_time(max_time)
                display_recipe_list(results)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "5":
            break


def view_recipe():
    """View a specific recipe."""
    recipes = load_recipes()
    if not recipes:
        print("No recipes in the book yet!")
        return

    display_recipe_list(recipes)

    try:
        choice = int(get_input("\nEnter recipe number to view (0 to cancel): "))
        if 0 < choice <= len(recipes):
            display_recipe(recipes[choice - 1])
    except ValueError:
        print("Invalid choice.")


def scale_recipe_menu():
    """Scale a recipe to different servings."""
    recipes = load_recipes()
    if not recipes:
        print("No recipes in the book yet!")
        return

    display_recipe_list(recipes)

    try:
        choice = int(get_input("\nEnter recipe number to scale (0 to cancel): "))
        if 0 < choice <= len(recipes):
            recipe = recipes[choice - 1]
            new_servings = int(get_input(f"Current servings: {recipe.servings}. New servings: "))
            scaled = scale_recipe(recipe, new_servings)
            display_recipe(scaled)
    except ValueError:
        print("Invalid input.")


def unit_converter_menu():
    """Standalone unit converter."""
    print("\n--- Unit Converter ---")
    try:
        amount = float(get_input("Amount: "))
        from_unit = get_input("From unit (e.g., cups, oz, g): ")
        to_unit = get_input("To unit: ")

        result = convert_unit(amount, from_unit, to_unit)
        if result is not None:
            print(f"\n{amount} {from_unit} = {result} {to_unit}")
        else:
            print("\nCannot convert between these units.")
    except ValueError:
        print("Invalid amount.")


def main():
    """Main application loop."""
    print("\n" + "=" * 50)
    print("       RECIPE BOOK")
    print("=" * 50)

    while True:
        print("\n--- Main Menu ---")
        print("1. View all recipes")
        print("2. View a recipe")
        print("3. Add a recipe")
        print("4. Search recipes")
        print("5. Scale a recipe")
        print("6. Unit converter")
        print("7. Delete a recipe")
        print("8. Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            recipes = load_recipes()
            display_recipe_list(recipes)
        elif choice == "2":
            view_recipe()
        elif choice == "3":
            add_new_recipe()
        elif choice == "4":
            search_menu()
        elif choice == "5":
            scale_recipe_menu()
        elif choice == "6":
            unit_converter_menu()
        elif choice == "7":
            name = get_input("Recipe name to delete: ")
            if delete_recipe(name):
                print(f"Recipe '{name}' deleted.")
            else:
                print(f"Recipe '{name}' not found.")
        elif choice == "8":
            print("\nGoodbye! Happy cooking!\n")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

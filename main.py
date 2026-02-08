"""Recipe Book - Main CLI interface."""

from recipe import Recipe
from storage import (
    load_recipes, add_recipe, delete_recipe, save_recipes,
    update_recipe, export_recipes, import_recipes
)
from search import (
    search_by_name,
    search_by_ingredient,
    search_by_category,
    search_by_max_time,
    get_all_categories
)
from converter import scale_recipe, convert_unit
from shopping import generate_shopping_list, format_shopping_list


def display_recipe(recipe):
    """Display a single recipe in a readable format."""
    print(f"\n{'=' * 50}")
    fav_marker = " [FAVORITE]" if recipe.favorite else ""
    print(f"  {recipe.name.upper()}{fav_marker}")
    print(f"{'=' * 50}")

    if recipe.category:
        print(f"Category: {recipe.category}")

    print(f"Rating: {recipe.get_rating_display()}")
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
        fav_str = "<3" if r.favorite else ""
        rating_str = f"{'*' * r.rating}" if r.rating > 0 else ""
        print(f"  {i}. {fav_str} {r.name} {rating_str} {time_str}")


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
        print("5. View top rated")
        print("6. View favorites")
        print("7. Back to main menu")

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
            view_top_rated()
        elif choice == "6":
            view_favorites()
        elif choice == "7":
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


def edit_recipe_menu():
    """Edit an existing recipe."""
    recipes = load_recipes()
    if not recipes:
        print("No recipes in the book yet!")
        return

    display_recipe_list(recipes)

    try:
        choice = int(get_input("\nEnter recipe number to edit (0 to cancel): "))
        if choice == 0:
            return
        if not (0 < choice <= len(recipes)):
            print("Invalid choice.")
            return

        recipe = recipes[choice - 1]
        old_name = recipe.name

        print(f"\n--- Editing: {recipe.name} ---")
        print("(Press Enter to keep current value)\n")

        # Get updated values
        new_name = input(f"Name [{recipe.name}]: ").strip() or recipe.name
        new_category = input(f"Category [{recipe.category}]: ").strip() or recipe.category

        prep_input = input(f"Prep time [{recipe.prep_time}]: ").strip()
        new_prep = int(prep_input) if prep_input else recipe.prep_time

        cook_input = input(f"Cook time [{recipe.cook_time}]: ").strip()
        new_cook = int(cook_input) if cook_input else recipe.cook_time

        servings_input = input(f"Servings [{recipe.servings}]: ").strip()
        new_servings = int(servings_input) if servings_input else recipe.servings

        # Ask about ingredients
        print(f"\nCurrent ingredients: {len(recipe.ingredients)}")
        edit_ing = input("Edit ingredients? (y/n): ").strip().lower()

        if edit_ing == 'y':
            print("\nEnter new ingredients (format: 'amount unit item')")
            print("Type 'done' when finished.\n")
            new_ingredients = []
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
                        new_ingredients.append({"amount": amount, "unit": parts[1], "item": parts[2]})
                    else:
                        new_ingredients.append({"amount": "", "unit": "", "item": ing_input})
        else:
            new_ingredients = recipe.ingredients

        # Ask about instructions
        print(f"\nCurrent instructions: {len(recipe.instructions)} steps")
        edit_inst = input("Edit instructions? (y/n): ").strip().lower()

        if edit_inst == 'y':
            print("\nEnter new instructions (one step per line)")
            print("Type 'done' when finished.\n")
            new_instructions = []
            step_num = 1
            while True:
                step = input(f"Step {step_num}: ").strip()
                if step.lower() == 'done':
                    break
                if step:
                    new_instructions.append(step)
                    step_num += 1
        else:
            new_instructions = recipe.instructions

        # Create updated recipe
        updated = Recipe(new_name, new_ingredients, new_instructions,
                        new_prep, new_cook, new_servings, new_category)

        if update_recipe(old_name, updated):
            print(f"\nRecipe '{new_name}' updated successfully!")
        else:
            print("\nError updating recipe.")

    except ValueError:
        print("Invalid input.")


def shopping_list_menu():
    """Generate a shopping list from selected recipes."""
    recipes = load_recipes()
    if not recipes:
        print("No recipes in the book yet!")
        return

    print("\n--- Generate Shopping List ---")
    display_recipe_list(recipes)

    print("\nEnter recipe numbers to include (comma-separated)")
    print("Example: 1, 2, 3")
    selection = input("\nRecipes: ").strip()

    if not selection:
        print("No recipes selected.")
        return

    # Parse selection
    selected_names = []
    try:
        indices = [int(x.strip()) for x in selection.split(",")]
        for idx in indices:
            if 0 < idx <= len(recipes):
                selected_names.append(recipes[idx - 1].name)
    except ValueError:
        print("Invalid input. Please enter numbers separated by commas.")
        return

    if not selected_names:
        print("No valid recipes selected.")
        return

    print(f"\nGenerating shopping list for: {', '.join(selected_names)}")

    shopping = generate_shopping_list(selected_names)
    print(format_shopping_list(shopping))


def export_menu():
    """Export recipes to a file."""
    recipes = load_recipes()
    if not recipes:
        print("No recipes to export!")
        return

    print("\n--- Export Recipes ---")
    display_recipe_list(recipes)

    print("\nEnter recipe numbers to export (comma-separated)")
    print("Or press Enter to export all recipes")
    selection = input("\nRecipes (Enter for all): ").strip()

    # Get filename
    filename = input("Export filename (default: my_recipes.json): ").strip()
    if not filename:
        filename = "my_recipes.json"
    if not filename.endswith(".json"):
        filename += ".json"

    try:
        if selection:
            indices = [int(x.strip()) for x in selection.split(",")]
            selected_names = []
            for idx in indices:
                if 0 < idx <= len(recipes):
                    selected_names.append(recipes[idx - 1].name)
            count = export_recipes(filename, selected_names)
        else:
            count = export_recipes(filename)

        print(f"\nExported {count} recipe(s) to {filename}")
    except Exception as e:
        print(f"\nError exporting: {e}")


def import_menu():
    """Import recipes from a file."""
    print("\n--- Import Recipes ---")

    filename = input("Import filename: ").strip()
    if not filename:
        print("No filename provided.")
        return

    overwrite = input("Overwrite existing recipes with same name? (y/n): ").strip().lower() == 'y'

    try:
        imported, skipped = import_recipes(filename, overwrite)
        print(f"\nImported {imported} recipe(s)")
        if skipped:
            print(f"Skipped {skipped} recipe(s) (already exist)")
    except FileNotFoundError:
        print(f"\nFile not found: {filename}")
    except Exception as e:
        print(f"\nError importing: {e}")


def rate_recipe_menu():
    """Rate a recipe."""
    recipes = load_recipes()
    if not recipes:
        print("No recipes in the book yet!")
        return

    display_recipe_list(recipes)

    try:
        choice = int(get_input("\nEnter recipe number to rate (0 to cancel): "))
        if choice == 0:
            return
        if not (0 < choice <= len(recipes)):
            print("Invalid choice.")
            return

        recipe = recipes[choice - 1]
        print(f"\nRating: {recipe.name}")
        print(f"Current rating: {recipe.get_rating_display()}")
        print("\nEnter new rating (1-5 stars, or 0 to clear):")

        rating = int(get_input("Rating: "))
        if not (0 <= rating <= 5):
            print("Rating must be between 0 and 5.")
            return

        recipe.rating = rating
        if update_recipe(recipe.name, recipe):
            if rating == 0:
                print(f"\nRating cleared for '{recipe.name}'")
            else:
                print(f"\nRated '{recipe.name}' with {'*' * rating}")
        else:
            print("\nError updating recipe.")

    except ValueError:
        print("Invalid input.")


def toggle_favorite_menu():
    """Toggle favorite status for a recipe."""
    recipes = load_recipes()
    if not recipes:
        print("No recipes in the book yet!")
        return

    display_recipe_list(recipes)

    try:
        choice = int(get_input("\nEnter recipe number to toggle favorite (0 to cancel): "))
        if choice == 0:
            return
        if not (0 < choice <= len(recipes)):
            print("Invalid choice.")
            return

        recipe = recipes[choice - 1]
        recipe.favorite = not recipe.favorite

        if update_recipe(recipe.name, recipe):
            status = "added to" if recipe.favorite else "removed from"
            print(f"\n'{recipe.name}' {status} favorites!")
        else:
            print("\nError updating recipe.")

    except ValueError:
        print("Invalid input.")


def view_top_rated():
    """View top-rated recipes."""
    recipes = load_recipes()
    if not recipes:
        print("No recipes in the book yet!")
        return

    # Filter and sort by rating
    rated = [r for r in recipes if r.rating > 0]
    if not rated:
        print("\nNo recipes have been rated yet.")
        return

    rated.sort(key=lambda r: r.rating, reverse=True)
    print("\n--- Top Rated Recipes ---")
    for i, r in enumerate(rated, 1):
        print(f"  {i}. {r.name} {'*' * r.rating} ({r.total_time()} min)")


def view_favorites():
    """View all favorite recipes."""
    recipes = load_recipes()
    favorites = [r for r in recipes if r.favorite]

    if not favorites:
        print("\nNo favorite recipes yet. Use option 13 to add favorites!")
        return

    print("\n--- Your Favorite Recipes ---")
    for i, r in enumerate(favorites, 1):
        time_str = f"({r.total_time()} min)" if r.total_time() > 0 else ""
        print(f"  {i}. <3 {r.name} {time_str}")


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
        print("7. Edit a recipe")
        print("8. Delete a recipe")
        print("9. Shopping list")
        print("10. Export recipes")
        print("11. Import recipes")
        print("12. Rate a recipe")
        print("13. Toggle favorite")
        print("0. Exit")

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
            edit_recipe_menu()
        elif choice == "8":
            name = get_input("Recipe name to delete: ")
            if delete_recipe(name):
                print(f"Recipe '{name}' deleted.")
            else:
                print(f"Recipe '{name}' not found.")
        elif choice == "9":
            shopping_list_menu()
        elif choice == "10":
            export_menu()
        elif choice == "11":
            import_menu()
        elif choice == "12":
            rate_recipe_menu()
        elif choice == "13":
            toggle_favorite_menu()
        elif choice == "0":
            print("\nGoodbye! Happy cooking!\n")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

"""Recipe data structure and related utilities."""


class Recipe:
    """Represents a single recipe."""

    def __init__(self, name, ingredients, instructions, prep_time=0, cook_time=0, servings=1, category="", rating=0):
        """
        Create a new recipe.

        Args:
            name: Recipe name
            ingredients: List of dicts with 'item', 'amount', 'unit'
            instructions: List of instruction steps
            prep_time: Preparation time in minutes
            cook_time: Cooking time in minutes
            servings: Number of servings
            category: Recipe category (e.g., "breakfast", "dinner", "dessert")
            rating: Recipe rating (0-5 stars, 0 = unrated)
        """
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.servings = servings
        self.category = category
        self.rating = rating

    def total_time(self):
        """Return total time (prep + cook) in minutes."""
        return self.prep_time + self.cook_time

    def to_dict(self):
        """Convert recipe to dictionary for JSON storage."""
        return {
            "name": self.name,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "prep_time": self.prep_time,
            "cook_time": self.cook_time,
            "servings": self.servings,
            "category": self.category,
            "rating": self.rating
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Recipe from a dictionary."""
        return cls(
            name=data["name"],
            ingredients=data["ingredients"],
            instructions=data["instructions"],
            prep_time=data.get("prep_time", 0),
            cook_time=data.get("cook_time", 0),
            servings=data.get("servings", 1),
            category=data.get("category", ""),
            rating=data.get("rating", 0)
        )

    def get_rating_display(self):
        """Return star display for rating."""
        if self.rating == 0:
            return "Not rated"
        return "*" * self.rating + "-" * (5 - self.rating)

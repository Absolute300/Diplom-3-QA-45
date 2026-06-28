# data.py

from typing import Dict, Literal

# Константы для идентификаторов ингредиентов
INGREDIENT_IDS = {
    "bun": {
        "fluorescent": "61c0c5a71d1f82001bdaaa6d",  # Флюоресцентная булка
        "crust": "61c0c5a71d1f82001bdaaa6f"  # Космическая краторная булка
    },
    "sauce": {
        "spicy": "61c0c5a71d1f82001bdaaa72",  # Соус Spicy-X
        "sour_cream": "61c0c5a71d1f82001bdaaa71"  # Соус традиционный галактический
    },
    "main": {
        "biocutlet": "61c0c5a71d1f82001bdaaa73",  # Биокотлета из марсианской Магнолии
        "beef": "61c0c5a71d1f82001bdaaa74"  # Говяжий метеорит
    }
}

# Типы для аннотаций
IngredientType = Literal["bun", "sauce", "main"]
IngredientName = Literal["fluorescent", "crust", "spicy", "sour_cream", "biocutlet", "beef"]


class TestUser:
    def __init__(self):
        self._credentials = {
            "email": self.generate_test_email(),
            "password": self.generate_test_password(),
            "name": self.generate_test_name()
        }

    @staticmethod
    def generate_test_email(prefix: str = "test") -> str:
        import uuid
        return f"{prefix}_{uuid.uuid4().hex[:8]}@example.com"

    @staticmethod
    def generate_test_password() -> str:
        import uuid
        return f"P@ssw0rd_{uuid.uuid4().hex[:4]}"

    @staticmethod
    def generate_test_name() -> str:
        import uuid
        return f"User_{uuid.uuid4().hex[:4]}"

    @property
    def valid_credentials(self) -> Dict[str, str]:
        return self._credentials


def get_ingredient_id(ingredient_type: IngredientType, name: IngredientName) -> str:
    """Возвращает идентификатор ингредиента по типу и названию."""
    try:
        return INGREDIENT_IDS[ingredient_type][name]
    except KeyError as e:
        raise KeyError(f"Ingredient {name} of type {ingredient_type} not found") from e
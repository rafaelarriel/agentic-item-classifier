"""Fonte de dados simples do catálogo, independente do transporte MCP."""

from app.schemas.classifier import Category

CATEGORIES: tuple[Category, ...] = (
    Category(id="electronics", name="Eletrônicos"),
    Category(id="computers", name="Informática"),
    Category(id="food", name="Alimentos"),
    Category(id="beverages", name="Bebidas"),
    Category(id="clothing", name="Roupas"),
    Category(id="shoes", name="Calçados"),
    Category(id="home", name="Casa"),
    Category(id="automotive", name="Automotivo"),
    Category(id="other", name="Outros"),
)

CATEGORY_EXAMPLES: dict[str, list[str]] = {
    "electronics": ["smartphone", "televisão", "fone bluetooth"],
    "computers": ["notebook", "teclado", "monitor"],
    "food": ["arroz", "macarrão", "café"],
    "beverages": ["água", "refrigerante", "suco"],
    "clothing": ["camiseta", "calça", "jaqueta"],
    "shoes": ["tênis", "sandália", "bota"],
    "home": ["panela", "travesseiro", "lâmpada"],
    "automotive": ["óleo de motor", "pneu", "capacete"],
    "other": ["produto sem categoria específica"],
}


def list_catalog() -> list[Category]:
    """Retorna uma cópia serializável das categorias disponíveis."""

    return list(CATEGORIES)


def find_category(category_id: str) -> Category | None:
    """Localiza uma categoria pelo identificador estável."""

    return next((category for category in CATEGORIES if category.id == category_id), None)

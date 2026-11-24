"""Matches menu dishes with the dish database and flags dishes that are missing."""
import json
import re


def normalize(name: str) -> str:
    """Turkish-aware key: 'Tas  Kebabı' -> 'tas kebabı', 'Domates Çorbası' -> 'domates çorba'."""
    name = name.replace("İ", "i").replace("I", "ı").lower()
    name = re.sub(r"\s*/\s*", " / ", name)
    name = " ".join(name.split())
    return name.replace("çorbası", "çorba")


def load_database(path) -> dict:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    return {normalize(k): v for k, v in raw.items()}


def enrich_menu(menu: list[dict], database: dict) -> tuple[list[dict], list[str]]:
    missing = set()
    for day in menu:
        enriched = []
        for dish in day["dishes"]:
            info = database.get(normalize(dish["name"]))
            if info is None:
                missing.add(dish["name"])
                enriched.append({"name": dish["name"], "category": dish.get("course", ""), "missing": True})
            else:
                enriched.append({**info, "menu_name": dish["name"], "missing": False})
        day["dishes"] = enriched
    return menu, sorted(missing)

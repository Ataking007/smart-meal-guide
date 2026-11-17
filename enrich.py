"""Matches menu dishes with the dish database and flags dishes that are missing."""
import json


def normalize(name: str) -> str:
    return " ".join(name.lower().split())


def load_database(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def enrich_menu(menu: list[dict], database: dict) -> tuple[list[dict], list[str]]:
    missing = set()
    for day in menu:
        enriched = []
        for dish in day["dishes"]:
            info = database.get(normalize(dish))
            if info is None:
                missing.add(dish)
                enriched.append({"name": dish, "missing": True})
            else:
                enriched.append({**info, "missing": False})
        day["dishes"] = enriched
    return menu, sorted(missing)

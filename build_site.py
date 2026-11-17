"""Generates the Smart Meal Guide web page from the enriched menu."""
from html import escape

LABEL_ICONS = {"vegan": "🌱 Vegan", "vegetarian": "🥕 Vegetarian", "gluten-free": "🌾 Gluten-free"}


def dish_card(d: dict) -> str:
    if d["missing"]:
        return (f'<div class="card missing"><h3>{escape(d["name"])}</h3>'
                f'<p>⚠️ Not in database yet – flagged for completion.</p></div>')
    n = d["nutrition_per_portion"]
    labels = " ".join(f'<span class="tag">{LABEL_ICONS.get(l, l)}</span>' for l in d["labels"])
    allergens = ", ".join(d["allergens"]) or "none"
    return f"""<div class="card">
  <img src="{escape(d['photo'])}" alt="{escape(d['name'])}" onerror="this.style.display='none'">
  <h3>{escape(d['name'])}</h3>
  <div>{labels}</div>
  <p><b>Allergens:</b> {escape(allergens)}</p>
  <p><b>Ingredients:</b> {escape(', '.join(d['ingredients']))}</p>
  <table>
    <tr><th colspan="2">Nutrition facts ({n['portion_g']} g portion)</th></tr>
    <tr><td>Energy</td><td>{n['energy_kcal']} kcal</td></tr>
    <tr><td>Protein</td><td>{n['protein_g']} g</td></tr>
    <tr><td>Carbohydrate</td><td>{n['carbohydrate_g']} g</td></tr>
    <tr><td>Fat</td><td>{n['fat_g']} g</td></tr>
    <tr><td>Fiber</td><td>{n['fiber_g']} g</td></tr>
    <tr><td>Salt</td><td>{n['salt_g']} g</td></tr>
  </table>
  <details><summary>Estimated recipe</summary><p>{escape(d['recipe'])}</p></details>
</div>"""


def build_page(menu: list[dict]) -> str:
    days = "".join(
        f'<section><h2>{escape(day["date"])}</h2><div class="grid">'
        + "".join(dish_card(d) for d in day["dishes"]) + "</div></section>"
        for day in menu)
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Smart Meal Guide</title>
<style>
body{{font-family:system-ui,sans-serif;margin:0;background:#f6f4ef;color:#222}}
header{{background:#2f5d50;color:#fff;padding:1rem 2rem}}
section{{padding:1rem 2rem}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1rem}}
.card{{background:#fff;border-radius:10px;padding:1rem;box-shadow:0 1px 4px #0002}}
.card img{{width:100%;border-radius:6px}}
.missing{{background:#fff4e0}}
.tag{{display:inline-block;background:#e3efe9;border-radius:12px;padding:2px 8px;margin:2px;font-size:.85em}}
table{{width:100%;border-collapse:collapse;font-size:.9em}} td,th{{border-bottom:1px solid #ddd;padding:3px;text-align:left}}
</style></head><body>
<header><h1>🍽️ Smart Meal Guide</h1><p>Cafeteria menu – draft version</p></header>
{days}
</body></html>"""

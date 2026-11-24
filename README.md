# Smart Meal Guide 🍽️

**GMS 4039 Information Technologies – Group Project, Option 4**
**Status:** Working version (24.11.2026)

🌐 **Live website:** https://ataking007.github.io/smart-meal-guide/

A digital guide for a staff/student cafeteria. The daily/weekly menu is pulled
automatically from the institution's website, and every dish is enriched with a
photo, ingredients, dietary labels (vegan / vegetarian / gluten-free), a nutrition
facts table per portion, allergen warnings and an estimated recipe.

## Team

| Name | Role |
|------|------|
| Özlem Yılmaz | Dish database, nutrition (TürKomp) |
| Vahdet Can Şahiner | Photos, interface, testing & survey |
| Atahan Arslan | Development (scraper / automation), report & video |

## How it works

```
Cafeteria website ──► scraper.py ──► enrich.py ──► build_site.py ──► index.html
                                      ▲
                       dishes.json (dish database:
                       photo, ingredients, labels, nutrition, allergens, recipe)
```

1. **Automated menu retrieval** – `scraper.py` downloads the menu page from the
   URL in `config.json` and extracts the dishes per day (no manual entry).
2. **Enrichment** – `enrich.py` matches every dish name with `dishes.json`.
   Dishes not yet in the database are **flagged for completion** (`missing_dishes.json`).
3. **Output** – `build_site.py` generates the guide as a web page (`index.html`).

## Requirements checklist

| Requirement | Status |
|---|---|
| Automated menu retrieval from website | 🟡 Working on sample week menu, real cafeteria URL to be connected |
| Photo library (2 weeks of dishes) | 🔴 Photographing starts this week |
| Ingredients for each dish | 🟡 16 dishes done |
| Dietary labels (vegan / vegetarian / gluten-free) | 🟢 Implemented, with filters on the website |
| Calories + nutrition table per portion (TürKomp) | 🟡 16 dishes done (estimates, being checked with TürKomp) |
| Allergen warnings | 🟢 Implemented |
| Estimated recipe | 🟡 16 dishes done |
| Full automation + flagging new dishes | 🟢 Implemented (prototype) |

## Run it

```bash
pip install -r requirements.txt
python main.py            # uses the URL in config.json
python main.py --sample   # offline demo with sample_menu.html
```
This regenerates `index.html`, the website published with GitHub Pages.

## Project structure

| File | Purpose |
|---|---|
| `main.py` | runs the whole pipeline |
| `scraper.py` | automated menu retrieval |
| `enrich.py` | matches dishes with the database, flags missing ones |
| `build_site.py` | generates the website (`index.html`) |
| `index.html` | the website (GitHub Pages) |
| `dishes.json` | dish database |
| `sample_menu.html` | sample menu page for testing |
| `config.json` | cafeteria menu URL |
| `DRAFT_REPORT.md` | draft report / plan |

Dish photos will be added in a `photos/` folder.

## Timeline

| Date | Task |
|---|---|
| 10.11 – 22.11.2026 | App design and development |
| 17.11.2026 | Draft program on GitHub ✅ |
| **24.11.2026** | **Completed program + live website** ✅ |
| 23.11 – 29.11.2026 | User testing with 20 participants |
| 01.12.2026 | Survey results |
| 30.11 – 07.12.2026 | Data analysis, report and documentary video |
| 08.12.2026 | Project video presentation in class |
| 15.12.2026 | Gastronomy Fair – jury presentation |

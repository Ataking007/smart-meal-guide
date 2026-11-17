# Draft Report – Smart Meal Guide (Option 4)

**Course:** GMS 4039 Information Technologies
**Date:** 17.11.2026

## 1. Objective
Develop a digital guide for a staff/student cafeteria. The menu is pulled
automatically from the institution's website and each dish is enriched with a
photo, ingredients, dietary labels, nutrition facts, allergen warnings and an
estimated recipe.

## 2. What has been done so far
- GitHub repository and project structure created.
- Menu scraper prototype (`scraper.py`) – parses a menu table into days and dishes.
- Dish database format defined (`dishes.json`), 3 sample dishes completed
  (ingredients, labels, allergens, nutrition per portion, recipe).
- Automatic matching of menu dishes with the database; unknown dishes are
  flagged for completion (`missing_dishes.json`).
- First version of the guide page (`index.html`).

## 3. Methods and tools
- **Language:** Python 3 (requests, BeautifulSoup)
- **Output:** static web page (HTML/CSS), can be opened on phone or computer
- **Nutrition reference:** TürKomp (Turkish food composition database) – values per
  portion are calculated from the ingredient amounts in the estimated recipe.
- **Photos:** real dishes photographed in the cafeteria over two weeks; may be
  enhanced with AI tools (lighting, background, color) while still showing the real dish.

## 4. Next steps (until 24.11.2026)
1. Connect the scraper to the real cafeteria menu URL and adapt the parser.
2. Photograph all dishes served over two weeks and add them to a `photos/` folder.
3. Complete the database for all dishes (ingredients, TürKomp nutrition, recipes).
4. Improve the interface (filters for vegan / vegetarian / gluten-free).
5. Prepare the user test survey (20 participants, 23–29.11.2026).

## 5. Task distribution
| Member | Task |
|---|---|
| _Name_ | Scraper and automation |
| _Name_ | Dish database and nutrition calculation |
| _Name_ | Photos and interface |
| _Name_ | Testing, survey, report and video |

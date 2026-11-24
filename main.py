"""Smart Meal Guide pipeline: retrieve menu -> enrich dishes -> build website (index.html).

    python main.py           # downloads the menu from menu_url in config.json
    python main.py --sample  # uses the local test copy sample_menu.pdf
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from scraper import get_menu, get_menu_from_file
from enrich import load_database, enrich_menu
from build_site import build_page


def main():
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    url = config["menu_url"]

    if "--sample" in sys.argv or "REPLACE" in url:
        menu, source = get_menu_from_file(ROOT / "sample_menu.pdf"), "sample_menu.pdf (test copy)"
    else:
        try:
            menu, source = get_menu(url)
        except Exception as e:  # keep the current website if the cafeteria site is down
            print(f"Could not download the menu ({e}). Website not changed.")
            return

    if not menu:
        print("No menu table found. Website not changed.")
        return

    database = load_database(ROOT / config["dish_database"])
    menu, missing = enrich_menu(menu, database)

    (ROOT / config["output"]).write_text(
        build_page(menu, config.get("cafeteria_name", "Cafeteria"), source), encoding="utf-8")
    (ROOT / "missing_dishes.json").write_text(
        json.dumps(missing, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Menu source: {source}")
    print(f"Days: {len(menu)} | Website written to {config['output']}")
    print(f"Dishes flagged for completion: {', '.join(missing) or 'none'}")


if __name__ == "__main__":
    main()

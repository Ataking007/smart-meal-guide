"""Smart Meal Guide pipeline: retrieve menu -> enrich dishes -> build guide page."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from scraper import fetch_html, parse_menu
from enrich import load_database, enrich_menu
from build_site import build_page


def main():
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    if "--sample" in sys.argv:
        html = (ROOT / "sample_menu.html").read_text(encoding="utf-8")
    else:
        html = fetch_html(config["menu_url"])

    menu = parse_menu(html)
    database = load_database(ROOT / config["dish_database"])
    menu, missing = enrich_menu(menu, database)

    out = ROOT / config["output"]
    out.write_text(build_page(menu), encoding="utf-8")
    (ROOT / "missing_dishes.json").write_text(
        json.dumps(missing, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Menu days: {len(menu)} | Guide written to {out}")
    print(f"Dishes flagged for completion: {', '.join(missing) or 'none'}")


if __name__ == "__main__":
    main()

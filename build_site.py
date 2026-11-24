"""Generates the Smart Meal Guide website (index.html) from the enriched menu.

The page is fully self-contained (data embedded), so it works on GitHub Pages
and when opened directly from the computer.
"""
import json
from datetime import datetime

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Smart Meal Guide – Cafeteria Menu</title>
<style>
:root{--green:#2f5d50;--green2:#e4efe9;--cream:#faf7f1;--ink:#1f2a27;--muted:#66706c;--orange:#d9822b;--red:#b3412e;--card:#fff;--line:#e7e2d8}
*{box-sizing:border-box}
body{margin:0;font-family:"Segoe UI",system-ui,-apple-system,Roboto,Arial,sans-serif;background:var(--cream);color:var(--ink);line-height:1.45}
header{background:var(--green);color:#fff;padding:28px 20px 22px}
.wrap{max-width:1100px;margin:0 auto;padding:0 20px}
header h1{margin:0;font-size:2rem;letter-spacing:.3px}
header p{margin:6px 0 0;opacity:.85}
.updated{font-size:.85rem;opacity:.75;margin-top:10px}
nav.days{display:flex;gap:8px;overflow-x:auto;padding:18px 0 6px}
nav.days button{flex:0 0 auto;border:1px solid var(--line);background:#fff;border-radius:12px;padding:10px 16px;cursor:pointer;font:inherit;text-align:center;color:var(--ink)}
nav.days button b{display:block;font-size:.95rem}
nav.days button span{font-size:.8rem;color:var(--muted)}
nav.days button.active{background:var(--green);border-color:var(--green);color:#fff}
nav.days button.active span{color:#dfe9e4}
.toolbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:14px 0}
.toolbar .lbl{color:var(--muted);font-size:.9rem;margin-right:4px}
.chip{border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 14px;cursor:pointer;font:inherit;font-size:.9rem}
.chip.active{background:var(--green2);border-color:var(--green);color:var(--green);font-weight:600}
.summary{background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 18px;display:flex;flex-wrap:wrap;gap:22px;margin-bottom:18px}
.summary div{font-size:.85rem;color:var(--muted)}
.summary b{display:block;font-size:1.25rem;color:var(--ink)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px;padding-bottom:30px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;display:flex;flex-direction:column}
.card.hide{display:none}
.photo{height:150px;background:var(--green2);display:flex;align-items:center;justify-content:center;font-size:3.6rem;position:relative}
.photo img{width:100%;height:100%;object-fit:cover;position:absolute;inset:0}
.photo small{position:absolute;bottom:8px;right:10px;font-size:.7rem;color:var(--muted);background:#fffc;padding:2px 8px;border-radius:8px}
.body{padding:14px 16px 16px;display:flex;flex-direction:column;gap:8px;flex:1}
.cat{font-size:.75rem;text-transform:uppercase;letter-spacing:.8px;color:var(--orange);font-weight:700}
.card h3{margin:0;font-size:1.05rem}
.kcal{font-size:1.5rem;font-weight:700;color:var(--green)}
.kcal span{font-size:.85rem;color:var(--muted);font-weight:400}
.tags{display:flex;flex-wrap:wrap;gap:5px}
.tag{font-size:.75rem;padding:3px 9px;border-radius:999px;background:var(--green2);color:var(--green);font-weight:600}
.allergen{font-size:.8rem;color:var(--red);background:#fbeae6;border-radius:8px;padding:5px 9px}
details{border-top:1px solid var(--line);padding-top:8px}
summary{cursor:pointer;font-weight:600;font-size:.9rem;color:var(--green)}
table.nf{width:100%;border-collapse:collapse;font-size:.85rem;margin-top:6px}
table.nf td{padding:3px 0;border-bottom:1px solid #eee}
table.nf td:last-child{text-align:right;font-weight:600}
details p{margin:6px 0 0;font-size:.88rem}
.missing .photo{background:#fdf0dc}
.missing .body{background:#fffaf1}
.flag{font-size:.85rem;color:#8a5a14}
.empty{color:var(--muted);padding:20px 0}
section.about{background:#fff;border-top:1px solid var(--line);padding:26px 0;margin-top:10px}
section.about h2{margin-top:0;color:var(--green)}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px}
footer{text-align:center;font-size:.8rem;color:var(--muted);padding:18px}
a{color:var(--green)}
</style>
</head>
<body>
<header><div class="wrap">
  <h1>🍽️ Smart Meal Guide</h1>
  <p>Weekly cafeteria menu with photos, ingredients, dietary labels, nutrition facts, allergens and recipes.</p>
  <div class="updated">Menu automatically updated: __UPDATED__</div>
</div></header>

<main class="wrap">
  <nav class="days" id="days"></nav>
  <div class="toolbar">
    <span class="lbl">Show:</span>
    <button class="chip active" data-f="all">All dishes</button>
    <button class="chip" data-f="vegan">🌱 Vegan</button>
    <button class="chip" data-f="vegetarian">🥕 Vegetarian</button>
    <button class="chip" data-f="gluten-free">🌾 Gluten-free</button>
  </div>
  <div class="summary" id="summary"></div>
  <div class="grid" id="grid"></div>
</main>

<section class="about"><div class="wrap cols">
  <div>
    <h2>About the project</h2>
    <p>Smart Meal Guide pulls the cafeteria menu automatically from the institution's website. Every dish is matched with our dish database and shown with its photo, ingredients, dietary labels, nutrition facts per portion, allergen warnings and an estimated recipe. New dishes that are not in the database yet are flagged for completion.</p>
  </div>
  <div>
    <h2>Nutrition data</h2>
    <p>Nutrition values per portion are calculated from the estimated recipe using <b>TürKomp</b> (Turkish Food Composition Database) as the reference. Values are estimates and may differ slightly from the served portion.</p>
  </div>
  <div>
    <h2>Team</h2>
    <p>__TEAM__</p>
    <p>GMS 4039 Information Technologies – Group Project, Option 4</p>
    <p><a href="https://github.com/Ataking007/smart-meal-guide">Source code on GitHub</a></p>
  </div>
</div></section>
<footer>Smart Meal Guide · 2026</footer>

<script>
const MENU = __MENU__;
const ICON = {Soup:"🍲",Main:"🍛",Side:"🍚",Extra:"🥗"};
const LABEL = {"vegan":"🌱 Vegan","vegetarian":"🥕 Vegetarian","gluten-free":"🌾 Gluten-free"};
const DAYS = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
let current = 0, filter = "all";

function parseDate(s){const [d,m,y]=s.split(".").map(Number);return new Date(y,m-1,d);}
function esc(s){return String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));}

function card(d){
  if(d.missing){
    return `<div class="card missing" data-labels=""><div class="photo">❓</div><div class="body">
      <div class="cat">New dish</div><h3>${esc(d.name)}</h3>
      <div class="flag">⚠️ Not in the database yet – flagged for completion. Photo, labels and nutrition will be added.</div></div></div>`;
  }
  const n=d.nutrition_per_portion;
  const icon=ICON[d.category]||"🍽️";
  const tags=d.labels.map(l=>`<span class="tag">${LABEL[l]||l}</span>`).join("");
  const allergens=d.allergens.length?`<div class="allergen">⚠️ Contains: ${d.allergens.map(esc).join(", ")}</div>`:`<div class="tag" style="align-self:flex-start">No major allergens</div>`;
  return `<div class="card" data-labels="${d.labels.join(" ")}">
    <div class="photo">${icon}<img src="${esc(d.photo)}" alt="${esc(d.name)}" onerror="this.remove()"><small>photo coming soon</small></div>
    <div class="body">
      <div class="cat">${esc(d.category)}</div>
      <h3>${esc(d.name)}</h3>
      <div class="kcal">${n.energy_kcal} <span>kcal / ${n.portion_g} g portion</span></div>
      <div class="tags">${tags}</div>
      ${allergens}
      <details><summary>Nutrition facts</summary>
        <table class="nf">
          <tr><td>Energy</td><td>${n.energy_kcal} kcal</td></tr>
          <tr><td>Protein</td><td>${n.protein_g} g</td></tr>
          <tr><td>Carbohydrate</td><td>${n.carbohydrate_g} g</td></tr>
          <tr><td>Fat</td><td>${n.fat_g} g</td></tr>
          <tr><td>Fiber</td><td>${n.fiber_g} g</td></tr>
          <tr><td>Salt</td><td>${n.salt_g} g</td></tr>
        </table></details>
      <details><summary>Ingredients</summary><p>${d.ingredients.map(esc).join(", ")}</p></details>
      <details><summary>Estimated recipe</summary><p>${esc(d.recipe)}</p></details>
    </div></div>`;
}

function render(){
  document.querySelectorAll("#days button").forEach((b,i)=>b.classList.toggle("active",i===current));
  const day=MENU[current];
  const known=day.dishes.filter(d=>!d.missing);
  const sum=k=>known.reduce((a,d)=>a+d.nutrition_per_portion[k],0);
  const missing=day.dishes.length-known.length;
  document.getElementById("summary").innerHTML=
    `<div>Full tray energy<b>${Math.round(sum("energy_kcal"))} kcal</b></div>
     <div>Protein<b>${sum("protein_g").toFixed(1)} g</b></div>
     <div>Carbohydrate<b>${sum("carbohydrate_g").toFixed(1)} g</b></div>
     <div>Fat<b>${sum("fat_g").toFixed(1)} g</b></div>
     <div>Dishes<b>${day.dishes.length}${missing?` <span style="font-size:.8rem;color:#8a5a14">(${missing} flagged)</span>`:""}</b></div>`;
  const grid=document.getElementById("grid");
  grid.innerHTML=day.dishes.map(card).join("");
  let shown=0;
  grid.querySelectorAll(".card").forEach(c=>{
    const ok=filter==="all"||c.dataset.labels.split(" ").includes(filter);
    c.classList.toggle("hide",!ok); if(ok) shown++;
  });
  if(!shown) grid.innerHTML+=`<div class="empty">No dishes match this filter today.</div>`;
}

const nav=document.getElementById("days");
MENU.forEach((day,i)=>{
  const dt=parseDate(day.date);
  const b=document.createElement("button");
  b.innerHTML=`<b>${DAYS[dt.getDay()]}</b><span>${day.date}</span>`;
  b.onclick=()=>{current=i;render();};
  nav.appendChild(b);
});
const today=new Date();today.setHours(0,0,0,0);
const idx=MENU.findIndex(d=>parseDate(d.date).getTime()===today.getTime());
current=idx>=0?idx:0;
document.querySelectorAll(".chip").forEach(c=>c.onclick=()=>{
  filter=c.dataset.f;
  document.querySelectorAll(".chip").forEach(x=>x.classList.toggle("active",x===c));
  render();
});
render();
</script>
</body>
</html>
"""

TEAM = "Özlem Yılmaz<br>Vahdet Can Şahiner<br>Atahan Arslan"


def build_page(menu: list[dict]) -> str:
    data = json.dumps(menu, ensure_ascii=False).replace("</", "<\\/")
    return (TEMPLATE
            .replace("__MENU__", data)
            .replace("__UPDATED__", datetime.now().strftime("%d.%m.%Y %H:%M"))
            .replace("__TEAM__", TEAM))

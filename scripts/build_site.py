#!/usr/bin/env python3
"""Génère le site statique (dossier site/) à partir des documents de docs/sixt/."""
import html, json, re, shutil
from pathlib import Path
import markdown

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "sixt"
OUT = ROOT / "site"

PAGES = [
    ("contexte", "SIXT_Contexte_Complet.md", "Contexte & finances",
     "Identité, gouvernance, actionnariat, chiffres 2025 et S1 2026, financement, risques."),
    ("offres", "SIXT_Offres_Produits_et_Strategie_Commerciale.md", "Offres & vente",
     "Les 11 produits, les prix d'appel, les canaux de vente et le marketing."),
    ("croissance", "SIXT_Strategie_Croissance_Marketing_et_Digital.md", "Croissance & digital",
     "Piliers stratégiques, parts de marché, app, IA, unit economics, playbook."),
    ("style", "SIXT_Style_Ton_et_Voix.md", "Style, ton & voix",
     "ADN de marque, règles d'écriture, gabarits, lexique, checklist."),
]

TAGS = {
    "S": "Source officielle SIXT", "P": "Presse ou site tiers", "A": "Analyse ou source secondaire, à vérifier",
    "D": "Donnée dérivée (calculée)", "I": "Standard interne SIXT", "E": "Exemple original, non officiel",
    "U": "Document fourni par l'utilisateur", "G": "Connaissance générale, à vérifier",
}
TAG_RE = re.compile(r"\[(S|P|A|D|I|E|U|G)((?:\s*[,/+]\s*[^\]\[]{1,60})?)\]")
SKIP_RE = re.compile(r"(<pre.*?</pre>|<code.*?</code>|<[^>]+>)", re.S)


def badge(m):
    letter, rest = m.group(1), m.group(2)
    extra = f" ({html.escape(rest.strip(' ,/+'))})" if rest.strip() else ""
    return f'<span class="tag tag-{letter}" title="{TAGS[letter]}{extra}">{letter}</span>'


def add_badges(h):
    parts = SKIP_RE.split(h)
    return "".join(p if i % 2 else TAG_RE.sub(badge, p) for i, p in enumerate(parts))


def strip_tags(h):
    return html.unescape(re.sub(r"<[^>]+>", " ", h)).replace("\n", " ")


def nav(current):
    items = [f'<a href="index.html" class="{"on" if current == "index" else ""}">Accueil</a>']
    for slug, _, title, _ in PAGES:
        items.append(f'<a href="{slug}.html" class="{"on" if slug == current else ""}">{title}</a>')
    items.append(f'<a href="legende.html" class="{"on" if current == "legende" else ""}">Légende</a>')
    return "\n".join(items)


def layout(slug, title, body, toc=""):
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | Base de connaissances SIXT</title>
<link rel="stylesheet" href="style.css"></head>
<body>
<header class="top">
  <button id="menu" aria-label="Menu">☰</button>
  <a class="brand" href="index.html">SIXT<span>savoir</span></a>
  <div class="search"><input id="q" type="search" placeholder="Rechercher (ex. SIXT ONE, prix, marge EBT)" autocomplete="off"><div id="res"></div></div>
</header>
<div class="wrap">
  <aside id="side"><nav>{nav(slug)}</nav>{toc}</aside>
  <main>{body}
  <footer>Documents générés le 8 octobre 2026. Les tags <span class="tag tag-A">A</span> <span class="tag tag-D">D</span> sont des analyses ou calculs, pas des chiffres publiés par SIXT. <a href="legende.html">Voir la légende</a>.</footer></main>
</div>
<script src="search-index.js"></script><script src="app.js"></script>
</body></html>"""


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    index = []
    for slug, fname, title, _ in PAGES:
        md = markdown.Markdown(extensions=["tables", "toc", "fenced_code", "sane_lists"],
                               extension_configs={"toc": {"toc_depth": "2-3"}})
        h = md.convert((SRC / fname).read_text(encoding="utf-8"))
        h = add_badges(h)
        h = h.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
        # blocs de code : bouton copier
        h = h.replace("<pre>", '<pre class="code"><button class="copy">Copier</button>')
        toc_items = "".join(
            f'<a class="l{t["level"]}" href="#{t["id"]}">{html.escape(html.unescape(t["name"]))}</a>'
            for t in md.toc_tokens for t in [t] + t.get("children", []))
        toc = f'<div class="toc"><h4>Dans cette page</h4>{toc_items}</div>'
        (OUT / f"{slug}.html").write_text(layout(slug, title, f'<article>{h}</article>', toc), encoding="utf-8")
        # index de recherche : une entrée par section h2/h3
        for chunk in re.split(r'(?=<h[23] id=)', h):
            m = re.match(r'<h[23] id="([^"]+)">(.*?)</h[23]>', chunk, re.S)
            if m:
                index.append({"p": slug, "pt": title, "id": m.group(1),
                              "t": strip_tags(re.sub(r'<span class="tag.*?</span>', "", m.group(2))).strip(), "x": strip_tags(chunk)[:6000]})
    (OUT / "search-index.js").write_text("window.IDX=" + json.dumps(index, ensure_ascii=False) + ";", encoding="utf-8")

    cards = "".join(f'<a class="card" href="{s}.html"><h3>{t}</h3><p>{d}</p><span>Ouvrir →</span></a>'
                    for s, _, t, d in PAGES)
    kpis = [("4 283 M€", "CA 2025 (+7,0 %)"), ("9,4 %", "Marge EBT 2025"), ("2 118 M€", "CA S1 2026"),
            ("+2 300", "Agences (juin 2026)"), ("≈ 80 %", "Réservations en ligne"), ("> 1 M", "Utilisateurs actifs de l'app")]
    kp = "".join(f'<div class="kpi"><b>{a}</b><span>{b}</span></div>' for a, b in kpis)
    home = f"""<section class="hero"><h1>Tout savoir sur <em>SIXT</em></h1>
<p>Contexte financier, offres, stratégie de croissance, digital et guide de style : quatre documents réunis, consultables et filtrables par recherche.</p></section>
<div class="kpis">{kp}</div>
<h2 class="sec">Les quatre documents</h2><div class="cards">{cards}</div>
<h2 class="sec">À retenir</h2><ul class="keys">
<li><b>Positionnement</b> : premium à un prix qu'on aime. Caractère de marque « Bold, Fun, Premium ».</li>
<li><b>Modèle</b> : flotte qui croît moins vite que la demande (S1 2026 : CA +11,3 % à taux constants, flotte +9,0 %).</li>
<li><b>Produits</b> : une app, un compte, sept produits (rent, van &amp; truck, share, ride, SIXT+, charge, SIXT ONE).</li>
<li><b>Guidance 2026</b> : CA de 4,45 à 4,60 Md€, marge EBT d'environ 10 %. Prochaine publication : 12 novembre 2026.</li>
</ul>"""
    (OUT / "index.html").write_text(layout("index", "Accueil", home), encoding="utf-8")

    rows = "".join(f'<tr><td><span class="tag tag-{k}">{k}</span></td><td>{v}</td></tr>' for k, v in TAGS.items())
    leg = f"""<article><h1>Légende de fiabilité</h1><p>Chaque information des documents porte un tag qui indique sa provenance. Un chiffre <span class="tag tag-A">A</span>, <span class="tag tag-D">D</span> ou <span class="tag tag-P">P</span> ne doit jamais être présenté comme officiel.</p>
<div class="tw"><table><tr><th>Tag</th><th>Signification</th></tr>{rows}</table></div>
<p>Survolez un tag dans les pages pour voir sa signification.</p></article>"""
    (OUT / "legende.html").write_text(layout("legende", "Légende", leg), encoding="utf-8")

    (OUT / "style.css").write_text(CSS, encoding="utf-8")
    (OUT / "app.js").write_text(JS, encoding="utf-8")
    print(f"Site généré dans {OUT} ({len(index)} sections indexées)")


CSS = """
:root{--o:#FF5000;--k:#1A1A1A;--g:#65696F;--bg:#E9EBEE;--w:#fff}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:70px}
body{margin:0;font:16px/1.6 Helvetica,Roboto,Arial,sans-serif;color:var(--k);background:var(--bg)}
a{color:var(--o)}
.top{position:sticky;top:0;z-index:20;display:flex;gap:16px;align-items:center;background:var(--k);padding:10px 20px}
.brand{color:#fff;font-weight:800;font-size:22px;letter-spacing:.04em;text-decoration:none}
.brand span{color:var(--o);font-weight:400;margin-left:6px;font-size:14px;letter-spacing:0}
#menu{display:none;background:none;border:0;color:#fff;font-size:24px;cursor:pointer}
.search{position:relative;flex:1;max-width:520px;margin-left:auto}
.search input{width:100%;padding:9px 16px;border-radius:999px;border:0;font-size:15px}
#res{position:absolute;top:44px;left:0;right:0;background:#fff;border-radius:12px;box-shadow:0 8px 30px #0003;max-height:70vh;overflow:auto;display:none}
#res a{display:block;padding:10px 16px;color:var(--k);text-decoration:none;border-bottom:1px solid var(--bg)}
#res a:hover{background:var(--bg)}#res small{color:var(--g);display:block}
#res mark{background:#ffd9c7}
.wrap{display:flex;max-width:1400px;margin:0 auto}
aside{width:270px;flex:none;position:sticky;top:58px;align-self:flex-start;max-height:calc(100vh - 58px);overflow:auto;padding:20px}
aside nav a{display:block;padding:8px 12px;border-radius:8px;color:var(--k);text-decoration:none;font-weight:600}
aside nav a:hover{background:#fff}aside nav a.on{background:var(--o);color:#fff}
.toc{margin-top:18px;border-top:1px solid #0002;padding-top:12px}.toc h4{margin:0 0 6px;color:var(--g);font-size:12px;text-transform:uppercase;letter-spacing:.06em}
.toc a{display:block;font-size:13px;line-height:1.35;padding:3px 0;color:var(--g);text-decoration:none}
.toc a.l3{padding-left:12px}.toc a:hover,.toc a.act{color:var(--o)}
main{flex:1;min-width:0;padding:20px 24px 60px}
article,.hero,.kpis,.cards,.keys{max-width:980px}
article{background:#fff;border-radius:16px;padding:28px 36px;box-shadow:0 1px 3px #0001}
article h1{font-size:30px;line-height:1.2;margin-top:0;border-left:6px solid var(--o);padding-left:14px}
article h2{margin-top:2.2em;padding-bottom:6px;border-bottom:2px solid var(--o)}
article h3{margin-top:1.8em}
blockquote{margin:1em 0;padding:10px 18px;background:#fff3ec;border-left:4px solid var(--o);border-radius:0 8px 8px 0}
blockquote p{margin:.4em 0}
.tw{overflow-x:auto;margin:1em 0}
table{border-collapse:collapse;width:100%;font-size:14.5px}
th{background:var(--k);color:#fff;text-align:left;position:sticky;top:0}
th,td{padding:8px 12px;border:1px solid #d5d8dc;vertical-align:top}
tr:nth-child(even) td{background:#f7f8f9}
code{background:#f0f1f3;padding:1px 5px;border-radius:4px;font-size:.92em}
pre.code{position:relative;background:var(--k);color:#f4f4f4;padding:16px;border-radius:10px;overflow:auto}
pre.code code{background:none;color:inherit}.copy{position:absolute;top:8px;right:8px;background:var(--o);color:#fff;border:0;border-radius:6px;padding:4px 10px;cursor:pointer}
hr{border:0;border-top:1px solid #d5d8dc;margin:2em 0}
.tag{display:inline-block;min-width:1.5em;text-align:center;font:700 11px/1.5 Helvetica,Arial,sans-serif;border-radius:4px;padding:0 5px;color:#fff;vertical-align:1px;cursor:help}
.tag-S{background:#22C55E}.tag-P{background:#1658C7}.tag-A{background:#FFBC1F;color:#1A1A1A}
.tag-D{background:#8a4fff}.tag-I{background:#1A1A1A}.tag-E{background:var(--o)}.tag-U{background:#65696F}.tag-G{background:#b0b4ba}
.hero{background:var(--k);color:#fff;border-radius:16px;padding:44px 36px;margin-bottom:20px}
.hero h1{font-size:44px;margin:0 0 10px;line-height:1.1}.hero em{color:var(--o);font-style:normal}.hero p{font-size:18px;color:#ddd;max-width:640px;margin:0}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.kpi{background:#fff;border-radius:12px;padding:16px;border-top:4px solid var(--o)}
.kpi b{display:block;font-size:26px}.kpi span{color:var(--g);font-size:13px}
.sec{margin:32px 0 12px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}
.card{background:#fff;border-radius:14px;padding:20px;color:var(--k);text-decoration:none;display:flex;flex-direction:column;gap:6px;transition:.15s}
.card:hover{transform:translateY(-3px);box-shadow:0 8px 24px #0002}.card h3{margin:0}.card p{margin:0;color:var(--g);font-size:14px;flex:1}.card span{color:var(--o);font-weight:700}
.keys{background:#fff;border-radius:14px;padding:18px 18px 18px 40px}.keys li{margin:8px 0}
footer{max-width:980px;margin-top:24px;font-size:13px;color:var(--g)}
@media(max-width:860px){#menu{display:block}aside{position:fixed;z-index:30;left:0;top:58px;bottom:0;background:var(--bg);transform:translateX(-100%);transition:.2s;box-shadow:4px 0 20px #0003;max-height:none}
aside.open{transform:none}main{padding:12px}article{padding:18px}.hero h1{font-size:32px}}
@media print{.top,aside{display:none}article{box-shadow:none}}
"""

JS = r"""
const side=document.getElementById('side');
document.getElementById('menu').onclick=()=>side.classList.toggle('open');
document.querySelectorAll('.copy').forEach(b=>b.onclick=()=>{navigator.clipboard.writeText(b.parentElement.querySelector('code').innerText);b.textContent='Copié';setTimeout(()=>b.textContent='Copier',1200)});
const q=document.getElementById('q'),res=document.getElementById('res');
const norm=s=>s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();
q.addEventListener('input',()=>{
  const v=norm(q.value.trim());if(v.length<2){res.style.display='none';return}
  const words=v.split(/\s+/);
  const hits=(window.IDX||[]).map(e=>{const t=norm(e.t),x=norm(e.x);
    if(!words.every(w=>t.includes(w)||x.includes(w)))return null;
    return{e,s:words.reduce((a,w)=>a+(t.includes(w)?10:0)+(x.split(w).length-1),0)}}).filter(Boolean)
    .sort((a,b)=>b.s-a.s).slice(0,12);
  res.innerHTML=hits.length?hits.map(({e})=>{const i=norm(e.x).indexOf(words[0]);
    const sn=e.x.slice(Math.max(0,i-50),i+110).replace(/</g,'&lt;');
    return `<a href="${e.p}.html#${e.id}">${e.t}<small>${e.pt} · …${sn}…</small></a>`}).join(''):'<a>Aucun résultat</a>';
  res.style.display='block'});
document.addEventListener('click',e=>{if(!e.target.closest('.search'))res.style.display='none'});
const heads=[...document.querySelectorAll('article h2[id],article h3[id]')];
if(heads.length)addEventListener('scroll',()=>{let c=null;for(const h of heads){if(h.getBoundingClientRect().top<90)c=h.id}
  document.querySelectorAll('.toc a').forEach(a=>a.classList.toggle('act',a.getAttribute('href')==='#'+c))});
"""

if __name__ == "__main__":
    build()

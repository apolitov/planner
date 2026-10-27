#!/usr/bin/env python3
"""Сборка путеводителя «Три дня, семь маршрутов» в стилистике alexe.pt.

python3 build.py → index.html. Данные: content.py (маршруты), photos.json (атрибуция Commons),
highlights.json (фото и точки Komoot), tracks-merged.json + tracks.js (треки), poi.json (заезды, если есть).
"""
import html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = json.load(open(os.path.join(HERE, "photos.json"), encoding="utf-8"))
HL = json.load(open(os.path.join(HERE, "highlights.json"), encoding="utf-8"))
TRACKS = json.load(open(os.path.join(HERE, "tracks-merged.json"), encoding="utf-8"))
POI = json.load(open(os.path.join(HERE, "poi.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, "poi.json")) else {}
from content import ROUTES  # noqa: E402

NB, TH = " ", " "
HL_BY_NAME = {h["name"]: h for v in HL.values() for h in v}


def t(s):
    s = re.sub(r"(\d) (км|м|€|ч|мин|%|кг|мм|человек|велосипед)", lambda m: m.group(1) + NB + m.group(2), s)
    s = re.sub(r"(\d{1,3}) (\d{3})\b", lambda m: m.group(1) + TH + m.group(2), s)
    return s.replace(" — ", NB + "— ")


def esc(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------- фото
def fig(key, caption, full=False):
    base = f"img/{key}"
    if not os.path.exists(os.path.join(HERE, base + ".jpg")):
        return ""
    p = PHOTOS.get(key, {})
    sizes = "100vw" if full else "(max-width: 700px) 100vw, 560px"
    return (f'<figure{" class=\"full\"" if full else ""}><a class="lb" href="{base}.jpg"><img loading="lazy" src="{base}_t.jpg" '
            f'srcset="{base}_t.jpg 800w, {base}.jpg 1920w" sizes="{sizes}" alt="{esc(caption)}"></a>'
            f'<figcaption>{t(esc(caption))} · {esc(p.get("author", "неизвестен"))} · <a href="{esc(p.get("page", "#"))}">{esc(p.get("license", "лицензия"))}</a></figcaption></figure>')


def kfig(name):
    h = HL_BY_NAME.get(name)
    if not h or not h.get("img"):
        return ""
    cap = h.get("note") or h["name"]
    return (f'<figure><a class="lb" href="{esc(h["img"])}"><img loading="lazy" src="{esc(h["img"])}" alt="{esc(h["name"])}"></a>'
            f'<figcaption>{t(esc(cap))} · <a href="{esc(h["url"])}">фото: Komoot, {esc(h["name"])}</a></figcaption></figure>')


def gal(figs, cls="gal"):
    figs = [f for f in figs if f]
    return f'<div class="{cls}">{"".join(figs)}</div>' if figs else ""


# ---------------------------------------------------------------- блоки
def stages(rows):
    out = ['<div class="stw"><table><thead><tr><th>День</th><th>Откуда → куда</th><th>км</th><th>набор</th><th>Покрытие, заметки</th></tr></thead><tbody>']
    for d, seg, km, up, note_ in rows:
        out.append(f"<tr><td class=\"mono\">{t(d)}</td><td>{t(seg)}</td><td class=\"mono\">{t(km)}</td><td class=\"mono\">{t(up)}</td><td>{t(note_)}</td></tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def surface(rows):
    out = ['<div class="stw"><table><thead><tr><th>Участок</th><th>Покрытие</th><th></th></tr></thead><tbody>']
    for seg, cov, url in rows:
        link = f'<a href="{esc(url)}">источник</a>' if url and not url.startswith("#") else (f'<a href="{esc(url)}">↑</a>' if url else "")
        out.append(f"<tr><td>{t(seg)}</td><td>{t(cov)}</td><td class=\"mono\">{link}</td></tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def ul(cls, items):
    return f'<ul class="{cls}">' + "".join(f"<li>{t(i)}</li>" for i in items) + "</ul>"


def links(items):
    return '<ul class="links">' + "".join(
        f'<li><a href="{esc(u)}">{esc(n)}</a>{(" · " + t(d)) if d else ""}</li>' for n, u, d in items) + "</ul>"


def note(title, items, cls="note"):
    return f'<div class="{cls}"><h4>{title}</h4>{ul("", items)}</div>'


def poi_block(rid):
    rows = POI.get(rid) or []
    if not rows:
        return ""
    items = []
    for p in rows:
        head = f'<b>{t(esc(p["name"]))}</b>'
        det = f' <span class="mono soft">{t(esc(p["detour"]))}</span>' if p.get("detour") else ""
        body = t(esc(p.get("what", "")))
        prac = f' <span class="soft">{t(esc(p["prac"]))}</span>' if p.get("prac") else ""
        src = f' <a class="mono" href="{esc(p["url"])}">источник</a>' if p.get("url") else ""
        items.append(f"<li>{head}{det}<br>{body}{prac}{src}</li>")
    return f'<h3>Куда заехать</h3><ul class="poi">{"".join(items)}</ul>'


def komoot_plan(wps):
    la, lo = wps.split("|")[0].split(",")
    q = "&".join("p[%d][loc]=%s" % (j, p) for j, p in enumerate(wps.split("|")))
    return f"https://www.komoot.com/plan/@{la},{lo},9.407z?sport=touringbicycle&{q}"


def tracks_block(rid):
    x = TRACKS.get(rid)
    if not x:
        return ""
    kmup = t("%s км / %d м" % (str(x["km"]).replace(".", ","), x["up"]))
    items = [f'<li><span class="sw"></span><b>Весь маршрут</b> · {t(x["name"])} · <span class="mono">{kmup}</span> · <a href="gpx/{rid}.gpx" download>GPX</a> · <a href="{esc(komoot_plan(x["wps"]))}">план в Komoot</a></li>']
    files = [rid]
    alt = TRACKS.get(rid + "-long")
    if alt:
        kmup2 = t("%s км / %d м" % (str(alt["km"]).replace(".", ","), alt["up"]))
        items.append(f'<li><span class="sw sw--alt"></span><b>Вариант</b> · {t(alt["name"])} · <span class="mono">{kmup2}</span> · <a href="gpx/{rid}-long.gpx" download>GPX</a> · <a href="{esc(komoot_plan(alt["wps"]))}">план в Komoot</a></li>')
        files.append(rid + "-long")
    return (f'<h3>Трек</h3><div class="map" id="map-{rid}" data-files=\'{json.dumps(files)}\'></div><ul class="legend">{"".join(items)}</ul>'
            f'<p class="small">{t("Проложено планировщиком Komoot в режиме велотуризма: велодорожки, тихие дороги и ровный грунт, без троп. Якоря стоят на известных участках. Подложка CyclOSM показывает велодорожки и покрытие. Набор по планировщику, ±20 %.")}</p>')


def segment(s):
    body = "".join(f"<p>{t(p)}</p>" for p in s["text"])
    photos = gal([kfig(n) for n in s.get("photos_k", [])], "gal gal--k")
    return f'<section class="seg"><h3>{t(s["title"])} <span class="hand">{t(s["km"])}</span></h3>{body}{photos}</section>'


def render_route(r):
    fav = '<span class="hand fav">← фаворит</span>' if r["fav"] else ""
    cover = fig(r["cover"], r["cover_cap"], full=True)
    segs = "".join(segment(s) for s in r["segments"])
    commons = gal([fig(k, c) for k, c in r["photos"]])
    return f"""
<article class="route" id="{r['id']}">
  <div class="wrap">
    <p class="kicker mono">Маршрут {r['letter']} · {t(r['days'])} · {t(r['km'])} · набор {t(r['up'])} · {t(r['people'])}</p>
    <h2>{t(r['title'])} {fav}</h2>
    <p class="lead">{t(r['sub'])}</p>
    <p class="tags">{''.join(f'<span>{t(x)}</span>' for x in r['tags'])}</p>
  </div>
  {cover}
  <div class="wrap narrow2">
    <p class="lede">{t(r['lede'])}</p>
    <h3>По дням</h3>
    {stages(r['stages'])}
    {segs}
    <h3>Покрытие по Komoot</h3>
    {surface(r['surface'])}
    {note('⚠ Песок и сложные места', r['sandnotes'], 'note note--sand')}
    {poi_block(r['id'])}
    {note('Логистика', r['prac'])}
    {tracks_block(r['id'])}
    <h3>Нитки и GPX</h3>
    {links(r['tracks'])}
    {commons}
  </div>
</article>"""


REJECTED = [
    ("Нижняя Гуадиана по GR15", "VRSA → Alcoutim 67 км при ~2 000 м набора, по асфальту 51 км и 584 м; Alcoutim → Mértola 36–40 км и 574–637 м. Каменистая пешеходная тропа, по тепловой карте Strava почти никто не ездит. От Mértola до поезда ещё 52–55 км и 600 м до Beja."),
    ("Долина Тежу и Лезирия", "Плоско (Carregado → Golegã 69 км / 330 м), но промзоны, без тени и сервисов до Сантарена, а 6–15 ноября в Голегане Feira Nacional do Cavalo: людно и нет жилья."),
    ("Заброска поездом в Обидуш или Калдаш", "Linha do Oeste от Meleças до Caldas da Rainha закрыта с 16.03.2026, автобусы замены велосипеды не берут; открытие обещают к концу 2026 – началу 2027. Поэтому D только с машиной."),
    ("Уэльва и дамба Одьеля как цель", "Из Уэльвы в Лиссабон поезда нет; возвращаться всё равно к парому в Аямонте, а дамба добавляет 50 км по бетону."),
    ("Экопишты центра, Дору, Минью", "Экопишты по 40–50 км и не стыкуются; север даёт 1 100–1 500 м набора в день."),
]

LOGISTICS = [
    "<b>CP, велосипед в поезде.</b> Бесплатно во всех поездах. В Intercidades только в собранном виде на крюке при брони конкретного места во 2-м классе: места 12 и 18 на линиях Évora и Faro, места 15 и 17 на линиях Porto, Coimbra, Aveiro. Два велосипеда на вагон. На крюк велосипед до 15 кг, сумки снять. Alfa Pendular только разобранным в чехле. Регионалы без брони, решает контролёр.",
    "<b>Fertagus Lisboa → Setúbal.</b> Бесплатно, без ограничений по часам, до двух велосипедов на вагон, из Roma-Areeiro каждые 20 минут, 58 минут в пути.",
    "<b>Паром Setúbal ↔ Tróia (Atlantic Ferries).</b> Велосипед только на ferry, не на катамаран. 5,50 € человек и 5,50 € велосипед. Из Setúbal 07:30 и далее каждый час в :30 до 19:30, затем 20:40 и 22:00; из Tróia каждый час в :00 до 20:00.",
    "<b>Паром Ayamonte ↔ VRSA.</b> 2,50 € человек и 1,60 € велосипед. В воскресенье последний из Ayamonte в 17:15 по Испании (16:15 по Португалии).",
    "<b>Световой день 6–8 ноября.</b> Рассвет около 07:10, закат 17:23–17:31. Чистого света 10 часов 15 минут. При темпе 19 км/ч чистого хода 100 км занимают 5,5 часов хода и 8 часов с остановками.",
    "<b>Расписания CP</b> в силе с 19.07, 06.09 и 20.09.2026, взяты из официальных PDF. Перед покупкой перепроверить в app CP: продажи и бронь велосипедного места открываются там же.",
]

SOURCES = [
    ("CP, Transporte de bicicletas", "https://cp.pt/info/pt/w/transporte-bicicletas"),
    ("CP, расписание Lisboa ↔ Faro / Lagos / VRSA (с 19.07.2026)", "https://www.cp.pt/info/documents/d/cp/comboio-porto-lisboa-faro-lagos-v-r-s-antonio"),
    ("CP, расписание Lisboa ↔ Évora / Beja (с 06.09.2026)", "https://www.cp.pt/info/documents/d/cp/comboios-lisboa-evora-beja"),
    ("CP, расписание Alfa Pendular / Intercidades Lisboa ↔ Norte (с 20.09.2026)", "https://cp.pt/info/documents/d/cp/comboios-alfa-pendular-intercidades-lisboa-norte-sul"),
    ("Fertagus, Transporte de velocípedes", "https://www.fertagus.pt/Fertagus-pt/Viajar/Transporte-de-Velocípedes"),
    ("Atlantic Ferries, расписание низкого сезона 2026", "https://www.atlanticferries.pt/wp-content/uploads/2025/12/Ferries_EpocaBaixa_2026.pdf"),
    ("Паром Ayamonte ↔ VRSA", "https://rioguadiana.net/"),
    ("24notícias, 13.08.2026: автобусы замены Linha do Oeste и велосипеды", "https://24noticias.sapo.pt/"),
    ("EuroVelo Portugal (FPCUB): секции и GPX", "https://euroveloportugal.com/en/route/eurovelo1"),
    ("Bikemap: EuroVelo 1 Portugal, 15 этапов", "https://www.bikemap.net/fr/c/437009/"),
    ("Portuguese Trails: GPX Ecovia do Litoral и EuroVelo Alentejo", "https://www.portuguesetrails.com/en/node/18"),
    ("Caminos Naturales: Vía Verde del Litoral", "https://www.caminosnaturales.es/"),
    ("Diario de Huelva, 17.03.2026: платформа за восстановление виа-верде", "https://www.diariodehuelva.es/articulo/provincia/nace-plataforma-ciudadana-recuperar-via-verde-litoral-entre-gibraleon-ayamonte/20260317131844335266.html"),
    ("Junta de Andalucía, проект EuroVelo 1 tramo 3", "https://www.juntadeandalucia.es/sites/default/files/inline-files/2025/01/TAA4005APR1%20DOC01%20MEMORIA%20V03.pdf"),
    ("Fundação Mata do Buçaco", "https://fmb.pt/"),
    ("Center of Portugal: Estrada Atlântica и Ecovia do Mondego", "https://www.centerofportugal.com/article/atlantic-road-cycling-path"),
    ("APA: заполнение водохранилищ, 19.10.2026", "https://www.apambiente.pt/"),
    ("Strava Global Heatmap (гравел), снимки 27.10.2026", "https://www.strava.com/maps/global-heatmap?sport=GravelRide"),
    ("Komoot: туры, хайлайты и планировщик (ссылки в карточках)", "https://www.komoot.com/"),
    ("Wikiloc: треки (ссылки в карточках)", "https://www.wikiloc.com/"),
    ("AllTrails: трейлы Алентежу и Алгарве", "https://www.alltrails.com/"),
    ("Wikimedia Commons: фотографии, авторы и лицензии в подписях", "https://commons.wikimedia.org/"),
]

CSS = """
:root{--paper:#ffffff;--ink:#141414;--soft:#5f5f5c;--line:#e4e2dc;--marker:#ffd83d;--tint:#f6f5f1;--sand:#fff3c2;
--sans:"Onest",system-ui,sans-serif;--mono:"JetBrains Mono",ui-monospace,monospace;--hand:"Caveat",cursive}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font:400 18px/1.55 var(--sans);-webkit-font-smoothing:antialiased}
a{color:inherit}
a:focus-visible{outline:3px solid var(--marker);outline-offset:3px}
img{max-width:100%;display:block}
.wrap{max-width:1120px;margin:0 auto;padding:0 24px}
.narrow2{max-width:760px;margin-left:auto;margin-right:auto}
.mono{font-family:var(--mono);font-size:14px}
.soft{color:var(--soft)}
.small{font:400 13px/1.5 var(--mono);color:var(--soft)}
.hand{font:600 22px/1 var(--hand);white-space:nowrap;margin-left:6px;color:var(--ink)}
mark{color:inherit;padding:0 .12em;margin:0 -.12em;background:linear-gradient(transparent 52%,var(--marker) 52%,var(--marker) 92%,transparent 92%);border-radius:2px}
p a{text-decoration:none;background:linear-gradient(transparent 60%,var(--marker) 60%,var(--marker) 92%,transparent 92%)}
.top{display:flex;align-items:center;justify-content:space-between;padding:22px 0;font-size:15px}
.top__logo{display:block;width:30px;height:30px}
.top__link{font-family:var(--mono);font-size:13px;text-decoration:none;color:var(--soft)}
.top__link:hover{color:var(--ink)}
.hero{text-align:center;padding:56px 0 36px}
.hero h1{margin:0 0 18px;font-weight:700;letter-spacing:-.035em;line-height:.98;font-size:clamp(46px,9vw,104px)}
.hero .role{margin:0 0 30px;font:500 14px/1.4 var(--mono);letter-spacing:.02em;color:var(--soft)}
.hero p.lead{font-size:clamp(20px,2.6vw,26px);font-weight:500;line-height:1.3;letter-spacing:-.01em;margin:0 auto 18px;max-width:760px;text-wrap:pretty}
.hero p{margin:0 auto 12px;max-width:680px;text-wrap:pretty}
.heroimg{max-width:1120px;margin:28px auto 0;padding:0 24px}
.heroimg img{width:100%;aspect-ratio:21/9;object-fit:cover;border-radius:16px;border:1.5px solid var(--ink);transform:rotate(-1deg)}
.heroimg figcaption{text-align:right;font:400 12px/1.4 var(--mono);color:var(--soft);padding:12px 8px 0}
.heroimg figcaption a{color:inherit}
nav.chips{position:sticky;top:0;z-index:50;background:#fffffff2;backdrop-filter:blur(8px);border-bottom:1.5px solid var(--ink)}
nav.chips .in{display:flex;gap:8px;overflow-x:auto;padding:10px 24px;scrollbar-width:none;max-width:1120px;margin:0 auto}
nav.chips .in::-webkit-scrollbar{display:none}
nav.chips a{flex:0 0 auto;font:500 13px/1 var(--mono);text-decoration:none;color:var(--ink);padding:9px 14px;border:1.5px solid var(--ink);border-radius:999px;white-space:nowrap;background-color:var(--paper);background-image:linear-gradient(transparent 50%,var(--marker) 50%,var(--marker) 96%,transparent 96%);background-repeat:no-repeat;background-size:0% 100%;transition:background-size .3s}
nav.chips a:hover,nav.chips a.fav{background-size:100% 100%}
.block{padding:56px 0 24px}
.block h2{margin:0 0 20px;font-size:clamp(28px,4vw,40px);font-weight:700;letter-spacing:-.025em;line-height:1.1}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;padding:12px 0 40px}
.card{display:block;border:1.5px solid var(--ink);border-radius:16px;padding:16px 20px 20px;background:var(--paper);text-decoration:none;position:relative;transition:box-shadow .15s,transform .15s}
.card:hover{transform:translate(-3px,-3px);box-shadow:6px 6px 0 var(--marker)}
.card .l{font:700 44px/1 var(--sans);letter-spacing:-.03em;margin:0 0 6px}
.card h2{margin:0 0 8px;font-size:19px;font-weight:700;letter-spacing:-.01em;line-height:1.25}
.card p{margin:0;font-size:15px;line-height:1.5;color:#2c2c2a}
.card .m{margin-top:10px;font:400 13px/1.6 var(--mono);color:var(--soft)}
.card .hand{position:absolute;right:16px;top:14px;transform:rotate(-6deg)}
table{width:100%;border-collapse:collapse;font-size:16px}
th{text-align:left;font:400 13px/1.4 var(--mono);color:var(--soft);padding:0 16px 8px 0;border-bottom:1.5px solid var(--ink)}
td{padding:12px 16px 12px 0;border-bottom:1px solid var(--line);vertical-align:top}
td.mono{white-space:nowrap}
.stw{overflow-x:auto;margin:0 0 8px}
.stw table{min-width:560px}
.route{padding:72px 0 24px;border-top:1.5px solid var(--ink)}
.route .kicker{margin:0 0 12px;font:500 13px/1.4 var(--mono);letter-spacing:.02em;color:var(--soft);text-transform:uppercase}
.route h2{margin:0 0 14px;font-size:clamp(32px,5vw,54px);font-weight:700;letter-spacing:-.03em;line-height:1.05}
.route .lead{margin:0 0 14px;font-size:clamp(19px,2.2vw,23px);font-weight:500;line-height:1.3;letter-spacing:-.01em;color:#2c2c2a}
.tags{margin:0 0 24px}
.tags span{display:inline-block;font:500 13px/1 var(--mono);border:1.5px solid var(--ink);border-radius:999px;padding:7px 12px;margin:0 6px 8px 0}
figure{margin:0}
figure.full{margin:0 auto 28px;max-width:1120px;padding:0 24px}
figure.full img{width:100%;max-height:68vh;object-fit:cover;border-radius:16px;border:1.5px solid var(--ink)}
figcaption{font:400 12px/1.5 var(--mono);color:var(--soft);padding:8px 2px 0}
figcaption a{color:inherit}
.lede{font-size:19px;margin:0 0 22px;text-wrap:pretty}
.route h3{margin:40px 0 14px;font-size:26px;font-weight:700;letter-spacing:-.015em;line-height:1.2}
.route p{margin:0 0 14px;text-wrap:pretty}
.seg{padding:6px 0 10px}
.seg h3 .hand{font-size:20px;color:var(--soft)}
.gal{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:12px 0 10px}
.gal img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:12px;border:1.5px solid var(--ink)}
.gal--k{grid-template-columns:repeat(3,1fr)}
.gal--k img{aspect-ratio:1/1}
.gal:not(:has(figure + figure)){grid-template-columns:1fr}
.gal:not(:has(figure + figure)) img{aspect-ratio:16/9}
a.lb img{cursor:zoom-in}
ul.poi,ul.links,ul.legend,ul.plain{list-style:none;margin:0 0 10px;padding:0}
ul.poi li,ul.links li,ul.legend li,ul.plain li{padding:10px 0;border-bottom:1px solid var(--line);font-size:16.5px;line-height:1.45}
ul.poi li b{font-weight:600}
ul.links li a,ul.legend li a{text-decoration:none;background:linear-gradient(transparent 60%,var(--marker) 60%,var(--marker) 92%,transparent 92%)}
.note{margin:24px 0;padding:18px 22px;background:var(--tint);border-radius:14px;font-size:16.5px}
.note--sand{background:var(--sand)}
.note h4{margin:0 0 8px;font:400 13px/1.4 var(--mono);color:var(--soft);text-transform:uppercase;letter-spacing:.06em}
.note ul{list-style:none;margin:0;padding:0}
.note li{padding:5px 0 5px 1.2em;position:relative}
.note li::before{content:"›";position:absolute;left:.2em;color:var(--ink);font-weight:700}
.map{height:460px;border:1.5px solid var(--ink);border-radius:16px;margin:8px 0 10px;background:var(--tint);overflow:hidden}
@media(max-width:560px){.map{height:360px}}
.sw{display:inline-block;width:14px;height:14px;border-radius:3px;background:var(--ink);vertical-align:-2px;margin-right:.5rem}
.sw--alt{background:var(--marker);border:1.5px solid var(--ink)}
.leaflet-container{font:inherit}
.rej{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:0 0 20px}
.rej div{border:1.5px solid var(--ink);border-radius:16px;padding:16px 20px 18px}
.rej h5{margin:0 0 6px;font-size:19px;font-weight:700;letter-spacing:-.01em;line-height:1.2}
.rej p{margin:0;font-size:15.5px;color:#2c2c2a}
.end{padding:64px 0 24px;border-top:1.5px solid var(--ink)}
.end h2{margin:0 0 20px;font-size:clamp(28px,4vw,40px);font-weight:700;letter-spacing:-.025em;line-height:1.1}
.foot{padding:36px 0;text-align:center;font:400 13px/1.4 var(--mono);color:var(--soft)}
#lbox{position:fixed;inset:0;background:#141414f0;display:none;align-items:center;justify-content:center;z-index:99;cursor:zoom-out}
#lbox.on{display:flex}
#lbox img{max-width:94vw;max-height:94vh;object-fit:contain;border-radius:8px}
@media(max-width:960px){.cards{grid-template-columns:repeat(2,1fr)}}
@media(max-width:640px){body{font-size:17px}.wrap{padding:0 16px}.hero{padding:36px 0 24px}.cards,.rej{grid-template-columns:1fr}.gal,.gal--k{grid-template-columns:1fr}.gal--k img{aspect-ratio:4/3}figure.full{padding:0 16px}.heroimg{padding:0 16px}.heroimg img{aspect-ratio:4/3}.card .hand{position:static;display:block;transform:none;margin:0 0 6px}}
"""

LOGO = '<svg class="top__logo" viewBox="0 0 32 32" aria-hidden="true"><rect x="2" y="2" width="28" height="28" rx="7" fill="none" stroke="#141414" stroke-width="2.6"/><path d="M9 22.5h14" stroke="#ffd83d" stroke-width="6" stroke-linecap="round" fill="none"/></svg>'


def render():
    nav = "".join(f'<a href="#{r["id"]}"{" class=\"fav\"" if r["fav"] else ""}>{r["letter"]} · {esc(r["short"])}</a>' for r in ROUTES)
    nav += '<a href="#rej">отсев</a><a href="#fin">поезда и паромы</a>'
    cards = "".join(
        f'<a class="card" href="#{r["id"]}">{"<span class=\"hand\">← сюда хочу</span>" if r["fav"] else ""}<p class="l">{r["letter"]}</p><h2>{t(esc(r["title"]))}</h2><p>{t(esc(r["sub"]))}</p><p class="m">{t(esc(r["days"]))} · {t(esc(r["km"]))} · {t(esc(r["up"]))} · {t(esc(r["people"]))}</p></a>'
        for r in ROUTES)
    rej = "".join(f"<div><h5>{t(n)}</h5><p>{t(d)}</p></div>" for n, d in REJECTED)
    logi = "".join(f"<li>{t(x)}</li>" for x in LOGISTICS)
    src = "".join(f'<li><a href="{esc(u)}">{esc(n)}</a></li>' for n, u in SOURCES)
    ck = "d/nazare-sitio"
    cp = PHOTOS.get(ck, {})
    out = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Гравел на три дня</title>
<meta name="description" content="Семь веломаршрутов по Португалии и Уэльве на 6–8 ноября 2026: куски маршрута, покрытие, песок, куда заехать, поезда, треки и фото">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect x='2' y='2' width='28' height='28' rx='7' fill='none' stroke='%23141414' stroke-width='2.6'/><path d='M9 22.5h14' stroke='%23ffd83d' stroke-width='6' stroke-linecap='round' fill='none'/></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;600&family=JetBrains+Mono:wght@400;500&family=Onest:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <header class="top"><a class="top__domain" href="https://alexe.pt/" aria-label="alexe.pt">{LOGO}</a><a class="top__link" href="https://alexe.pt/">alexe.pt</a></header>
  <section class="hero">
    <p class="role">Гравел · 6–8 ноября 2026 · двое · поезд</p>
    <h1>Три дня, семь маршрутов</h1>
    <p class="lead">{t('Португалия и ближняя Уэльва: до 220 км, 75–100 км в день, <mark>поменьше холмов, побольше воды</mark>, малолюдно.')}</p>
    <p>{t('Trek Checkpoint на 38 мм с сумками, ночёвки в отелях, заброска поездом или машиной, обратно поездом. Асфальт допустим, главное чтобы ехать было комфортно.')}</p>
  </section>
</div>
<figure class="heroimg"><img src="img/{ck}.jpg" alt="Назаре с Ситиу" fetchpriority="high"><figcaption>Назаре с мирадора Суберку · {esc(cp.get("author", ""))} · <a href="{esc(cp.get("page", "#"))}">{esc(cp.get("license", ""))}</a></figcaption></figure>

<nav class="chips"><div class="in">{nav}</div></nav>

<div class="wrap">
  <section class="block">
    <h2>Как читать</h2>
    <div class="narrow2" style="margin-left:0">
    <p>{t('Три фаворита стоят первыми: <mark>D с заброской машиной в Обидуш</mark>, <mark>E как самый ровный</mark>, <mark>C как самый безлюдный</mark>. У них есть треки, расширение в лес Бусако и список заездов. Остальные четыре тоже проходимы и описаны так же: по кускам, с покрытием и фото.')}</p>
    <p>{t('Цифры набора из планировщика Komoot и официальных GPX EuroVelo, точность ±20 %. Покрытие в процентах из записанных туров Komoot на том же участке. Людность по тепловой карте Strava для гравела. Песок отмечен там, где его видели источники 2019–2026 годов; свежих полевых отчётов за осень 2026 нет ни по одному участку. Отели в ноябре не проверены: названы города, где жильё есть круглый год.')}</p>
    </div>
    <div class="cards">{cards}</div>
  </section>
</div>

{''.join(render_route(r) for r in ROUTES)}

<section class="route" id="rej"><div class="wrap">
  <p class="kicker mono">Отсев</p>
  <h2>Что не вошло и почему</h2>
  <div class="rej">{rej}</div>
</div></section>

<section class="end" id="fin"><div class="wrap narrow2">
  <h2>Поезда, паромы, свет</h2>
  <ul class="plain">{logi}</ul>
  <h2 style="margin-top:48px">Источники</h2>
  <ul class="plain small" style="font-size:14px">{src}</ul>
  <p class="small">{t('Данные собраны 27.10.2026. Фотографии с Wikimedia Commons под свободными лицензиями, авторы в подписях; кадры Komoot показаны по ссылке с указанием источника. Страница для личного пользования.')}</p>
</div></section>
<p class="foot">гравел · ноябрь 2026 · собрано из открытых источников · <a href="https://alexe.pt/">alexe.pt</a></p>

<div id="lbox"><img alt=""></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script src="tracks.js"></script>
<script>
(function(){{
  if(!window.L||!window.TRACKS)return;
  document.querySelectorAll('.map').forEach(el=>{{
    const files=JSON.parse(el.dataset.files);
    const m=L.map(el,{{scrollWheelZoom:false}});
    L.tileLayer('https://{{s}}.tile-cyclosm.openstreetmap.fr/cyclosm/{{z}}/{{x}}/{{y}}.png',{{maxZoom:18,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> · <a href="https://www.cyclosm.org">CyclOSM</a>'}}).addTo(m);
    const all=[];
    files.forEach((f,i)=>{{
      const pts=window.TRACKS[f]; if(!pts)return;
      L.polyline(pts,{{color:i?'#ffd83d':'#141414',weight:i?5:4,opacity:i?.95:.9,dashArray:i?'2 8':null}}).addTo(m);
      if(!i){{L.circleMarker(pts[0],{{radius:7,color:'#141414',fillColor:'#ffd83d',fillOpacity:1,weight:2}}).addTo(m);
      L.circleMarker(pts[pts.length-1],{{radius:7,color:'#141414',fillColor:'#ffffff',fillOpacity:1,weight:2}}).addTo(m);}}
      all.push(...pts);
    }});
    if(all.length)m.fitBounds(L.latLngBounds(all),{{padding:[20,20]}});
  }});
}})();
const lbox=document.getElementById('lbox');
document.addEventListener('click',e=>{{
  const a=e.target.closest('a.lb');
  if(a){{e.preventDefault();lbox.querySelector('img').src=a.getAttribute('href');lbox.classList.add('on');}}
  else if(e.target.closest('#lbox')){{lbox.classList.remove('on');}}
}});
document.addEventListener('keydown',e=>{{if(e.key==='Escape')lbox.classList.remove('on');}});
</script>
</body>
</html>"""
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
        f.write(out)
    print("index.html", len(out.encode()), "bytes")


if __name__ == "__main__":
    render()

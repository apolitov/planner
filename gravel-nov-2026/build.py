#!/usr/bin/env python3
"""Сборка одностраничника «Гравел на 2–3 дня, 6–8 ноября 2026».

python3 build.py  →  index.html рядом. Фото берутся из img/<route>/<name>.jpg + _t.jpg,
атрибуция — из photos.json (author, license, page). Нет файла — карточка фото пропускается.
"""
import html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = json.load(open(os.path.join(HERE, "photos.json"), encoding="utf-8"))
TRACKS = json.load(open(os.path.join(HERE, "tracks-merged.json"), encoding="utf-8"))
TRACKCOL = {"d": "#1F5A3C", "e": "#2F5D9E", "c": "#B96F1E"}


def komoot_plan(wps):
    la, lo = wps.split("|")[0].split(",")
    q = "&".join("p[%d][loc]=%s" % (j, p) for j, p in enumerate(wps.split("|")))
    return f"https://www.komoot.com/plan/@{la},{lo},9.407z?sport=touringbicycle&{q}"


def tracks_block(rid):
    """Карта с одним треком на маршрут, GPX и план Komoot; для C ещё длинный вариант второго дня."""
    x = TRACKS.get(rid)
    if not x:
        return ""
    col = TRACKCOL.get(rid, "#1F5A3C")
    kmup = t("%s км / %d м" % (str(x["km"]).replace(".", ","), x["up"]))
    items = [f'<li><span class="sw" style="background:{col}"></span><b>Весь маршрут</b> · {t(x["name"])} · <span class="mono">{kmup}</span> · '
             f'<a href="gpx/{rid}.gpx" download>GPX</a> · <a href="{html.escape(komoot_plan(x["wps"]))}">план в Komoot</a></li>']
    alt = TRACKS.get(rid + "-long")
    files = [rid]
    if alt:
        kmup2 = t("%s км / %d м" % (str(alt["km"]).replace(".", ","), alt["up"]))
        items.append(f'<li><span class="sw" style="background:{col};opacity:.45"></span><b>Вариант</b> · {t(alt["name"])} · <span class="mono">{kmup2}</span> · '
                     f'<a href="gpx/{rid}-long.gpx" download>GPX</a> · <a href="{html.escape(komoot_plan(alt["wps"]))}">план в Komoot</a></li>')
        files.append(rid + "-long")
    return (f'<h4>Трек</h4><div class="map" id="map-{rid}" data-files=\'{json.dumps(files)}\' data-col="{col}"></div>'
            f'<ul class="legend">{"".join(items)}</ul>'
            f'<p class="small">{t("Проложено планировщиком Komoot в режиме велотуризма: велодорожки, тихие дороги и ровный грунт, без троп. Якорные точки стоят на известных участках (просека Лейрии, дамба Мондегу, экопишта, дюнная дорога Миры). Подложка CyclOSM показывает велодорожки и покрытие. Набор по планировщику, ±20 %.")}</p>')



NB = " "   # неразрывный пробел
TH = " "   # тонкий (разряды)


def t(s):
    """Типографика: число+единица и разряды через неразрывные пробелы."""
    s = re.sub(r"(\d) (км|м|€|ч|мин|%|кг|мм|человек|велосипед)", lambda m: m.group(1) + NB + m.group(2), s)
    s = re.sub(r"(\d{1,3}) (\d{3})\b", lambda m: m.group(1) + TH + m.group(2), s)
    s = s.replace(" — ", NB + "— ")
    return s


def fig(key, caption, full=False):
    """Фигура с лайтбоксом. key = 'd/obidos-lagoa'."""
    base = f"img/{key}"
    if not os.path.exists(os.path.join(HERE, base + ".jpg")):
        return ""
    p = PHOTOS.get(key, {})
    author = html.escape(p.get("author", "неизвестен"))
    lic = html.escape(p.get("license", "см. страницу файла"))
    page = html.escape(p.get("page", "https://commons.wikimedia.org/"))
    sizes = "100vw" if full else "(max-width: 700px) 100vw, 640px"
    img = (f'<a class="lb" href="{base}.jpg"><img loading="lazy" src="{base}_t.jpg" '
           f'srcset="{base}_t.jpg 800w, {base}.jpg 1920w" sizes="{sizes}" alt="{html.escape(caption)}"></a>')
    cap = f'<figcaption>{t(html.escape(caption))} · {author} · <a href="{page}">{lic}</a></figcaption>'
    cls = ' class="full"' if full else ""
    return f"<figure{cls}>{img}{cap}</figure>"


def ext_fig(url, caption, source, link):
    """Внешнее фото (Komoot/AllTrails) — по ссылке, без копии у нас."""
    return (f'<figure><a class="lb" href="{html.escape(url)}"><img loading="lazy" src="{html.escape(url)}" '
            f'alt="{html.escape(caption)}"></a><figcaption>{t(html.escape(caption))} · фото: '
            f'<a href="{html.escape(link)}">{html.escape(source)}</a></figcaption></figure>')


def gal(*figs):
    figs = [f for f in figs if f]
    return f'<div class="gal">{"".join(figs)}</div>' if figs else ""


def stages(rows):
    out = ['<div class="stw"><table class="st"><thead><tr><th>День</th><th>Откуда → куда</th><th>км</th><th>набор</th><th>Покрытие, заметки</th></tr></thead><tbody>']
    for d, seg, km, up, note in rows:
        out.append(f"<tr><td>{d}</td><td>{t(seg)}</td><td>{t(km)}</td><td>{t(up)}</td><td>{t(note)}</td></tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def ul(cls, items):
    return f'<ul class="{cls}">' + "".join(f"<li>{t(i)}</li>" for i in items) + "</ul>"


def links(items):
    return '<ul class="links">' + "".join(
        f'<li><a href="{html.escape(u)}">{html.escape(n)}</a>{(" — " + t(d)) if d else ""}</li>' for n, u, d in items) + "</ul>"


def prac(title, items):
    return f'<div class="prac"><div class="t">{title}</div>{ul("", items)}</div>'


def sand(items):
    return f'<div class="sand"><div class="t">⚠ Песок и сложные места</div>{ul("", items)}</div>'


# ----------------------------------------------------------------------------
# Маршруты
# ----------------------------------------------------------------------------
ROUTES = []

ROUTES.append(dict(
    id="d", letter="D", short="Обидуш → Коимбра", fav=True,
    title="Обидуш → Назаре → сосняк Лейрии → Фигейра → Мондегу → Коимбра",
    sub="Заброска машиной в Обидуш, назад поездом из Коимбры",
    days="3 дня", km="165–175 км", up="~1 100–1 300 м", people="малолюдно",
    tags=["лагуна", "океан", "сосновый лес", "река", "замки", "Коимбра"],
    cover="d/nazare-sitio", cover_cap="Назаре (Nazaré) с мирадора Субéрку на Ситиу",
    lede="Единственный маршрут с заброской машиной, и этим он ценен: из Лиссабона нет поезда с велосипедом ни в Обидуш, ни в Калдаш. Дальше всё линейно на север: лагуна Обидуша, Назаре, 60 км бетонной велодорожки сквозь сосняк Лейрии, эстуарий Мондегу и финиш в Коимбре, откуда Intercidades везёт домой.",
    body=[
        "Первый день самый горбатый: холмы Серра-ду-Бору между Фош-ду-Арелью и Сан-Мартинью и подъём на Ситиу в Назаре. Если выезд из Лиссабона ранний, можно добить до Сан-Педру-де-Моэл (São Pedro de Moel), но там в ноябре с жильём хуже, чем в Назаре, поэтому базовый план ночует в Назаре.",
        "Второй день ровный и быстрый: EuroVelo 1 здесь идёт по велодорожке Estrada Atlântica, на 87 % твёрдой (бетон и асфальт), с одной прямой через Mata Nacional de Leiria на десятки километров. После Педрогана лес сменяется дюнами и солеварнями у устья Мондегу.",
        "Третий день по дамбам Байшу-Мондегу: самый накатанный плоский гравий в выборке по тепловой карте Strava, но дорога вдоль канала после Фигейры вся в ямах, а вид местами закрывает дамба. В Монтемор стоит заехать ради замка, в Коимбре финиш у Шупала (Mata Nacional do Choupal).",
    ],
    stages=[
        ("Пт 6.11", "Óbidos → Foz do Arelho → São Martinho do Porto → Nazaré", "~40 км", "~550 м", "асфальт и гравий у лагуны; подъёмы Serra do Bouro; EV1 секция 19 по GPX ~520 м"),
        ("Сб 7.11", "Nazaré → São Pedro de Moel → Praia da Vieira → Pedrógão → Figueira da Foz", "81 км", "~430 м", "велодорожка Estrada Atlântica, бетон и асфальт 87 %; Komoot-тур 2025: 104 км / 590 м с заездами"),
        ("Вс 8.11", "Figueira da Foz → Montemor-o-Velho → Coimbra", "43–55 км", "~130 м", "дамбы Мондегу: асфальт с ямами и ~25–50 % грунта; ж/д мост не пересечь"),
    ],
    sandnotes=[
        "Серра-ду-Бору (Serra do Bouro) между Foz do Arelho и São Martinho: короткие, но крутые холмы, набор дня в основном здесь.",
        "Подъём на Ситиу в Назаре: фуникулёр возит велосипеды, но с сентября 2025 его закрывали, проверить на месте; объезд по дороге.",
        "Сосняк Лейрии: шторм Kristin в январе 2026 повалил около 100 тыс. м³ леса; главные дороги и велодорожка расчищены, второстепенные просеки могут быть завалены. Держаться Estrada Atlântica.",
        "Мондегу: дорога вдоль канала после Фигейры «постоянный слалом между ямами» (Komoot), участок 150 м с запретом езды (вести), железнодорожный мост через реку на велосипеде не пересечь, нужен длинный объезд. Северный ветер в лицо на дамбах.",
        "Глубокого песка на нитке нет ни по одному источнику; песчаные тропы только в стороне, к пляжам.",
    ],
    see=[
        "<b>Обидуш (Óbidos)</b>: стены замка и улица Direita до старта, 6 км до лагуны.",
        "<b>Лагуна Обидуша (Lagoa de Óbidos)</b>: гравийная тропа по южному берегу, мирадор Atlântico над Foz do Arelho.",
        "<b>Сан-Мартинью-ду-Порту</b>: круглая бухта-ракушка, вид с дороги на Salir do Porto.",
        "<b>Назаре</b>: Ситиу, мирадор Суберку, форт Сан-Мигел с музеем больших волн; в ноябре сезон свеллов.",
        "<b>Пенеду-да-Саудаде</b>: маяк на утёсе у São Pedro de Moel.",
        "<b>Mata Nacional de Leiria</b>: сосняк XIII века, посаженный от дюн; лагуна Ervedeira с кафе на км 57 тура.",
        "<b>Эстуарий Мондегу</b>: солеварни, рис, остров Morraceira, монастырь Seiça, приливная мельница у Alqueidão.",
        "<b>Монтемор-у-Велью</b>: замок над долиной, лучший обзор на Байшу-Мондегу.",
        "<b>Коимбра</b>: университет, библиотека Жуанина, Шупал.",
    ],
    prac=[
        "Заброска: машиной до Óbidos, высадка у стен. Из Лиссабона ~1 ч.",
        "Обратно: IC Coimbra-B → Lisboa Santa Apolónia, в воскресенье последние 18:56, 20:20 и 20:56 (в Oriente 22:53). Велосипед на местах 15 и 17 во 2-м классе, бронь в app CP.",
        "Запасные выходы: станции Valado-Nazaré, Leiria и Figueira да Foz на линии Caldas ↔ Coimbra-B (около 5 поездов в день); из Figueira в Coimbra-B каждый час в xx:58.",
        "Ночёвки: Nazaré (много круглогодичного жилья), Figueira da Foz (много). Работа конкретных отелей в ноябре не проверялась.",
        "Световой день 07:10–17:25.",
    ],
    tracks=[
        ("EuroVelo 1 Portugal, секции 19–22 (официальные GPX, 2023)", "https://euroveloportugal.com/en/route/eurovelo1", "Foz do Arelho → Nazaré → Praia da Vieira → Marinha das Ondas → Figueira"),
        ("Komoot: Óbidos → Nazaré → São Pedro de Moel (план, гравел)", "https://www.komoot.com/plan/@39.362066,-9.157156,9.407z?sport=mtb_easy&p[0][loc]=39.3619514,-9.1571530&p[1][loc]=39.4329582,-9.2173901&p[2][loc]=39.5135311,-9.1335905&p[3][loc]=39.6029108,-9.0701572&p[4][loc]=39.7579326,-9.0293991", "61 км / 750 м"),
        ("Komoot: Figueira da Foz → Nazaré (тур, май 2025)", "https://www.komoot.com/tour/2256367100", "104 км / 590 м, велодорожка 56 км"),
        ("Komoot: Lagoa de Óbidos Gravel Trail, петля от Caldas", "https://www.komoot.com/smarttour/32136538", "45 км / 415 м, местами вести"),
        ("Komoot: Nazaré road to the top + Atlantic Coast Cycle Path", "https://www.komoot.com/smarttour/23775095", "47 км / 446 м"),
        ("Komoot: Mondego Cycle Path, петля от Fontela", "https://www.komoot.com/smarttour/32157391", "39 км / 105 м, 25 % грунт"),
        ("Komoot: Figueira → Montemor → Coimbra (план, гравел)", "https://www.komoot.com/plan/@40.148463,-8.855657,9.407z?sport=mtb_easy&p[0][loc]=40.1485808,-8.8556550&p[1][loc]=40.1726640,-8.6845418&p[2][loc]=40.2111874,-8.4291478", "43 км / 131 м"),
        ("Bikemap: EuroVelo 1 Portugal, этапы Vieira → São Martinho и далее", "https://www.bikemap.net/fr/c/437009/", "покрытие по этапам"),
    ],
    photos=[("d/obidos-lagoa", "Лагуна Обидуша"), ("d/obidos-vila", "Стены Обидуша"), ("d/sao-pedro-de-moel", "Маяк Пенеду-да-Саудаде"),
            ("d/pinhal-leiria", "Велодорожка в сосняке Лейрии"), ("d/montemor", "Замок Монтемор-у-Велью"), ("d/coimbra", "Коимбра над Мондегу")],
    ext_photos=[("https://d2exd72xrrp1s7.cloudfront.net/www/000/1k8/f0/f0iby27besqz0j9xe755dc84yt0sbo7-uhi71669380/0", "Прямая через Mata Nacional de Leiria", "Komoot", "https://www.komoot.com/highlight/6583523"),
                ("https://d2exd72xrrp1s7.cloudfront.net/www/1p/1pyqfixq2mg2g1bcow564jzuwf4yitvi0t-p445885796-full/18f11472315", "Гравийная тропа лагуны Обидуша", "Komoot", "https://www.komoot.com/smarttour/32136538")],
))

ROUTES.append(dict(
    id="e", letter="E", short="Авейру → Коимбра", fav=True,
    title="Риа-де-Авейру → Коста-Нова → Мира → Фигейра → Коимбра",
    sub="Самый ровный вариант: лагуны, дюны и дамбы Мондегу",
    days="2–3 дня", km="120–165 км", up="~450–550 м", people="малолюдно",
    tags=["лагуна", "океан", "дюны", "сосновый лес", "Коимбра"],
    cover="e/costa-nova", cover_cap="Полосатые палейруш Коста-Новы (Costa Nova)",
    lede="Если главный критерий ровно, это он: от Авейру до Коимбры нет ни одного настоящего подъёма. Плата за это однообразие: вторая половина первого дня идёт сосняком и дюнами, где пейзаж не меняется километрами. Зато соль, лагуны, птицы и полосатые дома.",
    body=[
        "Из Лиссабона Intercidades довозит до Авейру к девяти утра, и день начинается с солеварен и каналов. Дальше по дюнной дороге Costa Nova → Vagueira → Praia de Mira, самой накатанной гравийной оси региона по тепловой карте Strava. Дорогу Mira → Quiaios к весне 2025 заасфальтировали.",
        "Маршрут можно сжать в два дня (Aveiro → Figueira 76 км и Figueira → Coimbra 45 км) или растянуть на три с петлёй по мосткам Риа-де-Авейру в первый день и подъёмом на Серра-да-Боа-Виажен ради вида с мыса Мондегу во второй.",
        "Третий день совпадает с третьим днём маршрута D: дамбы Байшу-Мондегу, замок Монтемор, Шупал в Коимбре.",
    ],
    stages=[
        ("Пт 6.11", "Aveiro → салинас → Costa Nova → Vagueira → Praia de Mira (с петлёй по мосткам риа)", "40–65 км", "~100 м", "асфальт и велодорожки; EV1 секция 24: 27 км / ~45 м"),
        ("Сб 7.11", "Praia de Mira → Tocha → Quiaios → (Serra da Boa Viagem) → Figueira da Foz", "45–55 км", "~270–400 м", "EV1 секция 23; Mira → Quiaios асфальт с 2025; подъём на серру по желанию"),
        ("Вс 8.11", "Figueira da Foz → Montemor-o-Velho → Coimbra", "43–55 км", "~130 м", "дамбы Мондегу, ямы и грунт, как в маршруте D"),
    ],
    sandnotes=[
        "Глубокий песок только на лесных тропах в стороне от дюнной дороги (отчёт CycleBlaze, 2023). Держаться асфальта и велодорожки.",
        "Береговая тропа Quiaios → Cabo Mondego в 2021 году описана как опасная: камнепад, край обрыва. На серру подниматься по дороге, не по тропе.",
        "Дамбы Мондегу: ямы, участок, где велосипед надо вести, железнодорожный мост не для велосипедов. Северный ветер.",
        "Первый день короткий по километрам, если не делать петлю: не растягивать, иначе Praia de Mira в ноябре встречает закрытыми кафе.",
    ],
    see=[
        "<b>Авейру (Aveiro)</b>: каналы, лодки-молисейру, ар-нуво, солеварни Marinha da Troncalhada.",
        "<b>Мостки Риа-де-Авейру</b>: 7 км деревянных настилов по лагуне, птицы.",
        "<b>Коста-Нова</b>: полосатые палейруш, пляж за дюной.",
        "<b>Баррінья-де-Мира (Barrinha de Mira)</b>: пресная лагуна за дюнами, Praia de Mira с палейруш.",
        "<b>Дюны Миры и Гандары</b>: охраняемые дюны, сосняк, посаженный от песка.",
        "<b>Серра-да-Боа-Виажен</b>: единственная высота у берега, мыс Мондегу и вид на Фигейру.",
        "<b>Монтемор-у-Велью и Коимбра</b>: как в маршруте D.",
    ],
    prac=[
        "Туда: IC 521 Lisboa Santa Apolónia 06:30 → Oriente 06:39 → Aveiro 09:04 (пн–сб) или IC 721 09:30 → Aveiro 12:04 (ежедневно). Велосипед на местах 15 и 17, бронь в app CP.",
        "Обратно: IC Coimbra-B → Lisboa, вс последние 18:56, 20:20, 20:56.",
        "Запасные выходы: из Figueira da Foz в Coimbra-B региональный каждый час в xx:58; из Aveiro IC весь день.",
        "Ночёвки: Praia de Mira (мало, часть закрыта в ноябре), Figueira da Foz (много). Не проверялось.",
        "Вариант на два дня: Aveiro → Figueira 76 км / 308 м и Figueira → Coimbra 45 км.",
    ],
    tracks=[
        ("EuroVelo 1 Portugal, секции 23–24 (официальные GPX)", "https://euroveloportugal.com/en/route/eurovelo1", "Aveiro → Praia de Mira → Figueira"),
        ("Komoot: Aveiro → Costa Nova → Mira → Quiaios → Figueira (план, гравел)", "https://www.komoot.com/plan/@40.640451,-8.653942,9.407z?sport=mtb_easy&p[0][loc]=40.6404960,-8.6537841&p[1][loc]=40.6200727,-8.7526244&p[2][loc]=40.4556419,-8.8026211&p[3][loc]=40.2150976,-8.8500062&p[4][loc]=40.1485808,-8.8556550", "76 км / 308 м"),
        ("Komoot: Ria de Aveiro Boardwalks, петля от Esgueira", "https://www.komoot.com/smarttour/23775925", "41 км / 104 м"),
        ("Komoot: Costa Nova, петля от маяка Авейру", "https://www.komoot.com/smarttour/32147093", "49 км / 60 м"),
        ("Komoot: Castro de Santa Olalla, петля от Figueira", "https://www.komoot.com/smarttour/23775103", "45 км / 332 м, Serra da Boa Viagem"),
        ("Komoot: Figueira → Montemor → Coimbra (план)", "https://www.komoot.com/plan/@40.148463,-8.855657,9.407z?sport=mtb_easy&p[0][loc]=40.1485808,-8.8556550&p[1][loc]=40.1726640,-8.6845418&p[2][loc]=40.2111874,-8.4291478", "43 км / 131 м"),
        ("Bikemap: EuroVelo 1 Portugal, этап Ovar → Mira", "https://www.bikemap.net/fr/c/437009/", "78 км / 109 м, грунт 21 %"),
    ],
    photos=[("e/aveiro", "Солеварни Авейру"), ("e/praia-de-mira", "Прайя-де-Мира"), ("e/figueira", "Мыс Мондегу над Фигейрой"), ("d/montemor", "Замок Монтемор-у-Велью")],
    ext_photos=[("https://d2exd72xrrp1s7.cloudfront.net/www/1c/1cx2tsfuux7991j1bhxm1hp02c5s1kc9bc-p707890274-full/19e0771c3be", "Мостки Риа-де-Авейру", "Komoot", "https://www.komoot.com/smarttour/23775925")],
))

ROUTES.append(dict(
    id="c", letter="C", short="Алкева", fav=True,
    title="Алкева петлёй: Эвора → экопишта → Монсараш → Амиейра → Портел → Эвора",
    sub="Самый безлюдный, с озером и мегалитами, поезд в обе стороны",
    days="3 дня", km="145–190 км", up="~820–1 230 м", people="почти никого",
    tags=["озеро", "монтаду", "мегалиты", "замки", "тёмное небо"],
    cover="c/monsaraz", cover_cap="Монсараш (Monsaraz) над водохранилищем Алкева",
    lede="Алкева, самое большое искусственное озеро Западной Европы, заполнена на 80 %. Вокруг неё монтаду, кромлехи и две крепости на холмах. На тепловой карте Strava здесь почти пусто: проверенных гравийных ниток мало, зато нет и людей. С 2024 года первый день почти плоский: по бывшей железной дороге Évora → Reguengos.",
    body=[
        "Intercidades уходит с Oriente в 07:02 и 09:02, через 1 ч 45 мин Эвора. Экопишта Реггенгуш (Ecopista de Reguengos) открыта 17 сентября 2024: 39 км по насыпи через монтаду с мостом над Дегебе; покрытие нигде не описано, по OSM это path без тега. От Реггенгуша до Монсараша 17 км с подъёмом к стенам.",
        "Второй день гибкий: напрямую до Амиейры 29 км и 140 м, или большим кругом через Мораун и дамбу Алкева (69 км, 480 м) с переездом по дороге-дамбе через озеро у Корвала. Третий день через Портел обратно в Эвору, 56 км и 380 м, к поезду 16:51 или 19:14.",
        "Самый холмистый из трёх фаворитов, но ни один день не выходит за 450 м, если не делать круг через Мораун. Главный вопрос: жильё в Амиейре и Портеле в ноябре, его надо подтвердить до брони поездов.",
    ],
    stages=[
        ("Пт 6.11", "Évora → Ecopista de Reguengos → Reguengos → Cromeleque do Xerez → Monsaraz", "57–67 км", "~300–445 м", "экопишта 39 км без описания покрытия; Komoot-план по координатам 61,5 км / 444 м; Bikemap 66,6 км / 374 м"),
        ("Сб 7.11", "Monsaraz → (Mourão → плотина Alqueva) → Amieira", "29 или 69 км", "~140 или 480 м", "тихий асфальт и грунт; через дамбу-дорогу у Corval; петля Xerez–Monsaraz 45 % грунта"),
        ("Вс 8.11", "Amieira → Portel → Évora", "56 км", "~380 м", "дороги через монтаду; готовой гравийной нитки нет, прокладывать в Komoot"),
    ],
    sandnotes=[
        "Данных о песке вокруг Алкевы нет ни в одном источнике. На соседней экопиште Évora → Arraiolos в 2023 году отмечали «packed, sandy, gravelly, spots of loose sand»; ждать того же на Reguengos.",
        "Покрытие экопишты Reguengos не описано. Если окажется рыхлым, параллельно идёт N256 с небольшим трафиком.",
        "Второй день через Мораун добавляет 40 км и 340 м; решать по погоде и ветру утром.",
        "Жильё: Amieira и Portel небольшие, Mourão тоже. Если не найдётся, ночевать в Monsaraz две ночи и ехать петлю налегке.",
    ],
    see=[
        "<b>Эвора (Évora)</b>: римский храм, собор, капелла костей; весь центр в списке ЮНЕСКО.",
        "<b>Экопишта</b>: монтаду, пробковые дубы, мост над Дегебе.",
        "<b>Кромлех Шереш (Cromeleque do Xerez)</b> и монастырь Орада у подножия Монсараша: мегалиты перенесены сюда при затоплении долины.",
        "<b>Монсараш (Monsaraz)</b>: крепость-деревня над озером, ночёвка внутри стен, закат над водой.",
        "<b>Дорога-дамба у Корвала</b>: переезд по озеру, вид на обе стороны.",
        "<b>Мораун (Mourão)</b>: замок и ворота, если ехать длинным кругом.",
        "<b>Плотина Алкева и марина Амиейра</b>: плотина 96 м высотой, плавучие дома в марине.",
        "<b>Dark Sky Alqueva</b>: первый в мире сертифицированный заповедник тёмного неба, в ноябре темнеет к 18:00.",
    ],
    prac=[
        "Туда: IC Lisboa Oriente → Évora пт 07:02 или 09:02 (также 13:35, 17:02, 19:02), 1 ч 45 мин. Велосипед на местах 12 и 18 во 2-м классе, бронь обязательна.",
        "Обратно: IC Évora → Oriente вс 09:14, 16:51, 19:14.",
        "Ночёвки: Monsaraz (внутри стен несколько casas), Amieira или Portel. Ноябрьская работа не проверена.",
        "Вода Алкевы 19.10.2026: 80 % (APA).",
        "Запасной выход: из Beja IC с пересадкой в Casa Branca (вс 16:06, 18:20), но Beja в стороне от петли.",
    ],
    tracks=[
        ("Komoot: Évora → Reguengos → Monsaraz (план, гравел, по координатам)", "https://www.komoot.com/plan/@38.570795,-7.90926,9.407z?sport=mtb_easy&p[0][loc]=38.5707742,-7.9092808&p[1][loc]=38.4244000,-7.5347000&p[2][loc]=38.4432000,-7.3804000", "61,5 км / 444 м"),
        ("Komoot: Monsaraz → Mourão → Amieira → Portel → Évora (план, меньше набора)", "https://www.komoot.com/plan/@38.443191,-7.380406,9.407z?sport=mtb_easy&tags=less_elevation&p[0][loc]=38.4432000,-7.3804000&p[1][loc]=38.2976000,-7.2223000&p[2][loc]=38.2854000,-7.5587000&p[3][loc]=38.3086000,-7.7050000&p[4][loc]=38.5707742,-7.9092808", "147 км / 1 235 м за два дня"),
        ("Komoot: Cromlech of Xerez – Monsaraz Castle, петля от Reguengos", "https://www.komoot.com/tour/32163822", "50 км / 458 м, грунт и гравий 45 %"),
        ("Komoot: View of Alqueva, петля через дамбу от Corval (шоссе)", "https://www.komoot.com/tour/31402021", "83 км / 731 м, асфальт 92 %"),
        ("Bikemap: Évora → Monsaraz", "https://www.bikemap.net/en/c/270511", "66,6 км / 374 м"),
        ("Bikemap: Évora → Mourão через Monsaraz", "https://www.bikemap.net/en/c/286758/", "94,6 км / 501 м"),
        ("Infraestruturas de Portugal: Ecopista de Reguengos", "https://www.infraestruturasdeportugal.pt/", "открыта 17.09.2024, ~39 км"),
    ],
    photos=[("c/evora", "Римский храм Эворы"), ("c/alqueva", "Плотина Алкева"), ("c/xerez", "Кромлех Шереш"), ("c/amieira", "Марина Амиейра"), ("c/ecopista", "Экопишта")],
    ext_photos=[("https://d2exd72xrrp1s7.cloudfront.net/www/000/1k7/10/10mjie2uua0ob1xz6370ppekeh4rg0qcf5-uhi66825001/0", "Петля Шереш — Монсараш", "Komoot", "https://www.komoot.com/tour/32163822")],
))

ROUTES.append(dict(
    id="a", letter="A", short="Алентежу, берег", fav=False,
    title="Побережье Алентежу: паром в Трою → Компорта → Санту-Андре → Синеш → Порту-Кову → Милфонтеш → Кабу-Сардан",
    sub="Самый природный: рис, лагуны, скалы и аисты, набор малый",
    days="2–3 дня", km="150–180 км", up="~740–1 200 м", people="малолюдно",
    tags=["океан", "лагуны", "рис", "скалы", "аисты"],
    cover="a/cabo-sardao", cover_cap="Кабу-Сардан (Cabo Sardão)",
    lede="Классика EuroVelo 1 от парома в Трое до скал Кабу-Сардана. Первый день плоский почти целиком, второй короткий и красивый. Песок здесь есть, но локализован и обходится по дорогам. Слабое место одно: обратно к поезду 35–50 км в гору.",
    body=[
        "Fertagus до Сетубала за час, паром до Трои каждый час в :30 (только ferry, не катамаран). Дальше рисовые поля Компорты с аистами на церкви, сосняк до Мелидеш, лагуна Санту-Андре (в ноябре закрыта от моря) и Синеш с его промзоной, которую надо обойти по прибрежной дороге.",
        "Второй день самый фотогеничный: Порту-Кову, остров Пессегейру с фортом, устье Миры в Милфонтеше, Алмограве, аисты на скалах Кабу-Сардана и Замбужейра. На 38 мм гружёным Trilho dos Pescadores не для нас, он пешеходный и песчаный; едем по EV1 и дорогам.",
        "Третий день служебный: из Замбужейры 34 км и 460 м до станции Santa Clara-Sabóia (IC 15:20 и 19:25) или из Милфонтеша 49 км и 400 м до Funcheira (IC 15:54 и 19:54). Если ограничиться двумя днями, в воскресенье утром выезжать из Милфонтеша.",
    ],
    stages=[
        ("Пт 6.11", "Setúbal → паром Tróia → Comporta → Carvalhal → Melides → Lagoa de Santo André → Sines → Porto Covo", "87–97 км", "~320–460 м", "асфальт и гравий; EV1 секции 12–11; объезд песка у лагуны по дорогам"),
        ("Сб 7.11", "Porto Covo → Vila Nova de Milfontes → Almograve → Cabo Sardão → Zambujeira do Mar", "51 км", "~280 м", "EV1 секция 10–9; 0,7 км песка к северу от Milfontes обходится по дороге"),
        ("Вс 8.11", "Zambujeira → Santa Clara-Sabóia (станция) или Milfontes → Funcheira (станция)", "34 / 49 км", "~460 / 400 м", "асфальт в гору, через серру"),
    ],
    sandnotes=[
        "Lagoa de Santo André: официальный GPX EuroVelo секции Sines → Melides содержит около 4,5 км песка (16 % секции) вокруг лагуны. Обход: N261 и местные дороги к Vila Nova de Santo André.",
        "Сразу к северу от Milfontes на EV1 около 0,7 км «mushy deep sand», в отчёте 2019 года велосипед вели. Обход по N390 и мосту.",
        "Около 0,7 км песка у Cabo Sardão на секции Odeceixe → Milfontes; к маяку подъезжать по асфальту.",
        "Comporta → Carvalhal: гравийная двойная колея 6,5 км, на север зарастает травой; дорога у эстуария асфальт.",
        "Trilho dos Pescadores: только пешком, «lots of sand». Не заезжать на тропы Rota Vicentina вдоль обрывов.",
        "Подъезд к Sines с севера около 10 км вдоль A26 и промзона: планировать по прибрежной дороге через Vila Nova de Santo André и Costa de Santo André.",
        "Жильё в Porto Covo и Zambujeira в ноябре не подтверждено; Milfontes и Sines работают круглый год.",
    ],
    see=[
        "<b>Троя (Tróia)</b>: римские руины рыбозасолочного комплекса у причала.",
        "<b>Компорта (Comporta)</b>: рисовые поля, гнёзда аистов на церкви, свайный причал Carrasqueira в 5 км в сторону.",
        "<b>Лагуна Санту-Андре</b>: заповедник лагун Santo André и Sancha, птицы.",
        "<b>Порту-Кову</b> и остров <b>Пессегейру</b> с фортом XVI века.",
        "<b>Вила-Нова-де-Милфонтеш</b>: форт и устье Миры.",
        "<b>Кабу-Сардан</b>: маяк и единственные в мире аисты, гнездящиеся на морских скалах (гнёзда видны круглый год).",
        "<b>Замбужейра-ду-Мар</b>: пляж в скалах, закат.",
    ],
    prac=[
        "Туда: Fertagus Roma-Areeiro → Setúbal каждые 20 мин, 58 мин, велосипед бесплатно, до 2 на вагон. Паром Setúbal (Doca do Comércio) → Tróia: 07:30 и каждый час в :30 до 19:30, ferry, 5,50 € человек + 5,50 € велосипед.",
        "Обратно: IC из Santa Clara-Sabóia вс 10:25, 15:20, 19:25 или из Funcheira 10:56, 15:54, 19:54 (в Oriente 12:56, 17:56, 21:56). Места 12 и 18, бронь.",
        "Ночёвки: Porto Covo (O Lugar и гестхаусы), Milfontes (Casa do Adro и др.), Zambujeira (Soldavila). Ноябрь не проверен.",
        "Из Sines поездов нет с 1990 года.",
    ],
    tracks=[
        ("EuroVelo 1 Portugal, секции 9–12 (официальные GPX)", "https://euroveloportugal.com/en/route/eurovelo1", "Odeceixe → Milfontes → Sines → Melides → Tróia"),
        ("Portuguese Trails: EuroVelo 1 Alentejo, GPX", "https://www.portuguesetrails.com/sites/default/files/routes/gpx/Eurovelo_Alentejo.gpx", "весь Алентежу одним файлом"),
        ("Komoot: Tróia → Comporta → Melides → Santo André → Sines → Porto Covo (план, гравел)", "https://www.komoot.com/plan/@38.486177,-8.883885,9.407z?sport=mtb_easy&p[0][loc]=38.4859195,-8.8836429&p[1][loc]=38.3803765,-8.7859968&p[2][loc]=38.3692980,-8.7937612&p[3][loc]=38.1472980,-8.7285840&p[4][loc]=38.0541917,-8.8162999&p[5][loc]=37.9565490,-8.8689639&p[6][loc]=37.8517287,-8.7918410", "97 км / 462 м"),
        ("Komoot: Porto Covo → Milfontes → Cabo Sardão → Zambujeira (план, гравел)", "https://www.komoot.com/plan/@37.851792,-8.791889,9.407z?sport=mtb_easy&p[0][loc]=37.8517287,-8.7918410&p[1][loc]=37.7252803,-8.7822865&p[2][loc]=37.6542256,-8.7567390&p[3][loc]=37.5986309,-8.8161381&p[4][loc]=37.5256480,-8.7848108", "51 км / 283 м"),
        ("Bikemap: EV1 Setúbal → Porto Covo", "https://www.bikemap.net/en/r/17525416/", "83 км / 531 м, асфальт 89 %"),
        ("Bikemap: EV1 Porto Covo → Aljezur", "https://www.bikemap.net/en/r/17525417/", "76 км / 558 м, песок 6 км (8 %)"),
        ("Komoot: Melides – Costa de Santo André, петля", "https://www.komoot.com/tour/23773128", "85 км / 935 м, грунт 46 %"),
        ("AllTrails: Tróia – Melides", "https://www.alltrails.com/trail/portugal/setubal--3/troia-melides", "87 км / 465 м туда-обратно"),
    ],
    photos=[("a/comporta", "Рисовые поля Компорты"), ("a/carrasqueira", "Свайный причал Карраскейры"), ("a/santo-andre", "Лагуна Санту-Андре"),
            ("a/porto-covo", "Порту-Кову и остров Пессегейру"), ("a/milfontes", "Устье Миры в Милфонтеше"), ("a/zambujeira", "Замбужейра-ду-Мар")],
    ext_photos=[],
))

ROUTES.append(dict(
    id="b", letter="B", short="Садо + берег", fav=False,
    title="Садо и побережье без паромов: Грандола → Алкасер → Карраскейра → Компорта → Синеш → Порту-Кову → Милфонтеш → Фуншейра",
    sub="Та же природа, что A, плюс эстуарий Садо, но все три дня полные",
    days="3 дня", km="~220 км", up="~1 130 м", people="почти никого",
    tags=["эстуарий", "фламинго", "рис", "океан", "скалы"],
    cover="b/sado", cover_cap="Эстуарий Садо (Estuário do Sado)",
    lede="Вариант для тех, кто хочет три полных дня и не хочет зависеть от парома. Первый день начинается в 11:30 на станции Грандола, идёт к замку Алкасера и через рисовые поля и каналы заповедника Садо к свайному причалу Карраскейры. Дальше как маршрут A.",
    body=[
        "Петля Komoot от Алкасера по заповеднику даёт 86 % грунта и местами ступени, где велосипед надо нести; на этом участке по тепловой карте Strava ездят единицы. Фламинго в эстуарии держатся круглый год, зимой их больше.",
        "Третий день самый длинный: 18 км до Милфонтеша и 49 км с 400 м набора до станции Funcheira к поезду 15:54 или 19:54. Это цена отсутствия паромов.",
    ],
    stages=[
        ("Пт 6.11", "ст. Grândola → Alcácer do Sal → рисовые поля RN Sado → Carrasqueira → Comporta", "~75 км", "~250 м", "27 км асфальта до Alcácer, дальше грунт 86 %, ступени"),
        ("Сб 7.11", "Comporta → Melides → Santo André → Sines → Porto Covo", "~80 км", "~400 м", "как день 1 маршрута A"),
        ("Вс 8.11", "Porto Covo → Vila Nova de Milfontes → Funcheira (станция)", "67 км", "~480 м", "18 км по побережью, затем 49 км асфальта в гору"),
    ],
    sandnotes=[
        "Песка на петле Садо в отзывах нет, но есть ступени и участки, где велосипед несут (Komoot).",
        "Дальше те же места, что в A: лагуна Santo André (4,5 км песка на EV1, объезд), север Milfontes (0,7 км), промзона Sines.",
        "Старт в 11:30 и закат в 17:25: на первый день 6 часов света на 75 км с грунтом, без запаса на осмотры.",
    ],
    see=[
        "<b>Алкасер-ду-Сал (Alcácer do Sal)</b>: замок-поусада, набережная, пешеходный мост через Садо.",
        "<b>Заповедник эстуария Садо</b>: каналы, рис, фламинго, дельфины в эстуарии.",
        "<b>Карраскейра</b>: свайный причал 1950-х, лабиринт мостков.",
        "<b>Компорта, Санту-Андре, Порту-Кову, Милфонтеш</b>: как в A.",
    ],
    prac=[
        "Туда: IC 570 Lisboa Oriente 10:02 → Grândola 11:21. Места 12 и 18, бронь.",
        "Обратно: IC из Funcheira вс 15:54 → Oriente 17:56 или 19:54 → 21:56.",
        "Ночёвки: Comporta или Carvalhal, Porto Covo. Ноябрь не проверен.",
        "В Alcácer do Sal поездов нет с 2011 года.",
    ],
    tracks=[
        ("Komoot: Carrasqueira – Alcácer do Sal, петля по заповеднику", "https://www.komoot.com/tour/32127350", "62,5 км / 244 м, грунт 86 %"),
        ("Komoot: Alcácer → Carrasqueira → Comporta → Tróia (план, гравел)", "https://www.komoot.com/plan/@38.373208,-8.512401,9.407z?sport=mtb_easy&p[0][loc]=38.3729735,-8.5122705&p[1][loc]=38.3751000,-8.7845200&p[2][loc]=38.3803765,-8.7859968&p[3][loc]=38.4859195,-8.8836429", "50 км / 187 м"),
        ("AllTrails: Açude de Vale dos Coelheiros – Comporta – Cais da Carrasqueira", "https://www.alltrails.com/trail/portugal/setubal--3/carrasqueira-acude-de-vale-dos-coelheiros-comporta-cais-palafitico-da-carrasquei", "49 км / 195 м"),
        ("Komoot: хайлайт Cais Palafítico da Carrasqueira", "https://www.komoot.com/highlight/3498040", ""),
        ("Дальше нитки маршрута A", "#a", ""),
    ],
    photos=[("b/alcacer", "Алкасер-ду-Сал над Садо"), ("a/carrasqueira", "Свайный причал Карраскейры"), ("a/comporta", "Рис Компорты")],
    ext_photos=[("https://d2exd72xrrp1s7.cloudfront.net/www/000/1k8/46/46ntzau574wl1vcoacjnhvvea58c52wlu-uhi81930731/0", "Петля по заповеднику Садо", "Komoot", "https://www.komoot.com/tour/32127350")],
))

ROUTES.append(dict(
    id="f", letter="F", short="Алгарве + Уэльва", fav=False,
    title="Восточный Алгарве и Уэльва: Фару → Тавира → VRSA → паром → Исла-Кристина → Эль-Ромпидо → назад к парому",
    sub="Самый ровный из всех, но самый людный и с тесной воскресной логистикой",
    days="3 дня", km="160–200 км", up="~660 м", people="людно",
    tags=["лагуна", "солеварни", "марши", "две страны"],
    cover="f/cacela", cover_cap="Касела-Велья (Cacela Velha) над Риа-Формозой",
    lede="Риа-Формоза и марши Уэльвы дают самый ровный профиль в выборке, но по тепловой карте Strava это и самая плотная сетка велосипедистов. Виа-верде-дель-Литораль частично заброшена: мост Тавирона закрыт, за Лепе 4 км песка только пешком. Рабочая схема держится западного куска виа-верде и прибрежных дорог.",
    body=[
        "Intercidades приходит в Фару в 13:31, региональный довозит до Тавиры к 14:30, и остаток дня можно проехать по Экови до Тавиры сами (35 км) или начать с Тавиры. Второй день: Касела-Велья, Монте-Горду, VRSA, паром в Аямонте, виа-верде до Исла-Кристины (щебень, местами песчано), Ла-Антилья, Эль-Ромпидо.",
        "Третий день возвращается к парому: Пунта-Умбрия и Уэльва добавляют 40 км и не дают ничего, кроме дамбы Одьеля, а из Уэльвы в Лиссабон поезда нет. Последний воскресный паром из Аямонте в 16:15 по Португалии, региональный из VRSA в 16:34, IC из Фару в 18:15. Запас 19 минут.",
    ],
    stages=[
        ("Пт 6.11", "Faro → Olhão → Fuseta → Santa Luzia → Tavira", "35 км", "~190 м", "Ecovia do Litoral: грунт ~60 % между Olhão и Tavira, тропы местами песчаные"),
        ("Сб 7.11", "Tavira → Cacela Velha → Monte Gordo → VRSA → паром → Ayamonte → Isla Cristina → La Antilla → El Rompido", "~78 км", "~250 м", "Ecovia грунт ~54 % после Cacela; VV Ayamonte → Isla Cristina щебень, «местами очень песчано»; мост Tavirona закрыт, объезд N-431"),
        ("Вс 8.11", "El Rompido → Cartaya → Lepe → Ayamonte (паром до 16:15 PT)", "45–55 км", "~150 м", "дороги, виа-верде у Lepe не брать (песок)"),
    ],
    sandnotes=[
        "Vía Verde del Litoral: за Lepe около 4 км «sólo es posible a pie» (Caminos Naturales); перед Lepe короткий песчаный участок «dificulta el tránsito».",
        "Мост La Tavirona через Río Piedras: настил разворован, закрыт с 2014 года. Объезд по мосту N-431 у Lepe/Cartaya (1–1,5 км трассы).",
        "Isla Cristina → Ayamonte: щебень-zahorra «ciclable» (Junta 2022), в Komoot «partly good gravel road, but also very sandy» (2022).",
        "Tavira → Fuseta → Olhão: около 7 км грунта, в OSM одна точка «sand», Cycling Safaris 2025 пишет «sandy trails». Мост Fuseta–Olhão починен (12.2024).",
        "Воскресенье: паром Ayamonte 17:15 исп. = 16:15 PT, от причала до вокзала VRSA 1,3 км, поезд 16:34. Опоздание = ночёвка в Фару.",
    ],
    see=[
        "<b>Риа-Формоза</b>: мостки, птицы, солеварни Santa Luzia и Luz de Tavira.",
        "<b>Тавира (Tavira)</b>: замок, «римский» мост, Форте São João da Barra в Кабанаше.",
        "<b>Касела-Велья</b>: крепость над лагуной, вид на косу.",
        "<b>Каштру-Марин</b>: замок и солончаки Sapal, 4 км от VRSA.",
        "<b>Исла-Кристина</b>: марши с фламинго, приливная мельница, голубятня Huerta Noble на 36 тысяч гнёзд.",
        "<b>Эль-Ромпидо</b>: коса Flecha del Rompido и марши Río Piedras.",
    ],
    prac=[
        "Туда: IC 570 Oriente 10:02 → Faro 13:31 (места 12 и 18, бронь); R 13:56 → Tavira 14:29 → VRSA 14:58.",
        "Паром Ayamonte ↔ VRSA: 2,50 € + 1,60 € велосипед; пн–сб из VRSA 9:30, 10:30, 11:30, 12:30, 14:30, 15:30, 17:00 PT; вс из Ayamonte последний 17:15 исп. (16:15 PT).",
        "Обратно: R VRSA 16:34 → Faro 17:35; IC 674 Faro 18:15 → Oriente 21:56. Предыдущий IC 672 14:15.",
        "Ночёвки: Tavira (много), El Rompido или Isla Cristina (курортные, ноябрь не проверен).",
        "Часы: Испания на час вперёд.",
    ],
    tracks=[
        ("EuroVelo 1 Portugal, секция 1 VRSA → Faro (GPX 10.12.2024)", "https://euroveloportugal.com/files/2023/05/EuroVelo-1-Portugal-Section-01-Vila-Real-de-Santo-Antonio-Faro-2024-12-10.gpx", "68 км / ~410 м, грунт 35 %"),
        ("Portuguese Trails: Ecovia do Litoral, GPX", "https://www.portuguesetrails.com/sites/default/files/routes/gpx/EcoviaAlgarve1a4.gpx", "весь Алгарве, восточный трек первый"),
        ("Komoot: Faro → Olhão → Fuseta → Tavira → Cacela → VRSA (план, гравел)", "https://www.komoot.com/plan/@37.016334,-7.935292,9.407z?sport=mtb_easy&p[0][loc]=37.0162944,-7.9351820&p[1][loc]=37.0270369,-7.8411287&p[2][loc]=37.0551731,-7.7461861&p[3][loc]=37.1262493,-7.6499121&p[4][loc]=37.1573916,-7.5462157&p[5][loc]=37.2136976,-7.4420708", "65 км / 341 м"),
        ("Komoot: Ayamonte → Isla Cristina → La Antilla → El Rompido → Punta Umbría → Huelva (план)", "https://www.komoot.com/plan/@37.215692,-7.406189,9.407z?sport=mtb_easy&p[0][loc]=37.2157970,-7.4060169&p[1][loc]=37.2036925,-7.3238913&p[2][loc]=37.2075848,-7.2116537&p[3][loc]=37.2225915,-7.1237849&p[4][loc]=37.1830237,-6.9662203&p[5][loc]=37.2575874,-6.9484945", "88 км / 329 м, песок не учитывает"),
        ("Komoot: Ayamonte → Isla Cristina по кругу через Isla del Moral", "https://www.komoot.com/smarttour/e986950657/from-ayamonte-to-isla-cristina-circular-via-isla-del-moral", "27,5 км"),
        ("Komoot: марши Гуадианы, гравийная петля от Isla Cristina (июль 2026)", "https://www.komoot.com/tour/44796364", "53 км / 373 м, грунт 38 %"),
        ("Islantilla: Islantilla – El Rompido, GPX", "https://www.islantilla.es/wp-content/uploads/2024/03/islantilla-el-rompido-cycling-friendly.zip", "переправа через Río Piedras в другой точке"),
        ("AllTrails: Tavira – Loulé via Ecovia do Litoral", "https://www.alltrails.com/trail/portugal/faro/tavira-loule-via-ecovia-do-litoral", "61 км / 473 м"),
    ],
    photos=[("f/ria-formosa", "Риа-Формоза у Ольяна"), ("f/tavira", "Тавира"), ("f/castro-marim", "Каштру-Марин"), ("f/isla-cristina", "Марши Исла-Кристины"), ("f/el-rompido", "Коса Эль-Ромпидо")],
    ext_photos=[("https://d2exd72xrrp1s7.cloudfront.net/www/000/1k8/15/15dib2nixgae6gd55zw8ddsmr4w6k1v8q-uhi69336948/0", "Марши Гуадианы у Исла-Кристины", "Komoot", "https://www.komoot.com/tour/44796364")],
))

ROUTES.append(dict(
    id="g", letter="G", short="Садо коротко", fav=False,
    title="Садо коротко: Грандола → Алкасер → Карраскейра → Компорта → Троя → паром",
    sub="Два дня, ноль подъёмов, эстуарий и рис",
    days="2 дня", km="110–135 км", up="~490 м", people="почти никого",
    tags=["эстуарий", "фламинго", "рис"],
    cover="a/carrasqueira", cover_cap="Свайный причал Карраскейры (Cais Palafítico da Carrasqueira)",
    lede="Короткая версия B для двух дней: поезд в Грандолу, заповедник Садо и Карраскейра, ночь в Компорте, утром 20 км до Трои, паром и Fertagus домой. Самый спокойный и самый ровный вариант в Алентежу, но километров на три дня здесь нет.",
    body=[
        "Если нужны три дня, второй день можно отдать Аррабиде на том берегу: от Сетубала к Портиньо-да-Аррабида и обратно, но это уже горы, а не ровно.",
    ],
    stages=[
        ("День 1", "ст. Grândola → Alcácer do Sal → RN Sado → Carrasqueira → Comporta", "~75 км", "~250 м", "27 км асфальта, затем грунт 86 %, ступени"),
        ("День 2", "Comporta → Tróia → паром → Setúbal (+ Arrábida по желанию)", "20–60 км", "~50–240 м", "асфальт"),
    ],
    sandnotes=[
        "Как у B: ступени на петле Садо, песка в отзывах нет.",
        "Паром из Tróia каждый час до 20:00, велосипед только на ferry.",
    ],
    see=["<b>Алкасер, заповедник Садо, Карраскейра, Компорта, руины Трои</b>: см. A и B."],
    prac=[
        "Туда: IC 570 Oriente 10:02 → Grândola 11:21.",
        "Обратно: паром Tróia → Setúbal в :00 каждый час до 20:00, затем 21:15, 22:40; Fertagus до Лиссабона 58 мин.",
    ],
    tracks=[
        ("Komoot: петля по заповеднику Садо от Alcácer", "https://www.komoot.com/tour/32127350", "62,5 км / 244 м"),
        ("Komoot: Alcácer → Carrasqueira → Comporta → Tróia (план)", "https://www.komoot.com/plan/@38.373208,-8.512401,9.407z?sport=mtb_easy&p[0][loc]=38.3729735,-8.5122705&p[1][loc]=38.3751000,-8.7845200&p[2][loc]=38.3803765,-8.7859968&p[3][loc]=38.4859195,-8.8836429", "50 км / 187 м"),
    ],
    photos=[("g/troia", "Римские руины Трои"), ("b/alcacer", "Алкасер-ду-Сал")],
    ext_photos=[],
))

REJECTED = [
    ("Нижняя Гуадиана: VRSA → Каштру-Марин → Алкоутин → Мертола по GR15",
     "VRSA → Alcoutim по GR15 67 км при ~2 000 м набора, по асфальту 51 км и 584 м; Alcoutim → Mértola 36–40 км и 574–637 м. Каменистая пешеходная тропа, крутые подъёмы, по тепловой карте Strava почти никто не ездит. Из Mértola до поезда ещё 52–55 км и 600 м до Beja."),
    ("Долина Тежу и Лезирия: Вила-Франка → Сантарен → Голеган → Констансия",
     "Плоско (Carregado → Golegã 69 км / 330 м), но промзоны, без тени и сервисов до Сантарена. Главное: 6–15 ноября в Голегане Feira Nacional do Cavalo, в эти даты там людно и нет жилья."),
    ("Заброска поездом в Обидуш или Калдаш",
     "Linha do Oeste от Meleças до Caldas da Rainha закрыта с 16.03.2026, автобусы замены велосипеды не берут. Открытие обещают к концу 2026 — началу 2027. Поэтому маршрут D только с машиной."),
    ("Уэльва и дамба Одьеля как цель",
     "Из Уэльвы в Лиссабон поезда нет; возвращаться всё равно к парому в Аямонте, а дамба Juan Carlos I добавляет 50 км туда-обратно по бетону."),
    ("Экопишты центра (Dão, Vouga, Tâmega), Дору, Минью",
     "Экопишты отличные, но по 40–50 км и не стыкуются; север даёт 1 100–1 500 м набора в день."),
]

LOGISTICS = [
    "<b>CP, велосипед в поезде.</b> Бесплатно во всех поездах. В Intercidades только в собранном виде на крюке при брони конкретного места во 2-м классе: места 12 и 18 на линиях Évora и Faro, места 15 и 17 на линиях Porto, Coimbra, Aveiro. Два велосипеда на вагон. На крюк велосипед до 15 кг, сумки снять. Alfa Pendular только разобранным в чехле. Регионалы без брони, решает контролёр.",
    "<b>Fertagus Lisboa → Setúbal.</b> Бесплатно, без ограничений по часам, до двух велосипедов на вагон, из Roma-Areeiro каждые 20 минут, 58 минут в пути.",
    "<b>Паром Setúbal ↔ Tróia (Atlantic Ferries).</b> Велосипед только на ferry, не на катамаран. 5,50 € человек и 5,50 € велосипед. Из Setúbal 07:30 и далее каждый час в :30 до 19:30, затем 20:40 и 22:00; из Tróia каждый час в :00 до 20:00.",
    "<b>Паром Ayamonte ↔ VRSA.</b> 2,50 € человек и 1,60 € велосипед. В воскресенье последний из Ayamonte в 17:15 по Испании (16:15 по Португалии).",
    "<b>Световой день 6–8 ноября.</b> Рассвет около 07:10, закат 17:23–17:31. Чистого света 10 часов 15 минут. При темпе 19 км/ч чистого хода (Рюген, июль 2026) 100 км занимают 5,5 часов хода и 8 часов с остановками.",
    "<b>Расписания CP</b> в силе с 19.07, 06.09 и 20.09.2026, взяты из официальных PDF. Перед покупкой перепроверить в app CP: продажи и бронь велосипедного места открываются там же.",
]

SOURCES = [
    ("CP, Transporte de bicicletas", "https://cp.pt/info/pt/w/transporte-bicicletas"),
    ("CP, расписание Lisboa ↔ Faro / Lagos / VRSA (с 19.07.2026)", "https://www.cp.pt/info/documents/d/cp/comboio-porto-lisboa-faro-lagos-v-r-s-antonio"),
    ("CP, расписание Lisboa ↔ Évora / Beja (с 06.09.2026)", "https://www.cp.pt/info/documents/d/cp/comboios-lisboa-evora-beja"),
    ("CP, расписание Alfa Pendular / Intercidades Lisboa ↔ Norte (с 20.09.2026)", "https://cp.pt/info/documents/d/cp/comboios-alfa-pendular-intercidades-lisboa-norte-sul"),
    ("Fertagus, Transporte de velocípedes", "https://www.fertagus.pt/Fertagus-pt/Viajar/Transporte-de-Velocípedes"),
    ("Atlantic Ferries, расписание низкого сезона 2026", "https://www.atlanticferries.pt/wp-content/uploads/2025/12/Ferries_EpocaBaixa_2026.pdf"),
    ("Паром Ayamonte ↔ VRSA, расписание", "https://rioguadiana.net/"),
    ("24notícias, 13.08.2026: автобусы замены Linha do Oeste и велосипеды", "https://24noticias.sapo.pt/"),
    ("EuroVelo Portugal (FPCUB): секции и GPX", "https://euroveloportugal.com/en/route/eurovelo1"),
    ("Bikemap: EuroVelo 1 Portugal, 15 этапов", "https://www.bikemap.net/fr/c/437009/"),
    ("Portuguese Trails: GPX Ecovia do Litoral и EuroVelo Alentejo", "https://www.portuguesetrails.com/en/node/18"),
    ("Caminos Naturales: Vía Verde del Litoral, предупреждения", "https://www.caminosnaturales.es/"),
    ("Diario de Huelva, 17.03.2026: платформа за восстановление виа-верде", "https://www.diariodehuelva.es/articulo/provincia/nace-plataforma-ciudadana-recuperar-via-verde-litoral-entre-gibraleon-ayamonte/20260317131844335266.html"),
    ("Junta de Andalucía, проект EuroVelo 1 tramo 3 (мост Tavirona, песок)", "https://www.juntadeandalucia.es/sites/default/files/inline-files/2025/01/TAA4005APR1%20DOC01%20MEMORIA%20V03.pdf"),
    ("Odiana: гид GR15 с профилями", "https://baixoguadiana.com/media/route_files/guia_gr15_pt_ing_ma2KhZ8.pdf"),
    ("Center of Portugal: Estrada Atlântica и Ecovia do Mondego", "https://www.centerofportugal.com/article/atlantic-road-cycling-path"),
    ("APA: заполнение водохранилищ, 19.10.2026", "https://www.apambiente.pt/"),
    ("Strava Global Heatmap (гравел), снимки 27.10.2026", "https://www.strava.com/maps/global-heatmap?sport=GravelRide"),
    ("Komoot: планировщик и туры (ссылки в разделах маршрутов)", "https://www.komoot.com/"),
    ("AllTrails: трейлы Алентежу и Алгарве", "https://www.alltrails.com/"),
    ("Wikimedia Commons: фотографии, авторы и лицензии в подписях", "https://commons.wikimedia.org/"),
]

# ----------------------------------------------------------------------------
# Рендер
# ----------------------------------------------------------------------------
CSS = """
:root{
  --paper:#F3F2EC; --card:#FFFFFF; --ink:#1A1F1B; --muted:#4E564F;
  --sea:#1F5A3C; --sea-soft:#1f5a3c14; --cider:#8F5410; --cider-border:#B96F1E; --cider-soft:#b96f1e14;
  --sand:#8a5a00; --sand-soft:#d8a21a1f; --line:#D9D8CF; --dash:#BDBCB2; --fav:#B96F1E;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --paper:#15181A; --card:#1C2124; --ink:#ECEFEA; --muted:#A9B3AB;
    --sea:#7CCB9C; --sea-soft:#7ccb9c1f; --cider:#E7A863; --cider-border:#E09A4C; --cider-soft:#e09a4c1f;
    --sand:#F0C25A; --sand-soft:#f0c25a1f; --line:#2C3336; --dash:#3D4649; --fav:#E7A863;
  }
}
:root[data-theme="dark"]{
  --paper:#15181A; --card:#1C2124; --ink:#ECEFEA; --muted:#A9B3AB;
  --sea:#7CCB9C; --sea-soft:#7ccb9c1f; --cider:#E7A863; --cider-border:#E09A4C; --cider-soft:#e09a4c1f;
  --sand:#F0C25A; --sand-soft:#f0c25a1f; --line:#2C3336; --dash:#3D4649; --fav:#E7A863;
}
*{box-sizing:border-box;margin:0}
html{scroll-behavior:smooth}
body{background:var(--paper);color:var(--ink);font:400 17px/1.65 "IBM Plex Sans",system-ui,sans-serif}
img{max-width:100%;display:block}
a{color:var(--sea)}
.wrap{max-width:720px;margin:0 auto;padding:0 20px}
.wide{max-width:960px;margin:0 auto;padding:0 20px}
h1,h2,h3,.disp{font-family:"Forum",Georgia,serif;font-weight:400;line-height:1.12;letter-spacing:.015em}
h3{font-size:1.9rem;margin:0 0 .35rem}
.mono{font-family:"IBM Plex Mono",monospace}
.cover{position:relative;min-height:88svh;display:flex;align-items:flex-end;color:#F4F6F5;overflow:hidden;background:#223}
.cover img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.cover::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,#0005 0%,#0000 35%,#000a 78%,#000c 100%)}
.cover .wrap{position:relative;z-index:2;padding-bottom:3rem;width:100%}
.kicker{font-family:"IBM Plex Mono",monospace;font-size:.78rem;letter-spacing:.22em;text-transform:uppercase;opacity:.85}
.cover h1{font-size:clamp(2.6rem,9vw,5rem);margin:.4rem 0 .7rem;text-transform:uppercase}
.cover .route{font-size:.98rem;opacity:.92;max-width:36em}
.cover figcaption{position:absolute;right:12px;bottom:8px;z-index:2;font-size:.62rem;opacity:.6;font-family:"IBM Plex Mono",monospace;color:#fff}
.cover figcaption a{color:inherit}
nav{position:sticky;top:0;z-index:50;background:var(--paper);border-bottom:1px solid var(--line)}
@supports (background: color-mix(in srgb, red 50%, blue)){nav{background:color-mix(in srgb,var(--paper) 88%,transparent);backdrop-filter:blur(10px)}}
nav .in{display:flex;gap:4px;overflow-x:auto;padding:9px 14px;scrollbar-width:none;max-width:960px;margin:0 auto}
nav .in::-webkit-scrollbar{display:none}
nav a{flex:0 0 auto;font-family:"IBM Plex Mono",monospace;font-size:.74rem;letter-spacing:.04em;text-decoration:none;color:var(--muted);padding:5px 11px;border:1px solid var(--line);border-radius:999px;white-space:nowrap}
nav a b{color:var(--ink);font-weight:500}
nav a.fav{border-color:var(--cider-border);color:var(--cider)}
.intro{padding:3rem 0 1rem}
.intro h2{font-size:clamp(1.9rem,5vw,2.6rem);margin-bottom:.8rem}
.intro p{margin:0 0 1rem}
table{border-collapse:collapse;width:100%;font-size:.86rem}
.sum{margin:1.2rem 0 2rem;overflow-x:auto}
.sum table{min-width:760px}
th,td{text-align:left;vertical-align:top;padding:.5rem .6rem;border-bottom:1px solid var(--line)}
th{font-family:"IBM Plex Mono",monospace;font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:500}
td.l{font-family:"Forum",serif;font-size:1.2rem;color:var(--sea)}
tr.fav td.l{color:var(--fav)}
.pill{display:inline-block;font-family:"IBM Plex Mono",monospace;font-size:.66rem;letter-spacing:.12em;text-transform:uppercase;border:1px solid var(--cider-border);color:var(--cider);border-radius:999px;padding:1px 8px;margin-left:.4rem;vertical-align:middle}
.day{padding:4.2rem 0 1.4rem}
.day .num{font-family:"Forum",serif;font-size:1.05rem;letter-spacing:.28em;text-transform:uppercase;color:var(--sea)}
.day .num .pill{margin-left:.6rem}
.day h2{font-size:clamp(1.9rem,6vw,2.8rem);margin:.25rem 0 .5rem}
.day .sub{color:var(--muted);font-size:1.02rem;margin-bottom:.8rem}
.kmpost{display:flex;flex-wrap:wrap;gap:.5rem 1.6rem;font-family:"IBM Plex Mono",monospace;font-size:.8rem;color:var(--muted)}
.kmpost b{color:var(--ink);font-weight:500}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin:.8rem 0 0}
.tags span{font-family:"IBM Plex Mono",monospace;font-size:.68rem;letter-spacing:.08em;color:var(--sea);background:var(--sea-soft);border-radius:999px;padding:2px 10px}
.road{border:none;border-top:2px dashed var(--dash);margin:1.5rem 0 0}
section.loc{padding:1.2rem 0 1rem}
figure.full{margin:0 0 1.5rem}
figure.full img{width:100%;max-height:62svh;object-fit:cover;border-radius:2px}
figcaption{font-family:"IBM Plex Mono",monospace;font-size:.7rem;color:var(--muted);padding:6px 20px 0;max-width:960px;margin:0 auto}
figcaption a{color:var(--muted)}
.lede{font-size:1.06rem;margin:.2rem 0 1rem;color:var(--muted)}
.loc p{margin:0 0 1rem}
h4{font-family:"IBM Plex Mono",monospace;font-size:.74rem;letter-spacing:.2em;text-transform:uppercase;color:var(--sea);margin:1.6rem 0 .7rem}
ul.see{list-style:none;padding:0;margin:0 0 1.2rem}
ul.see li{padding:.42rem 0 .42rem 1.35rem;position:relative;border-bottom:1px solid var(--line)}
ul.see li::before{content:"›";position:absolute;left:.15rem;color:var(--sea);font-weight:600}
ul.see b{font-weight:600}
.stw{overflow-x:auto;margin:.4rem 0 1.2rem}
.st{min-width:560px}
.st td:nth-child(3),.st td:nth-child(4){white-space:nowrap}
.prac,.sand{border-radius:0 4px 4px 0;padding:.9rem 1.1rem;margin:1.2rem 0;font-size:.92rem}
.prac{background:var(--cider-soft);border-left:3px solid var(--cider-border)}
.sand{background:var(--sand-soft);border-left:3px solid var(--sand)}
.prac .t,.sand .t{font-family:"IBM Plex Mono",monospace;font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;margin-bottom:.4rem}
.prac .t{color:var(--cider)} .sand .t{color:var(--sand)}
.prac ul,.sand ul{list-style:none;padding:0}
.prac li,.sand li{padding:.22rem 0}
.map{height:440px;border:1px solid var(--line);border-radius:6px;margin:.4rem 0 .8rem;background:var(--card)}
@media(max-width:560px){.map{height:360px}}
ul.legend{list-style:none;padding:0;margin:0 0 .6rem;font-size:.88rem}
ul.legend li{padding:.3rem 0;border-bottom:1px solid var(--line)}
.sw{display:inline-block;width:14px;height:14px;border-radius:3px;vertical-align:-2px;margin-right:.5rem}
.leaflet-container{font:inherit}
ul.links{list-style:none;padding:0;margin:0 0 1.2rem;font-size:.9rem}
ul.links li{padding:.3rem 0;border-bottom:1px solid var(--line)}
.gal{display:grid;grid-template-columns:1fr;gap:10px;margin:1.4rem 0 .6rem}
.gal:has(figure + figure){grid-template-columns:1fr 1fr}
.gal:not(:has(figure + figure)) img{aspect-ratio:16/10}
.gal figure{margin:0}
.gal img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:2px}
.gal figcaption{padding:4px 2px 0}
@media(max-width:560px){.gal{grid-template-columns:1fr !important}}
.rej{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:1.4rem 0}
@media(max-width:640px){.rej{grid-template-columns:1fr}}
.rej div{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:.9rem 1rem}
.rej h5{font-family:"Forum",Georgia,serif;font-weight:400;font-size:1.2rem;line-height:1.2;margin:0 0 .4rem}
.rej p{font-size:.88rem;margin:0}
.fin{background:var(--card);border-top:1px solid var(--line);margin-top:3.5rem;padding:3rem 0 2rem}
.fin h2{font-size:2rem;margin-bottom:1rem}
.fin p,.fin li{font-size:.95rem}
ul.plain{list-style:none;padding:0;margin:0 0 1.5rem}
ul.plain li{padding:.45rem 0;border-bottom:1px solid var(--line)}
.small{font-size:.82rem;color:var(--muted)}
.small li{padding:.15rem 0}
footer{padding:2rem 20px 3rem;text-align:center;font-family:"IBM Plex Mono",monospace;font-size:.68rem;color:var(--muted)}
a.lb img{cursor:zoom-in}
#lbox{position:fixed;inset:0;background:#000d;display:none;align-items:center;justify-content:center;z-index:99;cursor:zoom-out}
#lbox.on{display:flex}
#lbox img{max-width:94vw;max-height:94vh;object-fit:contain}
@media (prefers-reduced-motion: reduce){html{scroll-behavior:auto}}
"""


def render_route(r):
    pill = '<span class="pill">фаворит</span>' if r["fav"] else ""
    head = f"""
<div class="wrap day" id="{r['id']}">
  <div class="num">Маршрут {r['letter']}{pill}</div>
  <h2>{t(r['title'])}</h2>
  <div class="sub">{t(r['sub'])}</div>
  <div class="kmpost"><span><b>{t(r['days'])}</b></span><span><b>{t(r['km'])}</b> · набор {t(r['up'])}</span><span>{t(r['people'])}</span></div>
  <div class="tags">{''.join(f'<span>{t(x)}</span>' for x in r['tags'])}</div>
  <hr class="road">
</div>"""
    cover = fig(r["cover"], r["cover_cap"], full=True)
    body = "".join(f"<p>{t(p)}</p>" for p in r["body"])
    photos = gal(*[fig(k, c) for k, c in r["photos"]], *[ext_fig(*e) for e in r["ext_photos"]])
    sec = f"""
<section class="loc">
  {cover}
  <div class="wrap">
  <p class="lede">{t(r['lede'])}</p>
  {body}
  <h4>По дням</h4>
  {stages(r['stages'])}
  {sand(r['sandnotes'])}
  <h4>Что смотреть</h4>
  {ul('see', r['see'])}
  {prac('Логистика', r['prac'])}
  {tracks_block(r['id'])}
  <h4>Нитки и GPX</h4>
  {links(r['tracks'])}
  {photos}
  </div>
</section>"""
    return head + sec


def render():
    nav = "".join(
        f'<a href="#{r["id"]}"{" class=\"fav\"" if r["fav"] else ""}><b>{r["letter"]}</b> {html.escape(r["short"])}</a>'
        for r in ROUTES)
    nav += '<a href="#rej">отсев</a><a href="#fin">поезда и паромы</a><a href="#src">источники</a>'

    sumrows = "".join(
        f'<tr{" class=\"fav\"" if r["fav"] else ""}><td class="l"><a href="#{r["id"]}" style="text-decoration:none;color:inherit">{r["letter"]}</a></td>'
        f'<td>{t(r["title"])}{"<span class=\"pill\">фаворит</span>" if r["fav"] else ""}</td><td>{t(r["days"])}</td><td>{t(r["km"])}</td><td>{t(r["up"])}</td><td>{t(r["people"])}</td></tr>'
        for r in ROUTES)

    rej = "".join(f"<div><h5>{t(n)}</h5><p>{t(d)}</p></div>" for n, d in REJECTED)
    logi = "".join(f"<li>{t(x)}</li>" for x in LOGISTICS)
    src = "".join(f'<li><a href="{html.escape(u)}">{html.escape(n)}</a></li>' for n, u in SOURCES)

    cover_key = "d/nazare-sitio" if os.path.exists(os.path.join(HERE, "img/d/nazare-sitio.jpg")) else ROUTES[0]["cover"]
    cp = PHOTOS.get(cover_key, {})
    cover_img = f'<img src="img/{cover_key}.jpg" alt="" fetchpriority="high">'
    cover_cap = f'<figcaption>Фото: {html.escape(cp.get("author", ""))} · <a href="{html.escape(cp.get("page", "#"))}">{html.escape(cp.get("license", ""))}</a></figcaption>'

    out = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta name="robots" content="noindex">
<title>Гравел на три дня</title>
<meta name="description" content="Семь веломаршрутов по Португалии и Уэльве на 6–8 ноября 2026: километраж, набор, песок, поезда, нитки и фото">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚲</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Forum&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<style>{CSS}</style>
</head>
<body>
<header class="cover">
  {cover_img}
  <div class="wrap">
    <div class="kicker">Гравел · 6–8 ноября 2026 · двое · поезд</div>
    <h1>Три дня, семь маршрутов</h1>
    <p class="route">{t('Португалия и ближняя Уэльва: до 220 км, 75–100 км в день, поменьше холмов, побольше воды. Trek Checkpoint на 38 мм с сумками, ночёвки в отелях, заброска поездом или машиной, обратно поездом.')}</p>
  </div>
  {cover_cap}
</header>

<nav><div class="in">{nav}</div></nav>

<div class="wrap intro">
  <h2>Как читать</h2>
  <p>{t('Три фаворита стоят первыми: D с заброской машиной в Обидуш, E как самый ровный, C как самый безлюдный. Остальные четыре тоже проходимы, их километраж и логистика проверены так же. Отсев в конце с причинами.')}</p>
  <p>{t('Цифры набора из планировщика Komoot (гравел) и официальных GPX EuroVelo, точность ±20 %. Людность по тепловой карте Strava для гравела и по сезону. Песок отмечен там, где его видели источники 2019–2026 годов; свежих полевых отчётов за осень 2026 нет ни по одному участку.')}</p>
  <p>{t('Отели в ноябре ни по одному маршруту не проверены: в карточках названы только города, где жильё есть круглый год.')}</p>
</div>
<div class="wide sum">
<table><thead><tr><th></th><th>Маршрут</th><th>Дни</th><th>км</th><th>Набор</th><th>Людность</th></tr></thead><tbody>{sumrows}</tbody></table>
</div>

{''.join(render_route(r) for r in ROUTES)}

<div class="wrap day" id="rej">
  <div class="num">Отсев</div>
  <h2>Что не вошло и почему</h2>
  <hr class="road">
  <div class="rej">{rej}</div>
</div>

<section class="fin" id="fin"><div class="wrap">
  <h2>Поезда, паромы, свет</h2>
  <ul class="plain">{logi}</ul>
  <h2 id="src">Источники</h2>
  <ul class="plain small">{src}</ul>
  <p class="small">{t('Данные собраны 27.10.2026. Тепловая карта Strava и планы Komoot сняты в тот же день. Фотографии с Wikimedia Commons под свободными лицензиями, авторы в подписях; кадры Komoot показаны по ссылке с указанием источника. Страница для личного пользования.')}</p>
</div></section>

<footer>гравел · ноябрь 2026 · собрано из открытых источников</footer>
<div id="lbox"><img alt=""></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script src="tracks.js"></script>
<script>
(function(){{
  if(!window.L||!window.TRACKS)return;
  document.querySelectorAll('.map').forEach(el=>{{
    const files=JSON.parse(el.dataset.files), col=el.dataset.col;
    const m=L.map(el,{{scrollWheelZoom:false}});
    L.tileLayer('https://{{s}}.tile-cyclosm.openstreetmap.fr/cyclosm/{{z}}/{{x}}/{{y}}.png',{{maxZoom:18,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> · <a href="https://www.cyclosm.org">CyclOSM</a>'}}).addTo(m);
    const all=[];
    files.forEach((f,i)=>{{
      const pts=window.TRACKS[f]; if(!pts)return;
      L.polyline(pts,{{color:col,weight:i?3:4,opacity:i?.45:.95,dashArray:i?'6 6':null}}).addTo(m);
      if(!i){{L.circleMarker(pts[0],{{radius:6,color:'#fff',fillColor:col,fillOpacity:1,weight:2}}).addTo(m);
      L.circleMarker(pts[pts.length-1],{{radius:6,color:'#fff',fillColor:col,fillOpacity:1,weight:2}}).addTo(m);}}
      all.push(...pts);
    }});
    if(all.length)m.fitBounds(L.latLngBounds(all),{{padding:[20,20]}});
  }});
}})();
</script>
<script>
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

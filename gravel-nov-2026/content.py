# -*- coding: utf-8 -*-
"""Контент путеводителя: маршруты, куски, покрытие, фото-хайлайты, заезды.

Импортируется build.py. Все тексты здесь. Фото Commons: ключи img/<route>/<name>;
фото Komoot: по имени хайлайта из highlights.json (поле photos_k).
"""

ROUTES = []

# ---------------------------------------------------------------------------
# D. Обидуш → Коимбра
# ---------------------------------------------------------------------------
ROUTES.append(dict(
    id="d", letter="D", short="Обидуш → Коимбра", fav=True,
    title="Обидуш → Назаре → сосняк Лейрии → Фигейра → Мондегу → Коимбра",
    sub="Заброска машиной в Обидуш, назад поездом из Коимбры; расширение в лес Бусако",
    days="3 дня", km="174 км", up="~990 м", people="малолюдно",
    tags=["лагуна", "океан", "сосновый лес", "река", "замки", "Коимбра", "Бусако"],
    cover="d/nazare-sitio", cover_cap="Назаре (Nazaré) с мирадора Субéрку на Ситиу",
    lede="Единственный маршрут с заброской машиной, и этим он ценен: из Лиссабона нет поезда с велосипедом ни в Обидуш, ни в Калдаш. Дальше всё линейно на север: лагуна Обидуша с фламинго, Назаре с его волнами, 60 км бетонной велодорожки сквозь сосняк Лейрии, солеварни и дамбы Мондегу, финиш в Коимбре. Если останутся силы, третий день продолжается в лес Бусако.",
    surface=[
        ("Лагуна Обидуша (петля Komoot 45 км)", "асфальт 45 %, укатанный гравий 40 %, грунт 8 %", "https://www.komoot.com/tour/32136538"),
        ("Назаре и велодорожка на север (петля 47 км)", "асфальт 36 %, грунт 31 %, бетон 29 %, брусчатка 4 %", "https://www.komoot.com/tour/23775095"),
        ("Figueira → Nazaré по EV1 (тур 104 км, 2025)", "бетон 46 %, асфальт 45 %, грунт 6 %; велодорожка 54 % длины", "https://www.komoot.com/tour/2256367100"),
        ("Дамбы Мондегу (петля 39 км)", "бетон 39 %, асфальт 36 %, грунт 25 %", "https://www.komoot.com/tour/32157391"),
    ],
    segments=[
        dict(title="Обидуш и лагуна", km="0–16 км", text=[
            "Старт у стен Обидуша (Óbidos): час на улицу Direita и обход по стене, потом 6 км вниз к лагуне. Южный берег Lagoa de Óbidos это самая оценённая гравийка округи: укатанная тропа через птичий заказник с мостками, вышкой для наблюдения и точкой, где фламинго стоят в сотне метров от колеса. Деревянный мост через протоку у Várzea da Rainha и дальше тропа выводит к устью и пляжу Bom Sucesso.",
        ], photos_k=["Lagoa de Óbidos Gravel Trail", "Flamingo Viewing Point", "Wooden Bridge Over Coastal Stream", "Cycle Path Through the Bird Sanctuary"]),
        dict(title="Фош-ду-Арелью → Сан-Мартинью → Назаре", km="16–44 км", text=[
            "От Foz do Arelho дорога уходит на обрывы: мостки над океаном, мирадор Atlântico, потом Серра-ду-Бору с короткими крутыми тычками. Весь набор дня здесь. Спуск к Salir do Porto с самой высокой дюной Португалии и бухта-ракушка São Martinho do Porto, которую лучше всего видно с мирадора Salir.",
            "Последние 10 км к Назаре идут верхом по Caminho da Gralha над обрывами, а в город въезжаешь через Ситиу: мирадор Суберку, форт Сан-Мигел с маяком и экспозицией о больших волнах, Praia do Norte. В ноябре начинается сезон больших свеллов, и в хорошую погоду на мысу стоит толпа с биноклями.",
        ], photos_k=["Walkway over the cliffs", "View of São Martinho do Porto Bay from Miradouro de Salir", "Salir do Porto Dune", "Caminho da Gralha Coastal Cliff Trail", "View of Nazaré Beach from the Sítio cliffs", "Nazaré Lighthouse", "Praia do Norte Cliffs"]),
        dict(title="Сосняк Лейрии по Estrada Atlântica", km="44–105 км", text=[
            "Второй день ровный и быстрый. С Ситиу на север уходит Atlantic Coast Cycle Path, велодорожка из бетона и асфальта вдоль Mata Nacional de Leiria. Лес посадили в XIII веке, чтобы остановить дюны, и просеки здесь прямые на десятки километров. По дороге подсочка смолы на соснах, мирадор над Praia da Polvoeira, бухта Praia da Concha и маяк Penedo da Saudade в São Pedro de Moel.",
            "После Praia da Vieira и Pedrógão тропа ныряет в Mata do Urso к лагуне Ervedeira, которая в 2026 поднялась и затопила пляж с мостками, дальше дюны Pedrógão–Leirosa и дикий пляж Leirosa. Шторм Kristin в январе 2026 повалил здесь около 100 тысяч кубометров леса. Велодорожка и главные дороги расчищены, второстепенные просеки могут быть завалены, поэтому держимся Estrada Atlântica.",
        ], photos_k=["Atlantic Coast Cycle Path", "Long Straight Road in Mata Nacional de Leiria", "Praia da Concha", "Praia da Polvoeira panoramic viewpoint", "Pine Resin Harvesting Site", "Lagoa da Ervedeira", "Praia da Leirosa"]),
        dict(title="Эстуарий и дамбы Мондегу", km="105–174 км", text=[
            "В Фигейру въезжаем через солеварни и остров Morraceira, ночуем в городе. Третий день по дамбам Байшу-Мондегу: велодорожка вдоль канала и железки, рисовые поля, мельница, мирадор на болота. Это самый накатанный плоский гравий в выборке по тепловой карте Strava, но у него есть известный дефект: участок после железнодорожного моста местные в Komoot назвали «сплошные ямы». Сам мост на велосипеде не пересечь, объезд по дорогам. Ветер здесь северный и в лицо.",
            "Замок Montemor-o-Velho стоит прямо над дамбой, подъём к нему пять минут. В Коимбру въезжаем через Шупал (Mata Nacional do Choupal) и пешеходный мост Педру и Инеш, до университета на холме ещё 100 м набора пешком.",
        ], photos_k=["Figueira da Foz Salt Pans", "Canal Path and Railway Line between Figueira da Foz and Montemor-o-Velho", "Mondego River Cycle Path", "Potholes galore", "Castelo de Montemor-o-Velho", "Pedro and Inês Footbridge", "Paço das Escolas, University of Coimbra"]),
        dict(title="Расширение: лес Бусако", km="+27 км / 446 м", text=[
            "Третий день короткий, 46 км, поэтому его можно продлить в Mata Nacional do Buçaco: от Коимбры 27 км с набором 446 м, из них последние 5 км вверх. Лес заложили кармелиты в 1628 году, папская булла запрещала рубить деревья под страхом отлучения, и сейчас здесь 250 видов, включая кедр 1644 года. Въезд через Portas de Coimbra, каскад Fonte Fria в 144 ступени, дворец-отель в неомануэлино и Cruz Alta на 549 м с видом до океана. На велосипеде вход бесплатный или 1 €, зимой лес открыт 9–17.",
            "Выезд через Portas de Sula вниз в Luso к источнику, станция Luso-Buçaco на линии Beira Alta: региональный до Coimbra-B идёт 20–25 минут, по агрегаторам последний около 18:43. Расписание надо подтвердить в app CP, в официальных PDF этой линии нет.",
        ], photos_k=["Portas de Coimbra", "Buçaco Palace Hotel", "Fonte Fria", "Cruz Alta Viewpoint", "Cedro de São José", "Vale das Feteiras"]),
    ],
    stages=[
        ("Пт 6.11", "Óbidos → Lagoa de Óbidos → Foz do Arelho → São Martinho do Porto → Nazaré", "44 км", "~520 м", "гравий у лагуны, асфальт, холмы Serra do Bouro"),
        ("Сб 7.11", "Nazaré → São Pedro de Moel → просека Лейрии → Praia da Vieira → Lagoa da Ervedeira → Marinha das Ondas → Figueira da Foz", "83 км", "~400 м", "велодорожка Estrada Atlântica, бетон и асфальт"),
        ("Вс 8.11", "Figueira da Foz → дамбы Мондегу → Montemor-o-Velho → Coimbra", "46 км", "~65 м", "дамбы: бетон, асфальт с ямами, грунт 25 %"),
        ("Вс 8.11, опция", "Coimbra → Portas de Coimbra → Buçaco → Luso", "+27 км", "+446 м", "асфальт, последние 5 км подъём; назад региональным Luso → Coimbra-B"),
    ],
    sandnotes=[
        "Серра-ду-Бору между Foz do Arelho и São Martinho: короткие крутые холмы, набор первого дня в основном здесь.",
        "Подъём на Ситиу в Назаре: фуникулёр снова работает с 28.03.2026 (7:15–24:00), берут ли велосипеды, не подтверждено; объезд по дороге 110 м набора.",
        "Сосняк Лейрии после шторма Kristin: велодорожка расчищена, боковые просеки могут быть завалены. На Wikiloc есть трек 2026 года «Praia de São Pedro de Moel... fui ver o desastre que deixou a tempestade Kristin», по нему видно, как это выглядит.",
        "Мондегу: ямы на дамбе после ж/д моста, участок 150 м с запретом езды, мост не для велосипедов. В феврале 2026 прорвало дамбу Casais у Коимбры, брешь заделана, но работы на дамбах идут до конца года. Северный ветер.",
        "Глубокого песка на нитке нет ни по одному источнику; песчаные тропы только в стороне, к пляжам.",
    ],
    prac=[
        "Заброска: машиной до Óbidos, высадка у стен. Из Лиссабона ~1 ч.",
        "Обратно: IC Coimbra-B → Lisboa Santa Apolónia, в воскресенье последние 18:56, 20:20 и 20:56 (в Oriente 22:53). Велосипед на местах 15 и 17 во 2-м классе, бронь в app CP.",
        "Запасные выходы: станции Valado-Nazaré, Leiria, Figueira da Foz на линии Caldas ↔ Coimbra-B (около 5 поездов в день); из Figueira в Coimbra-B каждый час в xx:58.",
        "Ночёвки: Nazaré и Figueira da Foz, круглогодичные города.",
        "Световой день 07:10–17:25.",
    ],
    tracks=[
        ("EuroVelo 1 Portugal, секции 19–22 (официальные GPX, 2023)", "https://euroveloportugal.com/en/route/eurovelo1", "Foz do Arelho → Nazaré → Praia da Vieira → Marinha das Ondas → Figueira"),
        ("Komoot: Figueira da Foz → Nazaré (тур, май 2025)", "https://www.komoot.com/tour/2256367100", "104 км / 590 м, велодорожка 56 км"),
        ("Komoot: Lagoa de Óbidos Gravel Trail, петля от Caldas", "https://www.komoot.com/smarttour/32136538", "45 км / 415 м"),
        ("Komoot: Nazaré road to the top + Atlantic Coast Cycle Path", "https://www.komoot.com/smarttour/23775095", "47 км / 446 м"),
        ("Komoot: Mondego Cycle Path, петля от Fontela", "https://www.komoot.com/smarttour/32157391", "39 км / 105 м"),
        ("Komoot: Coimbra → Buçaco → Luso (план, велотуризм)", "https://www.komoot.com/plan/@40.211195,-8.429142,9.407z?sport=touringbicycle&p[0][loc]=40.2112000,-8.4291000&p[1][loc]=40.3750000,-8.3704000&p[2][loc]=40.3756000,-8.3650000&p[3][loc]=40.3833000,-8.3764000", "27,5 км / 446 м"),
        ("Wikiloc: São Pedro de Moel после шторма Kristin (2026)", "https://www.wikiloc.com/mountain-biking-trails/praia-de-sao-pedro-de-moel-com-partida-em-marinha-grande-fui-ver-o-desastre-que-deixou-a-tempestade-258456570", "состояние леса"),
        ("Wikiloc: Marinha Grande / São Pedro de Moel / Paredes", "https://www.wikiloc.com/mountain-biking-trails/marinha-grande-sao-pedro-de-moel-paredes-203283522", "40 км / 264 м, умеренно"),
        ("Wikiloc: PR6 FIG Rota das Salinas, Figueira", "https://www.wikiloc.com/hiking-trails/pr6-fig-rota-das-salinas-241957686", "солеварни пешком"),
        ("Bikemap: EuroVelo 1 Portugal, этапы", "https://www.bikemap.net/fr/c/437009/", "покрытие по этапам"),
    ],
    photos=[("d/obidos-lagoa", "Лагуна Обидуша"), ("d/obidos-vila", "Стены Обидуша"), ("d/sao-pedro-de-moel", "Маяк Пенеду-да-Саудаде"), ("d/montemor", "Замок Монтемор-у-Велью"), ("d/coimbra", "Коимбра над Мондегу")],
))

# ---------------------------------------------------------------------------
# E. Авейру → Коимбра
# ---------------------------------------------------------------------------
ROUTES.append(dict(
    id="e", letter="E", short="Авейру → Коимбра", fav=True,
    title="Риа-де-Авейру → Коста-Нова → Мира → Фигейра → Коимбра",
    sub="Самый ровный вариант: лагуны, дюны и дамбы Мондегу; расширение в лес Бусако",
    days="2–3 дня", km="137 км", up="~430 м", people="малолюдно",
    tags=["лагуна", "океан", "дюны", "солеварни", "Коимбра", "Бусако"],
    cover="e/costa-nova", cover_cap="Полосатые палейруш Коста-Новы (Costa Nova)",
    lede="Если главный критерий ровно, это он: от Авейру до Коимбры нет ни одного настоящего подъёма, кроме добровольного заезда на Серра-да-Боа-Виажен. Соль, лагуны, фламинго, полосатые дома, дюнная гравийка и рисовые поля. Плата за это: вторая половина первого дня идёт сосняком, где пейзаж не меняется километрами.",
    surface=[
        ("Мостки Риа-де-Авейру (петля 41 км)", "грунт 57 %, асфальт 21 %, бетон 13 %, укатанный 8 %", "https://www.komoot.com/tour/23775925"),
        ("Costa Nova → Areão (петля 49 км от маяка)", "грунт 46 %, асфальт 34 %, бетон 18 %; велодорожка 38 %, тропа 30 %", "https://www.komoot.com/tour/32147093"),
        ("Mira → Quiaios", "асфальт (дорогу заасфальтировали к марту 2025, отзыв Komoot)", "https://www.komoot.com/"),
        ("Дамбы Мондегу (петля 39 км)", "бетон 39 %, асфальт 36 %, грунт 25 %", "https://www.komoot.com/tour/32157391"),
    ],
    segments=[
        dict(title="Авейру: каналы, соль, мостки", km="0–15 км", text=[
            "Intercidades привозит в Авейру к девяти утра. Завтрак на рыбном рынке, молисейру на центральном канале, и сразу к Cais do Sal: солеварни Marinha da Troncalhada работают по старой технологии, в ноябре соль уже собрана, но пирамиды стоят. Если день позволяет, петля по мосткам Ria de Aveiro на север от города даёт 7 км деревянных настилов над лагуной, смотровую вышку и фламинго.",
        ], photos_k=["Aveiro Central Canal", "Aveiro Fish Market", "Cais do Sal", "Ria de Aveiro Boardwalks", "View of the Ria de Aveiro from the Observation Tower"]),
        dict(title="Барра, Коста-Нова и гравийка по берегу риа", km="15–40 км", text=[
            "Через мост к маяку Barra, самому высокому в Португалии, и дальше полосатые палейруш Costa Nova: рыбацкие склады, перекрашенные в полоску ещё в XIX веке. От Costa Nova на юг идёт гравийная дорожка по берегу риа, 7,8 км, с пикниковой зоной, качелями и точкой, где фламинго стоят у самого берега. У Vagueira дюны между риа и океаном, у Areão дорога переходит в Mira Dunes Route.",
        ], photos_k=["Barra Lighthouse", "Costa Nova Striped Houses", "Gravel Path Along the Ria de Aveiro", "View of Flamingos in Ria de Aveiro", "Dune Landscape of Ria de Aveiro"]),
        dict(title="Мира: лагуны и дюнная дорога", km="40–85 км", text=[
            "Praia de Mira стоит между океаном и пресной Barrinha de Mira с цветочным мостом; за ней Lagoa de Mira и канал Vala Real. Посёлок в ноябре наполовину закрыт, но жильё есть. Дальше на юг дюнная дорога Costa Nova → Mira → Tocha: по тепловой карте Strava это самая накатанная гравийная ось региона, а дорогу Mira → Quiaios к весне 2025 заасфальтировали. Песок остаётся только на боковых тропах к пляжам, туда не сворачиваем.",
        ], photos_k=["View of Praia de Mira from the boardwalk", "Flower Bridge of Mira", "Mira Dunes Route", "Dunas de Mira, Gândara e Gafanhas"]),
        dict(title="Серра-да-Боа-Виажен и Фигейра", km="85–91 км", text=[
            "Единственная высота у берега: Серра-да-Боа-Виажен, 257 м. Подъём по дороге от Quiaios, наверху мирадор Bandeira с видом на всё побережье до Назаре и мыс Мондегу с окаменелостями юрского периода. Прибрежную тропу Quiaios → Cabo Mondego не брать: в 2021 году её описывали как опасную, камнепад и край обрыва. Спуск в Buarcos и Фигейру, ночёвка.",
        ], photos_k=["Boardwalk of Quiaios and Murtinheira Beaches", "Bandeira Viewpoint", "Cabo Mondego Viewpoint", "Quiaios Waterfall", "Santa Catarina Fort Beach"]),
        dict(title="Дамбы Мондегу и Коимбра", km="91–137 км", text=[
            "Третий день тот же, что у маршрута D: солеварни Фигейры, велодорожка вдоль канала, рисовые поля, ямы после ж/д моста, замок Montemor-o-Velho, Шупал и мост Педру и Инеш в Коимбре. Подробности, покрытие и расширение в Бусако смотри в карточке D.",
        ], photos_k=["Canal Path and Railway Line between Figueira da Foz and Montemor-o-Velho", "Castelo de Montemor-o-Velho", "Pedro and Inês Footbridge"]),
    ],
    stages=[
        ("Пт 6.11", "Aveiro → солеварни → Barra → Costa Nova → Vagueira → Praia de Mira (с петлёй по мосткам +25 км)", "37–62 км", "~50–150 м", "асфальт, велодорожки, гравийка по берегу риа"),
        ("Сб 7.11", "Praia de Mira → Praia da Tocha → Quiaios → Serra da Boa Viagem → Figueira da Foz", "54 км", "~310 м", "дюнная дорога, асфальт Mira → Quiaios, подъём на серру по дороге"),
        ("Вс 8.11", "Figueira da Foz → дамбы Мондегу → Montemor-o-Velho → Coimbra", "46 км", "~65 м", "как в D"),
        ("Вс 8.11, опция", "Coimbra → Buçaco → Luso", "+27 км", "+446 м", "как в D"),
    ],
    sandnotes=[
        "Глубокий песок только на лесных тропах в стороне от дюнной дороги (CycleBlaze, 2023). Держаться асфальта и велодорожки.",
        "Береговая тропа Quiaios → Cabo Mondego: камнепад, край обрыва (2021). На серру по дороге.",
        "Дамбы Мондегу: ямы, участок, где велосипед надо вести, ж/д мост не для велосипедов; после прорыва дамбы Casais в феврале 2026 работы идут до конца года. Северный ветер.",
        "Praia de Mira в ноябре: часть кафе закрыта, еду на вечер искать заранее.",
    ],
    prac=[
        "Туда: IC 521 Lisboa Santa Apolónia 06:30 → Oriente 06:39 → Aveiro 09:04 (пн–сб) или IC 721 09:30 → Aveiro 12:04 (ежедневно). Места 15 и 17, бронь.",
        "Обратно: IC Coimbra-B → Lisboa, вс последние 18:56, 20:20, 20:56.",
        "Запасные выходы: из Figueira da Foz в Coimbra-B региональный каждый час в xx:58; из Aveiro IC весь день.",
        "Ночёвки: Praia de Mira (мало, часть закрыта в ноябре), Figueira da Foz (много).",
        "Вариант на два дня: Aveiro → Figueira 76 км / 308 м и Figueira → Coimbra 46 км.",
    ],
    tracks=[
        ("EuroVelo 1 Portugal, секции 23–24 (официальные GPX)", "https://euroveloportugal.com/en/route/eurovelo1", "Aveiro → Praia de Mira → Figueira"),
        ("Komoot: Ria de Aveiro Boardwalks, петля от Esgueira", "https://www.komoot.com/smarttour/23775925", "41 км / 104 м"),
        ("Komoot: Costa Nova, петля от маяка Авейру", "https://www.komoot.com/smarttour/32147093", "49 км / 60 м"),
        ("Komoot: Castro de Santa Olalla, петля от Figueira", "https://www.komoot.com/smarttour/23775103", "45 км / 332 м, Serra da Boa Viagem"),
        ("Komoot: Mondego Cycle Path, петля от Fontela", "https://www.komoot.com/smarttour/32157391", "39 км / 105 м"),
        ("Wikiloc: Lagoas de Mira (Barrinha, Lagoa, Praia de Mira)", "https://www.wikiloc.com/hiking-trails/lagoas-de-mira-barrinha-lagoa-e-praia-de-mira-mira-58311166", "петля по лагунам"),
        ("Wikiloc: Trails of the Serra da Boa Viagem", "https://www.wikiloc.com/hiking-trails/boa-viagem-139301217", "тропы серры"),
        ("Bikemap: EuroVelo 1 Portugal, этап Ovar → Mira", "https://www.bikemap.net/fr/c/437009/", "78 км / 109 м"),
    ],
    photos=[("e/aveiro", "Солеварни Авейру"), ("e/praia-de-mira", "Прайя-де-Мира"), ("e/figueira", "Мыс Мондегу над Фигейрой"), ("d/montemor", "Замок Монтемор-у-Велью")],
))

# ---------------------------------------------------------------------------
# C. Алкева
# ---------------------------------------------------------------------------
ROUTES.append(dict(
    id="c", letter="C", short="Алкева", fav=True,
    title="Алкева петлёй: Эвора → экопишта → Монсараш → Амиейра → Портел → Эвора",
    sub="Самый безлюдный, с озером и мегалитами, поезд в обе стороны",
    days="3 дня", km="156 км", up="~1 340 м", people="почти никого",
    tags=["озеро", "монтаду", "мегалиты", "замки", "тёмное небо"],
    cover="c/monsaraz", cover_cap="Монсараш (Monsaraz) над водохранилищем Алкева",
    lede="Алкева, самое большое искусственное озеро Западной Европы, заполнена на 80 %. Вокруг монтаду, кромлехи и две крепости на холмах, а на тепловой карте Strava почти пусто: проверенных ниток мало, зато нет и людей. Первый день почти плоский по бывшей железной дороге, второй короткий вдоль воды, третий через Портел обратно к поезду.",
    surface=[
        ("Ecopista Évora → Reguengos (39,7 км)", "официального описания нет; по фото Komoot укатанный светлый гравий шириной ~3 м, без асфальта", "https://www.komoot.com/highlight/6717521"),
        ("Reguengos → Xerez → Monsaraz (петля 50 км)", "грунт 35 %, асфальт 32 %, бетон 22 %, гравий 10 %", "https://www.komoot.com/tour/32163822"),
        ("Corval → дамба через озеро → Portel (петля 83 км)", "асфальт 92 %, тихие дороги", "https://www.komoot.com/tour/31402021"),
    ],
    segments=[
        dict(title="Эвора и экопишта", km="0–45 км", text=[
            "Поезд приходит в Эвору в 08:47. Если выехать в 07:02, до старта остаётся час на римский храм, собор и капеллу костей; акведук Água de Prata XVI века уводит из города на запад, но нам на восток. Ecopista de Reguengos открыта в сентябре 2024 на насыпи бывшей железной дороги: 39,7 км через монтаду с пробковыми дубами, бывшие станции Machede и Montoito и мост над Дегебе. По фото это укатанный светлый гравий шириной метра три, без асфальта. Сервисов между Эворой и Montoito нет, Montoito в километре от линии с рестораном и кафе.",
        ], photos_k=["Roman Temple of Évora", "Chapel of Bones, Évora", "Silver Water Aqueduct (Évora)", "End of the Ecopista Évora–Reguengos de Monsaraz"]),
        dict(title="Реггенгуш, мегалиты, Монсараш", km="45–63 км", text=[
            "Reguengos de Monsaraz это вода, кафе на площади Liberdade и винодельни. Дальше гончарная деревня São Pedro do Corval и мегалиты: менгир Outeiro 5,6 м, менгир Bulhoa с гравировками, кромлех Xerez, который перенесли на холм при затоплении долины, и монастырь Orada рядом. Подъём к Monsaraz 5 км и 132 м, ночёвка внутри стен, закат над озером со стен замка.",
        ], photos_k=["Praça da Liberdade, Reguengos de Monsaraz", "Menhir of Outeiro", "Menir da Bulhoa", "Cromlech of Xerez", "Convento da Orada", "Climb up to Monsaraz Castle", "Monsaraz Castle", "View of Monsaraz and the Alqueva Dam", "Historic Streets of Monsaraz"]),
        dict(title="Вдоль Алкевы к Амиейре", km="63–98 км", text=[
            "Короткий второй день: вниз от Монсараша мимо лошадей поместья São Lourenço do Barrocal, через Campinho и по тихим дорогам к заливу Дегебе и марине Amieira с плавучими домами. 35 км и 290 м, остаётся время на озеро. Длинный вариант через Mourão с замком и качелями над водой, по дороге-дамбе через озеро и к плотине Alqueva высотой 96 м даёт 91 км и 840 м, он лежит пунктиром на карте.",
        ], photos_k=["Wild Horses of São Lourenço do Barrocal", "Castle of Mourão", "Swing with a View of Mourão Castle and Alqueva Reservoir", "Alqueva Lake", "Degebe River"]),
        dict(title="Портел и обратно в Эвору", km="98–154 км", text=[
            "Третий день через ZPE Reguengos, орнитологическую зону с тихой дорогой, к Portel, где замок закрыт на реставрацию и виден только снаружи, и дальше 40 км монтаду до Эворы к поезду 16:51 или 19:14. Готовой гравийной нитки на этом куске нет, трек проложен планировщиком по тихим дорогам.",
            "Alqueva это первый в мире сертифицированный заповедник тёмного неба. В ноябре темнеет к 18:00, так что обе ночи небо будет уже до ужина.",
        ], photos_k=["Scenic road in ZPE Reguengos", "View from the Walkable Castle Wall in Portel", "View of Évora from Alto de São Bento Windmills"]),
    ],
    stages=[
        ("Пт 6.11", "Évora → Ecopista: Machede → Montoito → Reguengos → Cromeleque do Xerez → Monsaraz", "65 км", "~540 м", "экопишта: укатанный гравий; дальше тихий асфальт и грунт"),
        ("Сб 7.11", "Monsaraz → Campinho → Amieira", "35 км", "~290 м", "тихий асфальт и грунт; вариант через Mourão и плотину 91 км / 840 м"),
        ("Вс 8.11", "Amieira → Portel → Évora", "56 км", "~510 м", "дороги через монтаду"),
    ],
    sandnotes=[
        "Данных о песке вокруг Алкевы нет ни в одном источнике. На соседней экопиште Évora → Arraiolos в 2023 году отмечали пятна рыхлого песка.",
        "Экопишта: укатанный гравий без асфальта; после дождя может раскиснуть, отзывов об этом нет. Параллельно идёт N256 с небольшим трафиком.",
        "Длинный второй день через Mourão добавляет 56 км и 550 м; решать по погоде и ветру утром.",
        "Жильё: Amieira и Portel небольшие. Если не найдётся, две ночи в Monsaraz и петля налегке.",
    ],
    prac=[
        "Туда: IC Lisboa Oriente → Évora пт 07:02 или 09:02 (также 13:35, 17:02, 19:02), 1 ч 45 мин. Места 12 и 18 во 2-м классе, бронь обязательна.",
        "Обратно: IC Évora → Oriente вс 09:14, 16:51, 19:14.",
        "Ночёвки: Monsaraz (внутри стен несколько casas), Amieira или Portel.",
        "Вода Алкевы 19.10.2026: 80 % (APA).",
        "Запасной выход: из Beja IC с пересадкой в Casa Branca (вс 16:06, 18:20), но Beja в стороне от петли.",
    ],
    tracks=[
        ("Komoot: Cromlech of Xerez – Monsaraz Castle, петля от Reguengos", "https://www.komoot.com/tour/32163822", "50 км / 458 м"),
        ("Komoot: View of Alqueva, петля через дамбу от Corval (шоссе)", "https://www.komoot.com/tour/31402021", "83 км / 731 м"),
        ("Bikemap: Évora → Monsaraz", "https://www.bikemap.net/en/c/270511", "66,6 км / 374 м"),
        ("Bikemap: Évora → Mourão через Monsaraz", "https://www.bikemap.net/en/c/286758/", "94,6 км / 501 м"),
        ("Wikiloc: Amieira → Alqueva com o lago a seus pés (PR1 Portel)", "https://www.wikiloc.com/hiking-trails/amieira-a-alqueva-com-o-lago-a-seus-pes-pr-1-portel-13399829", "пешая петля у Амиейры"),
        ("Wikiloc: PR1 RMZ Escritas de pedra e cal", "https://www.wikiloc.com/hiking-trails/pr1-rmz-escritas-de-pedra-e-cal-alargado-209201350", "мегалиты Reguengos пешком"),
        ("Wikiloc: PR1 MOU Património vivo de Mourão", "https://www.wikiloc.com/hiking-trails/pr1-mou-patrimonio-vivo-de-mourao-encurtado-209083596", "Mourão"),
    ],
    photos=[("c/evora", "Римский храм Эворы"), ("c/alqueva", "Плотина Алкева"), ("c/xerez", "Кромлех Шереш"), ("c/amieira", "Марина Амиейра"), ("c/ecopista", "Экопишта")],
))

# ---------------------------------------------------------------------------
# A. Побережье Алентежу
# ---------------------------------------------------------------------------
ROUTES.append(dict(
    id="a", letter="A", short="Алентежу, берег", fav=False,
    title="Побережье Алентежу: паром в Трою → Компорта → Санту-Андре → Синеш → Порту-Кову → Милфонтеш → Кабу-Сардан",
    sub="Самый природный: рис, лагуны, скалы и аисты, набор малый",
    days="2–3 дня", km="150–180 км", up="~740–1 200 м", people="малолюдно",
    tags=["океан", "лагуны", "рис", "скалы", "аисты"],
    cover="a/cabo-sardao", cover_cap="Кабу-Сардан (Cabo Sardão)",
    lede="Классика EuroVelo 1 от парома в Трое до скал Кабу-Сардана. Первый день плоский почти целиком, второй короткий и самый фотогеничный. Песок здесь есть, но локализован и обходится по дорогам. Слабое место одно: обратно к поезду 35–50 км в гору.",
    surface=[
        ("EV1 Setúbal → Porto Covo (Bikemap, 83 км)", "асфальт 89 %, грунт 3 %", "https://www.bikemap.net/en/r/17525416/"),
        ("EV1 Porto Covo → Aljezur (Bikemap, 76 км)", "асфальт 51 %, грунт 18 %, из них песок 6 км (8 %)", "https://www.bikemap.net/en/r/17525417/"),
        ("Melides → Costa de Santo André (петля 85 км)", "грунт 46 %, асфальт 28 %, бетон 25 %", "https://www.komoot.com/tour/23773128"),
        ("Santo André → Melides по дорогам (петля 64 км)", "асфальт 92 %", "https://www.komoot.com/tour/10318203"),
    ],
    segments=[
        dict(title="Троя, Компорта, рис", km="0–30 км", text=[
            "Паром из Сетубала причаливает к Cais Sul в Трое прямо у римских руин рыбозасолочного комплекса. Полуостров это сосны и дюны, через 20 км начинаются рисовые поля Компорты с гнёздами аистов на церкви. Карраскейра с её свайным причалом в 5 км в сторону, по плоскому, и стоит крюка.",
        ], photos_k=["Rice Fields of Comporta / Galé", "Boardwalk Through the Dunes of Comporta / Galé"]),
        dict(title="Мелидеш, лагуна Санту-Андре, Синеш", km="30–75 км", text=[
            "От Carvalhal гравийная двойная колея 6,5 км, дальше тихий асфальт до Melides с его лагуной и пляжем. Лагуна Santo André в ноябре закрыта от моря песчаной косой, заповедник полон птиц; официальный GPX EuroVelo здесь на 4,5 км уходит в песок, поэтому идём по дорогам через Vila Nova de Santo André и Costa de Santo André. Синеш обходится по прибрежной дороге, промзона остаётся слева, первый нормальный пляж после неё São Torpes.",
        ], photos_k=["Melides Beach", "Costa de Santo André Beach", "São Torpes Beach"]),
        dict(title="Порту-Кову → Милфонтеш → Кабу-Сардан", km="75–150 км", text=[
            "Самый красивый кусок: бухта Engardaceira, остров Pessegueiro с фортом XVI века, пляж Malhão и скала аистов. Сразу к северу от Milfontes на EV1 0,7 км глубокого песка, объезд по N390 и мосту через Миру. Дальше Almograve, дюны и обрывы Costa Vicentina, маяк Cabo Sardão со скальной аркой и единственными в мире аистами, гнездящимися на морских скалах. Trilho dos Pescadores вдоль обрывов только пешком, на велосипеде его не трогаем.",
        ], photos_k=["Engardaceira Beach", "Pessegueiro Island Beach", "Malhão Beach", "Stork Rock", "Sandy coastal trail in Parque Natural", "View of the Mira River and the bridge at Vila Nova de Milfontes", "View of Almograve Beach", "Dunes and Cliffs of the Costa Vicentina", "Cabo Sardão Lighthouse", "Costa Vicentina Rock Arch and Cliffs", "Stork nests on the Costa Vicentina cliffs", "Zambujeira do Mar Beach"]),
    ],
    stages=[
        ("Пт 6.11", "Setúbal → паром Tróia → Comporta → Carvalhal → Melides → Lagoa de Santo André → Sines → Porto Covo", "87–97 км", "~320–460 м", "асфальт и гравий; EV1 секции 12–11; объезд песка у лагуны по дорогам"),
        ("Сб 7.11", "Porto Covo → Vila Nova de Milfontes → Almograve → Cabo Sardão → Zambujeira do Mar", "51 км", "~280 м", "EV1 секции 10–9; 0,7 км песка к северу от Milfontes обходится по дороге"),
        ("Вс 8.11", "Zambujeira → Santa Clara-Sabóia (станция) или Milfontes → Funcheira (станция)", "34 / 49 км", "~460 / 400 м", "асфальт в гору, через серру"),
    ],
    sandnotes=[
        "Lagoa de Santo André: GPX EuroVelo секции Sines → Melides содержит около 4,5 км песка вокруг лагуны. Обход: N261 и местные дороги.",
        "Сразу к северу от Milfontes на EV1 около 0,7 км «mushy deep sand» (2019). Обход по N390 и мосту.",
        "Около 0,7 км песка у Cabo Sardão; к маяку по асфальту.",
        "Comporta → Carvalhal: гравийная двойная колея 6,5 км, на север зарастает травой.",
        "Trilho dos Pescadores: только пешком. Не заезжать на тропы Rota Vicentina вдоль обрывов.",
        "Подъезд к Sines с севера около 10 км вдоль A26: планировать по прибрежной дороге через Santo André.",
        "Жильё в Porto Covo и Zambujeira в ноябре не подтверждено; Milfontes и Sines работают круглый год.",
    ],
    prac=[
        "Туда: Fertagus Roma-Areeiro → Setúbal каждые 20 мин, 58 мин, велосипед бесплатно. Паром Setúbal (Doca do Comércio) → Tróia: 07:30 и каждый час в :30 до 19:30, ferry, 5,50 € человек + 5,50 € велосипед.",
        "Обратно: IC из Santa Clara-Sabóia вс 10:25, 15:20, 19:25 или из Funcheira 10:56, 15:54, 19:54 (в Oriente 12:56, 17:56, 21:56). Места 12 и 18, бронь.",
        "Ночёвки: Porto Covo, Milfontes, Zambujeira.",
        "Из Sines поездов нет с 1990 года.",
    ],
    tracks=[
        ("EuroVelo 1 Portugal, секции 9–12 (официальные GPX)", "https://euroveloportugal.com/en/route/eurovelo1", "Odeceixe → Milfontes → Sines → Melides → Tróia"),
        ("Portuguese Trails: EuroVelo 1 Alentejo, GPX", "https://www.portuguesetrails.com/sites/default/files/routes/gpx/Eurovelo_Alentejo.gpx", "весь Алентежу одним файлом"),
        ("Komoot: Tróia → Comporta → Melides → Santo André → Sines → Porto Covo (план, гравел)", "https://www.komoot.com/plan/@38.486177,-8.883885,9.407z?sport=mtb_easy&p[0][loc]=38.4859195,-8.8836429&p[1][loc]=38.3803765,-8.7859968&p[2][loc]=38.3692980,-8.7937612&p[3][loc]=38.1472980,-8.7285840&p[4][loc]=38.0541917,-8.8162999&p[5][loc]=37.9565490,-8.8689639&p[6][loc]=37.8517287,-8.7918410", "97 км / 462 м"),
        ("Komoot: Porto Covo → Milfontes → Cabo Sardão → Zambujeira (план, гравел)", "https://www.komoot.com/plan/@37.851792,-8.791889,9.407z?sport=mtb_easy&p[0][loc]=37.8517287,-8.7918410&p[1][loc]=37.7252803,-8.7822865&p[2][loc]=37.6542256,-8.7567390&p[3][loc]=37.5986309,-8.8161381&p[4][loc]=37.5256480,-8.7848108", "51 км / 283 м"),
        ("Bikemap: EV1 Setúbal → Porto Covo", "https://www.bikemap.net/en/r/17525416/", "83 км / 531 м"),
        ("Bikemap: EV1 Porto Covo → Aljezur", "https://www.bikemap.net/en/r/17525417/", "76 км / 558 м, песок 6 км"),
        ("Komoot: Melides – Costa de Santo André, петля", "https://www.komoot.com/tour/23773128", "85 км / 935 м"),
        ("AllTrails: Tróia – Melides", "https://www.alltrails.com/trail/portugal/setubal--3/troia-melides", "87 км / 465 м туда-обратно"),
    ],
    photos=[("a/comporta", "Рисовые поля Компорты"), ("a/carrasqueira", "Свайный причал Карраскейры"), ("a/santo-andre", "Лагуна Санту-Андре"), ("a/porto-covo", "Порту-Кову и остров Пессегейру"), ("a/milfontes", "Устье Миры в Милфонтеше"), ("a/zambujeira", "Замбужейра-ду-Мар")],
))

# ---------------------------------------------------------------------------
# B. Садо и побережье
# ---------------------------------------------------------------------------
ROUTES.append(dict(
    id="b", letter="B", short="Садо + берег", fav=False,
    title="Садо и побережье без паромов: Грандола → Алкасер → Карраскейра → Компорта → Синеш → Порту-Кову → Милфонтеш → Фуншейра",
    sub="Та же природа, что A, плюс эстуарий Садо, но все три дня полные",
    days="3 дня", km="~220 км", up="~1 130 м", people="почти никого",
    tags=["эстуарий", "фламинго", "рис", "океан", "скалы"],
    cover="b/sado", cover_cap="Эстуарий Садо (Estuário do Sado)",
    lede="Вариант для тех, кто хочет три полных дня и не хочет зависеть от парома. Первый день начинается в 11:30 на станции Грандола, идёт к замку Алкасера и через рисовые поля и каналы заповедника Садо к свайному причалу Карраскейры. Дальше как маршрут A.",
    surface=[
        ("Alcácer → RN Sado → Carrasqueira (петля 62,5 км)", "грунт 86 %, асфальт 10 %, брусчатка 1 %; на маршруте ступени", "https://www.komoot.com/tour/32127350"),
        ("Дальше как A", "см. покрытие маршрута A", "#a"),
    ],
    segments=[
        dict(title="Алкасер и заповедник Садо", km="0–75 км", text=[
            "27 км асфальта от станции до Alcácer do Sal: замок-поусада над рекой, соляные галеоны на набережной, пешеходный мост через Садо. Дальше петля по заповеднику: 86 % грунта по дамбам между рисовыми чеками и каналами, фламинго круглый год, зимой больше. По тепловой карте Strava здесь ездят единицы. Свайный причал Карраскейры строили рыбаки в 1950-х, чтобы добираться до лодок через ил в отлив. Ночёвка в Comporta или Carvalhal.",
        ], photos_k=["Pousada Castle of Alcácer do Sal", "Pedestrian Bridge over the Sado in Alcácer do Sal", "View of Alcácer do Sal and Castle Over the Rice Fields", "Galeões do Sal of Alcácer do Sal", "Carrasqueira Palafitic Pier", "Rice Fields of Comporta / Galé"]),
        dict(title="Побережье и выезд к поезду", km="75–220 км", text=[
            "Второй день повторяет первый день маршрута A: Melides, лагуна Santo André, Sines, Porto Covo. Третий день самый длинный: 18 км до Милфонтеша и 49 км с 400 м набора до станции Funcheira к поезду 15:54 или 19:54. Это цена отсутствия паромов.",
        ], photos_k=[]),
    ],
    stages=[
        ("Пт 6.11", "ст. Grândola → Alcácer do Sal → рисовые поля RN Sado → Carrasqueira → Comporta", "~75 км", "~250 м", "27 км асфальта, дальше грунт 86 %, ступени"),
        ("Сб 7.11", "Comporta → Melides → Santo André → Sines → Porto Covo", "~80 км", "~400 м", "как день 1 маршрута A"),
        ("Вс 8.11", "Porto Covo → Vila Nova de Milfontes → Funcheira (станция)", "67 км", "~480 м", "18 км по побережью, затем 49 км асфальта в гору"),
    ],
    sandnotes=[
        "Песка на петле Садо в отзывах нет, но есть ступени и участки, где велосипед несут (Komoot).",
        "Дальше те же места, что в A: лагуна Santo André, север Milfontes, промзона Sines.",
        "Старт в 11:30 и закат в 17:25: на первый день 6 часов света на 75 км с грунтом, без запаса на осмотры.",
    ],
    prac=[
        "Туда: IC 570 Lisboa Oriente 10:02 → Grândola 11:21. Места 12 и 18, бронь.",
        "Обратно: IC из Funcheira вс 15:54 → Oriente 17:56 или 19:54 → 21:56.",
        "Ночёвки: Comporta или Carvalhal, Porto Covo.",
        "В Alcácer do Sal поездов нет с 2011 года.",
    ],
    tracks=[
        ("Komoot: Carrasqueira – Alcácer do Sal, петля по заповеднику", "https://www.komoot.com/tour/32127350", "62,5 км / 244 м, грунт 86 %"),
        ("Komoot: Alcácer → Carrasqueira → Comporta → Tróia (план, гравел)", "https://www.komoot.com/plan/@38.373208,-8.512401,9.407z?sport=mtb_easy&p[0][loc]=38.3729735,-8.5122705&p[1][loc]=38.3751000,-8.7845200&p[2][loc]=38.3803765,-8.7859968&p[3][loc]=38.4859195,-8.8836429", "50 км / 187 м"),
        ("AllTrails: Açude de Vale dos Coelheiros – Comporta – Cais da Carrasqueira", "https://www.alltrails.com/trail/portugal/setubal--3/carrasqueira-acude-de-vale-dos-coelheiros-comporta-cais-palafitico-da-carrasquei", "49 км / 195 м"),
        ("Дальше нитки маршрута A", "#a", ""),
    ],
    photos=[("b/alcacer", "Алкасер-ду-Сал над Садо"), ("a/carrasqueira", "Свайный причал Карраскейры"), ("a/comporta", "Рис Компорты")],
))

# ---------------------------------------------------------------------------
# F. Алгарве и Уэльва
# ---------------------------------------------------------------------------
ROUTES.append(dict(
    id="f", letter="F", short="Алгарве + Уэльва", fav=False,
    title="Восточный Алгарве и Уэльва: Фару → Тавира → VRSA → паром → Исла-Кристина → Эль-Ромпидо → назад к парому",
    sub="Самый ровный из всех, но самый людный и с тесной воскресной логистикой",
    days="3 дня", km="160–200 км", up="~660 м", people="людно",
    tags=["лагуна", "солеварни", "марши", "две страны"],
    cover="f/cacela", cover_cap="Касела-Велья (Cacela Velha) над Риа-Формозой",
    lede="Риа-Формоза и марши Уэльвы дают самый ровный профиль в выборке, но по тепловой карте Strava это и самая плотная сетка велосипедистов. Виа-верде-дель-Литораль частично заброшена: мост Тавирона закрыт, за Лепе 4 км песка только пешком. Рабочая схема держится западного куска виа-верде и прибрежных дорог.",
    surface=[
        ("EV1 VRSA → Faro (официальный GPX, 68 км)", "по OSM грунт ~35 %, твёрдое ~64 %; между Olhão и Tavira грунт около 60 %", "https://euroveloportugal.com/en/route/eurovelo1"),
        ("Ayamonte → Isla Cristina по кругу (28 км, Komoot)", "бетон 45 %, грунт 23 %, асфальт 19 %; велодорожка 48 %, паром 6 %", "https://www.komoot.com/smarttour/e986950657/from-ayamonte-to-isla-cristina-circular-via-isla-del-moral"),
        ("Марши Гуадианы от Isla Cristina (петля 53 км, 2026)", "грунт 38 %, асфальт 32 %, бетон 17 %, укатанный 13 %", "https://www.komoot.com/tour/44796364"),
    ],
    segments=[
        dict(title="Фару → Тавира по Эковии", km="0–35 км", text=[
            "Из старого Фару через Arco da Vila на восток: кубические дома Ольяна, мостки Эковии по Риа-Формоза, солеварни Фузеты. Грунт здесь около 60 %, тропы местами песчаные, но проезжаемые; обрушенный мост Fuseta–Olhão починили в конце 2024. В Тавире «римский» мост, замок с садом и ночёвка.",
        ], photos_k=["Arco da Vila, Faro", "Olhão Old Town", "Ecovia boardwalk in Ria Formosa Natural Park", "Fuseta Salt Pans", "Anchor Cemetery, Praia do Barril", "Tavira Roman Bridge"]),
        dict(title="Касела, Каштру-Марин, паром в Испанию", km="35–75 км", text=[
            "Cacela Velha стоит на обрыве над лагуной: крепость, церковь, вид на косу. Дальше Monte Gordo с дюнными мостками, помбалинский VRSA и в 4 км солончаки Castro Marim с фламинго и замком. Паром через Гуадиану в Ayamonte идёт 15 минут, часы переводятся на час вперёд.",
        ], photos_k=["Cacela Velha — Historic Village and Fortress", "View of the Ria Formosa lagoon", "Flamingos in the Castro Marim Salt Marsh", "Castro Marim Castle", "Praça Marquês de Pombal, VRSA"]),
        dict(title="Исла-Кристина и марши Уэльвы", km="75–200 км", text=[
            "От Аямонте виа-верде до Исла-Кристины: щебень, местами песчано, но ездят. Мостки Pasarela de la Gola, марши с фламинго, приливная мельница, голубятня Huerta Noble на 36 тысяч гнёзд. Дальше по побережью Islantilla → La Antilla → El Rompido с косой Flecha и маршами Río Piedras. Третий день возвращается к парому через Cartaya и Lepe по дорогам, виа-верде у Lepe не брать. Пунта-Умбрия и Уэльва добавляют 40 км, а поезда оттуда в Лиссабон нет.",
        ], photos_k=["Pasarela de la Gola", "Piedras River Marshes"]),
    ],
    stages=[
        ("Пт 6.11", "Faro → Olhão → Fuseta → Santa Luzia → Tavira", "35 км", "~190 м", "Ecovia: грунт ~60 %, тропы местами песчаные"),
        ("Сб 7.11", "Tavira → Cacela Velha → Monte Gordo → VRSA → паром → Ayamonte → Isla Cristina → La Antilla → El Rompido", "~78 км", "~250 м", "грунт ~54 % после Cacela; виа-верде щебень; мост Tavirona закрыт, объезд N-431"),
        ("Вс 8.11", "El Rompido → Cartaya → Lepe → Ayamonte (паром до 16:15 PT)", "45–55 км", "~150 м", "дороги, виа-верде у Lepe не брать"),
    ],
    sandnotes=[
        "Vía Verde del Litoral: за Lepe около 4 км «sólo es posible a pie»; перед Lepe короткий песчаный участок.",
        "Мост La Tavirona через Río Piedras закрыт с 2014 года. Объезд по мосту N-431 у Lepe/Cartaya.",
        "Isla Cristina → Ayamonte: щебень «ciclable», в Komoot «partly good gravel road, but also very sandy» (2022).",
        "Tavira → Fuseta → Olhão: около 7 км грунта, «sandy trails» (2025).",
        "Воскресенье: паром Ayamonte 17:15 исп. = 16:15 PT, до вокзала VRSA 1,3 км, поезд 16:34. Опоздание = ночёвка в Фару.",
    ],
    prac=[
        "Туда: IC 570 Oriente 10:02 → Faro 13:31 (места 12 и 18); R 13:56 → Tavira 14:29 → VRSA 14:58.",
        "Паром Ayamonte ↔ VRSA: 2,50 € + 1,60 € велосипед; пн–сб из VRSA 9:30, 10:30, 11:30, 12:30, 14:30, 15:30, 17:00 PT; вс из Ayamonte последний 17:15 исп.",
        "Обратно: R VRSA 16:34 → Faro 17:35; IC 674 Faro 18:15 → Oriente 21:56.",
        "Ночёвки: Tavira, El Rompido или Isla Cristina.",
        "Часы: Испания на час вперёд.",
    ],
    tracks=[
        ("EuroVelo 1 Portugal, секция 1 VRSA → Faro (GPX 10.12.2024)", "https://euroveloportugal.com/files/2023/05/EuroVelo-1-Portugal-Section-01-Vila-Real-de-Santo-Antonio-Faro-2024-12-10.gpx", "68 км / ~410 м"),
        ("Portuguese Trails: Ecovia do Litoral, GPX", "https://www.portuguesetrails.com/sites/default/files/routes/gpx/EcoviaAlgarve1a4.gpx", "весь Алгарве"),
        ("Komoot: Faro → Tavira → Cacela → VRSA (план, гравел)", "https://www.komoot.com/plan/@37.016334,-7.935292,9.407z?sport=mtb_easy&p[0][loc]=37.0162944,-7.9351820&p[1][loc]=37.0270369,-7.8411287&p[2][loc]=37.0551731,-7.7461861&p[3][loc]=37.1262493,-7.6499121&p[4][loc]=37.1573916,-7.5462157&p[5][loc]=37.2136976,-7.4420708", "65 км / 341 м"),
        ("Komoot: Ayamonte → Isla Cristina по кругу через Isla del Moral", "https://www.komoot.com/smarttour/e986950657/from-ayamonte-to-isla-cristina-circular-via-isla-del-moral", "27,5 км"),
        ("Komoot: марши Гуадианы, петля от Isla Cristina (2026)", "https://www.komoot.com/tour/44796364", "53 км / 373 м"),
        ("Islantilla: Islantilla – El Rompido, GPX", "https://www.islantilla.es/wp-content/uploads/2024/03/islantilla-el-rompido-cycling-friendly.zip", "переправа через Río Piedras"),
        ("AllTrails: Tavira – Loulé via Ecovia do Litoral", "https://www.alltrails.com/trail/portugal/faro/tavira-loule-via-ecovia-do-litoral", "61 км / 473 м"),
    ],
    photos=[("f/ria-formosa", "Риа-Формоза у Ольяна"), ("f/tavira", "Тавира"), ("f/castro-marim", "Каштру-Марин"), ("f/isla-cristina", "Марши Исла-Кристины"), ("f/el-rompido", "Коса Эль-Ромпидо")],
))

# ---------------------------------------------------------------------------
# G. Садо коротко
# ---------------------------------------------------------------------------
ROUTES.append(dict(
    id="g", letter="G", short="Садо коротко", fav=False,
    title="Садо коротко: Грандола → Алкасер → Карраскейра → Компорта → Троя → паром",
    sub="Два дня, ноль подъёмов, эстуарий и рис",
    days="2 дня", km="110–135 км", up="~490 м", people="почти никого",
    tags=["эстуарий", "фламинго", "рис"],
    cover="a/carrasqueira", cover_cap="Свайный причал Карраскейры (Cais Palafítico da Carrasqueira)",
    lede="Короткая версия B для двух дней: поезд в Грандолу, заповедник Садо и Карраскейра, ночь в Компорте, утром 20 км до Трои, паром и Fertagus домой. Самый спокойный и самый ровный вариант в Алентежу, но километров на три дня здесь нет.",
    surface=[("Как B", "грунт 86 % на петле Садо", "#b")],
    segments=[
        dict(title="Два дня у воды", km="110–135 км", text=[
            "Первый день как у B: замок Алкасера, дамбы заповедника, свайный причал. Второй день 20 км сосняком до Трои с римскими руинами у причала, паром каждый час до 20:00. Если нужны три дня, второй можно отдать Аррабиде на том берегу, но это уже горы.",
        ], photos_k=["Pousada Castle of Alcácer do Sal", "Carrasqueira Palafitic Pier"]),
    ],
    stages=[
        ("День 1", "ст. Grândola → Alcácer do Sal → RN Sado → Carrasqueira → Comporta", "~75 км", "~250 м", "27 км асфальта, затем грунт 86 %, ступени"),
        ("День 2", "Comporta → Tróia → паром → Setúbal (+ Arrábida по желанию)", "20–60 км", "~50–240 м", "асфальт"),
    ],
    sandnotes=["Как у B: ступени на петле Садо, песка в отзывах нет.", "Паром из Tróia каждый час до 20:00, велосипед только на ferry."],
    prac=["Туда: IC 570 Oriente 10:02 → Grândola 11:21.", "Обратно: паром Tróia → Setúbal в :00 каждый час до 20:00, затем 21:15, 22:40; Fertagus 58 мин."],
    tracks=[
        ("Komoot: петля по заповеднику Садо от Alcácer", "https://www.komoot.com/tour/32127350", "62,5 км / 244 м"),
        ("Komoot: Alcácer → Carrasqueira → Comporta → Tróia (план)", "https://www.komoot.com/plan/@38.373208,-8.512401,9.407z?sport=mtb_easy&p[0][loc]=38.3729735,-8.5122705&p[1][loc]=38.3751000,-8.7845200&p[2][loc]=38.3803765,-8.7859968&p[3][loc]=38.4859195,-8.8836429", "50 км / 187 м"),
    ],
    photos=[("g/troia", "Римские руины Трои"), ("b/alcacer", "Алкасер-ду-Сал")],
))

# POI «Куда заехать» заполняются из poi.json (собирают агенты), ключ = id маршрута.

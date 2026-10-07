# -*- coding: utf-8 -*-
# Google 地圖連結：景點頁的搜尋字串、車程日的路線。
from urllib.parse import quote_plus, urlencode

def gsearch(q):
    return "https://www.google.com/maps/search/?api=1&query=" + quote_plus(q)

def gdir(origin, destination, waypoints=()):
    params = {"api": "1", "origin": origin, "destination": destination, "travelmode": "driving"}
    if waypoints:
        params["waypoints"] = "|".join(waypoints)
    return "https://www.google.com/maps/dir/?" + urlencode(params)

# 景點頁「Google 地圖」按鈕；已在 links 自帶地圖的頁面不列（p-khm、p-imperial、p-concert）。
# 遊船與電車沒有固定地點，不列（p-vltava、p-tram）。
PLACE_MAP = {
  "p-vienna": "Stephansplatz, Wien",
  "p-wachau": "Wachau, Niederösterreich",
  "p-melk": "Stift Melk",
  "p-hundertwasser": "Hundertwasserhaus, Kegelgasse 36-38, Wien",
  "p-schonbrunn": "Schloss Schönbrunn, Wien",
  "p-hofburg": "Hofburg, Wien",
  "p-stephansdom": "Stephansdom, Wien",
  "p-hallstatt": "Marktplatz, Hallstatt",
  "p-stwolfgang": "Pfarrkirche St. Wolfgang im Salzkammergut",
  "p-salzwelten": "Salzwelten Hallstatt",
  "p-salzburg": "Altstadt Salzburg",
  "p-festung": "Festung Hohensalzburg",
  "p-sbg-altstadt": "Getreidegasse, Salzburg",
  "p-mirabell": "Mirabellgarten, Salzburg",
  "p-mozart": "Mozarts Geburtshaus, Getreidegasse 9, Salzburg",
  "p-krumlov": "Náměstí Svornosti, Český Krumlov",
  "p-budejovice": "Náměstí Přemysla Otakara II., České Budějovice",
  "p-marienbad": "Kolonáda, Mariánské Lázně",
  "p-karlovy": "Mlýnská kolonáda, Karlovy Vary",
  "p-prague": "Staroměstské náměstí, Praha",
  "p-charles": "Karlův most, Praha",
  "p-oldtownsq": "Staroměstské náměstí, Praha",
  "p-tyn": "Týnský chrám, Praha",
  "p-orloj": "Pražský orloj, Praha",
  "p-castle": "Pražský hrad",
  "p-vitus": "Katedrála svatého Víta, Praha",
  "p-golden": "Zlatá ulička, Praha",
  "p-vysehrad": "Vyšehrad, Praha",
  "p-klementinum": "Klementinum, Praha",
  "p-narodni": "Národní divadlo, Praha",
  "p-dancing": "Tančící dům, Praha",
  "p-parizska": "Pařížská, Praha",
  "p-slavia": "Café Slavia, Smetanovo nábřeží 2, Praha",
}

# 車程日路線（Day 5 鹽礦確切地點未定，不列）
DAY_ROUTES = {
  2: gdir("Flughafen Wien-Schwechat", "InterContinental Wien, Johannesgasse 28",
          ["Stift Melk", "Hundertwasserhaus, Kegelgasse 36-38, Wien"]),
  4: gdir("InterContinental Wien, Johannesgasse 28", "Romantik Hotel Im Weissen Rössl, St. Wolfgang im Salzkammergut",
          ["Hallstatt"]),
  6: gdir("Romantik Hotel Im Weissen Rössl, St. Wolfgang im Salzkammergut", "Hotel Zlatý Anděl, Český Krumlov",
          ["Altstadt Salzburg"]),
  7: gdir("Hotel Zlatý Anděl, Český Krumlov", "Rubezahl Marienbad Luxury Historical Castle Hotel & Golf, Mariánské Lázně",
          ["Náměstí Přemysla Otakara II., České Budějovice"]),
  8: gdir("Rubezahl Marienbad Luxury Historical Castle Hotel & Golf, Mariánské Lázně", "Hotel KINGS COURT, U Obecního domu 3, Praha",
          ["Mlýnská kolonáda, Karlovy Vary"]),
}

MEET_MAP = gsearch("Taoyuan International Airport Terminal 1")
PRG_T1_MAP = gsearch("Letiště Václava Havla Praha Terminál 1")

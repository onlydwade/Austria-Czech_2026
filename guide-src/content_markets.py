# -*- coding: utf-8 -*-
# 超市頁：總覽 m-markets，以及每間飯店附近的超市 m-xxx（飯店旁的「附近超市」按鈕連到這裡）。
# 座標來自 OpenStreetMap（經 Mapcarta 查詢），飯店座標另查訂房網站；
# 營業時間查自各店官網或商家目錄（ADEG 官網、Palladium 官網、firmy.cz、billa-prodejny.cz 等），以現場為準。

WD = "一二三四五六日"

def wk(weekday, sat, sun):
    """週一到週五同一個時段；None 表示公休。"""
    return [weekday] * 5 + [sat, sun]

# 每間飯店附近的超市。key 對應 build_guide.HOTEL_Q；ll 是 (緯度, 經度)，沒有可靠座標的寫 None，不畫在地圖上。
# dates：住在這裡、可能去買東西的日子（日期, 星期索引 0=一）。
MARKETS = {}

def M(mid, **kw):
    kw["id"] = mid
    MARKETS[mid] = kw

M("m-vienna", key="InterContinental Vienna", city="維也納", country="at", day=2,
  hotel_ll=(48.20179, 16.37900),
  dates=[("10/12", 0), ("10/13", 1)],
  when="平日。超市多半 20:00 前打烊，Wien Mitte 的 INTERSPAR-pronto 開到 23:00。",
  lede="飯店在市立公園旁，走路 5 分鐘內就有一家 SPAR。奧地利的超市大多 20:00 前打烊，晚上回飯店後還想買東西，就去 Wien Mitte 車站的 INTERSPAR-pronto，每天開到 23:00。",
  stores=[
    dict(name="SPAR Gourmet", kind="超市", q="SPAR Gourmet, Salesianergasse 1B, 1030 Wien", addr="Salesianergasse 1B, 1030 Wien", ll=(48.20075, 16.38105),
         hours=wk("07:30–20:00", "08:30–18:00", None),
         note="SPAR 的市區型門市，買水、水果、優格、零食很方便。"),
    dict(name="BILLA Corso", kind="超市", q="BILLA Corso, Kärntner Ring 9-13, 1010 Wien", addr="Kärntner Ring 9–13, 1010 Wien（Ringstraßen-Galerien 購物廊）", ll=(48.2023, 16.37205),
         hours=wk("07:40–20:00", "07:40–18:00", None),
         note="在環城大道旁的 Ringstraßen-Galerien 購物廊裡，往國家歌劇院、音樂協會的方向。"),
    dict(name="INTERSPAR（Wien Mitte）", kind="大型超市＋小超市", q="INTERSPAR Wien Mitte The Mall, Landstraßer Hauptstraße 1b, 1030 Wien", addr="Landstraßer Hauptstraße 1b, 1030 Wien（Wien Mitte The Mall）",
         ll=(48.2064, 16.38534),
         hours=["08:00–20:00・pronto 到 23:00"] * 3 + ["08:00–21:00・pronto 到 23:00"] * 2
               + ["08:00–18:00・pronto 到 23:00", "只有 pronto 06:00–23:00"],
         note="Wien Mitte 車站的購物中心，有兩層樓的大型 INTERSPAR。旁邊的 INTERSPAR-pronto 是小型店，每天 06:00–23:00、週日也開，是晚上最可靠的選擇。穿過市立公園就到。"),
  ],
  tips=[
    ("寶特瓶有押金", "2025 年起奧地利的寶特瓶和鋁罐有押金，每個 €0.25。喝完可以拿回超市的回收機退。"),
    ("想買伴手禮", "Manner 威化餅、紅金色包裝的 Mirabell 莫札特巧克力，BILLA、SPAR 都有，比專賣店便宜。"),
  ])

M("m-stwolfgang", key="Romantik Hotel Im Weissen Rössl", city="聖沃夫岡", country="at", day=4,
  hotel_ll=(47.737381, 13.448119),
  dates=[("10/14", 2), ("10/15", 3)],
  when="平日。村裡的小超市 18:00 就打烊。",
  lede="聖沃夫岡是湖邊小鎮，村子裡只有一家 ADEG 小超市，離飯店走路約 3 分鐘，但 18:00 就打烊。Day 4 傍晚到、Day 5 從鹽礦回來，要趁早去買。",
  stores=[
    dict(name="ADEG Kienberger", kind="小超市", q="ADEG Kienberger, Markt 4, 5360 St. Wolfgang im Salzkammergut", addr="Markt 4, 5360 St. Wolfgang", ll=(47.7388, 13.44717),
         hours=wk("07:00–18:00", "07:00–17:00", None),
         note="ADEG 是奧地利鄉鎮常見的超市，由當地商家經營。規模不大，水、飲料、麵包、零食都有。"),
  ],
  tips=[
    ("大一點的超市", "SPAR、BILLA 在湖東端的 Strobl 和湖西端的 St. Gilgen，沒有車不方便。需要的東西最好在維也納先買好。"),
  ])

# 飯店座標用主廣場（廣場 2 號資訊中心的座標）代替，飯店在同一個廣場的 11 號。
M("m-krumlov", key="Hotel Zlatý Anděl", city="庫倫洛夫", country="cz", day=6,
  hotel_ll=(48.810808, 14.315400),
  dates=[("10/16", 4), ("10/17", 5)],
  when="週五晚上到、週六早上走。主廣場上的食品店開到 22:00。",
  lede="飯店就在老城主廣場上，同一個廣場就有一家食品店，開到 22:00，晚上回飯店後通常還來得及買水。大一點的超市在老城外面。",
  stores=[
    dict(name="Market náměstí Svornosti", kind="食品店", q="Market, náměstí Svornosti 7, Český Krumlov", near=True, addr="náměstí Svornosti 7（主廣場 7 號）", ll=None,
         where="同一個廣場，走路 1 分鐘",
         hours=wk("09:00–22:00", "09:00–22:00", "09:00–22:00"),
         note="就在飯店所在的主廣場上，買水、飲料、零食最近。地圖上沒有另外標出。"),
    dict(name="Happy potraviny", kind="食品雜貨店", q="Happy potraviny, Na Ostrově 87, Český Krumlov", addr="Na Ostrově 87", ll=(48.8119, 14.31413),
         hours=wk("10:00–23:00", "10:00–24:00", "10:00–22:00"),
         note="小型食品雜貨店（potraviny），開得很晚，在主廣場西北邊，靠近市立軍械庫（Městská zbrojnice）。"),
    dict(name="PENNY", kind="折扣超市", q="PENNY, 5. května 418, Český Krumlov", addr="5. května 418（Plešivec）", ll=(48.80332, 14.31367),
         hours=wk("07:00–20:00", "07:00–20:00", "07:00–20:00"),
         note="老城南邊 Plešivec 區的連鎖超市，東西多又便宜，但離老城比較遠。"),
  ],
  tips=[
    ("老城裡的小店", "老城觀光區的小店價格通常比超市高，想大量買飲料或零食，PENNY 比較划算。"),
  ])

M("m-marienbad", key="Luxury Historical Castle Hotel & Golf", city="瑪麗安斯凱", country="cz", day=7,
  hotel_ll=None,
  dates=[("10/17", 5), ("10/18", 6)],
  when="週六晚上到、週日早上走。晚餐在飯店，通常用不到超市。",
  lede="這晚住在市區外圍高爾夫球場旁的城堡飯店，晚餐在飯店吃，隔天早上就出發，通常用不到超市。查到的連鎖超市都在市區的住宅區，離飯店不近，走路不方便；需要的東西最好前一晚在庫倫洛夫先買。",
  stores=[
    dict(name="BILLA", kind="超市", q="BILLA, Plzeňská, Mariánské Lázně", addr="Plzeňská, 353 01 Mariánské Lázně（Úšovice 區）", ll=None,
         where="市區南邊",
         hours=wk("07:00–20:00", "07:00–20:00", "08:00–20:00"),
         note=""),
    dict(name="PENNY", kind="折扣超市", q="PENNY, Chebská 676, Mariánské Lázně", addr="Chebská 676, 353 01 Mariánské Lázně", ll=None,
         where="市區西邊、往 Cheb 的路上",
         hours=wk("07:00–20:00", "07:00–20:00", "07:00–20:00"),
         note=""),
    dict(name="Lidl", kind="折扣超市", q="Lidl, Chebská 836, Mariánské Lázně", addr="Chebská 836/23a, 353 01 Mariánské Lázně", ll=None,
         where="市區西邊、往 Cheb 的路上",
         hours=wk("以官網為準", "以官網為準", "以官網為準"),
         note="週日也營業，但各資料寫的時間不一樣，以 Lidl 官網為準。"),
  ],
  tips=[
    ("真的需要", "請飯店櫃台叫計程車，或直接用 Google 地圖找最近的店。"),
  ])

M("m-prague", key="Hotel KINGS COURT Prague", city="布拉格", country="cz", day=8,
  hotel_ll=(50.08832, 14.42810),
  dates=[("10/18", 6), ("10/19", 0), ("10/20", 1)],
  when="週日到週二。捷克週日照開，飯店對面的 Albert 每天 07:00–22:00。",
  lede="飯店在共和廣場旁，對面 Palladium 購物中心地下就有 Albert 超市，每天 07:00–22:00。再晚一點，走路 2 分鐘的 BILLA 開到 23:00。捷克的超市週日照常營業，10/18 抵達當天也買得到。",
  stores=[
    dict(name="Albert（Palladium）", kind="超市", q="Albert, Palladium, náměstí Republiky 1, Praha", addr="náměstí Republiky 1，Palladium 購物中心地下 2 樓", ll=(50.08972, 14.42794),
         hours=wk("07:00–22:00", "07:00–22:00", "07:00–22:00"),
         note="就在飯店對面，有 9,500 多種商品。巧克力、溫泉薄餅、啤酒、零食一次買齊。"),
    dict(name="BILLA（V Celnici）", kind="超市", q="BILLA, V Celnici 1031/4, Praha", addr="V Celnici 1031/4（共產主義博物館旁）", ll=(50.08785, 14.43001),
         hours=wk("07:00–23:00", "07:00–23:00", "08:00–23:00"),
         note="入口在共產主義博物館旁邊，開到 23:00，是附近最晚打烊的大超市。"),
    dict(name="Žabka", kind="便利商店", q="Žabka, Na Poříčí 35, Praha", addr="Na Poříčí 35", ll=(50.09032, 14.43564),
         hours=wk("06:00–22:00", "06:00–22:00", "06:00–22:00"),
         note="波蘭來的連鎖便利商店，布拉格到處都有，賣飲料、零食、即食品和酒。這家在 Na Poříčí 街上，往 Florenc 方向。"),
  ],
  tips=[
    ("Kotva 百貨整修中", "共和廣場的 Kotva 百貨關閉整修，預計 2027 年重新開幕，裡面的 Albert 也沒開。舊的旅遊資料還會寫到它，不用特地過去。"),
    ("超市伴手禮", "溫泉薄餅、Studentská 巧克力、Becherovka 藥草酒、啤酒，捷克的超市一般都買得到。"),
  ])

# 總覽頁
OVERVIEW = dict(
  lede="奧地利的超市週日公休，捷克的超市週日照開。這趟在奧地利的 4 晚都是平日，在捷克又剛好碰到週日，兩國的國定假日也都在回國之後，所以不用擔心買不到東西。",
  austria=[
    ("BILLA", "奧地利最常見的超市，屬於 REWE 集團。BILLA PLUS 是大型店。"),
    ("SPAR", "另一個大品牌。SPAR 是一般店，EUROSPAR 中型，INTERSPAR 是大賣場，SPAR Gourmet 是市區型門市。"),
    ("HOFER、Lidl、PENNY", "折扣超市，東西便宜但品項少。HOFER 就是德國的 ALDI。"),
    ("ADEG", "鄉鎮常見的小超市，由當地商家經營，屬於 REWE 集團。"),
    ("營業時間", "法律規定平日最晚 21:00、週六最晚 18:00，週日和國定假日公休。大部分超市平日開到 19:30–20:00。車站和機場的店例外，週日也開。"),
    ("寶特瓶押金", "2025 年起寶特瓶和鋁罐有押金，每個 €0.25，玻璃瓶不在內。喝完拿回超市的回收機退。"),
  ],
  czech=[
    ("Albert、BILLA", "最常見的兩家連鎖超市。Albert 屬於 Ahold Delhaize 集團。"),
    ("Lidl、Kaufland、PENNY", "折扣超市和大賣場，常開在市區外圍。"),
    ("Žabka", "波蘭來的連鎖便利商店，店面約 50–100 m²，布拉格很多。"),
    ("Potraviny、Večerka", "街角的食品雜貨店，很多開到很晚，價格比超市高一點。"),
    ("營業時間", "週日照常營業，市中心的大超市多半 07:00–22:00 或更晚。"),
    ("國定假日", "200 m² 以上的店在 1/1、復活節星期一、5/8、9/28、10/28、12/25–26 不能營業，12/24 中午後也要關。這趟都碰不到。"),
  ],
  general=[
    ("購物袋", "結帳時要另外買，自備環保袋最方便。"),
    ("付款", "兩國都可以刷卡、感應付款，大型超市多有自助結帳機。"),
    ("這趟的假日", "奧地利國慶日 10/26、捷克建國紀念日 10/28，都在我們回國之後。"),
  ],
)

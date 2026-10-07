# -*- coding: utf-8 -*-
import html, re, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from content_places import PLACES
from content_hotels import HOTELS
from content_shops import SHOPS
from content_maps import PLACE_MAP, DAY_ROUTES, MEET_MAP, PRG_T1_MAP
HOTELS.update(SHOPS)  # shop pages share the hotel page layout
from content_gifts import GIFTS_MINE, GIFTS_AT, GIFTS_CZ, SHOP_PLAN, GIFT_TIPS

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "austria-czech-guide.html")   # Claude Artifact version (wrapped by the artifact host)
OUT_INDEX = os.path.join(ROOT, "index.html")            # standalone page served by GitHub Pages

# ───────────────────────── 每日行程 ─────────────────────────
# stops: (place_id, note)   status: upd / tbc / None
DAYS = [
 dict(n=1, date="10/11", wd="日", city="台北 → 維也納", theme="夜班機出發",
      route=["桃園 TPE", "✈", "維也納 VIE"],
      flight="CI63　TPE 23:45 → VIE 07:05（+1）・飛行約 13 小時 20 分", status="upd",
      timeline=[("21:00", "桃園機場第一航廈・中華航空團體櫃檯集合・[[" + MEET_MAP + "|地圖 ↗]]", False),
                ("23:45", "CI63 起飛", False)],
      intro=["搭華航直飛班機。抵達維也納是當地早上 7 點多，盡量在機上多睡一點，隔天一下飛機就開始行程。"],
      stops=[], meals=[("早", "X"), ("午", "X"), ("晚", "機上精選美食")],
      hotel=("機上過夜", "")),
 dict(n=2, date="10/12", wd="一", city="維也納 → 梅爾克 → 維也納", theme="梅爾克修道院・百水公寓", status="upd",
      route=["維也納", "梅爾克", "維也納"],
      intro=["早上 7 點多抵達維也納，先往西到多瑙河畔的梅爾克參觀修道院，下午回到維也納看百水公寓。"],
      stops=[("p-vienna", ""), ("p-melk", "門票已含"), ("p-hundertwasser", ""), ("p-wachau", "延伸閱讀")],
      meals=[("早", "機上精選美食"), ("午", "奧地利傳統豬肋排餐＋酒水"), ("晚", "奧地利饕客必推 牛肉料理＋酒水")],
      hotel=("InterContinental Vienna", "維也納兩晚連泊。飯店在市立公園旁，走路可到金色史特勞斯雕像。")),
 dict(n=3, date="10/13", wd="二", city="維也納", theme="熊布朗宮・霍夫堡皇宮・聖史蒂芬大教堂・維也納音樂會", status="upd",
      route=["維也納市區"],
      timeline=[("上午", "市區觀光：[[p-schonbrunn|熊布朗宮]]（入內）・[[p-hofburg|霍夫堡皇宮]]・[[p-stephansdom|聖史蒂芬大教堂]]", False),
                ("中午", "午餐：「米其林」推薦料理", False),
                ("14:30–18:00", "自由活動 → 你選了[[p-khm|藝術史博物館]]・[[https://maps.app.goo.gl/xHBEk7LS93W4T3LD6|Google 地圖 ↗]]", True),
                ("晚上", "晚餐後前往音樂協會[[p-concert|布拉姆斯廳]]聽音樂會・[[https://www.google.com/maps/search/?api=1&query=Musikverein+Wien%2C+Musikvereinsplatz+1%2C+1010+Wien|地圖 ↗]]", False)],
      stops=[("p-schonbrunn", "門票已含"), ("p-hofburg", ""), ("p-stephansdom", ""),
             ("p-khm", "自由活動・已選"), ("p-concert", "布拉姆斯廳")],
      alts=dict(title="其他自由活動選項（領隊提供）", items=[
          ("奧地利國家圖書館", "09:00–18:00", "世界最美的圖書館之一，介紹見[[p-hofburg|霍夫堡皇宮]]頁的國家圖書館大廳。", "https://maps.app.goo.gl/HdHGkvP5VUJaKQn88", "https://lillian.tw/osterreichische-nationalbibliothek/"),
          ("阿爾貝蒂納博物館 Albertina", "10:00–18:00", "阿爾貝特公爵的收藏，近代畫家為主，從莫內到畢卡索；最有名的館藏是杜勒的〈野兔〉，原作因怕光很少展出。", "https://maps.app.goo.gl/jrsm9VvQtnGhLosN6?g_st=al", None)]),
      meals=[("早", "飯店內早餐"), ("午", "感動味蕾體驗「米其林」推薦餐料理＋酒水"), ("晚", "風味料理＋酒水")],
      hotel=("InterContinental Vienna", "市立公園旁。走到音樂協會約 10 分鐘，到聖史蒂芬大教堂約 15 分鐘。")),
 dict(n=4, date="10/14", wd="三", city="維也納 → 湖區", theme="哈斯達特・聖沃夫岡", status="upd",
      route=["維也納", 288, "哈斯達特湖區", 37, "聖沃夫岡湖區"],
      intro=["今天直接從維也納往西開到湖區，288 公里車程約 3.5 小時，可以在車上補眠。"],
      stops=[("p-hallstatt", ""), ("p-stwolfgang", "")],
      meals=[("早", "飯店內早餐"), ("午", "當地特色料理＋酒水"), ("晚", "湖區新鮮鱒魚料理＋酒水")],
      hotel=("Romantik Hotel Im Weissen Rössl", "聖沃夫岡湖畔的白馬飯店，兩晚連泊。輕歌劇《白馬酒店》的舞台，有漂在湖上的溫水泳池。")),
 dict(n=5, date="10/15", wd="四", city="湖區", theme="世界最著名・鹽礦", status="upd",
      route=["聖沃夫岡湖區", 90, "鹽礦", "聖沃夫岡湖區"],
      stops=[("p-salzwelten", "門票已含")],
      extra=["回到聖沃夫岡後如果還有時間，可以去朝聖教堂看[[p-stwolfgang|帕赫祭壇]]，或在湖邊散步。"],
      meals=[("早", "飯店內早餐"), ("午", "當地風味料理＋酒水"), ("晚", "湖區風味料理＋酒水")],
      hotel=("Romantik Hotel Im Weissen Rössl", "連泊第二晚，不用整理大行李。")),
 dict(n=6, date="10/16", wd="五", city="薩爾茲堡 → 庫倫洛夫", theme="莫札特的故鄉・童話小鎮",
      route=["聖沃夫岡湖區", 75, "薩爾茲堡", 218, "庫倫洛夫"],
      intro=["上午在薩爾茲堡，特別安排搭★城堡纜車上山。下午越過邊境進入捷克，傍晚抵達庫倫洛夫。"],
      stops=[("p-salzburg", ""), ("p-festung", "★搭城堡纜車"), ("p-sbg-altstadt", ""), ("p-mirabell", ""), ("p-mozart", ""), ("p-krumlov", "")],
      meals=[("早", "飯店內早餐"), ("午", "奧地利風味料理＋酒水（如想逛街則改發餐費自理）"), ("晚", "穿越時光著中古世紀服飾 享受庫倫洛夫晚宴＋酒水")],
      hotel=("Hotel Zlatý Anděl", "金色天使飯店，就在庫倫洛夫的主廣場上，出門就是老城。")),
 dict(n=7, date="10/17", wd="六", city="南波希米亞 → 溫泉區", theme="百威啤酒的故鄉・瑪麗安斯凱", status="upd",
      route=["庫倫洛夫", 25, "巴德傑維契", 270, "瑪麗安斯凱"],
      stops=[("p-budejovice", ""), ("p-marienbad", "")],
      meals=[("早", "飯店內早餐"), ("午", "百威城主廚料理＋酒水"), ("晚", "飯店內主廚晚餐＋酒水")],
      hotel=("Luxury Historical Castle Hotel & Golf", "全名 Rübezahl Marienbad Luxury Historical Castle Hotel & Golf，20 世紀初的城堡建築，2015 年整修後重新開幕，附近就是 1905 年開幕的高爾夫球場。")),
 dict(n=8, date="10/18", wd="日", city="溫泉區 → 布拉格", theme="卡羅維瓦利・查理大橋・舊城廣場", status="upd",
      route=["瑪麗安斯凱", 55, "卡羅維瓦利", 128, "布拉格"],
      stops=[("p-karlovy", ""), ("p-prague", ""), ("p-charles", ""), ("p-oldtownsq", ""), ("p-tyn", ""), ("p-orloj", "")],
      extra=["在卡羅維瓦利記得試現烤的[[p-karlovy|溫泉薄餅]]，柱廊一帶到處都有店家・[[https://www.google.com/maps/search/?api=1&query=L%C3%A1ze%C5%88sk%C3%A9+oplatky%2C+Karlovy+Vary|薄餅店家地圖 ↗]]"],
      meals=[("早", "飯店內早餐"), ("午", "風味料理餐廳＋酒水"), ("晚", "捷克醬鴨料理＋酒水")],
      hotel=("Hotel KINGS COURT Prague", "布拉格三晚連泊。共和廣場旁，隔壁是市民會館和火藥塔，走到舊城廣場約 10 分鐘。")),
 dict(n=9, date="10/19", wd="一", city="布拉格", theme="城堡區・黃金巷・舊城廣場", status="upd",
      route=["布拉格"],
      intro=["布拉格景點集中，很適合連泊慢慢逛。城市主要分為城堡區、小城區、猶太區與新、舊城區，今天專心看城堡區。"],
      stops=[("p-castle", ""), ("p-vitus", "門票已含"), ("p-golden", "門票已含"), ("p-oldtownsq", "")],
      meals=[("早", "飯店內早餐"), ("午", "布拉格「米其林」推薦餐＋酒水"), ("晚", "旅遊書推薦必吃 捷克料理＋酒水")],
      hotel=("Hotel KINGS COURT Prague", "連泊第二晚。")),
 dict(n=10, date="10/20", wd="二", city="布拉格", theme="伏爾塔瓦河遊船・高堡・自由活動",
      route=["布拉格"],
      timeline=[("上午", "[[p-vltava|伏爾塔瓦河遊船]]・[[p-vysehrad|高堡]]・搭[[p-tram|有軌電車]]沿河看景・漫步到[[p-dancing|跳舞的房子]]", False),
                ("中午", "午餐：中式懷鄉料理（八菜一湯）", False),
                ("14:30 起", "自由活動。公司提供 24 小時電車地鐵票。想去[[p-parizska|巴黎街精品街]]逛 Celine・[[https://www.google.com/maps/search/?api=1&query=CELINE+Prague%2C+Pa%C5%99%C3%AD%C5%BEsk%C3%A1+15%2C+Praha+1|Google 地圖 ↗]]", True),
                ("18:00", "[[p-imperial|帝國咖啡館]]晚餐（6 位，已訂位）・[[h-imperial|設施介紹]]・[[https://www.google.com/maps/search/?api=1&query=Caf%C3%A9+Imperial%2C+Na+Po%C5%99%C3%AD%C4%8D%C3%AD+15%2C+Praha+1|Google 地圖 ↗]]", True)],
      stops=[("p-vltava", "船票已含"), ("p-vysehrad", ""), ("p-tram", "特別安排"), ("p-klementinum", "電車沿途"), ("p-narodni", "電車沿途"), ("p-dancing", ""),
             ("p-parizska", "想去 Celine"), ("p-imperial", "18:00 已訂位")],
      meals=[("早", "飯店內早餐"), ("午", "中式懷鄉料理（八菜一湯）"), ("晚", "自理：[[p-imperial|帝國咖啡館]] 18:00（6 位已訂位）", "Café Imperial")],
      hotel=("Hotel KINGS COURT Prague", "連泊第三晚。帝國咖啡館離飯店步行約 5 分鐘。")),
 dict(n=11, date="10/21", wd="三", city="布拉格 → 台北", theme="早班機返台", status="upd",
      route=["布拉格 PRG", "✈", "桃園 TPE"],
      flight="CI68　PRG 10:40 → TPE 05:05（+1）・飛行約 12 小時 25 分",
      intro=["早班機，早餐後就出發去機場。這趟的歐盟購物退稅，都要在最後離開歐盟的布拉格機場辦理海關蓋章，請預留時間。CI68 從第 1 航廈出發・[[" + PRG_T1_MAP + "|機場地圖 ↗]]"],
      stops=[], meals=[("早", "飯店內早餐（或早餐餐盒）"), ("午", "機上精選美食"), ("晚", "機上精選美食")],
      hotel=("機上", "")),
 dict(n=12, date="10/22", wd="四", city="抵達台北", theme="05:05 抵達桃園",
      route=["桃園 TPE"],
      intro=["清晨抵達桃園國際機場，旅程結束。"],
      stops=[], meals=[("早", "機上精選美食"), ("午", "X"), ("晚", "X")],
      hotel=("溫暖的家", "")),
]

# hotel display name → Google Maps search query
HOTEL_Q = {
  "InterContinental Vienna": "InterContinental Wien, Johannesgasse 28, 1037 Wien",
  "Romantik Hotel Im Weissen Rössl": "Romantik Hotel Im Weissen Rössl, St. Wolfgang im Salzkammergut",
  "Hotel Zlatý Anděl": "Hotel Zlatý Anděl, Náměstí Svornosti, Český Krumlov",
  "Luxury Historical Castle Hotel & Golf": "Rubezahl Marienbad Luxury Historical Castle Hotel & Golf, Mariánské Lázně",
  "Hotel KINGS COURT Prague": "Hotel KINGS COURT, U Obecního domu 3, Praha 1",
  "Café Imperial": "Café Imperial, Na Poříčí 15, Praha 1",
}
# hotel key → Chinese name (from the booklet where it gives one)
HOTEL_ZH = {
  "InterContinental Vienna": "維也納洲際飯店",
  "Romantik Hotel Im Weissen Rössl": "傳奇白馬飯店",
  "Hotel Zlatý Anděl": "金色天使飯店",
  "Luxury Historical Castle Hotel & Golf": "魯伯薩爾城堡飯店",
  "Hotel KINGS COURT Prague": "布拉格國王宮廷飯店",
}
STAYS = [
  ("10/12–10/13", "2 晚", "維也納", "InterContinental Vienna", "InterContinental Vienna", 2),
  ("10/14–10/15", "2 晚", "聖沃夫岡", "Romantik Hotel Im Weissen Rössl", "Romantik Hotel Im Weissen Rössl", 4),
  ("10/16", "1 晚", "庫倫洛夫", "Hotel Zlatý Anděl", "Hotel Zlatý Anděl", 6),
  ("10/17", "1 晚", "瑪麗安斯凱", "Rübezahl Castle Hotel & Golf", "Luxury Historical Castle Hotel & Golf", 7),
  ("10/18–10/20", "3 晚", "布拉格", "Hotel KINGS COURT", "Hotel KINGS COURT Prague", 8),
]

REGIONS = [
  ("vienna", "維也納與多瑙河"),
  ("lakes", "薩爾茲卡默古特湖區"),
  ("salzburg", "薩爾茲堡"),
  ("southbohemia", "南波希米亞"),
  ("spa", "西波希米亞溫泉區"),
  ("prague", "布拉格"),
]

CHANGES = [
  ("Day 1", "集合時間 21:00（桃園第一航廈華航團體櫃檯）。去程 CI63 改為 23:45 起飛、隔天 07:05 抵達（原為 23:20／07:00）。"),
  ("Day 2", "改為維也納 → 梅爾克修道院 → 維也納（百水公寓）。原 PDF 的霍夫堡、聖史蒂芬移到 Day 3。晚餐從水煮牛改為牛肉料理。"),
  ("Day 3", "改為熊布朗宮＋霍夫堡＋聖史蒂芬＋音樂會（布拉姆斯廳）。晚餐從炸肉排改為風味料理。新增 14:30–18:00 自由活動。"),
  ("Day 4", "梅爾克移到 Day 2，這天直接從維也納開往哈斯達特（288 km），住聖沃夫岡的白馬飯店。"),
  ("Day 5", "湖區連泊，專程去鹽礦。"),
  ("Day 6", "從聖沃夫岡出發（75 km 到薩爾茲堡、218 km 到庫倫洛夫），內容同原 PDF，確定住金色天使飯店。"),
  ("Day 7", "終點從卡羅維瓦利改為瑪麗安斯凱，晚餐改為飯店主廚晚餐，住 Rübezahl 城堡飯店。"),
  ("Day 8", "順序對調：瑪麗安斯凱 → 卡羅維瓦利 → 布拉格。景點與餐食同原 PDF。"),
  ("Day 8–10", "布拉格飯店確定為 Hotel KINGS COURT（原為 Hilton Old Town 或 Marriott）。"),
  ("Day 9", "午晚餐對調：午餐米其林推薦，晚餐捷克料理。"),
  ("Day 10", "14:30 起自由活動，公司提供 24 小時電車地鐵票，想去巴黎街逛 Celine；晚餐自理，已訂帝國咖啡館 18:00、6 位。"),
  ("Day 11", "回程 CI68 改為 10:40 起飛、隔天 05:05 抵達（原為 10:55／05:40）。"),
]

TIPS = [
  ("時差", "奧地利與捷克在 10/25 前是夏令時間，比台灣慢 6 小時。"),
  ("貨幣", "奧地利用歐元 EUR，捷克用克朗 CZK。兩國刷卡都很普遍，捷克換匯前先問清楚實拿金額。"),
  ("天氣", "10 月中旬白天約 10–16°C，早晚可能低到 5°C 以下，湖區與鹽礦更冷。洋蔥式穿法，帶防風外套和摺疊傘。"),
  ("電壓插座", "230V，雙圓孔插座（C／F 型），台灣電器需要轉接頭。"),
  ("網路", "行程贈送歐洲 SIM 卡，每天 1GB。"),
  ("飲水", "兩國自來水都可以生飲；餐廳的水要另外付費，行程每天提供一瓶瓶裝水。"),
  ("小費", "餐廳約 5–10%，結帳時直接告訴店員含小費的總額。"),
  ("退稅", "同一天在同一家店消費達門檻可以辦退稅（奧地利 €75.01、捷克 2,001 CZK），在最後離開歐盟的布拉格機場辦理海關蓋章。"),
  ("緊急電話", "歐盟通用 112。外交部旅外國人急難救助全球免付費專線：00-800-0885-0885。"),
]

# ───────────────────────── helpers ─────────────────────────
LINK_RE = re.compile(r"\[\[((?:p|h|s)-[a-z-]+)\|([^\]]+)\]\]")
EXT_RE = re.compile(r"\[\[(https?://[^|\]]+)\|([^\]]+)\]\]")

def rich(text):
    t = html.escape(text, quote=False)
    def rep(m):
        pid, label = m.group(1), m.group(2)
        if pid not in PLACES and pid not in HOTELS:
            raise SystemExit("unknown link " + pid)
        return f'<a class="xref" href="#{pid}">{label}</a>'
    t = LINK_RE.sub(rep, t)
    return EXT_RE.sub(lambda m: f'<a class="xref ext" href="{m.group(1)}" target="_blank" rel="noopener">{m.group(2)}</a>', t)

def esc(t):
    return html.escape(t, quote=True)

from urllib.parse import quote_plus
def gmap(key):
    return "https://www.google.com/maps/search/?api=1&query=" + quote_plus(HOTEL_Q[key])

HOTEL_PAGE = {h["key"]: hid for hid, h in HOTELS.items() if h.get("key")}

def gsearch_url(q):
    return "https://www.google.com/maps/search/?api=1&query=" + quote_plus(q)

def hotel_links(key, label="飯店設施 ›"):
    return (f'<span class="h-links"><a class="h-map" href="{esc(gmap(key))}" target="_blank" rel="noopener">Google 地圖 ↗</a>'
            f'<a class="h-fac" href="#{HOTEL_PAGE[key]}">{label}</a></span>')

MARK_CLASS = {"★": "star", "▲": "tri", "◆": "own", "": "dot"}
MARK_GLYPH = {"★": "★", "▲": "▲", "◆": "◆", "": "•"}
MARK_LABEL = {"★": "★ 入內參觀・已含", "▲": "▲ 主要景點", "◆": "◆ 我的安排", "": ""}

# place → days, order of first appearance
place_days = {}
order = []
for d in DAYS:
    for pid, _ in d["stops"]:
        place_days.setdefault(pid, [])
        if d["n"] not in place_days[pid]:
            place_days[pid].append(d["n"])
        if pid not in order:
            order.append(pid)
refs = []
for pid in PLACES:
    if pid not in place_days:
        if not PLACES[pid].get("ref"):
            raise SystemExit("place not used in itinerary: " + pid)
        refs.append(pid)

def day_by_n(n):
    return DAYS[n - 1]

# ───────────────────────── map ─────────────────────────
def proj(lon, lat):
    return (round(22 + (lon - 12.5) * 66, 1), round(18 + (50.35 - lat) * 100, 1))

CITIES = {
  # key: (lon, lat, label, dx, dy, anchor, day, overnight)
  "prague": (14.42, 50.08, "布拉格", 9, 4, "start", 8, True),
  "kv": (12.87, 50.23, "卡羅維瓦利", 8, 4, "start", 8, False),
  "ml": (12.70, 49.96, "瑪麗安斯凱", 8, 5, "start", 7, True),
  "cb": (14.47, 48.97, "巴德傑維契", 8, 4, "start", 7, False),
  "ck": (14.32, 48.81, "庫倫洛夫", -8, 5, "end", 6, True),
  "sbg": (13.04, 47.80, "薩爾茲堡", -6, 17, "middle", 6, False),
  "stw": (13.45, 47.74, "聖沃夫岡", 4, -11, "middle", 4, True),
  "hal": (13.65, 47.56, "哈斯達特", 8, 5, "start", 4, False),
  "melk": (15.33, 48.23, "梅爾克", 0, -11, "middle", 2, False),
  "vie": (16.37, 48.21, "維也納", 0, 20, "middle", 2, True),
}
ROUTE = ["vie", "hal", "stw", "sbg", "ck", "cb", "ml", "kv", "prague"]
BORDER = [(13.84, 48.77), (14.05, 48.60), (14.40, 48.57), (14.70, 48.60), (14.97, 48.77),
          (15.20, 48.95), (15.35, 49.00), (15.60, 48.90), (16.05, 48.80), (16.45, 48.80), (16.90, 48.65)]
DANUBE = [(12.9, 48.62), (13.47, 48.57), (14.29, 48.31), (14.9, 48.2), (15.33, 48.23), (15.6, 48.41),
          (16.05, 48.33), (16.37, 48.24), (16.9, 48.12)]
VLTAVA = [(13.95, 48.72), (14.32, 48.81), (14.47, 48.97), (14.42, 49.22), (14.17, 49.51),
          (14.43, 49.82), (14.42, 50.08), (14.47, 50.35)]

def pts(seq):
    return " ".join(f"{x},{y}" for x, y in (proj(a, b) for a, b in seq))

def build_map():
    o = ['<svg class="map-svg" viewBox="0 0 330 320" role="img" aria-label="路線示意圖：維也納、湖區、薩爾茲堡、庫倫洛夫、瑪麗安斯凱、卡羅維瓦利、布拉格">']
    o.append('<text class="m-country" x="250" y="118">ČESKO</text>')
    o.append('<text class="m-country" x="196" y="300">ÖSTERREICH</text>')
    o.append(f'<polyline class="m-border" points="{pts(BORDER)}"/>')
    o.append(f'<polyline class="m-river" points="{pts(DANUBE)}"/>')
    o.append(f'<polyline class="m-river" points="{pts(VLTAVA)}"/>')
    dx, dy = proj(14.6, 48.2)
    o.append(f'<text class="m-rivername" x="{dx}" y="{dy + 16}">Donau</text>')
    vx, vy = proj(14.17, 49.40)
    o.append(f'<text class="m-rivername" x="{vx - 6}" y="{vy}" text-anchor="end">Vltava</text>')
    # Day 2 side trip to Melk
    a = proj(*CITIES["vie"][:2]); b = proj(*CITIES["melk"][:2])
    o.append(f'<line class="m-route" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>')
    o.append(f'<polyline class="m-route" points="{pts([CITIES[k][:2] for k in ROUTE])}"/>')
    for k, (lon, lat, label, ldx, ldy, anchor, day, night) in CITIES.items():
        x, y = proj(lon, lat)
        cls = "m-node night" if night else "m-node"
        r = 5.5 if night else 3.6
        o.append(f'<a href="#d{day}" class="m-link"><circle class="{cls}" cx="{x}" cy="{y}" r="{r}"/>'
                 f'<text class="m-label{" big" if k in ("vie", "prague") else ""}" x="{x + ldx}" y="{y + ldy}" text-anchor="{anchor}">{label}</text></a>')
    # flight markers
    vx_, vy_ = proj(16.37, 48.21)
    px_, py_ = proj(14.42, 50.08)
    o.append(f'<text class="m-fly" x="{vx_ + 8}" y="{vy_ - 6}">✈ 抵</text>')
    o.append(f'<text class="m-fly" x="{px_ + 9}" y="{py_ + 18}">✈ 返台</text>')
    o.append('</svg>')
    return "".join(o)

# ───────────────────────── render ─────────────────────────
def render_route(d):
    parts = []
    r = d["route"]
    for i, item in enumerate(r):
        if isinstance(item, int):
            continue
        if item == "✈":
            parts.append('<span class="r-sep r-fly" aria-hidden="true">✈</span>')
            continue
        if i > 0 and not isinstance(r[i - 1], int) and r[i - 1] != "✈":
            parts.append('<span class="r-sep" aria-hidden="true">→</span>')
        if i > 0 and isinstance(r[i - 1], int):
            parts.append(f'<span class="r-sep r-km">{r[i - 1]} km →</span>')
        parts.append(f'<span class="r-stop">{esc(item)}</span>')
    note = f'<span class="pill tbc">{esc(d["route_note"])}</span>' if d.get("route_note") else ""
    if d["n"] in DAY_ROUTES:
        note += f'<a class="r-map" href="{esc(DAY_ROUTES[d["n"]])}" target="_blank" rel="noopener">看路線 ↗</a>'
    return f'<p class="route">{"".join(parts)}{note}</p>'

def render_stop(pid, note, day_n):
    p = PLACES[pid]
    mk = p["mark"]
    tag = f'<span class="tag{" own" if mk == "◆" else ""}">{esc(note)}</span>' if note else ""
    return (f'<li><a class="stop" href="#{pid}">'
            f'<span class="mk {MARK_CLASS[mk]}" aria-hidden="true">{MARK_GLYPH[mk]}</span>'
            f'<span class="st-tx"><span class="st-nm">{esc(p["name"])}</span>'
            f'<span class="st-og">{esc(p["orig"])}</span>'
            f'<span class="st-ln">{esc(p["short"])}</span></span>'
            f'{tag}<span class="chev" aria-hidden="true">›</span></a></li>')

def render_day(d):
    n = d["n"]
    pill = ""
    if d.get("status") == "upd":
        pill = '<span class="pill upd">已更新</span>'
    elif d.get("status") == "tbc":
        pill = '<span class="pill tbc">待確認</span>'
    o = [f'<section class="day" id="d{n}" data-label="Day {n}" data-date="{d["date"]}">']
    o.append(f'<header class="day-h"><span class="num" aria-hidden="true">{n}</span><div class="day-t">'
             f'<p class="when"><span class="sr">Day {n}・</span>{d["date"]}<span class="wd">週{d["wd"]}</span>{pill}'
             f'<span class="today-pill" hidden>今天</span></p>'
             f'<h2>{esc(d["city"])}</h2><p class="theme">{esc(d["theme"])}</p></div></header>')
    o.append(render_route(d))
    if d.get("flight"):
        o.append(f'<p class="flight"><span class="fl-k">航班</span>{esc(d["flight"])}</p>')
    if d.get("notice"):
        o.append(f'<p class="notice">{rich(d["notice"])}</p>')
    for para in d.get("intro", []):
        o.append(f'<p class="intro">{rich(para)}</p>')
    if d.get("timeline"):
        o.append('<ol class="timeline">')
        for t, txt, mine in d["timeline"]:
            own = '<span class="tag own">我的安排</span>' if mine else ""
            o.append(f'<li class="{"mine" if mine else ""}"><span class="tl-t">{esc(t)}</span><span class="tl-x">{rich(txt)}'
                     f'{own}</span></li>')
        o.append('</ol>')
    if d["stops"]:
        o.append('<ul class="stops">' + "".join(render_stop(pid, note, n) for pid, note in d["stops"]) + '</ul>')
    if d.get("alts"):
        a = d["alts"]
        o.append(f'<div class="alts"><p class="alts-h">{esc(a["title"])}</p><ul>')
        for name, hours, desc, maplink, blog in a["items"]:
            links = f'<a href="{esc(maplink)}" target="_blank" rel="noopener">地圖</a>'
            if blog:
                links += f'<a href="{esc(blog)}" target="_blank" rel="noopener">參觀資訊</a>'
            o.append(f'<li><p class="alt-n">{esc(name)}<span class="alt-h">{esc(hours)}</span></p>'
                     f'<p class="alt-d">{rich(desc)}</p><p class="alt-l">{links}</p></li>')
        o.append('</ul></div>')
    for para in d.get("extra", []):
        o.append(f'<p class="intro">{rich(para)}</p>')
    o.append('<dl class="ledger">')
    for m in d["meals"]:
        k, v = m[0], m[1]
        chips = hotel_links(m[2], "設施介紹 ›") if len(m) > 2 else ""
        o.append(f'<div><dt>{k}</dt><dd>{rich(v)}{chips}</dd></div>')
    hn, hnote = d["hotel"]
    hname = (f'<span class="h-name">{HOTEL_ZH[hn]}</span><span class="h-en">{esc(hn)}</span>{hotel_links(hn)}'
             if hn in HOTEL_Q else f'<span class="h-name">{esc(hn)}</span>')
    note_html = f'<span class="h-note">{esc(hnote)}</span>' if hnote else ""
    o.append(f'<div class="hotel"><dt>宿</dt><dd>{hname}{note_html}</dd></div>')
    o.append('</dl>')
    if d.get("meals_note"):
        o.append(f'<p class="fine">{esc(d["meals_note"])}</p>')
    o.append('</section>')
    return "".join(o)

def render_place(pid):
    p = PLACES[pid]
    days = place_days.get(pid, [])
    ref = not days
    first = days[0] if days else None
    back_href = f"#d{first}" if days else "#guide"
    back_label = f"Day {first}" if days else "景點百科"
    idx = order.index(pid) if not ref else -1
    nxt = order[idx + 1] if 0 <= idx < len(order) - 1 else None
    prv = order[idx - 1] if idx > 0 else None
    mk = p["mark"]
    badges = []
    if MARK_LABEL[mk]:
        badges.append(f'<span class="badge {MARK_CLASS[mk]}">{MARK_LABEL[mk]}</span>')
    for b in p.get("badges", []):
        badges.append(f'<span class="badge">{esc(b)}</span>')
    daylinks = "".join(f'<a class="daychip" href="#d{n}">Day {n}・{day_by_n(n)["date"]}</a>' for n in days)
    if ref:
        daylinks = '<span class="daychip ref">參考・未排入行程</span>'
    o = [f'<article class="place" id="{pid}" data-label="{esc(p["name"])}" data-back="{back_label}">']
    o.append(f'<div class="readbar"><a class="back" href="{back_href}"><span aria-hidden="true">‹</span> <span class="back-l">{back_label}</span></a>'
             f'<span class="rb-title">{esc(p["name"])}</span></div>')
    o.append('<div class="pl-in">')
    o.append(f'<header class="pl-h"><p class="eyebrow">{esc(p["city"])}</p><h1>{esc(p["name"])}</h1>'
             f'<p class="pl-og">{esc(p["orig"])}</p>'
             f'<p class="badges">{"".join(badges)}</p><p class="daychips">{daylinks}</p></header>')
    o.append(f'<p class="lede">{rich(p["lede"])}</p>')
    links = list(p.get("links", []))
    if pid in PLACE_MAP:
        links.insert(0, ("巴黎街地圖" if pid == "p-parizska" else "Google 地圖", gsearch_url(PLACE_MAP[pid])))
    if links:
        o.append('<p class="extlinks">' + "".join(
            f'<a href="{esc(u)}" target="_blank" rel="noopener">{esc(t)} ↗</a>' for t, u in links) + '</p>')
    for head, items in p["sections"]:
        o.append(f'<section class="pl-s"><h2>{esc(head)}</h2>')
        in_list = False
        for it in items:
            if isinstance(it, tuple):
                if not in_list:
                    o.append('<ul class="facts">'); in_list = True
                o.append(f'<li><b>{rich(it[0])}</b><span>{rich(it[1])}</span></li>')
            else:
                if in_list:
                    o.append('</ul>'); in_list = False
                o.append(f'<p>{rich(it)}</p>')
        if in_list:
            o.append('</ul>')
        o.append('</section>')
    if not ref:
        o.append('<nav class="pl-nav" aria-label="上一站、下一站">')
        o.append(f'<a class="pn prev" href="#{prv}"><small>上一站</small>{esc(PLACES[prv]["name"])}</a>' if prv else '<span></span>')
        o.append(f'<a class="pn next" href="#{nxt}"><small>下一站</small>{esc(PLACES[nxt]["name"])}</a>' if nxt else '<span></span>')
        o.append('</nav>')
        o.append(f'<p class="pl-foot"><a href="#d{first}">回到 Day {first} 行程</a>・<a href="#guide">景點百科目錄</a></p>')
    else:
        o.append('<p class="pl-foot"><a href="#guide">回到景點百科目錄</a></p>')
    o.append('</div></article>')
    return "".join(o)

def render_hotel(hid):
    h = HOTELS[hid]
    venue = h.get("kind") in ("venue", "shop")
    order_h = [HOTEL_PAGE[x[4]] for x in STAYS]
    idx = order_h.index(hid) if hid in order_h else -1
    prv = order_h[idx - 1] if idx > 0 else None
    nxt = order_h[idx + 1] if 0 <= idx < len(order_h) - 1 else None
    first = h.get("day")
    back_href, back_label = h.get("back", (f"#d{first}", f"Day {first}"))
    blist = h.get("badges", []) if venue else ["住宿・" + h["stay"]] + h.get("badges", [])
    badges = "".join(f'<span class="badge">{esc(b)}</span>' for b in blist)
    o = [f'<article class="place hotel" id="{hid}" data-label="{esc(h["zh"])}" data-back="{back_label}">']
    o.append(f'<div class="readbar"><a class="back" href="{back_href}"><span aria-hidden="true">‹</span> <span class="back-l">{back_label}</span></a>'
             f'<span class="rb-title">{esc(h["zh"])}</span></div>')
    o.append('<div class="pl-in">')
    eyebrow = esc(h["eyebrow"]) if h.get("eyebrow") else f'{"設施介紹" if venue else "住宿"}・{esc(h["city"])}'
    o.append(f'<header class="pl-h"><p class="eyebrow">{eyebrow}</p><h1>{esc(h["zh"])}</h1>'
             f'<p class="pl-og">{esc(h["en"])}</p><p class="badges">{badges}</p></header>')
    o.append(f'<p class="lede">{rich(h["lede"])}</p>')
    o.append('<p class="extlinks">' + "".join(
        f'<a href="{esc(u)}" target="_blank" rel="noopener">{esc(t)} ↗</a>' for t, u in h.get("links", [])) + '</p>')
    for head, items in h["sections"]:
        o.append(f'<section class="pl-s"><h2>{esc(head)}</h2>')
        in_list = False
        for it in items:
            if isinstance(it, tuple):
                if not in_list:
                    o.append('<ul class="facts">'); in_list = True
                o.append(f'<li><b>{rich(it[0])}</b><span>{rich(it[1])}</span></li>')
            else:
                if in_list:
                    o.append('</ul>'); in_list = False
                o.append(f'<p>{rich(it)}</p>')
        if in_list:
            o.append('</ul>')
        o.append('</section>')
    if not venue:
      o.append('<nav class="pl-nav" aria-label="上一間、下一間飯店">')
      o.append(f'<a class="pn prev" href="#{prv}"><small>上一間飯店</small>{esc(HOTELS[prv]["zh"])}</a>' if prv else '<span></span>')
      o.append(f'<a class="pn next" href="#{nxt}"><small>下一間飯店</small>{esc(HOTELS[nxt]["zh"])}</a>' if nxt else '<span></span>')
      o.append('</nav>')
      o.append(f'<p class="pl-foot"><a href="#d{first}">回到 Day {first} 行程</a>・<a href="#top">住宿一覽</a></p>')
    else:
      foot = h.get("foot") or [(f"#d{first}", f"回到 Day {first} 行程"), ("#p-imperial", "帝國咖啡館的故事")]
      o.append('<p class="pl-foot">' + "・".join(f'<a href="{href}">{esc(t)}</a>' for href, t in foot) + '</p>')
    o.append('</div></article>')
    return "".join(o)

def render_guide():
    o = ['<section class="guide wrap" id="guide" data-label="景點百科">',
         '<h2 class="sec-h">景點百科</h2><p class="sec-sub">依地區排列，共 ' + str(len(PLACES)) + ' 個深入介紹。點進去看歷史、典故與必看重點。</p>']
    for key, title in REGIONS:
        items = [pid for pid in order + refs if PLACES[pid]["region"] == key]
        o.append(f'<h3 class="reg-h">{title}</h3><ul class="g-list">')
        for pid in items:
            p = PLACES[pid]
            ds = "・".join(f"D{n}" for n in place_days.get(pid, [])) or "參考"
            o.append(f'<li><a href="#{pid}"><span class="mk {MARK_CLASS[p["mark"]]}" aria-hidden="true">{MARK_GLYPH[p["mark"]]}</span>'
                     f'<span class="g-nm">{esc(p["name"])}</span><span class="g-d">{ds}</span></a></li>')
        o.append('</ul>')
    o.append('</section>')
    return "".join(o)

def render_stays():
    rows = "".join(
        f'<tr><td class="s-d">{d}<span class="s-n">{n}</span></td><td class="s-c"><a href="#d{day}">{c}</a></td>'
        f'<td class="s-h"><span class="h-zh">{HOTEL_ZH[key]}</span>'
        f'<span class="h-en">{esc(h)}</span>{hotel_links(key)}</td></tr>'
        for d, n, c, h, key, day in STAYS)
    return (f'<div class="stays"><table><caption>住宿一覽・9 晚</caption>'
            f'<thead><tr><th>日期</th><th>城市</th><th>飯店（點開地圖）</th></tr></thead><tbody>{rows}</tbody></table></div>')

def render_gift(g):
    mk = "own" if g["mine"] else "dot"
    glyph = "◆" if g["mine"] else "•"
    maps = ""
    if g["maps"] or g.get("shop"):
        maps = '<span class="h-links">' + "".join(
            f'<a class="h-map" href="https://www.google.com/maps/search/?api=1&amp;query={quote_plus(q)}" target="_blank" rel="noopener">{esc(t)} 地圖 ↗</a>'
            for t, q in g["maps"])
        if g.get("shop"):
            maps += f'<a class="h-fac" href="#{g["shop"]}">門市介紹 ›</a>'
        maps += '</span>'
    tip = f'<p class="gf-t">{rich(g["tip"])}</p>' if g["tip"] else ""
    return (f'<li class="gift"><p class="gf-h"><span class="mk {mk}" aria-hidden="true">{glyph}</span>'
            f'<b>{esc(g["name"])}</b><i>{esc(g["orig"])}</i></p>'
            f'<p class="gf-w"><span class="gf-k">哪裡買</span>{rich(g["where"])}</p>'
            f'<p class="gf-d">{rich(g["desc"])}</p>{tip}{maps}</li>')

def render_gifts():
    o = ['<section class="wrap block gifts" id="gifts" data-label="伴手禮">',
         '<h2 class="sec-h">伴手禮</h2>',
         '<p class="sec-sub">你的清單加上幾樣推薦，最後附上照天數的購物路線和帶回台灣的注意事項。</p>']
    o.append('<h3 class="reg-h">你的清單</h3><ul class="gift-list">' + "".join(render_gift(g) for g in GIFTS_MINE) + '</ul>')
    o.append('<h3 class="reg-h">推薦加買・奧地利</h3><ul class="gift-list">' + "".join(render_gift(g) for g in GIFTS_AT) + '</ul>')
    o.append('<h3 class="reg-h">推薦加買・捷克</h3><ul class="gift-list">' + "".join(render_gift(g) for g in GIFTS_CZ) + '</ul>')
    rows = "".join(f'<tr><td class="p-d"><a href="#d{n}">{esc(t)}</a></td><td>{rich(x)}</td></tr>' for t, n, x in SHOP_PLAN)
    o.append(f'<h3 class="reg-h">照天數買</h3><div class="plan"><table><tbody>{rows}</tbody></table></div>')
    li = "".join(f'<li><b>{esc(k)}</b><span>{rich(v)}</span></li>' for k, v in GIFT_TIPS)
    o.append(f'<h3 class="reg-h">帶回台灣要注意</h3><ul class="facts">{li}</ul>')
    o.append('</section>')
    return "".join(o)

def render_changes():
    li = "".join(f'<li><b>{esc(k)}</b><span>{rich(v)}</span></li>' for k, v in CHANGES)
    return (f'<section class="wrap block" id="changes" data-label="行程更新"><h2 class="sec-h">和原 PDF 的差異</h2>'
            f'<p class="sec-sub">依新版手冊照片與你補充的安排整理。</p><ul class="facts">{li}</ul></section>')

def render_tips():
    li = "".join(f'<li><b>{esc(k)}</b><span>{esc(v)}</span></li>' for k, v in TIPS)
    return (f'<section class="wrap block" id="tips" data-label="旅途小抄"><h2 class="sec-h">旅途小抄</h2>'
            f'<ul class="facts">{li}</ul></section>')

def render_brief():
    return (
      '<div class="brief">'
      '<p class="brief-h">集合・航班</p>'
      '<dl class="brief-dl">'
      '<div><dt>集合</dt><dd><b>10/11（日）21:00</b>桃園國際機場第一航廈・中華航空團體櫃檯'
      f'・<a class="xref ext" href="{esc(MEET_MAP)}" target="_blank" rel="noopener">地圖 ↗</a></dd></div>'
      '<div><dt>去程</dt><dd><b>CI63　23:45 → 07:05+1</b>桃園 → 維也納・約 13 小時 20 分</dd></div>'
      '<div><dt>回程</dt><dd><b>CI68　10:40 → 05:05+1</b>10/21（三）布拉格 → 桃園・約 12 小時 25 分</dd></div>'
      '</dl></div>')

def render_rail():
    chips = "".join(
        f'<a class="chip" draggable="false" href="#d{d["n"]}" data-day="{d["n"]}"><b>{d["n"]}</b><span>{d["date"]}</span></a>' for d in DAYS)
    chips += ('<a class="chip txt" draggable="false" href="#guide">百科</a>'
              '<a class="chip txt" draggable="false" href="#gifts">伴手禮</a>'
              '<a class="chip txt" draggable="false" href="#tips">小抄</a>')
    return ('<nav class="rail" aria-label="跳到某一天"><div class="rail-row">'
            '<button type="button" class="rail-btn" id="railPrev" aria-label="往前捲動天數">‹</button>'
            f'<div class="rail-in" id="rail">{chips}</div>'
            '<button type="button" class="rail-btn" id="railNext" aria-label="往後捲動天數">›</button>'
            '</div></nav>')

CSS = open(os.path.join(os.path.dirname(__file__), "guide.css"), encoding="utf-8").read()
JS = open(os.path.join(os.path.dirname(__file__), "guide.js"), encoding="utf-8").read()

HEAD = f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>奧捷湖區 12 日</title>
<meta name="description" content="2026/10/11–10/22 奧地利捷克 12 日行程與景點深入介紹">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,wght@0,400;0,600;1,400;1,500&family=Noto+Sans+TC:wght@400;500;700&family=Noto+Serif+TC:wght@600;700&display=swap">
<style>{CSS}</style>
<script>document.documentElement.classList.add("js");</script>
'''

BODY = f'''<div id="app">
<main id="main" data-label="行程">
<header class="mast wrap" id="top" data-label="行程首頁">
  <p class="eyebrow">Austria &amp; Česko・2026</p>
  <h1>奧捷湖區典藏 12 日</h1>
  <p class="dates">10.11 <i>Sun</i> — 10.22 <i>Thu</i></p>
  <p class="sub">雙點進出・哈斯達特湖區・瓦豪河谷・布拉格三晚連泊</p>
  <p class="count" id="count">10/11（日）21:00 桃園機場集合</p>
  <a class="today-link" id="todayLink" href="#d1" hidden></a>
  <figure class="map">{build_map()}
    <figcaption><span class="lg night"></span>住宿<span class="lg pass"></span>途經　點城市可跳到當天</figcaption>
  </figure>
  {render_brief()}
  {render_stays()}
</header>
{render_rail()}
<div class="days wrap">
{"".join(render_day(d) for d in DAYS)}
</div>
{render_guide()}
{render_gifts()}
{render_changes()}
{render_tips()}
<footer class="foot wrap"><p>行程依旅行社 PDF 與新版手冊照片整理，並加入你補充的自由活動安排。景點介紹為一般公開的歷史與藝術資料；開放時間、票價與實際行程請以現場及領隊說明為準。</p></footer>
</main>
<div id="reader">
{"".join(render_place(pid) for pid in order + refs)}
{"".join(render_hotel(hid) for hid in HOTELS)}
</div>
</div>
<div class="fabs">
<a class="fab home" id="homeFab" href="#top" aria-label="回到首頁"><span aria-hidden="true">↑</span><small>首頁</small></a>
<a class="fab places" id="guideFab" href="#guide" aria-label="跳到景點百科"><span aria-hidden="true">▲</span><small>景點</small></a>
</div>
<script>{JS}</script>
'''

page = HEAD + BODY
with open(OUT, "w", encoding="utf-8") as f:
    f.write(page)

STANDALONE_META = '''<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#962437">
<meta name="apple-mobile-web-app-title" content="奧捷 12 日">
'''
standalone = ('<!doctype html>\n<html lang="zh-Hant">\n<head>\n' + HEAD + STANDALONE_META
              + '</head>\n<body>\n' + BODY + '</body>\n</html>\n')
with open(OUT_INDEX, "w", encoding="utf-8") as f:
    f.write(standalone)
print("wrote", OUT_INDEX, len(standalone.encode("utf-8")), "bytes;", len(PLACES), "places")

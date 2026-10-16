# -*- coding: utf-8 -*-
import html, re, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from content_places import PLACES
from content_hotels import HOTELS
from content_shops import SHOPS
from content_maps import PLACE_MAP, DAY_ROUTES, MEET_MAP, PRG_T1_MAP, WX_LOCS, DAY_WX
HOTELS.update(SHOPS)  # shop pages share the hotel page layout
from content_gifts import GIFTS_MINE, GIFTS_AT, GIFTS_CZ, GIFTS_MARKET, SHOP_PLAN, GIFT_TIPS
from content_markets import MARKETS, OVERVIEW, WD

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "austria-czech-guide.html")   # Claude Artifact version (wrapped by the artifact host)
OUT_INDEX = os.path.join(ROOT, "index.html")            # standalone page served by GitHub Pages

# ───────────────────────── 每日行程 ─────────────────────────
# stops: (place_id, note)   status: upd / tbc / None
DAYS = [
 dict(n=1, date="10/11", wd="日", city="台北 → 維也納", theme="夜班機出發",
      route=["桃園 TPE", "✈", "維也納 VIE"],
      flight="CI63　TPE 23:45 → VIE 07:05（+1）・飛行約 13 小時 20 分",
      timeline=[("20:50", "桃園機場第一航廈・中華航空團體櫃檯（10–11 號櫃檯後方）集合，領隊到了會用 LINE 通知。領取登機證、網路 SIM 卡、導覽耳機和行李牌・[[" + MEET_MAP + "|地圖 ↗]]", False),
                ("託運出境", "各自託運行李，等 X 光檢查通過再出境。安檢和護照查驗照航空公司與移民官指示。", False),
                ("登機", "登機門、登機時間和登機順序以當天宣布和登機證為準，準時到登機門。", False),
                ("23:45", "CI63 起飛", False)],
      notice="機場發的行李牌不是掛在飛機託運行李上的，先收好，到維也納機場領完行李再綁上。導覽耳機要歸還，遺失需賠償 2,000 元。",
      intro=["搭華航直飛班機，機型是 A350-900，經濟艙 3-3-3。抵達維也納是當地早上 7 點多，盡量在機上多睡一點，隔天一下飛機就開始行程。眼罩、耳塞、頸枕記得放隨身包；上機後需要拖鞋、眼罩、耳機，也可以跟空服員要。"],
      stops=[], meals=[("早", "X"), ("午", "X"), ("晚", "機上精選美食")],
      hotel=("機上過夜", "")),
 dict(n=2, date="10/12", wd="一", city="維也納 → 梅爾克 → 維也納", theme="梅爾克修道院・百水公寓",
      route=["維也納", "梅爾克", "杜恩施坦", "維也納"],
      intro=["早上 7 點多抵達維也納，先往西到多瑙河畔的梅爾克參觀修道院，下午回到維也納看百水公寓。"],
      notice="出關後就直接搭巴士出發，第一段車程約 1.5 小時。在機場先上洗手間、拿出保暖衣物，並綁上行李牌，飯店靠它幫忙搬行李。",
      timeline=[("07:05", "抵達維也納機場。下機後在航站內等全團到齊再一起去入境查驗；要搭接駁車的話先各自搭，到航站再集合。", False),
                ("入境", "先用自助機登錄護照資料、臉部照片和指紋（歐盟出入境系統 EES），再排人工查驗，教學影片在 LINE 群組。人多時分開排隊，家人到齊、通過查驗就照指示去行李轉盤。沿途有好幾個洗手間，排隊的話往後面的走。", False),
                ("領行李", "在行李轉盤集合。領隊確認全員和行李都到齊才一起出關，不要自己先走。", False),
                ("上午", "搭巴士前往[[p-melk|梅爾克]]（約 1.5 小時），逛梅爾克舊城和修道院花園。", False),
                ("中午", "午餐：肉醬斜管麵、香草奶油烤雞胸配奶油飯、杏桃蛋糕。", False),
                ("下午", "[[p-melk|梅爾克修道院]]入內導覽，之後前往[[p-hundertwasser|百水公寓]]（約 1.5 小時）。", False),
                ("傍晚", "百水公寓觀光，再到飯店（約 10 分鐘）。", False),
                ("晚上", "晚餐：[[p-vienna|維也納水煮牛 Tafelspitz]]。吃法見[[p-dining|歐洲用餐禮儀]]。", False)],
      extra=["梅爾克修道院的圖書館 2026 年整修中，可能看到鷹架；大陽台改走臨時便橋。導覽後可以逛北堡壘的露台和修道院商店（自製琴酒、啤酒、藥草鹽），見[[p-melk|梅爾克修道院]]。沿河地名見[[p-wachau|瓦豪河谷]]。"],
      log=[("去了", "去完梅爾克，又到瓦豪河谷的[[p-wachau|杜恩施坦 Dürnstein]]，藍白鐘樓和獅心王城堡的小鎮。"),
           ("買了", "杏桃酒、杏桃蛋糕、杏桃巧克力，還有一個麵包。"),
           ("麵包", "杜恩施坦是瓦豪小圓麵包 Wachauer Laberl 的發源地：1905 年由鎮上的麵包師傅 Rudolf Schmidl 發明，據說靈感來自法國長棍麵包，圓圓的，比凱撒麵包大。Schmidl 麵包店今天還在鎮上，配方是家族祕密。"),
           ("晚餐", "在這家吃：[[https://maps.app.goo.gl/R8uwXQstYMuV4goz7|餐廳 Google 地圖 ↗]]。行程菜單是維也納水煮牛 Tafelspitz，吃法見[[p-dining|歐洲用餐禮儀]]。"),
           ("帶回台灣", "杏桃酒放託運行李，用衣服包好；年滿 20 歲酒類免稅 1 公升。蛋糕看包裝上的日期，早點吃；巧克力避開暖氣和陽光。")],
      stops=[("p-vienna", ""), ("p-melk", "入內導覽・門票已含"), ("p-hundertwasser", ""), ("p-wachau", "杜恩施坦")],
      meals=[("早", "機上精選美食"), ("午", "肉醬斜管麵佐帕達諾乾酪・香草奶油烤雞胸配蔬菜和奶油飯・杏桃蛋糕佐鮮奶油＋酒水"),
             ("晚", "羊乳酪紅花菜豆沙拉・[[p-vienna|水煮牛 Tafelspitz]] 配薯餅、根莖蔬菜、蘋果辣根醬和細香蔥醬・皇帝煎餅配燉李子＋酒水")],
      hotel=("InterContinental Vienna", "維也納兩晚連泊。飯店在市立公園旁，走路可到金色史特勞斯雕像。")),
 dict(n=3, date="10/13", wd="二", city="維也納", theme="熊布朗宮・霍夫堡皇宮・聖史蒂芬大教堂・維也納音樂會",
      route=["維也納市區"],
      notice="06:30 開始早餐，在大廳樓層，入場時報房號。08:30 巴士上車集合。",
      timeline=[("06:30", "早餐開始，在大廳樓層，入場報房號。", False),
                ("08:30", "巴士上車集合。", False),
                ("上午", "導覽：[[p-schonbrunn|熊布朗宮]]（美泉宮，入內）・[[p-hofburg|霍夫堡皇宮]]（舊皇宮）・[[p-stephansdom|聖史蒂芬大教堂]]・名店街（大教堂周邊的克恩頓大街、格拉本大街一帶）。", False),
                ("中午", "午餐在 [[https://maps.app.goo.gl/XJfgMd58ohyjYwNa7|Buxbaum]]，米其林指南推薦的餐廳，三道菜，菜單見下面。", False),
                ("14:30–18:00", "自由活動 → 你選了[[p-khm|藝術史博物館]]・[[https://maps.app.goo.gl/xHBEk7LS93W4T3LD6|Google 地圖 ↗]]。看完走約 10 分鐘到[[s-sacher|薩赫飯店]]買薩赫蛋糕（門市開到 22:00）", True),
                ("晚上", "晚餐在 [[https://maps.app.goo.gl/XJdo8DZK4S3Kaxf56|Salm Bräu]] 吃豬肋排，之後前往音樂協會[[p-concert|布拉姆斯廳]]聽音樂會・[[https://www.google.com/maps/search/?api=1&query=Musikverein+Wien%2C+Musikvereinsplatz+1%2C+1010+Wien|地圖 ↗]]", False)],
      stops=[("p-schonbrunn", "門票已含"), ("p-hofburg", ""), ("p-stephansdom", ""),
             ("p-khm", "自由活動・已選"), ("p-concert", "布拉姆斯廳")],
      extra=["晚上的音樂會可以稍微打扮，避免短褲、短裙、露肩和拖鞋；進教堂也一樣。"],
      log=[("午餐", "Buxbaum，Grashofgasse 3，在聖十字修道院的庭院 Heiligenkreuzerhof 裡・[[https://maps.app.goo.gl/XJfgMd58ohyjYwNa7|Google 地圖 ↗]]。列在米其林指南裡的現代料理餐廳，做奧地利經典菜，也有國際風味的菜色。"),
           ("備註", "無酒精葡萄酒和葡萄汁很好喝。"),
           ("晚餐", "Salm Bräu，Rennweg 8，就在美景宮旁邊・[[https://maps.app.goo.gl/XJdo8DZK4S3Kaxf56|Google 地圖 ↗]]。1994 年開的自釀啤酒餐廳，設在 1717 年由皇后威廉明妮・阿瑪莉亞創立的修道院舊附屬建築裡，房子已有 450 多年歷史。自己釀五款啤酒（有小麥啤酒），豬肋排和豬腳是招牌。")],
      alts=dict(title="其他自由活動選項（領隊提供）", items=[
          ("奧地利國家圖書館", "09:00–18:00", "世界最美的圖書館之一，介紹見[[p-hofburg|霍夫堡皇宮]]頁的國家圖書館大廳。", "https://maps.app.goo.gl/HdHGkvP5VUJaKQn88", "https://lillian.tw/osterreichische-nationalbibliothek/"),
          ("阿爾貝蒂納博物館 Albertina", "10:00–18:00", "阿爾貝特公爵的收藏，近代畫家為主，從莫內到畢卡索；最有名的館藏是杜勒的〈野兔〉，原作因怕光很少展出。", "https://maps.app.goo.gl/jrsm9VvQtnGhLosN6?g_st=al", None)]),
      meals=[("早", "飯店內早餐，06:30 起，在大廳樓層，報房號入場"),
             ("午", "Buxbaum（[[https://maps.app.goo.gl/XJfgMd58ohyjYwNa7|地圖 ↗]]）「米其林」推薦餐＋酒水：前菜 胡桃南瓜（紅菊苣、瑞可塔乳酪、檸檬甜酸醬）・主菜 白梭吻鱸 Zander（紅椒甘藍菜、薩丁尼亞珍珠麵、酸豆）・甜點 三種巧克力（沙棘、腰果）。素食主菜換成奶油雞油菌 Eierschwammerl（森林區馬鈴薯丸子、芥末甘藍、罌粟籽、焦化奶油）；不吃魚換成粉紅色烤牛沙朗 Beiried（千層馬鈴薯、野生青花菜、彩色胡蘿蔔）"),
             ("晚", "Salm Bräu 自釀啤酒餐廳（[[https://maps.app.goo.gl/XJdo8DZK4S3Kaxf56|地圖 ↗]]）：粗麥粉丸子湯 Grießnockerlsuppe・豬肋排配炸馬鈴薯和兩種醬汁（2–4 人一盤共用）・冰涼的甜乳酪丸子佐冰草莓醬＋酒水")],
      hotel=("InterContinental Vienna", "市立公園旁。走到音樂協會約 10 分鐘，到聖史蒂芬大教堂約 15 分鐘。")),
 dict(n=4, date="10/14", wd="三", city="維也納 → 湖區", theme="哈斯達特・聖沃夫岡",
      route=["維也納", 288, "哈斯達特湖區", 37, "聖沃夫岡湖區"],
      intro=["今天直接從維也納往西開到湖區，288 公里車程約 3.5–4 小時，中途進休息站一次，可以在車上補眠。"],
      notice="07:30 前把大行李放到房門口，飯店行李員會來收，先確認行李牌綁好。08:15 大廳集合、確認行李上車，08:20 出發。護照、貴重物品和車上要用的東西隨身帶。",
      timeline=[("06:30", "早餐。", False),
                ("07:30", "大行李放房門口，飯店行李員來收。", False),
                ("08:15", "大廳集合，確認行李上車。", False),
                ("08:20", "出發前往[[p-hallstatt|哈斯達特]]，車程約 3.5–4 小時，中途進休息站一次。", False),
                ("中午", "午餐在市集廣場上的 [[https://maps.app.goo.gl/BNw2kUvtEhpiz8fe8|Seewirt Zauner]]：清湯佐湯珠、烤鱒魚、巧克力蛋糕配鮮奶油。", False),
                ("下午", "[[p-hallstatt|哈斯達特]]觀光。官方地圖上的 10 個景點整理在哈斯達特頁。", False),
                ("傍晚", "前往[[p-stwolfgang|聖沃夫岡]]，車程約 50 分鐘，入住白馬飯店。", False),
                ("晚上", "晚餐：招牌沙拉、有機小牛肉燉肉配米飯、水果沙拉佐自製雪酪。", False)],
      log=[("午餐", "Seewirt Zauner，哈斯達特市集廣場 51 號，就在官方地圖第 5 號的[[p-hallstatt|市集廣場]]上・[[https://maps.app.goo.gl/BNw2kUvtEhpiz8fe8|Google 地圖 ↗]]。一百多年前從一間叫「Zur Bierquelle」的葡萄酒早餐室發展起來，現在是旅館兼餐廳，以湖魚和薩爾茲卡默古特的地方菜出名。")],
      stops=[("p-hallstatt", ""), ("p-stwolfgang", "")],
      meals=[("早", "飯店內早餐，06:30"),
             ("午", "Seewirt Zauner（[[https://maps.app.goo.gl/BNw2kUvtEhpiz8fe8|地圖 ↗]]）：清湯佐湯珠・烤鱒魚・巧克力蛋糕配鮮奶油＋酒水"),
             ("晚", "招牌沙拉 Peter & Paul・有機小牛肉燉肉 Goulash 配米飯・水果沙拉佐自製雪酪＋酒水")],
      hotel=("Romantik Hotel Im Weissen Rössl", "聖沃夫岡湖畔的白馬飯店，兩晚連泊。輕歌劇《白馬酒店》的舞台，有漂在湖上的溫水泳池。")),
 dict(n=5, date="10/15", wd="四", city="湖區", theme="世界最著名・鹽礦",
      route=["聖沃夫岡湖區", 90, "鹽礦", "聖沃夫岡湖區"],
      notice="07:00 早餐，搭 3 號電梯到 0 樓（歐洲的 0 樓是地面層，相當於台灣的 1 樓）。08:20 巴士集合出發。鹽礦裡常年 8–12°C，進去前會套上長袖長褲的礦工服，裡面穿兩層就夠。",
      timeline=[("07:00", "早餐：搭 3 號電梯到 0 樓。", False),
                ("08:20", "巴士集合出發，前往[[p-salzwelten|鹽礦]]，車程約 75 分鐘。", False),
                ("上午", "[[p-salzwelten|鹽礦]]參觀。", False),
                ("中午", "午餐：沙拉、維也納炸肉排配馬鈴薯、李子蛋糕。", False),
                ("下午", "回白馬飯店，車程約 75 分鐘，之後在[[p-stwolfgang|聖沃夫岡]]自由活動。", False),
                ("晚上", "晚餐：番茄奶油湯、烤羊排、凝乳起司舒芙蕾。", False)],
      log=[("拍照點", "今天在聖沃夫岡這個碼頭拍照，光線好的時段可以一次拍到朝聖教堂、白馬飯店、湖邊小公園和碼頭・[[https://maps.app.goo.gl/avghL8M2VpCtMX386|Google 地圖 ↗]]")],
      stops=[("p-salzwelten", "門票已含")],
      extra=["下午回飯店後是自由時間，可以用白馬飯店湖上和室內的溫水泳池、三溫暖，記得帶泳衣。也可以去朝聖教堂看[[p-stwolfgang|帕赫祭壇]]，或在湖邊散步。"],
      meals=[("早", "飯店內早餐，07:00，搭 3 號電梯到 0 樓"),
             ("午", "沙拉・維也納炸肉排 Wiener Schnitzel 配馬鈴薯・李子蛋糕＋酒水"),
             ("晚", "番茄奶油湯・烤羊排佐迷迭香醬、四季豆和焗烤馬鈴薯・凝乳起司舒芙蕾配香草冰淇淋＋酒水")],
      hotel=("Romantik Hotel Im Weissen Rössl", "連泊第二晚，不用整理大行李。")),
 dict(n=6, date="10/16", wd="五", city="薩爾茲堡 → 庫倫洛夫", theme="莫札特的故鄉・童話小鎮",
      route=["聖沃夫岡湖區", 75, "薩爾茲堡", 218, "庫倫洛夫"],
      intro=["上午在薩爾茲堡市區導覽（原行程有搭★城堡纜車上山，實際以領隊安排為準）。午餐自理，下午越過邊境進入捷克，傍晚抵達庫倫洛夫。"],
      notice="14:30 在 Griesgasse 19/21 的 Billa 超市右前方廣場集合（領隊原本的訊息寫 14:00 出發，以領隊最新通知為準）。早上 07:30 大行李放房門口，手提行李自己帶；08:30 上車。庫倫洛夫的飯店在老城裡，巴士開不進去，每間房把當晚要用的東西集中成一件大行李箱，或準備一晚的過夜包。",
      timeline=[("07:00", "早餐。", False),
                ("07:30", "大行李放房門口，行李員來收。手提行李自己帶。", False),
                ("08:30", "上車出發，前往[[p-salzburg|薩爾茲堡]]，車程約 75 分鐘。", False),
                ("上午", "薩爾茲堡當地導遊帶市區導覽。", False),
                ("中午", "午餐自理，留一點時間逛街。推薦見下面。", False),
                ("14:30", "在 [[https://maps.app.goo.gl/4Gm7ie2HEXUbXkz16|Billa 超市]]（Griesgasse 19/21）右前方的廣場集合。", False),
                ("下午", "前往[[p-krumlov|庫倫洛夫]]，車程約 3.5–4 小時，中途進休息站一次。", False),
                ("晚上", "中世紀晚宴，換上中世紀服裝體驗。", False)],
      stops=[("p-salzburg", ""), ("p-festung", "★搭城堡纜車"), ("p-sbg-altstadt", ""), ("p-mirabell", ""), ("p-mozart", ""), ("p-krumlov", "")],
      alts=dict(title="午餐自理與順路逛：領隊和導遊推薦（都在老城，走路幾分鐘）", items=[
          ('Bosna 熱狗 Balkan Grill', '每天 11:00–18:30', '領隊和導遊推薦的老熱狗攤，薩爾茲堡自己的街頭小吃：烤香腸夾麵包，1949 年發明。有 4 種調味，部落客最推 2 號：洋蔥、巴西里、芥末，微辣。在 Getreidegasse 33 的穿堂裡，穿過去就是大學廣場，常要排隊。', 'https://www.google.com/maps/search/?api=1&query=Balkan+Grill%2C+Getreidegasse+33%2C+Salzburg', 'https://beri.tw/balkan-grill-walter-salzburg/'),
          ('BURGERISTA 漢堡', '營業時間以現場為準', '導遊推薦。奧地利本土的漢堡連鎖，2012 年從上奧地利邦的小漢堡攤起家。在 Griesgasse 15，離 Billa 集合點只有幾步路，吃完直接集合最方便。', 'https://maps.app.goo.gl/QMUDqxMFJwGmxxKQ8', None),
          ('Nordsee 魚堡', '營業時間以現場為準', '德國連鎖的海鮮速食，招牌是北海魚堡，Getreidegasse 上就有一家。想吃清爽一點可以選這個。', 'https://www.google.com/maps/search/?api=1&query=Nordsee%2C+Getreidegasse%2C+Salzburg', 'https://jingxuan.tw/nordsee/'),
          ('大學廣場市集 Grünmarkt', '週一到週五', '非假日才有的市集，Bosna 店的穿堂出去就是。有香腸攤、麵包、水果和小吃，可以邊走邊吃，順便買車上吃的。', 'https://www.google.com/maps/search/?api=1&query=Gr%C3%BCnmarkt%2C+Universit%C3%A4tsplatz%2C+Salzburg', 'https://www.tripadvisor.com.tw/Attraction_Review-g190441-d241192-Reviews-Grunmarkt-Salzburg_Austrian_Alps.html'),
          ('Café Tomaselli', '營業時間以現場為準', '奧地利最古老的咖啡館，1700 年開業，在舊市場廣場 Alter Markt 9。可以坐下來吃蛋糕、喝咖啡，也有簡餐。旁邊 Brodgasse 13 就是 Fürst 老店，順便買莫札特巧克力。', 'https://www.google.com/maps/search/?api=1&query=Caf%C3%A9+Tomaselli%2C+Alter+Markt+9%2C+Salzburg', 'https://www.salzburg.info/de/reiseinfos/salzburg-a-z/cafe-tomaselli_az_6929'),
          ('TEA & Co 茶葉店', '營業時間以現場為準', '導遊推薦的茶店，在 Griesgasse 7，往 Billa 集合點的路上。可以買茶葉當伴手禮，品項以現場為準。', 'https://maps.app.goo.gl/i4p4RuBkGiRpjqrC6', None),
      ]),
      extra=["下午要坐 3.5–4 小時的車，晚上又是中世紀晚宴，午餐吃輕一點就好，上車前買水和小點心。更多餐廳見部落格[[https://arita0519.pixnet.net/blog/post/468671258|薩爾斯堡美食總整理]]。",
             "維也納沒買到薩赫蛋糕的話，薩爾茲堡的[[s-sacher|Hotel Sacher]]也有門市，在米拉貝爾花園南邊的河岸。"],
      log=[("集合", "14:30，Billa 超市（Griesgasse 19/21）右前方的廣場・[[https://maps.app.goo.gl/4Gm7ie2HEXUbXkz16|地圖 ↗]]"),
           ("導遊推薦", "[[https://maps.app.goo.gl/i4p4RuBkGiRpjqrC6|TEA & Co 茶葉店]]（Griesgasse 7）、[[https://maps.app.goo.gl/QMUDqxMFJwGmxxKQ8|BURGERISTA 漢堡]]（Griesgasse 15），都在集合點附近的 Griesgasse 上。")],
      meals=[("早", "飯店內早餐，07:00"), ("午", "自理，老熱狗攤等推薦見上面"), ("晚", "穿越時光著中古世紀服飾 享受庫倫洛夫晚宴＋酒水")],
      hotel=("Hotel Zlatý Anděl", "金色天使飯店，就在庫倫洛夫的主廣場上，出門就是老城。")),
 dict(n=7, date="10/17", wd="六", city="南波希米亞 → 溫泉區", theme="百威啤酒的故鄉・瑪麗安斯凱",
      route=["庫倫洛夫", 25, "巴德傑維契", 270, "瑪麗安斯凱"],
      stops=[("p-budejovice", ""), ("p-marienbad", "")],
      meals=[("早", "飯店內早餐"), ("午", "百威城主廚料理＋酒水"), ("晚", "飯店內主廚晚餐＋酒水")],
      hotel=("Luxury Historical Castle Hotel & Golf", "全名 Rübezahl Marienbad Luxury Historical Castle Hotel & Golf，20 世紀初的城堡建築，2015 年整修後重新開幕，附近就是 1905 年開幕的高爾夫球場。")),
 dict(n=8, date="10/18", wd="日", city="溫泉區 → 布拉格", theme="卡羅維瓦利・查理大橋・舊城廣場",
      route=["瑪麗安斯凱", 55, "卡羅維瓦利", 128, "布拉格"],
      stops=[("p-karlovy", ""), ("p-prague", ""), ("p-charles", ""), ("p-oldtownsq", ""), ("p-tyn", ""), ("p-orloj", "")],
      extra=["在卡羅維瓦利記得試現烤的[[p-karlovy|溫泉薄餅]]，柱廊一帶到處都有店家・[[https://www.google.com/maps/search/?api=1&query=L%C3%A1ze%C5%88sk%C3%A9+oplatky%2C+Karlovy+Vary|薄餅店家地圖 ↗]]",
             "晚上在老城附近，想吃煙囪捲或冰淇淋，見[[p-prague-picks|布拉格口袋名單]]。"],
      meals=[("早", "飯店內早餐"), ("午", "風味料理餐廳＋酒水"), ("晚", "捷克醬鴨料理＋酒水")],
      hotel=("Hotel KINGS COURT Prague", "布拉格三晚連泊。共和廣場旁，隔壁是市民會館和火藥塔，走到舊城廣場約 10 分鐘。")),
 dict(n=9, date="10/19", wd="一", city="布拉格", theme="城堡區・黃金巷・舊城廣場",
      route=["布拉格"],
      intro=["布拉格景點集中，很適合連泊慢慢逛。城市主要分為城堡區、小城區、猶太區與新、舊城區，今天專心看城堡區。"],
      stops=[("p-castle", ""), ("p-vitus", "門票已含"), ("p-golden", "門票已含"), ("p-oldtownsq", "")],
      extra=["晚上回到老城附近，想吃煙囪捲或冰淇淋，見[[p-prague-picks|布拉格口袋名單]]。"],
      meals=[("早", "飯店內早餐"), ("午", "布拉格「米其林」推薦餐＋酒水"), ("晚", "旅遊書推薦必吃 捷克料理＋酒水")],
      hotel=("Hotel KINGS COURT Prague", "連泊第二晚。")),
 dict(n=10, date="10/20", wd="二", city="布拉格", theme="伏爾塔瓦河遊船・高堡・自由活動",
      route=["布拉格"],
      timeline=[("上午", "[[p-vltava|伏爾塔瓦河遊船]]・[[p-vysehrad|高堡]]・搭[[p-tram|有軌電車]]沿河看景・漫步到[[p-dancing|跳舞的房子]]", False),
                ("中午", "午餐：中式懷鄉料理（八菜一湯）", False),
                ("14:30 起", "自由活動。公司提供 24 小時電車地鐵票。想去[[p-parizska|巴黎街精品街]]逛 Celine・[[https://www.google.com/maps/search/?api=1&query=CELINE+Prague%2C+Pa%C5%99%C3%AD%C5%BEsk%C3%A1+15%2C+Praha+1|Google 地圖 ↗]]。煙囪捲、冰淇淋、伴手禮店見[[p-prague-picks|布拉格口袋名單]]", True),
                ("18:00", "[[p-imperial|帝國咖啡館]]晚餐（6 位，已訂位）・[[h-imperial|設施介紹]]・[[https://www.google.com/maps/search/?api=1&query=Caf%C3%A9+Imperial%2C+Na+Po%C5%99%C3%AD%C4%8D%C3%AD+15%2C+Praha+1|Google 地圖 ↗]]", True)],
      stops=[("p-vltava", "船票已含"), ("p-vysehrad", ""), ("p-tram", "特別安排"), ("p-klementinum", "電車沿途"), ("p-narodni", "電車沿途"), ("p-dancing", ""),
             ("p-parizska", "想去 Celine"), ("p-prague-picks", "煙囪捲・冰淇淋"), ("p-imperial", "18:00 已訂位")],
      meals=[("早", "飯店內早餐"), ("午", "中式懷鄉料理（八菜一湯）"), ("晚", "自理：[[p-imperial|帝國咖啡館]] 18:00（6 位已訂位）", "Café Imperial")],
      hotel=("Hotel KINGS COURT Prague", "連泊第三晚。帝國咖啡館離飯店步行約 5 分鐘。")),
 dict(n=11, date="10/21", wd="三", city="布拉格 → 台北", theme="早班機返台",
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
  ("topics", "專題閱讀"),
]

CHANGES = [
  ("Day 1", "集合時間 20:50（領隊行前通知，原為 21:00），桃園第一航廈華航團體櫃檯（10–11 號櫃檯後方）。去程 CI63 改為 23:45 起飛、隔天 07:05 抵達（原為 23:20／07:00）。"),
  ("Day 2", "改為維也納 → 梅爾克修道院 → 維也納（百水公寓）。實際上去完梅爾克也到了瓦豪河谷的杜恩施坦。原 PDF 的霍夫堡、聖史蒂芬移到 Day 3。依領隊提供的菜單，午餐是肉醬斜管麵和烤雞胸（原為豬肋排），晚餐是維也納水煮牛 Tafelspitz。"),
  ("Day 3", "改為熊布朗宮＋霍夫堡＋聖史蒂芬＋音樂會（布拉姆斯廳）。晚餐從炸肉排改為豬肋排。新增 14:30–18:00 自由活動。"),
  ("Day 4", "梅爾克移到 Day 2，這天直接從維也納開往哈斯達特（288 km），住聖沃夫岡的白馬飯店。依領隊菜單，鱒魚改在午餐吃，晚餐是有機小牛肉燉肉。"),
  ("Day 5", "湖區連泊，專程去鹽礦。依領隊菜單，午餐是維也納炸肉排，晚餐是烤羊排。"),
  ("Day 6", "從聖沃夫岡出發（75 km 到薩爾茲堡、218 km 到庫倫洛夫），確定住金色天使飯店。依領隊通知，午餐改為自理，晚餐是中世紀晚宴。"),
  ("Day 7", "終點從卡羅維瓦利改為瑪麗安斯凱，晚餐改為飯店主廚晚餐，住 Rübezahl 城堡飯店。"),
  ("Day 8", "順序對調：瑪麗安斯凱 → 卡羅維瓦利 → 布拉格。景點與餐食同原 PDF。"),
  ("Day 8–10", "布拉格飯店確定為 Hotel KINGS COURT（原為 Hilton Old Town 或 Marriott）。"),
  ("Day 9", "午晚餐對調：午餐米其林推薦，晚餐捷克料理。"),
  ("Day 10", "14:30 起自由活動，公司提供 24 小時電車地鐵票，想去巴黎街逛 Celine；晚餐自理，已訂帝國咖啡館 18:00、6 位。"),
  ("Day 11", "回程 CI68 改為 10:40 起飛、隔天 05:05 抵達（原為 10:55／05:40）。"),
]

TIPS = [
 ("出發前・機場", [
  ("護照", "帶有效護照。新辦的護照，請在個人資料頁上方的簽名欄簽名。已經交給旅行社的，領隊會帶去機場。"),
  ("集合", "10/11（日）20:50，桃園機場第一航廈華航團體櫃檯（10–11 號櫃檯後方）。領隊到了會用 LINE 通知，收護照換登機證，並發網路 SIM 卡、導覽耳機和行李牌。各自託運行李，等 X 光檢查通過再出境。登機門和登機時間以當天宣布和登機證為準。"),
  ("行前手冊", "出發前一定要看行前說明會手冊，尤其第 23–27 頁。"),
  ("特殊需求", "素食、不吃牛、過敏，以及床型需求，第一天再跟領隊確認一次。機上餐點要找業務人員。"),
  ("飛機座位", "華航 A350-900，經濟艙 3-3-3。團體座位可能和其他團交錯，沒有自己付費選位的，領隊會盡量讓同行家人坐在一起。"),
  ("機上好睡", "去程約 13.5 小時，建議帶眼罩、耳塞，需要的話加頸枕。上機後需要拖鞋、眼罩、耳機，可以跟空服員要。有線耳機可以在機上用，也能接行程中的導覽耳機。"),
  ("導覽耳機", "領隊在桃園機場發，旅程結束要歸還，遺失需賠償 2,000 元。"),
  ("行李牌", "機場發的行李牌不是掛飛機託運用的。到維也納機場領完行李再綁上，飯店靠它幫忙搬行李。"),
  ("抵達維也納", "入境要先用自助機登錄護照資料、臉部照片和指紋（歐盟出入境系統 EES），教學影片在 LINE 群組。在行李轉盤集合，全團和行李到齊才一起出關，出關後直接搭巴士約 1.5 小時，先在機場上洗手間。詳細流程見 Day 2。"),
 ]),
 ("行李", [
  ("託運", "2 件，每件 23 公斤（以華航規定為準）。建議帶一個大行李箱，加一個摺疊行李袋，回程裝衣服當第二件託運。"),
  ("手提", "登機箱 1 件（三邊合計 115 公分內、7 公斤），加隨身小包 1 件。"),
  ("行動電源", "每人最多 2 個，每個 100 Wh（約 27,000 mAh）以內。只能隨身帶、不能託運，機上全程禁止使用和充電。"),
  ("液體", "盡量放託運。隨身的每瓶 100 ml 以內，裝進一個 1 公升以內的透明夾鏈袋。不要帶噴霧罐、壓力罐。打火機每人限 1 個。"),
  ("肉類蔬果", "防疫檢查嚴格，生鮮蔬果和肉類製品都不要帶，違規會被罰款。"),
  ("充電", "充電器和轉接頭最容易忘。領隊會在機場發每人一個歐規轉接頭，需要多的請自己準備。"),
 ]),
 ("天氣・穿著", [
  ("天氣", "10 月中旬預測約 4–18°C，湖區和鹽礦更冷。山區天氣不穩定，最近有冷鋒，出發前整理行李時再看一次預報："
    "[[https://www.bbc.com/weather/3067696|BBC 布拉格]]・[[https://www.bbc.com/weather/2761369|BBC 維也納]]・"
    "[[https://www.bbc.com/weather/2776943|BBC 哈斯達特]]。每天行程開頭也有當天的天氣預報。"),
  ("衣服", "長袖為主，加厚外套，帶手套、圍巾、毛帽。室內和巴士有暖氣（約 20–23°C），穿好穿脫的。自助洗衣不方便，衣服帶足天數。"),
  ("鞋子", "維也納、布拉格以走路為主，幾乎每天超過一萬步。穿好走的鞋，防水更好，再帶一雙備用鞋。"),
  ("雨具・防曬", "一定要帶防風雨衣或短摺傘。晴天太陽可能很大，可以帶帽子、墨鏡和防曬。"),
  ("鹽礦", "裡面常年 8–12°C，進去前會套上長袖長褲的礦工服，裡面穿兩層就夠。"),
  ("教堂・音樂會", "避免短褲、短裙、露肩和拖鞋。維也納音樂會可以稍微打扮。"),
 ]),
 ("錢・付款", [
  ("貨幣", "奧地利用歐元，出發前先換好，每人約 €300–500 現金。捷克用克朗，約 1 歐元換 24 克朗，到當地匯兌所再換，也可以用美金換；換之前先問清楚實拿金額。歐元紙鈔上的建築見[[p-euro|從歐元看西方建築史]]。"),
  ("信用卡", "帶 2–3 張 Visa、Mastercard，需要的話先提高額度。手續費和回饋先問銀行，在歐盟消費多數沒有回饋。Apple Pay、Google Pay 能用的店越來越多。精品等大額消費用刷卡。"),
  ("小費", "餐廳約 5–10%，怎麼給見下面的「用餐」。"),
  ("退稅", "同一天在同一家店消費達門檻可以辦退稅（奧地利 €75.01、捷克 2,001 CZK），在最後離開歐盟的布拉格機場辦理海關蓋章。退稅單要填英文地址，先用[[https://www.post.gov.tw/post/internet/Postal/index.jsp?ID=207|中華郵政中文地址英譯]]翻好。想買的東西先列清單和型號，比較省時間。"),
 ]),
 ("用餐", [
  ("入座", "高級一點的餐廳在門口等帶位；咖啡館和小酒館通常自己找位子坐。桌上放著 Reserviert（奧）或 Rezervováno（捷）牌子的是預約位，不要坐。"),
  ("打招呼", "進餐廳、小店先打招呼，離開說謝謝。奧地利：Grüß Gott 或 Guten Tag（你好）、Danke（謝謝）。捷克：Dobrý den（你好）、Děkuji（謝謝）。"),
  ("開動・乾杯", "開動前說 Guten Appetit（奧）、Dobrou chuť（捷）。乾杯說 Prost（奧）、Na zdraví（捷）。大家都拿到酒才開始，跟同桌每個人碰杯，碰杯時看著對方的眼睛，不看會被當成沒禮貌。"),
  ("點水", "水要另外點、另外付錢，礦泉水常常預設是氣泡水。不要氣泡要說清楚：奧地利說 stilles Wasser，捷克說 neperlivá。維也納咖啡館點咖啡會附一杯水。"),
  ("吃相", "左手叉、右手刀，餐具由外往內用。喝湯、吃麵盡量不要發出聲音。餐具擺放、刀叉暗號、上菜順序、麵包怎麼吃，見[[p-dining|歐洲用餐禮儀]]。"),
  ("麵包・小菜", "桌上的麵包、小菜不一定免費。布拉格有些餐廳吃了會算錢，甚至沒吃也列在帳單上；不要的可以請服務生收走，結帳時看一下帳單。"),
  ("結帳", "服務生不會主動拿帳單，不會催你走。要結帳就舉手或用眼神示意，說 Zahlen, bitte（奧）或 Zaplatím, prosím（捷）。在座位上結，服務生會帶刷卡機來，常會問一起付還是分開付。"),
  ("小費", "台灣沒有，這裡要給，約 5–10%，或湊個整數。結帳時直接告訴服務生含小費的總額，例如帳單 €27 就說「30」，不要把錢留在桌上就走。布拉格觀光區有些帳單已經加了服務費（servis、service charge），有加就不用再給。團體餐的小費問領隊。"),
 ]),
 ("台灣可以、這裡不行", [
  ("上廁所", "公共廁所常要付費：維也納部分要 €0.50，布拉格約 10–20 克朗，飯店旁的 Palladium 購物中心也收 20 克朗。在餐廳、景點、飯店先上，身上留點零錢。"),
  ("搭車打票", "Day 10 公司發的 24 小時票，第一次搭車時打一次就好（地鐵在進站前、電車在車上的打票機），之後不要再打，重複打票會讓票失效。沒打票被查到要罰款，金額上千克朗。"),
  ("過馬路", "行人紅燈不要過，布拉格警察會取締開罰。維也納很多人行道上畫有自行車道，走路不要踩進去，腳踏車騎很快。"),
  ("路上喝酒", "布拉格市中心很多街道、廣場禁止在戶外喝酒，會被罰款；餐廳的戶外座位可以喝。買了酒就帶回飯店喝。"),
  ("比數字", "奧地利人比數字從大拇指開始：大拇指是 1，大拇指加食指是 2。只伸食指可能被當成 2，點餐時直接說數字，或用大拇指比。"),
  ("浴室", "很多浴室地板沒有排水孔。淋浴時把浴簾拉進浴缸裡，或關好玻璃門，水不要噴到外面。"),
  ("教堂", "進去脫帽、小聲說話。彌撒進行中不要走動參觀，也不要拍照。"),
 ]),
 ("飯店", [
  ("房型", "都是標準房，有衛浴但不保證有浴缸，沒有特殊景觀。沒提出需求就安排兩張單人床；奧捷很多飯店的雙人房是「德式雙人床」，一張床兩件被子。"),
  ("備品", "多數飯店不提供牙刷、牙膏和室內拖鞋，要自己帶。有洗髮精、沐浴乳、乳液、浴巾和吹風機；洗面乳和保養品自備。"),
  ("熱水", "房間有膠囊咖啡機或熱水壺。習慣喝熱水的可以帶保溫瓶；奧地利多數餐廳裝熱水要另外付費。"),
  ("庫倫洛夫", "飯店在老城裡，巴士開不進去。每間房把當晚要用的東西集中成一件大行李箱，或準備一晚的過夜包，減少搬行李的時間。"),
  ("白馬飯店", "有湖上和室內的溫水泳池、三溫暖，想用的記得帶泳衣。10/15 晚餐前預計安排自由時間。"),
 ]),
 ("生活", [
  ("時差", "奧地利與捷克在 10/25 前是夏令時間，比台灣慢 6 小時。"),
  ("網路", "行程贈送歐洲 SIM 卡，每人每天（每 24 小時）1GB，用完降速到只能傳文字。"),
  ("電壓插座", "230V，雙圓孔插座（C／F 型），台灣電器需要轉接頭。除非電器標示可用 220–240V，否則用飯店的電器比較安全。"),
  ("飲水", "奧地利自來水可以直接喝；捷克領隊建議買礦泉水。餐廳的水要另外付費，行程每人每天提供一瓶 500 ml 礦泉水。"),
  ("防扒", "歐洲扒手多。用可以斜背、拉到胸前的隨身包或防盜腰包，後背包只放水壺、雨傘等不貴重的東西。"),
  ("購物袋", "多數店家不提供免費袋子，自備環保袋。"),
  ("超市", "奧地利週日公休，捷克週日照開，這趟都碰得到營業日。各飯店附近的超市見[[m-markets|超市總覽]]，或點飯店旁的「附近超市」。"),
  ("乾燥", "歐洲空氣乾，帶乳液和護唇膏。捷克物價不貴，當地買也可以。"),
  ("藥品", "帶慣用的藥（腸胃藥、感冒藥、暈車藥）和慢性病藥。有處方箋的帶備用藥，歐洲買藥沒有台灣方便。"),
  ("緊急電話", "歐盟通用 112。外交部旅外國人急難救助全球免付費專線：00-800-0885-0885。"),
 ]),
]

# ───────────────────────── helpers ─────────────────────────
LINK_RE = re.compile(r"\[\[((?:p|h|s|m)-[a-z-]+)\|([^\]]+)\]\]")
EXT_RE = re.compile(r"\[\[(https?://[^|\]]+)\|([^\]]+)\]\]")

def rich(text):
    t = html.escape(text, quote=False)
    def rep(m):
        pid, label = m.group(1), m.group(2)
        if pid not in PLACES and pid not in HOTELS and pid not in MARKETS and pid != "m-markets":
            raise SystemExit("unknown link " + pid)
        return f'<a class="xref" href="#{pid}">{label}</a>'
    t = LINK_RE.sub(rep, t)
    return EXT_RE.sub(lambda m: f'<a class="xref ext" href="{m.group(1)}" target="_blank" rel="noopener">{m.group(2)}</a>', t)

def esc(t):
    return html.escape(t, quote=True)

from urllib.parse import quote_plus, urlencode
def gmap(key):
    return "https://www.google.com/maps/search/?api=1&query=" + quote_plus(HOTEL_Q[key])

HOTEL_PAGE = {h["key"]: hid for hid, h in HOTELS.items() if h.get("key")}

def gsearch_url(q):
    return "https://www.google.com/maps/search/?api=1&query=" + quote_plus(q)

MARKET_PAGE = {m["key"]: mid for mid, m in MARKETS.items()}
HOTEL_LL = {m["key"]: m["hotel_ll"] for m in MARKETS.values() if m["hotel_ll"]}

def hotel_links(key, label="飯店設施 ›"):
    mkt = f'<a class="h-mkt" href="#{MARKET_PAGE[key]}">附近超市 ›</a>' if key in MARKET_PAGE else ""
    return (f'<span class="h-links"><a class="h-map" href="{esc(gmap(key))}" target="_blank" rel="noopener">Google 地圖 ↗</a>'
            f'<a class="h-fac" href="#{HOTEL_PAGE[key]}">{label}</a>{mkt}</span>')

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

def render_wx(d):
    """每天的天氣預報小標題；預報由 guide.js 在手機上向 Open-Meteo 抓。"""
    y, m_, dd = 2026, *map(int, d["date"].split("/"))
    li, bbc = [], []
    for k in DAY_WX[d["n"]]:
        name, lat, lon, bid = WX_LOCS[k]
        li.append(f'<li data-loc="{k}" data-ll="{lat},{lon}"><span class="wx-c">{name}</span>'
                  f'<span class="wx-v">需要網路才看得到預報</span></li>')
        if bid:
            bbc.append(f'<a href="https://www.bbc.com/weather/{bid}" target="_blank" rel="noopener">BBC {name} ↗</a>')
    return (f'<div class="wx" data-date="{y}-{m_:02d}-{dd:02d}"><p class="wx-h">天氣預報</p>'
            f'<ul class="wx-list">{"".join(li)}</ul><p class="wx-src"><span class="wx-t"></span>{"".join(bbc)}</p></div>')

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
    if d.get("status") == "tbc":
        pill = '<span class="pill tbc">待確認</span>'
    o = [f'<section class="day" id="d{n}" data-label="Day {n}" data-date="{d["date"]}">']
    o.append(f'<header class="day-h"><span class="num" aria-hidden="true">{n}</span><div class="day-t">'
             f'<p class="when"><span class="sr">Day {n}・</span>{d["date"]}<span class="wd">週{d["wd"]}</span>{pill}'
             f'<span class="today-pill" hidden>今天</span></p>'
             f'<h2>{esc(d["city"])}</h2><p class="theme">{esc(d["theme"])}</p></div></header>')
    o.append(render_wx(d))
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
    if d.get("log"):
        o.append('<div class="daylog"><p class="daylog-h">旅途紀錄</p><dl>' + "".join(
            f'<div><dt>{esc(k)}</dt><dd>{rich(v)}</dd></div>' for k, v in d["log"]) + '</dl></div>')
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

def _fork(x, y, ang):
    """叉子：握柄在 (x, y)，往 ang 度方向伸出，長約 66。"""
    return (f'<g transform="translate({x},{y}) rotate({ang})"><path d="M0,0H52M52,-5V5M52,-5H66M52,0H66M52,5H66" '
            'stroke-width="2"/></g>')

def _knife(x, y, ang):
    return (f'<g transform="translate({x},{y}) rotate({ang})"><path d="M0,0H36" stroke-width="4"/>'
            '<path d="M36,-3L64,-2Q69,1 63,3L36,3Z" stroke-width="1.6"/></g>')

def _spoon(x, y, ang):
    return (f'<g transform="translate({x},{y}) rotate({ang})"><path d="M0,0H48" stroke-width="3"/>'
            '<ellipse cx="58" cy="0" rx="11" ry="6.5" stroke-width="1.8"/></g>')

def table_figure():
    """餐具擺放（俯視）與刀叉暗號，兩張 SVG。顏色跟著主題變。"""
    setting = ('<svg viewBox="0 0 340 236" role="img" aria-label="西式餐具擺放俯視圖">'
               '<circle class="pl" cx="70" cy="70" r="24"/>' + '<g class="u">' + _knife(52, 82, -28) + '</g>'
               '<circle class="pl" cx="170" cy="140" r="48"/><circle class="rim" cx="170" cy="140" r="35"/>'
               '<text x="170" y="144" text-anchor="middle">主餐盤</text>'
               # 叉子在左（外紅內黑），刀、湯匙在右
               '<g class="u first">' + _fork(92, 196, -90) + '</g><g class="u">' + _fork(110, 196, -90) + '</g>'
               '<g class="u">' + _knife(232, 196, -90) + '</g><g class="u first">' + _knife(248, 196, -90) + _spoon(266, 196, -90) + '</g>'
               # 盤子上方：甜點匙（柄朝右）、甜點叉（柄朝左）
               '<g class="u">' + _spoon(206, 66, 180) + _fork(136, 82, 0) + '</g>'
               '<circle class="gl" cx="236" cy="40" r="12"/><circle class="gl" cx="262" cy="52" r="10"/><circle class="gl" cx="284" cy="66" r="9"/>'
               '<text x="70" y="110" text-anchor="middle">麵包盤</text>'
               '<text x="212" y="78">甜點</text>'
               '<text x="262" y="90" text-anchor="middle">水杯・酒杯</text>'
               '<text x="170" y="226" text-anchor="middle" class="em">紅色＝先上的前菜和湯用，其餘＝主菜用</text></svg>')
    cx1, cx2, cy = 85, 255, 66
    signals = ('<svg viewBox="0 0 340 146" role="img" aria-label="刀叉暗號：休息中與吃完了">'
               f'<circle class="pl" cx="{cx1}" cy="{cy}" r="48"/><circle class="rim" cx="{cx1}" cy="{cy}" r="35"/>'
               '<g class="u">' + _fork(42, 104, -55) + _knife(128, 104, -125) + '</g>'
               f'<circle class="pl" cx="{cx2}" cy="{cy}" r="48"/><circle class="rim" cx="{cx2}" cy="{cy}" r="35"/>'
               '<g class="u">' + _fork(300, 84, -150) + _knife(292, 98, -150) + '</g>'
               f'<text x="{cx1}" y="132" text-anchor="middle" class="em">休息中：擺成八字</text>'
               f'<text x="{cx2}" y="132" text-anchor="middle" class="em">吃完了：並排、柄朝右下</text></svg>')
    return ('<section class="pl-s"><h2>餐具擺放圖</h2><figure class="tf">' + setting +
            '<figcaption>叉子在左，刀和湯匙在右，由外往內用。麵包在左、杯子在右。</figcaption></figure>'
            '<figure class="tf">' + signals + '<figcaption>刀叉的暗號，服務生看了就知道要不要收盤子。</figcaption></figure></section>')

FIGURES = {"table": table_figure}

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
        daylinks = '<span class="daychip ref">' + ("專題閱讀" if p.get("topic") else "參考・未排入行程") + '</span>'
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
    if p.get("figure"):
        o.append(FIGURES[p["figure"]]())
    if p.get("banknotes"):
        o.append('<section class="pl-s"><h2>七種面額一覽</h2><ol class="bn-list">')
        for b in p["banknotes"]:
            rows = "".join(f'<div><dt>{k}</dt><dd>{rich(b[f])}</dd></div>'
                           for k, f in (("正面", "front"), ("背面", "back"), ("像這座橋", "like"), ("這趟看得到", "trip")))
            o.append(f'<li class="bn" style="--bn:{b["color"]}"><p class="bn-h"><span class="bn-v">{esc(b["v"])}</span>'
                     f'<b>{esc(b["style"])}</b><span class="bn-p">{esc(b["period"])}</span></p><dl class="bn-dl">{rows}</dl></li>')
        o.append('</ol></section>')
    if p.get("pins"):
        key = p["hotel"]
        hll = HOTEL_LL[key]
        pins = p["pins"]
        for i, s in enumerate(pins):
            s["no"], s["d"] = i + 1, dist_m(hll, s["ll"])
        o.append(pin_map(hll, gmap(key), HOTEL_ZH[key], pins, None, p.get("landmarks", ())))
        o.append('<section class="pl-s"><h2>店家</h2>' + store_cards(pins, None, None) + '</section>')
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
      mkt = f'・<a href="#{MARKET_PAGE[h["key"]]}">附近超市</a>' if h.get("key") in MARKET_PAGE else ""
      o.append(f'<p class="pl-foot"><a href="#d{first}">回到 Day {first} 行程</a>・<a href="#top">住宿一覽</a>{mkt}</p>')
    else:
      foot = h.get("foot") or [(f"#d{first}", f"回到 Day {first} 行程"), ("#p-imperial", "帝國咖啡館的故事")]
      o.append('<p class="pl-foot">' + "・".join(f'<a href="{href}">{esc(t)}</a>' for href, t in foot) + '</p>')
    o.append('</div></article>')
    return "".join(o)

# ───────────────────────── 超市頁 ─────────────────────────
# 地圖底圖用 OpenStreetMap 圖磚（Google 的地圖圖片要付費 API 金鑰），店家和路線連到 Google 地圖。
MAP_W, MAP_HMIN, MAP_HMAX, MAP_PAD = 512, 300, 512, 56   # 畫布大小（以 zoom z 的像素計），用百分比縮放到螢幕寬度
MAP_WMIN = 320   # 範圍小的時候畫布變窄，等於再放大一點

def merc(lat, lon, z):
    n = 256 * 2 ** z
    s = math.sin(math.radians(lat))
    return (lon + 180) / 360 * n, (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * n

def dist_m(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(h))

def dist_text(d, prefix="直線約"):
    walk = math.ceil(d * 1.3 / 75)   # 直線距離乘 1.3 當作實際路程，每分鐘走 75 公尺
    far = f"{d / 1000:.1f} km" if d >= 1000 else f"{round(d, -1):.0f} m"
    return f"{prefix} {far}・走路約 {walk} 分鐘"

def gdir_url(origin, dest, mode="walking"):
    """origin 為 None 時不指定起點，手機上的 Google 地圖會從目前位置出發。"""
    params = {"api": "1", "destination": dest, "travelmode": mode}
    if origin:
        params = {"api": "1", "origin": origin, "destination": dest, "travelmode": mode}
    return "https://www.google.com/maps/dir/?" + urlencode(params)

def week_text(hours):
    names = ["週一", "週二", "週三", "週四", "週五", "週六", "週日"]
    if len(set(hours)) == 1:
        return f"每天 {hours[0]}" if hours[0][:1].isdigit() else hours[0]
    out, i = [], 0
    while i < 7:
        j = i
        while j + 1 < 7 and hours[j + 1] == hours[i]:
            j += 1
        when = names[i] if i == j else f"{names[i]}至{names[j][1]}"
        out.append(f"{when}公休" if hours[i] is None else f"{when} {hours[i]}")
        i = j + 1
    return "・".join(out)

CAT_LABEL = {"": "超市", "conv": "便利商店・小店", "sweet": "甜點", "souv": "伴手禮"}

def cat_cls(s):
    return s.get("cat", "")

def mk_no_cls(s):
    return ("mk-no " + cat_cls(s)).strip()

def pin_map(anchor_ll, anchor_href, anchor_name, stores, near, landmarks=()):
    """OpenStreetMap 底圖上的飯店（宿）與店家編號；landmarks 是 (座標, 文字, Google 地圖搜尋字串) 的參考點。"""
    pts = [anchor_ll] + [s["ll"] for s in stores if s.get("ll")] + [lm[0] for lm in landmarks]
    for z in range(17, 11, -1):
        xy = [merc(a, b, z) for a, b in pts]
        xs, ys = [p[0] for p in xy], [p[1] for p in xy]
        if max(xs) - min(xs) <= MAP_W - 2 * MAP_PAD and max(ys) - min(ys) <= MAP_HMAX - 2 * MAP_PAD:
            break
    W = round(min(MAP_W, max(MAP_WMIN, max(xs) - min(xs) + 2 * MAP_PAD)))
    H = round(max(MAP_HMIN, max(ys) - min(ys) + 2 * MAP_PAD))
    ox, oy = (max(xs) + min(xs)) / 2 - W / 2, (max(ys) + min(ys)) / 2 - H / 2
    T = 128   # 用 z+1 的圖磚（每張蓋 128 畫布像素），手機上比較清楚
    o = [f'<figure class="mk-map"><div class="mk-canvas" style="aspect-ratio:{W}/{H}">']
    for tx in range(math.floor(ox / T), math.floor((ox + W - 1) / T) + 1):
        for ty in range(math.floor(oy / T), math.floor((oy + H - 1) / T) + 1):
            o.append(f'<img src="https://tile.openstreetmap.org/{z + 1}/{tx}/{ty}.png" alt="" loading="lazy" decoding="async" '
                     f'style="left:{(tx * T - ox) / W * 100:.3f}%;top:{(ty * T - oy) / H * 100:.3f}%;'
                     f'width:{T / W * 100:.3f}%;height:{T / H * 100:.3f}%">')
    def pos(ll):
        x, y = merc(*ll, z)
        return f"left:{(x - ox) / W * 100:.2f}%;top:{(y - oy) / H * 100:.2f}%"
    for ll, text, q in landmarks:
        side = " left" if (merc(*ll, z)[0] - ox) / W > 0.6 else ""   # 靠右的參考點把文字放在左邊，免得被切掉
        o.append(f'<a class="mk-lm{side}" style="{pos(ll)}" href="{esc(gsearch_url(q))}" target="_blank" rel="noopener"><span>{esc(text)}</span></a>')
    for s in stores:
        if s.get("ll"):
            cls = " ".join(c for c in ("mk-pin", cat_cls(s), "near" if s is near else "") if c)
            o.append(f'<a class="{cls}" style="{pos(s["ll"])}" href="{esc(gsearch_url(s["q"]))}" target="_blank" rel="noopener" '
                     f'aria-label="{s["no"]} {esc(s["name"])}">{s["no"]}</a>')
    o.append(f'<a class="mk-pin hotel" style="{pos(anchor_ll)}" href="{esc(anchor_href)}" target="_blank" rel="noopener" '
             f'aria-label="飯店：{esc(anchor_name)}">宿</a>')
    mpp = 156543.03392 * math.cos(math.radians(anchor_ll[0])) / 2 ** z
    nice = max((n for n in (50, 100, 200, 250, 500, 1000, 2000) if n / mpp <= 130), default=50)
    label = f"{nice // 1000} km" if nice >= 1000 else f"{nice} m"
    o.append(f'<span class="mk-scale" style="width:{nice / mpp / W * 100:.2f}%">{label}</span>')
    o.append('<a class="mk-attr" href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">© OpenStreetMap</a>')
    cats = []
    for s in stores:
        if s.get("ll") and cat_cls(s) not in cats:
            cats.append(cat_cls(s))
    lg = "".join(f'　<span class="{("mk-lg " + c).strip()}">1</span>{CAT_LABEL[c]}' for c in cats)
    near_lg = '　<span class="mk-lg near">1</span>離飯店最近' if near and near.get("ll") else ""
    o.append(f'</div><figcaption><span class="mk-lg hotel">宿</span>飯店{lg}{near_lg}　點數字開 Google 地圖</figcaption></figure>')
    return "".join(o)

def market_map(m, stores, near):
    return pin_map(m["hotel_ll"], gmap(m["key"]), HOTEL_ZH[m["key"]], stores, near)

def store_cards(stores, near, origin_q):
    """店家卡片：名稱、地址、距離、營業時間、說明、地圖與路線連結。
    origin_q 為 None 時，路線從手機目前位置出發，距離改寫成「離飯店」。"""
    route_label = "從飯店的路線" if origin_q else "從目前位置的路線"
    o = ['<ol class="mk-list">']
    for s in stores:
        badge = '<span class="mk-near">離飯店最近</span>' if s is near else ""
        where = (dist_text(s["d"], "直線約" if origin_q else "離飯店直線約") if s.get("d") is not None
                 else s.get("where", ""))
        dest_mode = "walking" if s.get("d") is not None or s.get("near") else "driving"
        hours = s.get("hours_text") or week_text(s["hours"])
        note = f'<p class="mk-note">{rich(s["note"])}</p>' if s.get("note") else ""
        o.append(f'<li class="mk-store{" near" if s is near else ""}">'
                 f'<p class="mk-h"><span class="{mk_no_cls(s)}">{s["no"]}</span><b>{esc(s["name"])}</b><span class="mk-kind">{esc(s["kind"])}</span>{badge}</p>'
                 f'<p class="mk-meta">{esc(s["addr"])}</p>'
                 f'<p class="mk-meta mk-dist">{esc(where)}</p>'
                 f'<p class="mk-meta">{esc(hours)}</p>{note}'
                 f'<span class="h-links"><a class="h-map" href="{esc(gsearch_url(s["q"]))}" target="_blank" rel="noopener">地圖 ↗</a>'
                 f'<a class="h-map" href="{esc(gdir_url(origin_q, s["q"], dest_mode))}" target="_blank" rel="noopener">{route_label} ↗</a></span></li>')
    o.append('</ol>')
    if any(s.get("d") is not None for s in stores):
        o.append('<p class="fine">走路時間用直線距離估算，實際以 Google 地圖路線為準。</p>')
    return "".join(o)

def pl_sections(sections):
    o = []
    for head, items in sections:
        o.append(f'<section class="pl-s"><h2>{esc(head)}</h2><ul class="facts">')
        o.extend(f'<li><b>{rich(k)}</b><span>{rich(v)}</span></li>' for k, v in items)
        o.append('</ul></section>')
    return "".join(o)

def render_market(mid):
    m = MARKETS[mid]
    key, day, hll = m["key"], m["day"], m["hotel_ll"]
    stores = m["stores"]
    for i, s in enumerate(stores):
        s["no"] = i + 1
        s["d"] = dist_m(hll, s["ll"]) if hll and s.get("ll") else None
    near = next((s for s in stores if s.get("near")), None) or min(
        (s for s in stores if s["d"] is not None), key=lambda s: s["d"], default=None)
    stay = next(x for x in STAYS if x[4] == key)
    title = f'{m["city"]}・附近超市'
    o = [f'<article class="place market" id="{mid}" data-label="{esc(title)}" data-back="Day {day}">']
    o.append(f'<div class="readbar"><a class="back" href="#d{day}"><span aria-hidden="true">‹</span> <span class="back-l">Day {day}</span></a>'
             f'<span class="rb-title">{esc(title)}</span></div>')
    o.append('<div class="pl-in">')
    sunday = "奧地利・週日公休" if m["country"] == "at" else "捷克・週日照開"
    o.append(f'<header class="pl-h"><p class="eyebrow">附近超市・{esc(m["city"])}</p><h1>{esc(HOTEL_ZH[key])}附近</h1>'
             f'<p class="pl-og">{esc(stay[3])}</p><p class="badges"><span class="badge">住 {stay[0]}・{stay[1]}</span>'
             f'<span class="badge">{sunday}</span></p></header>')
    o.append(f'<p class="lede">{rich(m["lede"])}</p>')
    if hll:
        o.append(market_map(m, stores, near))
    o.append('<p class="extlinks">'
             f'<a href="{esc(gsearch_url("supermarket near " + HOTEL_Q[key]))}" target="_blank" rel="noopener">Google 地圖：飯店附近所有超市 ↗</a>'
             f'<a href="{esc(gmap(key))}" target="_blank" rel="noopener">飯店位置 ↗</a></p>')
    # 這幾天的營業時間
    head = "".join(f'<th>{d}（{WD[w]}）</th>' for d, w in m["dates"])
    rows = []
    for s in stores:
        cells = []
        for _, w in m["dates"]:
            h = s["hours"][w]
            cells.append('<td class="closed">公休</td>' if h is None else f'<td>{"<br>".join(esc(x).replace("–", "–<wbr>") for x in h.split("・"))}</td>')
        rows.append(f'<tr><th scope="row"><span class="{mk_no_cls(s)}">{s["no"]}</span>{esc(s["name"])}</th>{"".join(cells)}</tr>')
    o.append('<section class="pl-s"><h2>這幾天的營業時間</h2>'
             f'<div class="mk-hrs"><table><thead><tr><th>店家</th>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
             '<p class="fine">查自各店官網與商家目錄，臨時異動以現場為準。</p></section>')
    # 店家
    o.append('<section class="pl-s"><h2>店家</h2>' + store_cards(stores, near, HOTEL_Q[key]) + '</section>')
    if m.get("tips"):
        o.append(pl_sections([("小提醒", m["tips"])]))
    o.append(f'<p class="pl-foot"><a href="#d{day}">回到 Day {day} 行程</a>・<a href="#{HOTEL_PAGE[key]}">飯店介紹</a>・<a href="#m-markets">奧捷超市總覽</a></p>')
    o.append('</div></article>')
    return "".join(o)

def render_market_overview():
    v = OVERVIEW
    o = ['<article class="place market" id="m-markets" data-label="奧捷超市總覽" data-back="小提醒">']
    o.append('<div class="readbar"><a class="back" href="#tips"><span aria-hidden="true">‹</span> <span class="back-l">小提醒</span></a>'
             '<span class="rb-title">奧捷超市總覽</span></div>')
    o.append('<div class="pl-in">')
    o.append('<header class="pl-h"><p class="eyebrow">超市・便利商店</p><h1>奧捷超市總覽</h1>'
             '<p class="pl-og">Supermarkt・Supermarket</p><p class="badges"><span class="badge">奧地利・週日公休</span>'
             '<span class="badge">捷克・週日照開</span></p></header>')
    o.append(f'<p class="lede">{rich(v["lede"])}</p>')
    rows = "".join(
        f'<tr><td class="p-d">{"<br>".join(f"{d}（{WD[w]}）" for d, w in m["dates"])}</td>'
        f'<td><a class="xref" href="#{mid}">{esc(m["city"])}</a>・{esc(m["when"])}</td></tr>'
        for mid, m in MARKETS.items())
    o.append(f'<section class="pl-s"><h2>我們去的時候</h2><div class="plan"><table><tbody>{rows}</tbody></table></div>'
             '<p class="fine">點城市名稱，看飯店附近的超市、地圖和這幾天的營業時間。</p></section>')
    o.append(pl_sections([("奧地利的超市", v["austria"]), ("捷克的超市", v["czech"]),
                          ("便利商店和小店：適合去嗎？", v["conv"]), ("買東西小提醒", v["general"])]))
    links = "".join(f'<li><b><a class="xref" href="#{mid}">{esc(m["city"])}</a></b><span>{esc(HOTEL_ZH[m["key"]])}</span></li>'
                    for mid, m in MARKETS.items())
    o.append(f'<section class="pl-s"><h2>各飯店附近的超市</h2><ul class="facts">{links}</ul></section>')
    o.append('<p class="pl-foot"><a href="#tips">回到旅途小提醒</a>・<a href="#gifts">伴手禮清單</a></p>')
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
            ds = "・".join(f"D{n}" for n in place_days.get(pid, [])) or ("專題" if p.get("topic") else "參考")
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
    o.append('<h3 class="reg-h">超市就買得到</h3><ul class="gift-list">' + "".join(render_gift(g) for g in GIFTS_MARKET) + '</ul>')
    rows = "".join(f'<tr><td class="p-d"><a href="#d{n}">{esc(t)}</a></td><td>{rich(x)}</td></tr>' for t, n, x in SHOP_PLAN)
    o.append(f'<h3 class="reg-h">照天數買</h3><div class="plan"><table><tbody>{rows}</tbody></table></div>')
    li = "".join(f'<li><b>{esc(k)}</b><span>{rich(v)}</span></li>' for k, v in GIFT_TIPS)
    o.append(f'<h3 class="reg-h">帶回台灣要注意</h3><ul class="facts">{li}</ul>')
    o.append('</section>')
    return "".join(o)

def render_changes():
    """和原 PDF 的差異：內頁，從主頁最下面的連結打開。"""
    li = "".join(f'<li><b>{esc(k)}</b><span>{rich(v)}</span></li>' for k, v in CHANGES)
    return ('<article class="place" id="changes" data-label="和原 PDF 的差異" data-back="首頁">'
            '<div class="readbar"><a class="back" href="#top"><span aria-hidden="true">‹</span> <span class="back-l">首頁</span></a>'
            '<span class="rb-title">和原 PDF 的差異</span></div>'
            '<div class="pl-in"><header class="pl-h"><p class="eyebrow">行程更新</p><h1>和原 PDF 的差異</h1>'
            '<p class="pl-og">Changes</p></header>'
            '<p class="lede">依新版手冊照片、領隊通知和你補充的安排整理。行程頁顯示的都是最新內容，這裡只記錄改了什麼。</p>'
            f'<section class="pl-s"><ul class="facts">{li}</ul></section>'
            '<p class="pl-foot"><a href="#top">回到首頁</a></p></div></article>')

def render_tips():
    groups = "".join(
        f'<h3 class="reg-h">{esc(g)}</h3><ul class="facts">'
        + "".join(f'<li><b>{esc(k)}</b><span>{rich(v)}</span></li>' for k, v in items) + '</ul>'
        for g, items in TIPS)
    return (f'<section class="wrap block" id="tips" data-label="旅途小提醒"><h2 class="sec-h">旅途小提醒</h2>'
            f'<p class="sec-sub">整理自領隊的行前通知。行李與機上規定以華航公告和現場人員為準。</p>{groups}</section>')

def render_brief():
    return (
      '<div class="brief">'
      '<p class="brief-h">集合・航班</p>'
      '<dl class="brief-dl">'
      '<div><dt>集合</dt><dd><b>10/11（日）20:50</b>桃園國際機場第一航廈・中華航空團體櫃檯（10–11 號櫃檯後方）'
      f'・<a class="xref ext" href="{esc(MEET_MAP)}" target="_blank" rel="noopener">地圖 ↗</a></dd></div>'
      '<div><dt>去程</dt><dd><b>CI63　23:45 → 07:05+1</b>桃園 → 維也納・約 13 小時 20 分</dd></div>'
      '<div><dt>回程</dt><dd><b>CI68　10:40 → 05:05+1</b>10/21（三）布拉格 → 桃園・約 12 小時 25 分</dd></div>'
      '</dl></div>')

def render_rail():
    chips = "".join(
        f'<a class="chip" draggable="false" href="#d{d["n"]}" data-day="{d["n"]}"><b>{d["n"]}</b><span>{d["date"]}</span></a>' for d in DAYS)
    chips += ('<a class="chip txt" draggable="false" href="#guide">百科</a>'
              '<a class="chip txt" draggable="false" href="#gifts">伴手禮</a>'
              '<a class="chip txt" draggable="false" href="#tips">小提醒</a>')
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
  <p class="count" id="count">10/11（日）20:50 桃園機場集合</p>
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
{render_tips()}
<nav class="wrap foot-nav" aria-label="其他資訊"><a class="foot-link" href="#p-euro">從歐元看西方建築史 ›</a><a class="foot-link" href="#p-dining">歐洲用餐禮儀 ›</a><a class="foot-link" href="#changes">和原 PDF 的差異 ›</a></nav>
<footer class="foot wrap"><p>行程依旅行社 PDF 與新版手冊照片整理，並加入你補充的自由活動安排。景點介紹為一般公開的歷史與藝術資料；開放時間、票價與實際行程請以現場及領隊說明為準。</p></footer>
</main>
<div id="reader">
{"".join(render_place(pid) for pid in order + refs)}
{"".join(render_hotel(hid) for hid in HOTELS)}
{render_market_overview()}
{render_changes()}
{"".join(render_market(mid) for mid in MARKETS)}
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
<link rel="icon" type="image/png" sizes="192x192" href="favicon.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
'''
standalone = ('<!doctype html>\n<html lang="zh-Hant">\n<head>\n' + HEAD + STANDALONE_META
              + '</head>\n<body>\n' + BODY + '</body>\n</html>\n')
with open(OUT_INDEX, "w", encoding="utf-8") as f:
    f.write(standalone)
print("wrote", OUT_INDEX, len(standalone.encode("utf-8")), "bytes;", len(PLACES), "places")

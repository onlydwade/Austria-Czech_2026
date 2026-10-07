# -*- coding: utf-8 -*-
# 伴手禮門市介紹頁，與飯店頁共用版型（kind="shop"）。
from content_places import S, GMAP

SHOPS = {}

def SH(sid, **kw):
    kw["id"] = sid
    kw["kind"] = "shop"
    kw.setdefault("back", ("#gifts", "伴手禮"))
    kw.setdefault("foot", [("#gifts", "回到伴手禮清單")])
    SHOPS[sid] = kw

def M(q):
    return "[[" + GMAP(q) + "|地圖 ↗]]"

SH("s-manufaktura", zh="曼菲蘿", en="Manufaktura", eyebrow="伴手禮門市・捷克",
  badges=["捷克品牌・1991 年創立", "Day 6・8・8–10"],
  links=[("官方網站", "https://manufaktura.cz/"), ("門市列表", "https://manufaktura.cz/prodejny/")],
  lede="1991 年創立的捷克品牌，初衷是保存捷克與摩拉維亞的傳統手工藝，現在以天然保養品最有名。光是布拉格就有近 20 家門市，行程經過的城市幾乎都找得到。",
  sections=[
    S("你會經過的門市",
      ("布拉格舊城", "Melantrichova 17，舊城廣場往南走約 2 分鐘。・" + M("Manufaktura, Melantrichova 17, Praha 1")),
      ("布拉格 Palladium", "共和廣場的 Palladium 購物中心內，就在飯店隔壁。・" + M("Manufaktura, OC Palladium, Praha")),
      ("庫倫洛夫", "Latrán 44，城堡下方的 Latrán 街（Day 6）。・" + M("Manufaktura, Latrán 44, Český Krumlov")),
      ("卡羅維瓦利", "Stará Louka 375/2，溫泉區的主街（Day 8）。・" + M("Manufaktura, Stará Louka 375/2, Karlovy Vary")),
      ("布拉格機場", "第 1、第 2 航廈安檢後都有門市，早上 7:00 開門，10/21 登機前還能補貨。")),
    S("營業時間",
      "官網顯示上面幾家市區門市多是 10:00 開門，打烊時間各店不同。"),
    S("推薦商品",
      ("啤酒系列", "啤酒洗髮精和沐浴乳，最有捷克特色。"),
      ("葡萄酒系列", "以葡萄為主角的保養品。"),
      ("溫泉鹽系列", "卡羅維瓦利溫泉的泡澡鹽和保養品。"),
      ("手工藝", "傳統木製玩具和手工藝品，適合送小朋友。")),
    S("小提醒",
      "液體保養品每瓶超過 100 ml 要放託運；在機場安檢後的門市買的，可以直接帶上飛機。各店品項差不多，看到喜歡的先買，免得後面缺貨。"),
  ])

SH("s-botanicus", zh="菠丹妮", en="Botanicus", eyebrow="伴手禮門市・捷克",
  badges=["捷克品牌・1992 年創立", "Day 6・8・8–10"],
  links=[("官方網站", "https://botanicus.cz/en/"), ("門市列表", "https://botanicus.cz/en/shops/czech-republic")],
  lede="1992 年創立的捷克天然保養品牌，照老藥房的方式經營，在布拉格近郊 Ostrá 的自家有機農園種香草、花卉和蔬果，再拿來做保養品。",
  sections=[
    S("你會經過的門市",
      ("布拉格 Ungelt", "Týn 3（提恩教堂後方的 Ungelt 庭院），每天 10:00–19:00，電話 +420 702 207 096。・" + M("Botanicus Ungelt, Týn 3, Praha 1")),
      ("庫倫洛夫", "Kájovská 63（Day 6）。・" + M("Botanicus, Kájovská 63, Český Krumlov")),
      ("卡羅維瓦利", "I. P. Pavlova 8，Kolonáda 飯店內（Day 8）。・" + M("Botanicus, I. P. Pavlova 8, Karlovy Vary"))),
    S("推薦商品",
      ("玫瑰系列", "玫瑰精油、玫瑰水和玫瑰護手霜，是台灣旅客最常買的。"),
      ("手工香皂", "水果和花草造型的手工皂，包裝漂亮，適合分送。"),
      ("其他", "花草茶、糖漿、香料、精油和蜂蠟蠟燭。")),
    S("Ungelt 庭院",
      "布拉格店所在的 Ungelt 是中世紀外國商人繳稅、存貨的有圍牆庭院，也是提恩教堂名字的由來，見[[p-tyn|提恩教堂]]頁。現在庭院裡都是小店和咖啡館。"),
    S("小提醒",
      "玫瑰水和精油都算液體，超過 100 ml 要放託運。布拉格店離舊城廣場只要一兩分鐘，可以和天文鐘的整點表演排在一起逛。"),
  ])

SH("s-furst", zh="Fürst 莫札特巧克力老店", en="Café Konditorei Fürst", eyebrow="伴手禮門市・薩爾茲堡",
  badges=["1884 年開業", "Day 6"],
  links=[("官方網站", "https://www.original-mozartkugel.com/en/about-us"),
         ("薩爾茲堡觀光局介紹", "https://www.salzburg.info/en/dining-shopping/traditional-businesses/cafe-konditorei-fuerst")],
  lede="莫札特巧克力球的發明者。1890 年甜點師保羅・弗斯特在這裡做出第一顆，現在由第五代 Martin Fürst 經營，仍然全部手工製作。",
  sections=[
    S("門市",
      ("老店", "Brodgasse 13，老市場 Alter Markt 旁。這棟房子早在 1391 年的文獻裡就記載為宮廷麵包坊。・" + M("Café Konditorei Fürst, Brodgasse 13, Salzburg")),
      ("其他分店", "穀物小街 Getreidegasse、米拉貝爾廣場 Mirabellplatz（就在米拉貝爾花園旁）和 Ritzerbogen 拱廊。"),
      ("營業時間", "薩爾茲堡觀光局公布：週一至週三、週五、週六 9:30–18:00，週四 8:30–18:00，週日及假日 10:00–17:00（各分店可能不同）。10/16 是週五。")),
    S("Original 和超市版的差別",
      ("銀藍色 Original", "Fürst 的「Original Salzburger Mozartkugel」，手工製作，只在 Fürst 自家門市販售。"),
      ("紅金色 Mirabell", "量產品牌，超市和機場都有，便宜很多，適合大量分送。"),
      ("怎麼做的", "中心是開心果杏仁膏，外面包一層果仁糖，最後裹上黑巧克力。")),
    S("店裡還有",
      "薩赫蛋糕、多博斯蛋糕、艾斯特哈齊蛋糕，以及自家巧克力 Bach 方塊和 Wolf Dietrich 巧克力。老店座位很少（室內 13 席），想坐下來吃要碰運氣。"),
    S("小提醒",
      "手工巧克力怕熱，別放在大太陽下或靠近暖氣的地方。"),
  ])

SH("s-manner", zh="Manner 旗艦店", en="Manner Shop Stephansplatz", eyebrow="伴手禮門市・維也納",
  badges=["1890 年創立", "Day 2–3"],
  links=[("維也納觀光局介紹", "https://www.wien.info/en/see-do/shopping/old-city/manner-351530")],
  lede="粉紅色包裝的維也納國民零食。旗艦店就在聖史蒂芬大教堂前，剛好是創辦人 1890 年開第一家店的地方。",
  sections=[
    S("門市",
      ("地址", "Stephansplatz 7, 1010 Wien，聖史蒂芬大教堂前的廣場。・" + M("Manner Shop, Stephansplatz 7, Wien")),
      ("營業時間", "每天 10:00–21:00（旅遊網站資料，假日可能調整）。")),
    S("品牌故事",
      "1890 年約瑟夫・曼納在聖史蒂芬廣場開了第一家店，賣巧克力和無花果咖啡。1898 年推出至今仍是招牌的榛果威化餅。",
      "他取得了用聖史蒂芬大教堂當商標的權利，所以每一包粉紅色包裝上都印著大教堂。",
      "2004 年起在聖史蒂芬廣場開設旗艦店，概念是「回到起點」。"),
    S("推薦商品",
      ("經典榛果威化餅", "旗艦店的威化餅每天早上從工廠直送。"),
      ("復古鐵盒", "懷舊鐵盒裝，送禮比紙盒體面。"),
      ("其他", "莫札特巧克力球和 Ildefonso 牛軋糖方塊。")),
    S("小提醒",
      "旗艦店選擇最多，但同樣的經典款在超市 BILLA、SPAR 便宜不少，大量分送可以去超市買。"),
  ])

SH("s-sacher", zh="薩赫飯店", en="Hotel Sacher Wien・Original Sacher-Torte", eyebrow="伴手禮門市・維也納",
  badges=["1876 年開幕", "Day 3"],
  links=[("原版薩赫蛋糕介紹", "https://www.sacher.com/en/original-sacher-torte/"),
         ("常見問題（保存期限）", "https://shop.sacher.com/en/frequently-asked-questions")],
  lede="原版薩赫蛋糕的家。飯店就在國家歌劇院後面，咖啡館裡的 Sacher Shop 賣木盒包裝的整顆蛋糕和巧克力。",
  sections=[
    S("門市",
      ("地址", "Philharmonikerstraße 4, 1010 Wien，國家歌劇院後方。・" + M("Hotel Sacher Wien, Philharmonikerstraße 4")),
      ("怎麼去", "Day 3 下午從[[p-khm|藝術史博物館]]走過去約 10 分鐘。")),
    S("蛋糕的故事",
      "1832 年，梅特涅親王要宮廷廚房做一道新甜點，主廚剛好生病，16 歲的學徒法蘭茲・薩赫臨時做出了這款巧克力杏桃蛋糕。",
      "他的兒子愛德華在 1876 年開了薩赫飯店。後來薩赫飯店和甜點店 Demel 為了誰能叫「正宗」打了好幾年官司，最後薩赫取得「Original Sacher-Torte」的名稱，蛋糕上有圓形的巧克力封印。"),
    S("買回台灣",
      ("保存期限", "官方說明：Piccolo 小尺寸可放 14 天，1 號 16 天，2、3 號 18 天。"),
      ("保存方式", "放在原本的木盒和玻璃紙裡，存放在 16–18°C、避免陽光直射的地方。"),
      ("帶上飛機", "蛋糕不算液體，可以手提。10/13 買的話，回到台灣大約過了 9 天，小尺寸也來得及。")),
    S("小提醒",
      "咖啡館常排長隊；只買外帶蛋糕的話，可以直接到 Sacher Shop 的櫃檯結帳。"),
  ])

SH("s-moser", zh="莫瑟水晶", en="Moser", eyebrow="伴手禮門市・捷克",
  badges=["1857 年創立", "Day 8–10"],
  links=[("官方網站", "https://www.moser.com/en/"), ("全球門市", "https://www.moser.com/en/contacts/stores")],
  lede="1857 年在卡羅維瓦利創立的頂級水晶品牌，標語是「國王的玻璃」，至今仍以手工吹製和雕刻聞名。",
  sections=[
    S("門市",
      ("布拉格 Na Příkopě", "Na Příkopě 12，從飯店往火藥塔方向走約 5 分鐘，每天 10:00–19:00。・" + M("Moser, Na Příkopě 12, Praha")),
      ("布拉格舊城廣場", "舊城廣場上另有一家門市。"),
      ("卡羅維瓦利 普普大飯店", "Grandhotel Pupp 內的門市，就在溫泉區（Day 8）。"),
      ("卡羅維瓦利 工廠與博物館", "Kpt. Jaroše 46/19，在市區外圍，有超過 1,000 件展品的玻璃博物館、工廠參觀和門市。團體行程不一定會去。・" + M("Moser Visitor Centre, Kpt. Jaroše 46/19, Karlovy Vary"))),
    S("品牌故事",
      "創辦人路德維希・莫瑟原本是玻璃雕刻師。莫瑟水晶不含鉛，靠玻璃本身的配方和手工切割做出光澤。",
      "長年為許多王室和國家元首製作器皿，因此有「國王的玻璃」之稱。卡羅維瓦利的故事見[[p-karlovy|卡羅維瓦利]]頁。"),
    S("小提醒",
      "易碎品請手提上機，不要託運。單價高，記得索取退稅單，10/21 在布拉格機場辦理。"),
  ])

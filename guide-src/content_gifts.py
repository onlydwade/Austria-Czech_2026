# -*- coding: utf-8 -*-
# 伴手禮資料。where/desc/tip 可用 [[p-id|文字]] 連結；maps 是 (按鈕文字, Google 地圖搜尋字串)。

def G(name, orig, where, desc, tip="", maps=(), mine=False, shop=None):
    return dict(name=name, orig=orig, where=where, desc=desc, tip=tip, maps=list(maps), mine=mine, shop=shop)

GIFTS_MINE = [
  G("曼菲蘿", "Manufaktura",
    "布拉格舊城 Melantrichova 17（Day 8–10）・庫倫洛夫 Latrán 44（Day 6）・卡羅維瓦利 Stará Louka 2（Day 8）",
    "1991 年創立的捷克品牌，初衷是保存捷克與摩拉維亞的傳統手工藝。招牌是啤酒、葡萄酒和溫泉鹽系列的保養品，例如啤酒洗髮精、泡澡鹽和護手霜；店裡也賣傳統木製玩具和手工藝品。",
    "各分店品項差不多。Day 6 晚上在庫倫洛夫可以先逛，看好了再到布拉格補齊。",
    [("布拉格店", "Manufaktura, Melantrichova 17, Praha 1"),
     ("Palladium 店", "Manufaktura, OC Palladium, Praha"),
     ("庫倫洛夫店", "Manufaktura, Latrán 44, Český Krumlov"),
     ("卡羅維瓦利店", "Manufaktura, Stará Louka 375/2, Karlovy Vary")], mine=True, shop="s-manufaktura"),
  G("菠丹妮", "Botanicus",
    "布拉格 Týn 3（提恩教堂後方的 Ungelt 庭院，Day 8–10）・庫倫洛夫 Kájovská 63（Day 6）・卡羅維瓦利 I. P. Pavlova 8（Kolonáda 飯店內，Day 8）",
    "1992 年創立，照老藥房的方式經營，用自家有機農園種的香草和花卉做天然保養品。人氣商品是玫瑰系列（玫瑰精油、玫瑰水、護手霜）和手工香皂，也有花草茶和蠟燭。",
    "布拉格店就在[[p-tyn|提恩教堂]]後面，從飯店走過去不到 10 分鐘，可以和舊城廣場排在一起。",
    [("布拉格店", "Botanicus Ungelt, Týn 3, Praha 1"),
     ("庫倫洛夫店", "Botanicus, Kájovská 63, Český Krumlov"),
     ("卡羅維瓦利店", "Botanicus, I. P. Pavlova 8, Karlovy Vary")], mine=True, shop="s-botanicus"),
  G("布拉格天文鐘冰箱貼", "Pražský orloj magnet",
    "舊城廣場周邊的紀念品店（Day 8–10）",
    "最有布拉格代表性的小紀念品，有金屬、陶瓷、木頭等材質，有些指針還能轉動。看過真的[[p-orloj|天文鐘]]整點表演再買，更有紀念意義。",
    "廣場正前方的店通常最貴，往旁邊巷子走幾步價格就不一樣，買前比較一下。", mine=True),
  G("莫札特巧克力球", "Mozartkugel",
    "薩爾茲堡（Day 6）最齊全；維也納和各地超市也買得到",
    "中間是開心果杏仁膏，外面包一層果仁糖，最外層裹黑巧克力。1890 年由薩爾茲堡甜點師保羅・弗斯特發明，故事見[[p-sbg-altstadt|薩爾茲堡老城]]頁。",
    "銀藍色包裝的「Original Salzburger Mozartkugel」是 Fürst 自家手工做的，只在 Fürst 的店買得到，老店在 Brodgasse 13。紅金色包裝的 Mirabell 是量產品牌，超市就有，便宜很多，適合大量分送。",
    [("Fürst 老店", "Café Konditorei Fürst, Brodgasse 13, Salzburg")], mine=True, shop="s-furst"),
]

GIFTS_AT = [
  G("Manner 威化餅", "Manner Schnitten",
    "維也納（Day 2–3）",
    "粉紅色包裝的榛果威化餅，維也納人從小吃到大的國民零食，包裝上的圖案就是聖史蒂芬大教堂。",
    "大教堂旁的 Manner 旗艦店有各種口味和禮盒；超市 BILLA、SPAR 價格更便宜。",
    [("Manner 旗艦店", "Manner Shop, Stephansplatz 7, Wien")], shop="s-manner"),
  G("薩赫蛋糕", "Original Sacher-Torte",
    "維也納（Day 3 自由活動）",
    "裝在木盒裡的原版薩赫巧克力蛋糕，送禮很體面。薩赫飯店就在國家歌劇院後面，從藝術史博物館走過去不遠。",
    "保存期限比一般巧克力短，買前看包裝上的日期，回台後早點吃。",
    [("薩赫飯店", "Hotel Sacher Wien, Philharmonikerstraße 4")], shop="s-sacher"),
  G("杏桃果醬、杏桃酒", "Wachauer Marille",
    "瓦豪一帶（Day 2）、各地超市",
    "瓦豪河谷的杏桃受歐盟原產地保護，做成果醬、杏桃白蘭地和利口酒，見[[p-wachau|瓦豪河谷]]頁。",
    "果醬和酒都算液體，要放託運行李。"),
  G("哈斯達特鹽", "Hallstatt Salz",
    "哈斯達特、鹽礦商店（Day 4–5）",
    "來自七千年老鹽礦的鹽，有加香草的調味鹽、小罐裝和布袋裝，輕又便宜，很適合分送。見[[p-salzwelten|鹽礦]]頁。"),
]

GIFTS_CZ = [
  G("溫泉薄餅", "Lázeňské oplatky",
    "卡羅維瓦利（Day 8）；超市也有盒裝",
    "大片圓形薄脆餅，夾榛果、巧克力、香草等內餡，是卡羅維瓦利的代表點心，已列入慢食基金會的「美味方舟」名錄，見[[p-karlovy|卡羅維瓦利]]頁。",
    "柱廊一帶到處都有薄餅攤和店家，現烤的在當地吃，帶回台灣的買盒裝。地圖會列出溫泉區的薄餅店，挑離你最近的就好。",
    [("溫泉薄餅店家", "Lázeňské oplatky, Karlovy Vary")]),
  G("貝赫洛夫卡藥草酒", "Becherovka",
    "卡羅維瓦利（Day 8）、超市",
    "1807 年在卡羅維瓦利調配出來的草藥酒，被稱為「第 13 道溫泉」，捷克人當餐前或餐後酒。",
    "要放託運行李；入境台灣酒類免稅額是 1 公升。"),
  G("波希米亞水晶、莫瑟", "Bohemian crystal・Moser",
    "卡羅維瓦利莫瑟工廠與門市（Day 8）、布拉格門市",
    "捷克玻璃工藝歷史悠久，莫瑟是 1857 年創立的頂級水晶品牌，被稱為「國王的玻璃」。",
    "易碎品請手提上機；單價高的記得辦退稅。",
    [("莫瑟布拉格門市", "Moser, Na Příkopě 12, Praha")], shop="s-moser"),
  G("捷克石榴石首飾", "Český granát",
    "布拉格（Day 8–10）",
    "波希米亞出產的深紅色石榴石，19 世紀在歐洲非常流行，是很有捷克特色的首飾。",
    "選有產地證書的店，例如石榴石合作社 Granát Turnov 的門市，避免買到玻璃仿品。"),
  G("小鼴鼠玩偶", "Krtek",
    "布拉格（Day 8–10）",
    "捷克動畫家米勒 1956 年創造的卡通角色，在台灣也有很多人認得，玩偶、繪本和文具都有。"),
  G("提線木偶", "Marionety",
    "布拉格（Day 8–10）",
    "捷克的木偶戲傳統已列入聯合國教科文組織非物質文化遺產。手工木偶從小型吊飾到大型收藏品都有，女巫、騎士和莫札特造型最常見。"),
]

# 照天數的購物路線：(天數文字, 錨點日, 可以買)
SHOP_PLAN = [
  ("Day 2–3", 2, "維也納：Manner 威化餅、薩赫蛋糕、杏桃果醬、超市版莫札特巧克力"),
  ("Day 4–5", 4, "湖區：哈斯達特鹽"),
  ("Day 6", 6, "薩爾茲堡：Fürst 莫札特巧克力。晚上庫倫洛夫：曼菲蘿、菠丹妮"),
  ("Day 7", 7, "巴德傑維契：Budvar 啤酒（瓶裝重，要託運）"),
  ("Day 8", 8, "卡羅維瓦利：溫泉薄餅、貝赫洛夫卡、莫瑟水晶、曼菲蘿、菠丹妮"),
  ("Day 8–10", 9, "布拉格：菠丹妮、曼菲蘿、天文鐘冰箱貼、石榴石、小鼴鼠、木偶"),
  ("Day 11", 11, "布拉格機場：辦理退稅海關蓋章"),
]

GIFT_TIPS = [
  ("超市補貨", "共和廣場旁的 Palladium 購物中心地下有 Albert 超市，就在飯店隔壁，買巧克力、薄餅、零食最方便。・[[https://www.google.com/maps/search/?api=1&query=Albert%2C+Palladium%2C+N%C3%A1m%C4%9Bst%C3%AD+Republiky%2C+Praha|地圖 ↗]]"),
  ("液體", "酒、果醬、保養品液體每瓶超過 100 ml 要放託運，用衣服包好防破。"),
  ("酒類", "年滿 20 歲入境台灣，酒類免稅 1 公升，超過要申報。"),
  ("肉製品", "香腸、火腿、肉乾等肉製品一律不要帶回台灣，入境會被重罰。"),
  ("退稅", "同店同日消費滿額（奧地利 €75.01、捷克 2,001 CZK）可以退稅。在奧地利買的也一起在 10/21 布拉格機場辦海關蓋章，蓋章前商品別放進託運行李。"),
]

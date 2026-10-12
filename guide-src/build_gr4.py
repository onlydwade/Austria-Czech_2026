# -*- coding: utf-8 -*-
"""RICOH GR IV 拍照筆記：獨立頁面，寫到 GR4/index.html。

網址 https://onlydwade.github.io/Austria-Czech_2026/GR4/ ，行程主頁不放連結。
相機規格查自 RICOH 官網、DPReview、Amateur Photographer 等評測；濾鏡配方是建議起點，可以自己再調。
"""
import html, os, re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "GR4", "index.html")
SITE = "../"   # 回到行程網頁

def esc(t):
    return html.escape(t, quote=True)

LINK_RE = re.compile(r"\[\[([^|\]]+)\|([^\]]+)\]\]")

def rich(t):
    """[[網址或 #錨點|文字]]；行程主頁的錨點寫成 ../#d4。"""
    t = html.escape(t, quote=False)
    def rep(m):
        href, label = m.group(1), m.group(2)
        ext = href.startswith("http")
        attrs = ' target="_blank" rel="noopener"' if ext else ""
        return f'<a href="{esc(href)}"{attrs}>{label}{" ↗" if ext else ""}</a>'
    return LINK_RE.sub(rep, t)

# ───────────────────────── 內容 ─────────────────────────
TOP3 = [
    ("大部分時間用 Av 模式", "你決定光圈，相機決定快門。只要記住：拍人和食物用 F2.8，拍風景建築用 F8。"),
    ("畫面太亮太暗就按 ± 鍵", "曝光補償一次調 0.3。天空、白牆、雪地拍起來偏暗就往 +；夜景、深色背景偏亮就往 −。"),
    ("檔案存 RAW＋JPEG", "濾鏡效果只套在 JPEG，RAW 不受影響。JPEG 直接分享，RAW 留著之後想換濾鏡還能重調。"),
]

SPECS = [
    ("鏡頭", "28mm 等效廣角定焦，光圈 F2.8–F16。不能變焦，想拍大一點就走近。"),
    ("感光元件", "APS-C、約 2,574 萬畫素，ISO 100–204800。"),
    ("防手震", "機身 5 軸防手震，拍靜止的東西可以用比較慢的快門。"),
    ("內建 ND 濾鏡", "減 2 級光線。設成自動，大太陽下用 F2.8 時相機會自己開。"),
    ("微距", "最近可以對焦到 6 公分，拍食物細節很好用。"),
    ("快拍對焦 Snap", "預先設好對焦距離（0.3、1、1.5、2、2.5、3.5、5 公尺、無限遠），按下快門就拍，不用等對焦。"),
    ("裁切 35mm／50mm", "畫面會變窄，畫素降到約 1,630 萬／820 萬，而且拍完不能還原。這趟建議少用，靠走近或事後裁切。"),
    ("U1–U3", "模式轉盤上的自訂模式，可以把整組設定存起來，一轉就切換。建議設定見下方。"),
]

APERTURE = [
    ("F2.8", "人像、夜景、室內", "背景最模糊、進光最多。28mm 是廣角，背景本來就不容易糊，要靠近主體、讓背景離遠一點。"),
    ("F4", "美食", "盤子前後都比較清楚，背景還是有點柔。"),
    ("F5.6", "街拍", "配合快拍對焦 2.5 公尺，走路時舉起來就拍。"),
    ("F8–F11", "風景、建築、大合照", "從前到後都清楚。F11 以上畫質反而會變軟，不用再縮。"),
]

SHUTTER = [
    ("1/500 秒以上", "遊船、巴士窗外、電車、跑跳的人"),
    ("1/125 秒", "走動的人、街景"),
    ("1/60 秒", "站著不動的人"),
    ("1/15–1/8 秒", "夜景、室內的靜物，靠防手震手持；身體靠牆或欄杆更穩"),
]

ISO = [
    ("100–400", "晴天戶外"),
    ("800–1600", "陰天、室內、黃昏"),
    ("3200–6400", "夜景、昏暗的室內和鹽礦"),
    ("ISO 自動", "上限設 6400，相機會在範圍內自己調，最省事。"),
]

MODES = [
    ("Av 光圈優先（主力）", [
        "你決定光圈（F 值），相機決定快門速度，用來控制背景模糊或清楚。",
        "拍人像、美食、靜物特寫：用大光圈（如 F2.8）讓背景變模糊，凸顯主體。",
        "拍風景、建築、大合照：用小光圈（如 F8、F11）讓從前到後都清楚。",
        "景深參考：街拍 F5.6、人像 F2.8、食物 F4.0。這是最常用的模式。",
        "要注意畫面上的快門速度：拍人時低於 1/60，就把 ISO 調高。",
    ]),
    ("Tv 快門優先", ["你決定快門速度，相機決定光圈。遊船、車窗外、電車上用 1/500，畫面才不會糊。"]),
    ("P 程式自動", ["相機全部自己決定，臨時要拍、來不及想的時候用。"]),
    ("M 手動", ["光圈和快門都自己設。夜景想要固定效果時再用，這趟不一定需要。"]),
]

# 濾鏡（影像風格 Image Control）配方：-4 到 +4，0 是預設。值是建議起點。
PARAMS = ["飽和度 Saturation", "色相 Hue", "高/低調 High/Low Key", "對比 Contrast", "對比（亮部）Highlight",
          "對比（暗部）Shadow", "銳利度 Sharpness", "清晰度 Clarity", "顆粒 Grain"]
RECIPES = [
    dict(name="標準", en="Standard", color="#4C5668",
         good="人像、室內、需要真實顏色的時候。最不會出錯。",
         vals=["0", "0", "0", "0", "−1", "0", "+1", "0", "關"],
         note="亮部對比 −1 讓天空和白牆比較不會過曝。拍室內建築用 [[#umodes|U3]] 的加強版。"),
    dict(name="正片", en="Positive Film", color="#2F6EA3",
         good="晴天的湖景、藍天、建築、色彩豐富的食物。",
         vals=["+2", "0", "+1", "+1", "−2", "0", "+1", "0", "關"],
         note="顏色鮮豔、反差高。[[#umodes|U1]] 用的是更有底片感的 EktaSlide 參數；Travelog 見 [[#rr|Ricoh Recipes]]。"),
    dict(name="負片", en="Negative Film", color="#A07A0B",
         good="人像、陰天、老城街景，顏色柔和、膚色好看。",
         vals=["−1", "0", "+1", "0", "−2", "+1", "0", "0", "小・弱"],
         note="偏淡、偏懷舊。[[#umodes|U2]] 用的是濃一點、有底片感的 Pro Color 參數。想要高反差的版本，可以參考 RICOH 官方 GR Blog 的自訂負片（飽和度 −2、對比 +3、亮部對比 +4、暗部對比 −4）。"
              "・[[https://www.grblog.jp/en/article/7151/|官方 GR Blog]]"),
    dict(name="電影（黃）", en="Cinema (Yellow)", color="#C8661A",
         good="黃昏、夜景、咖啡館、布拉格的暖色街燈。",
         vals=["0", "0", "−1", "+1", "−2", "−1", "0", "0", "小・弱"],
         note="整體偏黃、有電影感。在很黃的燈光下會太橘，那時改用標準。"),
    dict(name="電影（綠）", en="Cinema (Green)", color="#3F8433",
         good="陰天或起霧的湖區、森林、雨天的老城。",
         vals=["−1", "0", "0", "0", "−1", "−1", "0", "0", "小・弱"],
         note="暗部偏綠、氣氛冷靜。晴天的藍天用它會有點灰，那時改用正片。"),
]

# Ricoh Recipes（ricohrecipes.com，Ritchie Roesch）GR IV 入門系列 Starter Collection 的彩色配方。
# 數值照網站抄錄；kv 是兩欄小表，wide 是整列。
RR_RECIPES = [
    dict(name="EktaSlide", base="正片", color="#2F6EA3", pick="風景、建築首選",
         why="模仿柯達 Ektachrome 正片：藍天和湖水乾淨、反差高。白平衡用自動，換到室內也不容易偏色，最萬用。",
         kv=[("飽和度", "+2"), ("色相", "+2"), ("高/低調", "+2"), ("對比", "+4"), ("亮部對比", "−4"), ("暗部對比", "0"),
             ("銳利度", "+1"), ("暗角", "0"), ("清晰度", "+1"), ("顆粒", "大小 1・強度 1"), ("亮部修正", "開"), ("暗部修正", "強")],
         wide=[("白平衡", "自動（白色優先）・補償 G6、A8"), ("其他", "周邊光量補正 開・高 ISO 降噪 關"), ("曝光補償", "0 到 +2/3")]),
    dict(name="Travelog", base="正片", color="#2F6EA3", pick="秋天湖區、旅行紀錄",
         why="名字就是「旅行日誌」。顏色很飽和、整體偏暖，十月的黃葉和木屋很好看。白平衡固定陰天，室內黃燈下會更橘。",
         kv=[("飽和度", "+4"), ("色相", "−1"), ("高/低調", "+3"), ("對比", "0"), ("亮部對比", "−3"), ("暗部對比", "+1"),
             ("銳利度", "−1"), ("暗角", "0"), ("清晰度", "−2"), ("顆粒", "大小 2・強度 2"), ("亮部修正", "開"), ("暗部修正", "中")],
         wide=[("白平衡", "陰天・補償 G8、B9"), ("其他", "周邊光量補正 開"), ("曝光補償", "−1/3 到 +1/3")]),
    dict(name="Pro Color", base="負片", color="#A07A0B", pick="人像、街景、美食",
         why="負片底，顏色濃但膚色自然，暗部比較亮，老城街景有底片感。白平衡固定日光，室內黃燈下會偏暖。",
         kv=[("飽和度", "+4"), ("色相", "−2"), ("高/低調", "+3"), ("對比", "+3"), ("亮部對比", "−2"), ("暗部對比", "+4"),
             ("銳利度", "−1"), ("暗角", "0"), ("清晰度", "−1"), ("顆粒", "大小 2・強度 1"), ("亮部修正", "開"), ("暗部修正", "強")],
         wide=[("白平衡", "日光・補償 G5、A10"), ("曝光補償", "−1/3 到 +1/3")]),
    dict(name="Lomo Color", base="電影（黃）", color="#C8661A", pick="黃昏、夜景、想玩的時候",
         why="LOMO 相機的感覺：顏色很濃、四角稍暗、偏暖。效果強，挑幾個場景玩就好，不適合整趟都用。",
         kv=[("飽和度", "+4"), ("色相", "+3"), ("高/低調", "+4"), ("對比", "+3"), ("亮部對比", "−4"), ("暗部對比", "+4"),
             ("銳利度", "−2"), ("暗角", "−1"), ("清晰度", "−2"), ("色調", "3"), ("顆粒", "大小 1・強度 3"), ("暗部修正", "中")],
         wide=[("白平衡", "陰影・補償 M4、B10"), ("其他", "周邊光量補正 開・高 ISO 降噪 關"), ("曝光補償", "−2/3 到 −1/3")]),
    dict(name="Expired Negative", base="電影（綠）", color="#3F8433", pick="想要懷舊、過期底片感",
         why="模仿過期或保存不好的底片：低對比、顆粒粗、偏色重。很有個性，但顏色不真實，當作偶爾玩的效果。",
         kv=[("飽和度", "−1"), ("色相", "−1"), ("對比", "−3"), ("亮部對比", "+4"), ("暗部對比", "+4"), ("銳利度", "−2"),
             ("清晰度", "−3"), ("色調", "3"), ("顆粒", "大小 3・強度 3")],
         wide=[("白平衡", "色溫 9700K・補償 G4、B14"), ("沒列的", "高/低調、暗角等項目見網站"), ("曝光補償", "+2/3 到 +1")]),
]

# 風景、建築、教堂：(場景, 首選, 備選, 重點)
SCENE_FILTERS = [
    ("風景・晴天", "EktaSlide 或正片", "Travelog（想暖一點，拍黃葉）", "藍天湖水最漂亮。曝光 −0.3 保住天空。"),
    ("風景・陰天、起霧", "電影（綠）", "負片", "陰天用正片會灰灰的；電影（綠）把灰變成氣氛。"),
    ("建築外觀・白天", "EktaSlide 或正片", "Pro Color（老城的底片感）", "清晰度 +1 讓雕刻和屋瓦更清楚。F8，相機拿正。"),
    ("建築・黃昏、夜景", "電影（黃）", "Lomo Color", "暖色街燈很有電影感。曝光 −0.7，燈才不會過曝。"),
    ("教堂、宮殿室內", "標準＋自動白平衡", "EktaSlide（也是自動白平衡）；想要暖色氣氛用電影（黃）",
     "金色裝飾和壁畫要顏色準，用標準最穩。Travelog、Pro Color、Lomo Color 的白平衡是固定的，在黃色燈光下會很橘，進室內前切回自動白平衡。"),
    ("彩繪玻璃", "正片", "EktaSlide", "對著亮的玻璃測光，曝光 −0.7 到 −1，顏色才飽滿。"),
]

# U1–U3：shot 是拍攝設定，kv 是影像風格參數（兩欄），wide 是白平衡等整列設定。
USER_MODES = [
    dict(key="U1", name="正片", use="風景、建築外觀、晴天", color="#2F6EA3",
         shot=[("模式", "Av"), ("光圈", "F8"), ("ISO 自動", "100–1600"), ("曝光補償", "0 到 −0.3"), ("測光", "多區"), ("ND", "自動"), ("檔案", "RAW＋JPEG")],
         kv=[("飽和度", "+2"), ("色相", "+2"), ("高/低調", "+2"), ("對比", "+4"), ("亮部對比", "−4"), ("暗部對比", "0"),
             ("銳利度", "+1"), ("暗角", "0"), ("清晰度", "+1"), ("顆粒", "小・弱")],
         wide=[("白平衡", "自動（白色優先）・補償 G6、A8"), ("修正", "亮部修正 開・暗部修正 強・周邊光量補正 開")],
         note="參數就是 Ricoh Recipes 的 EktaSlide：藍天湖水乾淨、反差高，白平衡自動，換到室內也不容易偏色。想要暖一點、拍黃葉，改用 [[#rr|Travelog]] 的參數。"),
    dict(key="U2", name="負片", use="人像、街景、美食", color="#A07A0B",
         shot=[("模式", "Av"), ("光圈", "F2.8"), ("ISO 自動", "100–3200"), ("最低快門", "1/125"), ("曝光補償", "+0.3"), ("測光", "多區"), ("檔案", "RAW＋JPEG")],
         kv=[("飽和度", "+4"), ("色相", "−2"), ("高/低調", "+3"), ("對比", "+3"), ("亮部對比", "−2"), ("暗部對比", "+4"),
             ("銳利度", "−1"), ("暗角", "0"), ("清晰度", "−1"), ("顆粒", "大小 2・強度 1")],
         wide=[("白平衡", "自動（白色優先）"), ("修正", "亮部修正 開・暗部修正 強")],
         note="參數來自 Ricoh Recipes 的 Pro Color，只把白平衡從「日光」改成自動：戶外看起來差不多，進餐廳黃燈下也不會變橘。晴天戶外想要更有底片味，可以改回日光、補償 G5、A10。街拍時光圈轉到 F5.6。"),
    dict(key="U3", name="室內建築", use="教堂、宮殿、圖書館、鹽礦", color="#4C5668",
         shot=[("模式", "Av"), ("光圈", "F4"), ("ISO 自動", "100–6400"), ("最低快門", "1/30"), ("曝光補償", "−0.3"), ("測光", "多區"), ("檔案", "RAW＋JPEG")],
         kv=[("飽和度", "+1"), ("色相", "0"), ("高/低調", "0"), ("對比", "0"), ("亮部對比", "−2"), ("暗部對比", "−1"),
             ("銳利度", "+1"), ("暗角", "0"), ("清晰度", "+1"), ("顆粒", "關")],
         wide=[("影像風格", "標準"), ("白平衡", "自動（白色優先）；想留暖色氣氛改「自動（暖色優先）」"),
               ("修正", "亮部修正 開・暗部修正 中・周邊光量補正 開"), ("畫面", "打開電子水準儀")],
         note="F4 對焦在 4 公尺左右，大約 2 公尺到最遠都清楚，又比 F8 亮兩級。亮部對比 −2、曝光 −0.3 保住窗戶和彩繪玻璃；暗部對比 −1 讓暗角落亮一點；清晰度 +1 讓雕刻和壁畫更清楚。"
              "靠防手震，1/30 秒手持拍靜止的建築沒問題；拍人時把最低快門改成 1/60。"),
]
# 測光：GR IV 有多區、中央重點、點、亮部優先四種。
METERING = [
    ("多區", "整個畫面一起判斷，大部分時候都用它。U1–U3 都設多區。"),
    ("亮部優先", "優先保住最亮的地方，暗的地方會比較暗。拍彩色玻璃、亮窗、夕陽、夜景燈光時切過去，曝光補償先改回 0 再看。"),
    ("點測光", "只看畫面中間一小塊。逆光拍人時，把臉放在畫面中間拍；嫌麻煩就維持多區、曝光 +0.7。"),
    ("中央重點", "以中間為主、四周為輔，這趟用不太到。"),
]
METER_TIP = "在顯示設定打開「亮部警告」：過曝的地方會閃，看到閃就把曝光往 − 調。"

U_TIPS = [
    "相機拿正：看電子水準儀，讓畫面水平，柱子和牆才不會歪。28mm 往上仰拍會讓建築往後倒，退後一點、相機拿平再拍。",
    "站在中央走道拍對稱構圖，教堂和圖書館最好看。",
    "不要開閃光燈；彌撒進行中不要拍。",
    "晚上拍建築也可以用 U3，影像風格改成電影（黃）、曝光改 −0.7。",
]

# 這趟的場景：(標題, 什麼時候, 設定, 濾鏡, 小提醒)
SCENES = [
    ("湖景：哈斯達特、沃夫岡湖", "[[../#d4|Day 4]]–[[../#d5|5]]",
     "U1・曝光 −0.3（保住天空和湖面亮部）",
     "晴天 EktaSlide 或正片；拍黃葉用 Travelog；陰天或起霧用電影（綠）",
     "壓低一點拍，湖面倒影會比較完整。哈斯達特是居民的家，不要闖進私人庭院或碼頭。"),
    ("鹽礦", "[[../#d5|Day 5]]",
     "U3・最低快門改 1/60（人一直在走）",
     "標準＋自動白平衡（礦裡是黃色燈光）",
     "礦裡很暗，人又一直在走。拍人時讓對方停一下。礦工滑梯會自動測速拍照，滑的時候把相機收好。"),
    ("建築：維也納、薩爾茲堡、布拉格城堡", "[[../#d2|Day 2]]、[[../#d3|3]]、[[../#d6|6]]、[[../#d9|9]]",
     "U1",
     "EktaSlide 或正片；陰天用負片或 Pro Color",
     "28mm 很廣，靠太近拍高樓會往後倒。退後幾步、相機拿正，或把建築放在畫面中間。梅爾克修道院兩翼之間的觀景平台可以拍多瑙河。"),
    ("教堂、宮殿、圖書館室內", "整趟",
     "U3",
     "標準＋自動白平衡；想要暖色氣氛用電影（黃）",
     "[[../#d3|熊布朗宮]]室內一般可以拍，但不能開閃光燈、不能用腳架和自拍棒，人多時工作人員可能請你停拍。[[../#d2|梅爾克修道院]]室內（圖書館、博物館）很多遊客回報不能拍，以現場標示為準。音樂會演出時不要拍，散場後再拍音樂廳。"),
    ("老城街景：庫倫洛夫、布拉格", "[[../#d6|Day 6]]、[[../#d8|8]]–[[../#d10|10]]",
     "U2，光圈改 F5.6・快拍對焦 2.5 公尺",
     "Pro Color 或負片；晴天也可以用 EktaSlide",
     "快拍對焦不用等對焦，走路時看到畫面就拍。庫倫洛夫可以從城堡往下拍河灣和紅屋頂。"),
    ("夜景：查理大橋、布拉格城堡、舊城廣場", "[[../#d8|Day 8]]–[[../#d10|10]] 晚上",
     "U3，影像風格改電影（黃）・曝光 −0.7・靜物快門可以到 1/15",
     "電影（黃）；想玩濃一點用 Lomo Color",
     "曝光往 − 調，燈光才不會過曝成一片白。畫面裡有人時，快門至少 1/60。"),
    ("遊船、巴士窗外、電車", "[[../#d10|Day 10]]，以及每天的車程",
     "Tv 1/500・ISO 自動",
     "EktaSlide 或正片",
     "鏡頭貼近玻璃、避開反光；穿深色衣服反光更少。"),
    ("人像：旅伴、合照", "整趟",
     "半身 U2；合照 U2 光圈改 F5.6–F8・逆光時曝光 +0.7",
     "戶外 Pro Color 或負片；室內用標準",
     "靠近拍半身，讓背景離人遠一點。合照時 28mm 很好用，站近一點就塞得下全團。"),
    ("美食：米其林午餐、帝國咖啡館、煙囪捲、冰淇淋", "[[../#d3|Day 3]]、[[../#d9|9]]、[[../#d10|10]]",
     "U2（F2.8–F4）・曝光 +0.3 到 +0.7・近拍用微距（最近 6 公分）",
     "正片或 EktaSlide（顏色鮮豔）、標準（顏色真實）。餐廳黃燈下不要用固定白平衡的配方",
     "坐靠窗的位置用自然光，斜 45 度或正上方拍。不要開閃光燈，也不要擋到別桌。"),
]

CHECKLIST = [
    ("時間", "把相機時間改成歐洲時間（比台灣慢 6 小時），照片日期才對。"),
    ("電池", "帶備用電池；行動電源只能隨身帶，飛機上禁止使用和充電。"),
    ("記憶卡", "清出空間；RAW＋JPEG 很佔容量，可以多帶一張卡。"),
    ("鏡頭", "出門前擦乾淨；放進有軟墊的包或專用套，鏡頭表面不要直接碰鑰匙等硬物。"),
    ("防扒", "相機掛在身上或手腕，不要放在桌上或後背包外層。"),
]

SOURCES = [
    ("RICOH GR IV 官方頁面", "https://us.ricoh-imaging.com/product/gr-iv/"),
    ("RICOH GR IV 使用手冊（PDF）", "https://www.ricoh-imaging.co.jp/resources/english/support/man-pdf/gr-4_en.pdf"),
    ("DPReview GR IV 評測", "https://www.dpreview.com/reviews/ricoh-gr-iv-in-depth-review/"),
    ("Amateur Photographer GR IV 評測", "https://amateurphotographer.com/review/ricoh-gr-iv-review/"),
    ("Ricoh Recipes：GR IV 第一個配方", "https://ricohrecipes.com/2025/10/24/my-ricoh-gr-iv-arrived-first-recipe-test/"),
    ("Ricoh Recipes：GR IV 入門系列（Starter Collection）", "https://ricohrecipes.com/the-starter-collection/"),
    ("Ricoh Recipes：GR IV 配方總覽", "https://ricohrecipes.com/ricoh-gr-iv-recipes/"),
    ("Ricoh Recipes App", "https://ricohrecipes.com/ricoh-recipes-app/"),
    ("RICOH GR Blog：自訂負片", "https://www.grblog.jp/en/article/7151/"),
    ("熊布朗宮參觀常見問題（拍照規定）", "https://www.schoenbrunn.at/en/visitor-information/faq"),
]

# ───────────────────────── 版面 ─────────────────────────
CSS = """
:root{--paper:#F1F3F2;--sheet:#FFFFFF;--ink:#18202C;--ink2:#4C5668;--rule:#D3D9DE;--accent:#962437;--river:#1E6878;
  --f-head:"Noto Serif TC","Songti TC","PMingLiU",serif;--f-body:"Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--paper:#10151C;--sheet:#18202A;--ink:#E8ECF1;--ink2:#A3ADBB;--rule:#2B3542;--accent:#EE8E9C;--river:#6CC0CF;color-scheme:dark}}
:root[data-theme="dark"]{--paper:#10151C;--sheet:#18202A;--ink:#E8ECF1;--ink2:#A3ADBB;--rule:#2B3542;--accent:#EE8E9C;--river:#6CC0CF;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--f-body);font-size:16px;line-height:1.75;-webkit-text-size-adjust:100%}
a{color:var(--accent)}
h1,h2,h3,p{margin:0}
.wrap{max-width:720px;margin-inline:auto;padding:0 16px}
header.top{padding:28px 16px 18px;max-width:720px;margin-inline:auto;display:grid;gap:6px}
.eyebrow{font-size:.8rem;letter-spacing:.08em;color:var(--ink2)}
h1{font-family:var(--f-head);font-size:clamp(1.9rem,8vw,2.5rem);line-height:1.25}
.sub{color:var(--ink2)}
nav.toc{position:sticky;top:0;z-index:5;background:var(--paper);border-bottom:1px solid var(--rule)}
nav.toc .in{max-width:720px;margin-inline:auto;display:flex;gap:6px;overflow-x:auto;padding:8px 16px;scrollbar-width:none}
nav.toc .in::-webkit-scrollbar{display:none}
nav.toc a{flex:0 0 auto;padding:4px 12px;border:1px solid var(--rule);border-radius:99px;background:var(--sheet);color:var(--ink);text-decoration:none;font-size:.85rem}
section{padding:26px 0 6px;scroll-margin-top:56px}
h2{font-family:var(--f-head);font-size:1.3rem;color:var(--accent);margin-bottom:10px}
.lead{color:var(--ink2);margin-bottom:12px}
.cards{display:grid;gap:10px}
.card{padding:12px 14px;border:1px solid var(--rule);border-radius:10px;background:var(--sheet)}
.card h3{font-size:1rem;margin-bottom:4px}
.card p{font-size:.93rem}
.card p+p{margin-top:4px}
.top3 .card{border-left:5px solid var(--accent)}
.top3 .n{display:inline-grid;place-items:center;width:22px;height:22px;margin-right:6px;border-radius:50%;background:var(--accent);color:#fff;font-size:.75rem;vertical-align:2px}
dl.facts{margin:0;display:grid;gap:8px}
dl.facts div{display:grid;grid-template-columns:7.5em 1fr;gap:10px;padding-bottom:8px;border-bottom:1px solid var(--rule)}
dl.facts dt{font-weight:700;font-size:.9rem}
dl.facts dd{margin:0;font-size:.93rem}
table{width:100%;border-collapse:collapse;font-size:.92rem}
th,td{text-align:left;vertical-align:top;padding:8px 6px;border-bottom:1px solid var(--rule)}
th{white-space:nowrap}
td.k{font-weight:700;white-space:nowrap}
h3.sub-h{font-size:1rem;margin:18px 0 6px;color:var(--river)}
.recipe{border-left:6px solid var(--rc)}
.recipe h3{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 8px}
.recipe h3 small{font-weight:400;color:var(--ink2);font-size:.8rem}
.recipe table{margin:8px 0}
.recipe td.v{text-align:right;font-variant-numeric:tabular-nums;font-weight:700;white-space:nowrap}
.kv{display:grid;grid-template-columns:1fr 1fr;gap:0 14px;margin-top:8px;font-size:.88rem}
.kv div{display:flex;justify-content:space-between;gap:8px;padding:5px 0;border-bottom:1px solid var(--rule)}
.kv b{font-variant-numeric:tabular-nums;text-align:right}
.kv.wide{grid-template-columns:1fr;margin-top:0}
.kv.wide span{flex:0 0 auto}
.card.warn{border-left:5px solid #C8661A;margin-bottom:10px}
.ukey{display:inline-grid;place-items:center;min-width:30px;height:24px;padding:0 6px;border-radius:6px;background:var(--rc);color:#fff;font-size:.8rem}
h4.mini{font-size:.8rem;color:var(--ink2);margin:10px 0 0;font-weight:700}
.pick{font-size:.72rem;font-weight:700;color:#fff;background:var(--accent);border-radius:99px;padding:1px 8px}
.fine{font-size:.8rem;color:var(--ink2);margin-top:8px}
.scene dl{margin:6px 0 0;display:grid;gap:4px}
.scene dl div{display:grid;grid-template-columns:3.2em 1fr;gap:8px}
.scene dt{font-size:.8rem;font-weight:700;color:var(--ink2);padding-top:2px}
.scene dd{margin:0;font-size:.93rem}
.scene .when{font-size:.8rem;color:var(--ink2)}
footer{max-width:720px;margin:24px auto 0;padding:16px 16px 40px;border-top:1px solid var(--rule);font-size:.85rem;color:var(--ink2)}
footer ul{padding-left:1.2em;margin:6px 0 12px}
"""

def build():
    o = []
    o.append('<header class="top"><p class="eyebrow">RICOH GR IV・奧捷 12 日</p><h1>GR IV 拍照筆記</h1>'
             '<p class="sub">風景、人像、美食都想拍：光圈、快門、ISO 怎麼設，濾鏡怎麼調，這趟每個景點怎麼拍。</p></header>')
    toc = [("top3", "先記這三個"), ("basics", "光圈快門 ISO"), ("modes", "拍攝模式"), ("recipes", "濾鏡配方"), ("rr", "Ricoh Recipes"),
           ("which", "風景・建築・教堂"), ("umodes", "U1–U3"), ("scenes", "這趟怎麼拍"), ("camera", "相機功能"), ("check", "出發前")]
    o.append('<nav class="toc" aria-label="目錄"><div class="in">' + "".join(f'<a href="#{i}">{t}</a>' for i, t in toc) + '</div></nav>')
    o.append('<main class="wrap">')
    # 先記這三個
    o.append('<section id="top3"><h2>先記這三個</h2><div class="cards top3">')
    for i, (h, p) in enumerate(TOP3, 1):
        o.append(f'<div class="card"><h3><span class="n">{i}</span>{esc(h)}</h3><p>{rich(p)}</p></div>')
    o.append('</div></section>')
    # 光圈快門 ISO
    o.append('<section id="basics"><h2>光圈、快門、ISO</h2>'
             '<p class="lead">三個一起決定照片亮暗。光圈管背景模糊，快門管會不會糊掉，ISO 管亮度但越高越多雜訊。</p>')
    o.append('<h3 class="sub-h">光圈（F 值）：數字越小，背景越模糊</h3><table><tbody>'
             + "".join(f'<tr><td class="k">{esc(a)}</td><td><b>{esc(b)}</b><br>{esc(c)}</td></tr>' for a, b, c in APERTURE) + '</tbody></table>')
    o.append('<h3 class="sub-h">快門：越快越不會糊</h3><table><tbody>'
             + "".join(f'<tr><td class="k">{esc(a)}</td><td>{esc(b)}</td></tr>' for a, b in SHUTTER) + '</tbody></table>')
    o.append('<h3 class="sub-h">ISO：越高越亮，也越多雜訊</h3><table><tbody>'
             + "".join(f'<tr><td class="k">{esc(a)}</td><td>{esc(b)}</td></tr>' for a, b in ISO) + '</tbody></table>')
    o.append('</section>')
    # 拍攝模式
    o.append('<section id="modes"><h2>拍攝模式</h2><div class="cards">')
    for h, ps in MODES:
        o.append(f'<div class="card"><h3>{esc(h)}</h3>' + "".join(f'<p>{rich(p)}</p>' for p in ps) + '</div>')
    o.append('</div></section>')
    # 濾鏡配方
    o.append('<section id="recipes"><h2>濾鏡配方（影像風格）</h2>'
             '<p class="lead">GR IV 的影像風格 Image Control 有 14 種，每種都能微調參數，範圍 −4 到 +4。下面是你想用的五種，數值是建議起點，拍幾張再依喜好調。白平衡都用自動。</p><div class="cards">')
    for r in RECIPES:
        rows = "".join(f'<tr><td>{esc(p)}</td><td class="v">{esc(v)}</td></tr>' for p, v in zip(PARAMS, r["vals"]))
        o.append(f'<div class="card recipe" style="--rc:{r["color"]}"><h3>{esc(r["name"])}<small>{esc(r["en"])}</small></h3>'
                 f'<p><b>適合：</b>{esc(r["good"])}</p><table><tbody>{rows}</tbody></table><p>{rich(r["note"])}</p></div>')
    o.append('</div><p class="fine">表上沒列的參數（暗角 Shading、色調 Toning 等）維持 0。顆粒只有正片、負片、兩種電影和黑白可以加，大小和強度各有三段。'
             '這些效果只套在 JPEG，RAW 不受影響。</p></section>')
    # Ricoh Recipes
    o.append('<section id="rr"><h2>Ricoh Recipes 推薦</h2><p class="lead">' + rich(
        "[[https://ricohrecipes.com/ricoh-gr-iv-recipes/|Ricoh Recipes]] 是攝影部落客 Ritchie Roesch 整理的 GR 配方網站，也有 iOS、Android App。"
        "GR IV 專用的入門系列有 7 個配方，其中 5 個彩色的剛好用正片、負片、電影（黃）、電影（綠）當底，跟你喜歡的濾鏡一樣。"
        "前三個最推薦。") + '</p>')
    o.append('<div class="cards">')
    for i, r in enumerate(RR_RECIPES):
        star = '<span class="pick">推薦</span>' if i < 3 else ''
        kv = "".join(f'<div><span>{esc(k)}</span><b>{esc(v)}</b></div>' for k, v in r["kv"])
        wide = "".join(f'<div><span>{esc(k)}</span><b>{esc(v)}</b></div>' for k, v in r["wide"])
        o.append(f'<div class="card recipe" style="--rc:{r["color"]}"><h3>{esc(r["name"])}<small>底：{esc(r["base"])}</small>{star}</h3>'
                 f'<p><b>適合：</b>{esc(r["pick"])}</p><p>{esc(r["why"])}</p>'
                 f'<div class="kv">{kv}</div><div class="kv wide">{wide}</div></div>')
    o.append('</div><p class="fine">數值抄自 Ricoh Recipes 網站，輸入前可以在 App 或網頁再對一次；選單名稱以相機為準。'
             '作者實測 GR III 的配方也能用在 GR IV，但 GR IV 拍起來偏暖、偏亮一點，所以這裡只挑 GR IV 專用的配方。'
             '另外兩個是黑白配方（Panchromatic 400 +Red、Pushed B&W），有興趣可以到網站看。</p></section>')
    # 風景、建築、教堂用哪個
    o.append('<section id="which"><h2>風景、建築、教堂用哪個濾鏡</h2>'
             '<p class="lead">一句話：晴天戶外用正片類，陰天用電影（綠），室內用標準，晚上用電影（黃）。</p>'
             '<div class="card warn"><h3>最容易踩的雷：白平衡</h3><p>Travelog（陰天）、Pro Color（日光）、Lomo Color（陰影）的白平衡是固定的。'
             '到教堂、宮殿、餐廳的黃色燈光下，照片會很橘。進室內前把白平衡切回自動，或改用 EktaSlide、標準。</p></div><div class="cards">')
    for sc, first, alt, tip in SCENE_FILTERS:
        o.append(f'<div class="card scene"><h3>{esc(sc)}</h3><dl><div><dt>首選</dt><dd><b>{esc(first)}</b></dd></div>'
                 f'<div><dt>備選</dt><dd>{esc(alt)}</dd></div><div><dt>重點</dt><dd>{esc(tip)}</dd></div></dl></div>')
    o.append('</div></section>')
    # U1–U3
    o.append('<section id="umodes"><h2>U1–U3 建議設定</h2><p class="lead">U1 正片、U2 負片、U3 室內建築。把三組存進轉盤，到現場轉一下就切換，不用每次重調。</p><div class="cards">')
    for u in USER_MODES:
        shot = "".join(f'<div><span>{esc(k)}</span><b>{esc(v)}</b></div>' for k, v in u["shot"])
        kv = "".join(f'<div><span>{esc(k)}</span><b>{esc(v)}</b></div>' for k, v in u["kv"])
        wide = "".join(f'<div><span>{esc(k)}</span><b>{esc(v)}</b></div>' for k, v in u["wide"])
        base = "" if any(k == "影像風格" for k, _ in u["wide"]) else f'<div><span>影像風格</span><b>{esc(u["name"])}</b></div>'
        o.append(f'<div class="card recipe" style="--rc:{u["color"]}"><h3><span class="ukey">{u["key"]}</span>{esc(u["name"])}<small>{esc(u["use"])}</small></h3>'
                 f'<h4 class="mini">拍攝設定</h4><div class="kv">{shot}</div>'
                 f'<h4 class="mini">影像風格參數</h4><div class="kv wide">{base}</div><div class="kv">{kv}</div><div class="kv wide">{wide}</div>'
                 f'<p class="fine">{rich(u["note"])}</p></div>')
    o.append('</div><div class="card" style="margin-top:10px"><h3>室內建築怎麼拍</h3>' + "".join(f'<p>・{esc(t)}</p>' for t in U_TIPS) + '</div>')
    o.append('<div class="card" style="margin-top:10px"><h3>測光怎麼選</h3><dl class="facts">'
             + "".join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in METERING)
             + f'</dl><p class="fine">{esc(METER_TIP)}</p></div>')
    o.append('<div class="card" style="margin-top:12px"><h3>怎麼存進相機</h3>'
             '<p>1. 模式轉盤轉到 Av，設好光圈。</p>'
             '<p>2. 影像風格選好「底」（正片、負片、電影…），照配方調參數。</p>'
             '<p>3. 按 WB 鍵設白平衡和補償。白平衡不在影像風格裡，要另外設。</p>'
             '<p>4. 在 ISO 設定裡把「自動」的上限和最低快門設好，再設曝光補償、測光和 RAW＋JPEG。</p>'
             '<p>5. 用選單裡儲存使用者設定的功能存到 U1、U2 或 U3。選單名稱以相機為準。</p></div></section>')
    # 這趟怎麼拍
    o.append('<section id="scenes"><h2>這趟怎麼拍</h2><div class="cards">')
    for t, when, setting, filt, tip in SCENES:
        o.append(f'<div class="card scene"><h3>{esc(t)}</h3><p class="when">{rich(when)}</p><dl>'
                 f'<div><dt>設定</dt><dd>{esc(setting)}</dd></div><div><dt>濾鏡</dt><dd>{esc(filt)}</dd></div>'
                 f'<div><dt>提醒</dt><dd>{rich(tip)}</dd></div></dl></div>')
    o.append('</div></section>')
    # 相機功能
    o.append('<section id="camera"><h2>GR IV 這台相機</h2><dl class="facts">'
             + "".join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in SPECS) + '</dl></section>')
    # 出發前
    o.append('<section id="check"><h2>出發前檢查</h2><dl class="facts">'
             + "".join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in CHECKLIST) + '</dl></section>')
    o.append('</main>')
    o.append('<footer><p>相機規格查自以下資料；濾鏡和參數是建議起點，不是官方設定。實際選單名稱以你的相機為準。</p><ul>'
             + "".join(f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(t)} ↗</a></li>' for t, u in SOURCES)
             + f'</ul><p><a href="{SITE}">回到奧捷 12 日行程</a></p></footer>')
    body = "".join(o)
    page = ('<!doctype html>\n<html lang="zh-Hant">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<title>GR IV 拍照筆記</title>\n<meta name="robots" content="noindex, nofollow">\n'
            '<meta name="theme-color" content="#962437">\n'
            '<link rel="icon" type="image/png" sizes="192x192" href="favicon.png">\n'
            '<link rel="apple-touch-icon" href="apple-touch-icon.png">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=Noto+Serif+TC:wght@600;700&display=swap">\n'
            f'<style>{CSS}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print("wrote", OUT, len(page.encode("utf-8")), "bytes")

if __name__ == "__main__":
    build()

# 奧捷湖區 12 日：行程網頁

2026/10/11–10/22 奧地利捷克團體旅行的手機行程網頁。用 GitHub Pages 發布：`main` 分支根目錄的 `index.html`。

## 修改流程

1. 不要手改 `index.html`，它是產生出來的。內容都在 `guide-src/`：
   - `build_guide.py`：每日行程 `DAYS`、住宿 `STAYS` / `HOTEL_Q` / `HOTEL_ZH`、和原 PDF 的差異 `CHANGES`、旅途小抄 `TIPS`，以及所有版面渲染。
   - `content_places.py`：景點介紹頁，`P("p-xxx", ...)`。
   - `content_hotels.py`：飯店與帝國咖啡館的設施頁，`H("h-xxx", ...)`。
   - `content_shops.py`：伴手禮門市頁，`SH("s-xxx", ...)`。
   - `content_gifts.py`：伴手禮清單、照天數買、帶回台灣注意事項。
   - `content_maps.py`：景點頁的 Google 地圖搜尋字串、車程日路線。
   - `guide.css`、`guide.js`：樣式與互動。
2. 產生網頁：`python guide-src/build_guide.py`（Python 3.8 以上）。會寫出 `index.html`（GitHub Pages 用）和 `austria-czech-guide.html`（Claude Artifact 用，已在 .gitignore）。
3. 檢查站內連結：`python guide-src/check_links.py`，必須顯示 OK。
4. 提交 `guide-src/` 和 `index.html`，推到 `main`。GitHub Pages 約 1 分鐘後更新。

## 內容寫法

- 文字中 `[[p-id|文字]]` 連到站內頁面（`p-` 景點、`h-` 飯店／設施、`s-` 門市），`[[https://...|文字]]` 是外部連結。
- 景點標記：`★` 入內含門票、`▲` 主要景點、`◆` 使用者自己的安排、空字串為一般或參考。
- 只放在景點百科、不在行程裡的景點，加 `ref=True`。
- 新的地點要給 Google 地圖連結：景點頁加在 `content_maps.PLACE_MAP`，行內文字用 `[[地圖網址|地圖 ↗]]`。

## 原則

- 使用者是台灣人：全部用繁體中文、台灣用語，句子短、直接。
- 事實要查證；查不到的寫「以官網／現場為準」，不要猜。
- 這是公開網頁：不放領隊或任何人的電話、Email 等個人聯絡資料。
- 旅途中使用者在歐洲（CEST，比台灣慢 6 小時）。

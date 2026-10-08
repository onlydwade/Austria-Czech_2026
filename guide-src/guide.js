(function () {
  var body = document.body;
  var rail = document.getElementById("rail");
  var ret = null; // where to go back to when a place was opened from the itinerary

  function jump(y) {
    var r = document.documentElement;
    var prev = r.style.scrollBehavior;
    r.style.scrollBehavior = "auto";
    window.scrollTo(0, y);
    r.style.scrollBehavior = prev;
  }

  function isPlace(el) { return el && el.classList && el.classList.contains("place"); }

  // Remember the itinerary position when a place link is tapped from the main view.
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"]');
    if (!a) return;
    var id = a.getAttribute("href").slice(1);
    var t = id && document.getElementById(id);
    if (isPlace(t) && !body.classList.contains("reading")) {
      var sec = a.closest("[data-label]");
      var label = sec ? sec.getAttribute("data-label") : "行程";
      if (sec && sec.id === "main") label = "行程";
      ret = { y: window.scrollY, label: label, hash: location.hash };
    }
    if (a.classList.contains("back") && ret) {
      e.preventDefault();
      location.hash = ret.hash && ret.hash.length > 1 ? ret.hash : "#main";
    }
  });

  function route() {
    var id = decodeURIComponent(location.hash.slice(1));
    var el = id ? document.getElementById(id) : null;
    var wasReading = body.classList.contains("reading");
    var open = document.querySelectorAll(".place.open");
    for (var i = 0; i < open.length; i++) open[i].classList.remove("open");
    if (isPlace(el)) {
      body.classList.add("reading");
      el.classList.add("open");
      var back = el.querySelector(".back-l");
      if (back) back.textContent = ret ? ret.label : el.getAttribute("data-back");
      jump(0);
      return;
    }
    body.classList.remove("reading");
    if (id === "top") {
      ret = null;
      if (wasReading) jump(0); else window.scrollTo(0, 0);
      return;
    }
    if (wasReading && ret && (id === "" || id === "main" || "#" + id === ret.hash)) {
      var y = ret.y;
      requestAnimationFrame(function () { jump(y); });
    } else if (el && id !== "main") {
      requestAnimationFrame(function () { el.scrollIntoView(); });
    }
  }
  window.addEventListener("hashchange", route);

  // Back-to-home button: works from anywhere, including an open place.
  var fab = document.getElementById("homeFab");
  function fabState() {
    var away = !body.classList.contains("reading") && window.scrollY < 400;
    fab.classList.toggle("away", away);
  }
  fab.addEventListener("click", function (e) {
    e.preventDefault();
    if (location.hash === "#top") route(); else location.hash = "#top";
    fabState();
  });
  var gfab = document.getElementById("guideFab");
  gfab.addEventListener("click", function (e) {
    e.preventDefault();
    if (location.hash === "#guide") route(); else location.hash = "#guide";
    fabState();
  });
  window.addEventListener("scroll", fabState, { passive: true });
  window.addEventListener("hashchange", fabState);

  // Day rail: arrow buttons, mouse drag and wheel, on top of native touch swipe.
  var prevB = document.getElementById("railPrev");
  var nextB = document.getElementById("railNext");
  var dragging = false;
  function railBtns() {
    var max = rail.scrollWidth - rail.clientWidth - 2;
    prevB.disabled = rail.scrollLeft <= 2;
    nextB.disabled = rail.scrollLeft >= max;
  }
  function railBy(dir) {
    var d = Math.max(120, rail.clientWidth * 0.75) * dir;
    try { rail.scrollBy({ left: d, behavior: "smooth" }); } catch (_) { rail.scrollLeft += d; }
  }
  if (rail) {
    prevB.addEventListener("click", function () { railBy(-1); });
    nextB.addEventListener("click", function () { railBy(1); });
    rail.addEventListener("scroll", railBtns, { passive: true });
    window.addEventListener("resize", railBtns);
    railBtns();
    rail.addEventListener("wheel", function (e) {
      if (Math.abs(e.deltaY) <= Math.abs(e.deltaX)) return;
      var max = rail.scrollWidth - rail.clientWidth;
      if ((e.deltaY < 0 && rail.scrollLeft > 0) || (e.deltaY > 0 && rail.scrollLeft < max)) {
        rail.scrollLeft += e.deltaY;
        e.preventDefault();
      }
    }, { passive: false });
    var start = null, moved = false;
    rail.addEventListener("pointerdown", function (e) {
      if (e.pointerType !== "mouse" || e.button !== 0) return;
      start = { x: e.clientX, s: rail.scrollLeft };
      moved = false;
    });
    window.addEventListener("pointermove", function (e) {
      if (!start) return;
      var dx = e.clientX - start.x;
      if (!moved && Math.abs(dx) > 5) { moved = true; dragging = true; rail.classList.add("dragging"); }
      if (moved) rail.scrollLeft = start.s - dx;
    });
    window.addEventListener("pointerup", function () {
      start = null;
      if (dragging) setTimeout(function () { dragging = false; rail.classList.remove("dragging"); }, 0);
    });
    rail.addEventListener("click", function (e) {
      if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; }
    }, true);
    rail.addEventListener("dragstart", function (e) { e.preventDefault(); });
  }

  // Copy the tour leader's number.
  var cb = document.getElementById("copyTel");
  if (cb) cb.addEventListener("click", function () {
    var t = document.getElementById("telN");
    function done(msg) { cb.textContent = msg; setTimeout(function () { cb.textContent = "複製"; }, 1600); }
    function selectIt() {
      var r = document.createRange(); r.selectNodeContents(t);
      var sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r);
      done("已選取");
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(t.textContent).then(function () { done("已複製"); }, selectIt);
    } else { selectIt(); }
  });

  // Highlight the day or section (百科・伴手禮・小提醒) in the rail while scrolling.
  // A section without a chip (和原 PDF 的差異) clears the highlight.
  var chips = rail ? rail.querySelectorAll(".chip") : [];
  function setActive(id) {
    for (var i = 0; i < chips.length; i++) {
      var on = chips[i].getAttribute("href") === "#" + id;
      chips[i].classList.toggle("on", on);
      if (on && !dragging) {
        var c = chips[i];
        var outside = c.offsetLeft < rail.scrollLeft || c.offsetLeft + c.offsetWidth > rail.scrollLeft + rail.clientWidth;
        if (outside) {
          // Instant on purpose: a smooth scroll here would cancel the page's own smooth scroll in Chromium.
          rail.scrollLeft = c.offsetLeft - rail.clientWidth / 2 + c.offsetWidth / 2;
        }
      }
    }
  }
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) setActive(en.target.id);
      });
    }, { rootMargin: "-35% 0px -60% 0px" });
    document.querySelectorAll(".day, #guide, .block").forEach(function (d) { io.observe(d); });
  }

  // Daily weather forecast from Open-Meteo (free, no API key), one request for every place.
  // Cached for 2 hours, and the last forecast stays visible when the phone is offline.
  (function () {
    var boxes = document.querySelectorAll(".wx");
    if (!boxes.length) return;
    var CODES = {
      0: ["☀️", "晴"], 1: ["🌤️", "大致晴朗"], 2: ["⛅", "晴時多雲"], 3: ["☁️", "陰"], 45: ["🌫️", "霧"], 48: ["🌫️", "霧"],
      51: ["🌦️", "毛毛雨"], 53: ["🌦️", "毛毛雨"], 55: ["🌧️", "毛毛雨"], 56: ["🌧️", "凍毛毛雨"], 57: ["🌧️", "凍毛毛雨"],
      61: ["🌧️", "小雨"], 63: ["🌧️", "中雨"], 65: ["🌧️", "大雨"], 66: ["🌧️", "凍雨"], 67: ["🌧️", "凍雨"],
      71: ["🌨️", "小雪"], 73: ["🌨️", "中雪"], 75: ["❄️", "大雪"], 77: ["🌨️", "霰"],
      80: ["🌦️", "陣雨"], 81: ["🌧️", "陣雨"], 82: ["⛈️", "強陣雨"], 85: ["🌨️", "陣雪"], 86: ["❄️", "強陣雪"],
      95: ["⛈️", "雷雨"], 96: ["⛈️", "雷雨夾冰雹"], 99: ["⛈️", "雷雨夾冰雹"]
    };
    var KEY = "wx-cache-v1", FRESH = 2 * 3600 * 1000;
    function iso(d) { return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2); }
    function shift(days) { var d = new Date(); d.setDate(d.getDate() + days); return iso(d); }
    // Open-Meteo forecasts 16 days ahead; stay a day short so the phone's time zone never asks past the limit.
    var from = ["2026-10-11", shift(-60)].sort()[1];
    var to = ["2026-10-22", shift(14)].sort()[0];
    var locs = {}, keys = [];
    document.querySelectorAll(".wx [data-loc]").forEach(function (li) {
      var k = li.getAttribute("data-loc");
      if (!locs[k]) { locs[k] = li.getAttribute("data-ll").split(","); keys.push(k); }
    });
    function stamp(t) { var d = new Date(t); return (d.getMonth() + 1) + "/" + d.getDate() + " " + d.getHours() + ":" + ("0" + d.getMinutes()).slice(-2); }
    function paint(c, offline) {
      boxes.forEach(function (box) {
        var date = box.getAttribute("data-date");
        box.querySelectorAll("[data-loc]").forEach(function (li) {
          var v = li.querySelector(".wx-v");
          var r = c && c.v[li.getAttribute("data-loc")];
          r = r && r[date];
          if (r && r[0] != null) {
            var w = CODES[r[0]] || ["", ""];
            var rain = r[3] == null ? "" : '<span class="wx-p">降雨 ' + r[3] + "%</span>";
            v.innerHTML = '<span class="wx-i" aria-hidden="true">' + w[0] + "</span>" + w[1] +
              " <b>" + Math.round(r[2]) + "–" + Math.round(r[1]) + "°C</b>" + rain;
          } else if (date > to) {
            v.textContent = "出發前約兩週才有預報";
          } else {
            v.textContent = c ? "沒有這天的預報" : "暫時抓不到預報";
          }
        });
        var t = box.querySelector(".wx-t");
        if (t && c) t.innerHTML = '<a href="https://open-meteo.com/" target="_blank" rel="noopener">Open-Meteo</a> ' +
          (offline ? "離線，顯示 " + stamp(c.t) + " 的預報" : stamp(c.t) + " 更新");
      });
    }
    var cached = null;
    try { cached = JSON.parse(localStorage.getItem(KEY)); } catch (_) { cached = null; }
    if (cached && Date.now() - cached.t < FRESH) { paint(cached, false); return; }
    if (from > to || !window.fetch) { paint(cached, !!cached); return; }
    boxes.forEach(function (box) {
      box.querySelectorAll(".wx-v").forEach(function (v) { v.textContent = "載入中…"; });
    });
    var url = "https://api.open-meteo.com/v1/forecast?latitude=" + keys.map(function (k) { return locs[k][0]; }).join(",") +
      "&longitude=" + keys.map(function (k) { return locs[k][1]; }).join(",") +
      "&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto" +
      "&start_date=" + from + "&end_date=" + to;
    fetch(url).then(function (res) {
      if (!res.ok) throw new Error("HTTP " + res.status);
      return res.json();
    }).then(function (json) {
      var list = Array.isArray(json) ? json : [json];
      var c = { t: Date.now(), v: {} };
      keys.forEach(function (k, i) {
        var d = list[i] && list[i].daily;
        if (!d) return;
        c.v[k] = {};
        d.time.forEach(function (day, j) {
          c.v[k][day] = ["weather_code", "temperature_2m_max", "temperature_2m_min", "precipitation_probability_max"]
            .map(function (name) { return d[name] ? d[name][j] : null; });
        });
      });
      try { localStorage.setItem(KEY, JSON.stringify(c)); } catch (_) {}
      paint(c, false);
    }).catch(function () { paint(cached, !!cached); });
  })();

  // Countdown before the trip, "today" during it.
  var start = new Date(2026, 9, 11);
  var now = new Date();
  var today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  var diff = Math.round((today - start) / 86400000);
  var count = document.getElementById("count");
  var link = document.getElementById("todayLink");
  if (diff < 0) {
    count.textContent = "出發倒數 " + (-diff) + " 天・10/11（日）21:00 桃園機場集合";
  } else if (diff <= 11) {
    var n = diff + 1;
    var sec = document.getElementById("d" + n);
    count.textContent = "旅途中・第 " + n + " 天";
    link.hidden = false;
    link.href = "#d" + n;
    link.innerHTML = "<span>今天是 Day " + n + "（" + sec.getAttribute("data-date") + "）</span><span>看今天行程 ›</span>";
    var pill = sec.querySelector(".today-pill");
    if (pill) pill.hidden = false;
    var chip = rail && rail.querySelector('.chip[data-day="' + n + '"]');
    if (chip) chip.classList.add("today");
  } else {
    count.textContent = "旅程已結束，歡迎回味";
  }

  route();
  fabState();
})();

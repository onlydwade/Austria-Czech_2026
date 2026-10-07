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

  // Highlight the day in the rail while scrolling.
  var chips = rail ? rail.querySelectorAll(".chip[data-day]") : [];
  function setActive(n) {
    for (var i = 0; i < chips.length; i++) {
      var on = chips[i].getAttribute("data-day") === String(n);
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
        if (en.isIntersecting) setActive(en.target.id.slice(1));
      });
    }, { rootMargin: "-35% 0px -60% 0px" });
    document.querySelectorAll(".day").forEach(function (d) { io.observe(d); });
  }

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

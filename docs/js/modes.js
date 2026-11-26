// Home screen, the daily quiz and Classic mode.
"use strict";

var ICONS = {
  classic: '<path d="M4 6h16M4 12h16M4 18h10"/>',
  survival: '<path d="M12 21s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 5.6-7 10-7 10z"/>',
  blitz: '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2.5M9.5 2.5h5"/>',
  hilo: '<path d="M7 20V5M3.5 8.5L7 5l3.5 3.5M17 4v15M13.5 15.5L17 19l3.5-3.5"/>',
  career: '<circle cx="11" cy="11" r="7"/><path d="M16 16l5 5"/><path d="M11 8v3.5M11 14.5v.01"/>',
  flags: '<path d="M5 21V4"/><path d="M5 4h11l-2 4 2 4H5"/>',
  live: '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
  duo: '<circle cx="8" cy="8" r="3"/><circle cx="16" cy="8" r="3"/><path d="M2.5 20c.6-3.4 2.8-5.5 5.5-5.5s4.9 2.1 5.5 5.5M10.5 20c.6-3.4 2.8-5.5 5.5-5.5s4.9 2.1 5.5 5.5"/>',
  challenge: '<path d="M14.5 4l5.5 5.5-9 9H5.5V13z"/><path d="M4 20l3-3"/>'
};
// `go` names a function so modes defined in later files (games.js) can be wired here.
var MODES = [
  {id: "duo", name: "2v2 Online", desc: "Team up with a mate and take on two more, live", go: "openDuo", hot: true},
  {id: "classic", name: "Classic", desc: "Pick a topic, level and timer", go: "openSetup"},
  {id: "flags", name: "Flags", desc: "Name the country from its flag", go: "openFlags"},
  {id: "survival", name: "Survival", desc: "One wrong and you're out", go: "startSurvival"},
  {id: "blitz", name: "Blitz", desc: "60 seconds, as many as you can", go: "startBlitz"},
  {id: "hilo", name: "Higher or lower", desc: "Which is bigger? Countries, peaks, rivers", go: "startHilo"},
  {id: "career", name: "Guess the country", desc: "Five clues, hardest first. Fewer = more points", go: "startCareer"},
  {id: "live", name: "Live 1v1", desc: "Race a mate in real time", go: "openLive"},
  {id: "challenge", name: "Challenge", desc: "Send a mate your exact quiz", go: "openChallengeHub"}
];
var lastStart = null;       // what "Play again" on the result screen does

function goHome() { renderHome(); show("home"); }

// ---------------------------------------------------------------- home

function renderModes() {
  var box = $("modes"); if (box.children.length) return;
  MODES.forEach(function (m) {
    var on = !!m.go;
    var b = h("button", {className: "mode tile" + (on ? " active" : "") + (m.hot ? " hot" : ""), disabled: !on},
      m.hot ? h("span", {className: "new"}, "New") : null,
      h("span", {className: "ic", innerHTML: '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + ICONS[m.id] + "</svg>"}),
      on ? null : h("span", {className: "soon"}, "Soon"),
      h("b", null, m.name), h("span", null, m.desc));
    b.setAttribute("data-mode", m.id);
    if (on) b.onclick = function () { window[m.go](); };
    else b.setAttribute("aria-label", m.name + ", coming soon");
    box.appendChild(b);
  });
}

function renderHome() {
  renderModes();
  $("subtitle").textContent = "Capitals, flags, landmarks and more" + (BANK.length ? " · " + BANK.length + " questions" : "");
  var st = store.get("stats", {played: 0, right: 0, asked: 0, best: 0});
  $("sPlayed").textContent = st.played;
  $("sPct").textContent = st.asked ? Math.round(100 * st.right / st.asked) + "%" : "–";
  $("sStreak").textContent = st.best;
  var seen = store.get("seen", []).length;
  $("seenNote").textContent = BANK.length ? "You've seen " + seen + " of " + BANK.length + " questions. Classic serves unseen ones first." : "";
  renderDailyCard();
  refreshDivStrip();
}

// ---------------------------------------------------------------- daily

function dailyLog() { return store.get("daily", {}); }
function dailyLabel(n) { return n > 0 ? "Daily quiz #" + n : "Daily quiz · preview"; }

function dailyStreak() {
  var log = dailyLog(), d = WQDaily.ukToday();
  if (!log[d]) d = WQDaily.addDays(d, -1);
  var n = 0;
  while (log[d]) { n++; d = WQDaily.addDays(d, -1); }
  return n;
}

function renderDailyCard() {
  var today = WQDaily.ukToday(), n = WQDaily.number(today), rec = dailyLog()[today];
  $("dLabel").textContent = dailyLabel(n);
  var s = dailyStreak();
  $("dFlame").textContent = s ? "🔥 " + s + (s === 1 ? " day" : " days") : "";
  $("dTodo").classList.toggle("hidden", !!rec);
  $("dDone").classList.toggle("hidden", !rec);
  $("dPlay").disabled = !PICKER;
  if (rec) {
    $("dScore").textContent = rec.correct + "/" + rec.total;
    var g = gridEl(rec.grid.split("").map(function (c) { return c === "1"; }));
    var old = $("dGrid"); g.id = "dGrid"; old.parentNode.replaceChild(g, old);
    $("dRank").textContent = rec.rank ? ordinal(rec.rank) + " of " + rec.players + " today so far" : "";
    $("dRank").classList.toggle("hidden", !rec.rank);
  }
  tickCountdown();
}

var countdownDay = null;
function tickCountdown() {
  var t = hms(WQDaily.msToReset());
  $("dCount1").textContent = t; $("dCount2").textContent = t;
  var d = WQDaily.ukToday();
  if (countdownDay && countdownDay !== d && !$("home").classList.contains("hidden")) { countdownDay = d; renderDailyCard(); }
  countdownDay = d;
}

async function dailyIds(date) {
  var local = PICKER.ids(date);
  var cache = store.get("dailyIds", {});
  try {
    var r = await api("/daily?date=" + date, null, 3000);
    var ok = r.ids && r.ids.length === local.length && r.ids.every(function (id) { return BY_ID[id]; });
    if (ok) { cache = {}; cache[date] = r.ids; store.set("dailyIds", cache); return r.ids; }
  } catch (e) { /* offline: fall back */ }
  if (cache[date] && cache[date].every(function (id) { return BY_ID[id]; })) return cache[date];
  return local;
}

async function startDaily() {
  var date = WQDaily.ukToday();
  if (dailyLog()[date]) { renderDailyCard(); return; }
  $("dPlay").disabled = true;
  var ids = await dailyIds(date);
  $("dPlay").disabled = false;
  startGame({mode: "daily", label: dailyLabel(WQDaily.number(date)), timer: 0,
             qs: ids.map(function (id) { return BY_ID[id]; }),
             onFinish: function (g) { finishDaily(g, date); }});
}

function shareDailyText(rec) {
  var n = rec.n > 0 ? "#" + rec.n : "(preview)";
  var squares = rec.grid.split("").map(function (c) { return c === "1" ? "🟩" : "🟥"; }).join("");
  var s = dailyStreak();
  return "World Quiz " + n + " 🌍 " + rec.correct + "/" + rec.total + "\n" + squares +
         (s > 1 ? "\n🔥 " + s + " day streak" : "") + "\n" + SITE;
}

function finishDaily(g, date) {
  var rec = {n: WQDaily.number(date), correct: g.right, total: g.qs.length, points: g.points,
             grid: g.marks.map(function (m) { return m ? "1" : "0"; }).join("")};
  var log = dailyLog(); log[date] = rec;
  // keep ~a year of history
  var keys = Object.keys(log).sort(); while (keys.length > 400) delete log[keys.shift()];
  store.set("daily", log);
  var s = dailyStreak();
  if (s > store.get("dbest", 0)) store.set("dbest", s);

  $("rLabel").textContent = dailyLabel(rec.n);
  $("final").textContent = rec.correct + "/" + rec.total;
  $("verdict").textContent = verdict(rec.correct / rec.total);
  var grid = gridEl(g.marks); grid.id = "rGrid"; var old = $("rGrid"); old.parentNode.replaceChild(grid, old);
  $("rFlame").textContent = "🔥 " + s + (s === 1 ? " day streak - come back tomorrow" : " day streak");
  $("rFlame").classList.remove("hidden");
  $("rShare").classList.remove("hidden");
  $("rShare").onclick = function () { shareText(shareDailyText(rec)); };
  $("again").classList.add("hidden");
  $("chBox").classList.add("hidden");
  renderMissed(g);
  show("done");
  showPushOffer();
  achCheck({k: "daily", correct: rec.correct, total: rec.total});
  if (rec.correct === rec.total) celebrate("Perfect!", rec.total + " out of " + rec.total);
  submitResult("daily", {date: date, answers: g.answers}, function (r, name) {
    var l = dailyLog(); if (l[date]) { l[date].rank = r.rank_today; l[date].players = r.players_today; store.set("daily", l); }
    postMsg("Posted as " + name + ": " + ordinal(r.rank_today) + " of " + r.players_today + " today · 🔥 " + r.streak + " day streak.",
            false, {text: "Daily board", fn: function () { openBoard("daily"); }});
  });
}

// Reset the shared result screen for a non-daily game.
function resultScreen() {
  $("rGrid").classList.add("hidden");
  $("rFlame").classList.add("hidden");
  $("rShare").classList.add("hidden");
  $("again").classList.remove("hidden");
  $("chBox").classList.add("hidden");
  $("pushAsk").classList.add("hidden");
  $("missedH").textContent = "What you missed";
  $("postMsg").classList.add("hidden");
  $("postAsk").classList.add("hidden");
}

function verdict(pct) {
  return pct === 1 ? "Perfect. A true globetrotter." :
    pct >= .8 ? "World class." : pct >= .6 ? "Well travelled." :
    pct >= .4 ? "Halfway round the world. Room to improve." : "Lost at sea. Try again!";
}

// ---------------------------------------------------------------- classic

function chips(el, map, key) {
  el.innerHTML = "";
  Object.keys(map).forEach(function (v) {
    var b = h("button", {className: "chip"}, map[v]);
    b.setAttribute("aria-pressed", String(settings[key] === v));
    b.onclick = function () { settings[key] = v; store.set("settings", settings); renderSetup(); };
    el.appendChild(b);
  });
}

function pool() {
  return BANK.filter(function (q) {
    return (settings.league === "all" || q.l === settings.league) && (settings.diff === "0" || String(q.d) === settings.diff);
  });
}

function renderSetup() {
  chips($("leagues"), CATS, "league");
  chips($("diffs"), DIFFS, "diff");
  chips($("lengths"), LENGTHS, "len");
  chips($("timers"), TIMERS, "timer");
  var p = pool(), seen = {};
  store.get("seen", []).forEach(function (id) { seen[id] = 1; });
  var fresh = p.filter(function (q) { return !seen[q.id]; }).length;
  $("pool").textContent = p.length ? p.length + " questions match · " + fresh + " you haven't seen yet" : "No questions match these settings.";
  $("start").disabled = !p.length;
}

function openSetup() { renderSetup(); show("setup"); }
// The Flags tile is Classic with the topic set to flags (still changeable on the setup screen).
function openFlags() { settings.league = "flg"; store.set("settings", settings); openSetup(); }

function startClassic() {
  var seen = {};
  store.get("seen", []).forEach(function (id) { seen[id] = 1; });
  var p = pool();
  // Unseen questions first, so repeats only start once a pool is exhausted.
  var picked = shuffle(p.filter(function (q) { return !seen[q.id]; }))
    .concat(shuffle(p.filter(function (q) { return seen[q.id]; }))).slice(0, Number(settings.len));
  lastStart = startClassic;
  startGame({mode: "classic", label: "Classic · " + CATS[settings.league], qs: picked,
             timer: Number(settings.timer), fifty: true, onFinish: finishClassic});
}

function finishClassic(g) {
  var n = g.qs.length, r = g.right;
  var st = store.get("stats", {played: 0, right: 0, asked: 0, best: 0});
  st.played++; st.right += r; st.asked += n; st.best = Math.max(st.best, g.best);
  store.set("stats", st);
  $("rLabel").textContent = "Final score";
  $("final").textContent = r + "/" + n;
  $("verdict").textContent = verdict(r / n) + " " + (Math.round(g.points * 10) / 10) + " pts." +
    (g.fiftyOn >= 0 ? " (50:50 used.)" : "");
  resultScreen();
  offerChallenge(g);
  renderMissed(g);
  show("done");
  var full = [10, 20, 50].indexOf(n) >= 0 && n === Number(settings.len);
  achCheck({k: "classic", correct: r, total: full ? n : 0, timer: Number(settings.timer)});
  if (r === n && full) celebrate("Perfect!", n + " out of " + n);
  // Only whole quizzes of 10/20/50 count; a short pool (e.g. Hard + one topic) doesn't.
  if (!([10, 20, 50].indexOf(n) >= 0 && n === Number(settings.len))) {
    postMsg("Leaderboard scores need a full 10, 20 or 50-question quiz.");
    return;
  }
  // `right` and `streak` are for the old server; the new one marks `answers` itself.
  var body = {total: n, right: g.byDiff, league: settings.league, diff: Number(settings.diff),
              timer: Number(settings.timer), streak: g.best, answers: g.answers, mode: "classic"};
  submitResult("scores", body, function (res, name) {
    postMsg("Posted as " + name + ": " + res.points + " pts · #" + res.rank_week + " this week · #" + res.rank_all + " all time.",
            false, {text: "View board", fn: function () { openBoard("classic", String(n)); }});
  });
}

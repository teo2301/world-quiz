// Wiring. Loaded last.
"use strict";
(function () {
  var tabs = document.querySelectorAll("#tabbar button");
  for (var i = 0; i < tabs.length; i++) tabs[i].onclick = function () {
    var t = this.getAttribute("data-tab");
    if (t === "home") return goHome();
    if (t === "boards") return openBoard();
    if (t === "leaguesTab") return openLeaguesTab();
    if (t === "me") renderMe();
    show(t);
  };
  $("dPlay").onclick = startDaily;
  $("dShare").onclick = function () {
    var rec = dailyLog()[WQDaily.ukToday()];
    if (rec) shareText(shareDailyText(rec));
  };
  $("dBoard").onclick = function () { boardState.dperiod = "today"; openBoard("daily"); };
  $("setupBack").onclick = goHome;
  $("start").onclick = startClassic;
  $("next").onclick = nextQuestion;
  $("quit").onclick = quitGame;
  $("again").onclick = function () { (lastStart || startClassic)(); };
  $("fifty").onclick = useFifty;
  $("hiBtn").onclick = function () { hiloGuess("hi"); };
  $("loBtn").onclick = function () { hiloGuess("lo"); };
  $("hiNext").onclick = hiloNext;
  $("hiQuit").onclick = quitGame;
  $("cGuessBtn").onclick = careerGuess;
  $("cGuess").addEventListener("keydown", function (e) { if (e.key === "Enter") careerGuess(); });
  $("cClue").onclick = careerClue;
  $("cGiveUp").onclick = careerGiveUp;
  $("cNext").onclick = careerNext;
  $("cQuit").onclick = quitGame;
  $("menu").onclick = goHome;
  $("postBtn").onclick = savePostName;
  $("nameIn").addEventListener("keydown", function (e) { if (e.key === "Enter") savePostName(); });
  $("meSave").onclick = saveMeName;
  $("meName").addEventListener("keydown", function (e) { if (e.key === "Enter") saveMeName(); });
  window.addEventListener("online", function () { flushPending(); syncBadges(); });
  wireFeel();
  $("goal").onclick = endCelebrate;
  wireCompete();
  wireLive();
  wireReport();
  wirePush();
  setInterval(tickCountdown, 1000);

  playerId();
  achInit();
  renderHome();
  loadBank().then(function () { renderHome(); flushPending(); handleHash() || handleLiveHash(); }).catch(function () {
    $("subtitle").textContent = "Couldn't load the questions. Check your connection and reload.";
    handleHash();
  });
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("sw.js").catch(function () {});
    warmFlags();
  }
})();

// Once the bank is in, ask the service worker to fetch every flag in the background, so the flag
// questions still show their flag offline. The SW skips the ones it already has.
function warmFlags() {
  Promise.all([navigator.serviceWorker.ready, loadBankOnce()]).then(function (r) {
    var seen = {}, urls = [];
    for (var i = 0; i < BANK.length; i++) {
      var u = BANK[i].img;
      if (u && !seen[u]) { seen[u] = 1; urls.push(u); }
    }
    if (urls.length && r[0].active) r[0].active.postMessage({type: "warm-flags", urls: urls});
  }).catch(function () {});
}
function loadBankOnce() {
  return BANK.length ? Promise.resolve() : new Promise(function (ok, no) {
    var n = 0, t = setInterval(function () {
      if (BANK.length) { clearInterval(t); ok(); } else if (++n > 60) { clearInterval(t); no(); }
    }, 500);
  });
}

// Offline support (scope "./" only, so it never touches other apps on teo2301.github.io). Bump VERSION after changing any app file or the file list.
// The data files (questions, stats, clues) are network-first so new content shows up without a bump.
const VERSION = "wq-v7";
const FLAGS = "wq-flags-v1";   // flag SVGs: cached the first time each is shown, never at install; kept across VERSION bumps
const DATA = ["/questions.json", "/stats.json", "/clues.json", "/data/countries.json"];
const FILES = ["./", "index.html", "app.css", "privacy.html", "questions.json", "stats.json", "clues.json", "manifest.json",
  "icon-192.png", "icon-512.png", "icon-mono.png", "badge-96.png", "sounds/right.mp3", "sounds/wrong.mp3", "sounds/finish.mp3",
  "js/daily-gen.js", "js/match.js", "js/ach-defs.js", "js/core.js", "js/achievements.js", "js/quiz.js", "js/social.js", "js/report.js", "js/modes.js", "js/games.js", "js/compete.js", "js/board.js", "js/push.js", "js/me.js", "js/app.js",
  "fonts/inter-latin.woff2", "fonts/inter-latin-ext.woff2", "fonts/space-grotesk-latin-600.woff2", "fonts/space-grotesk-latin-700.woff2",
  "fonts/space-grotesk-latin-ext-600.woff2", "fonts/space-grotesk-latin-ext-700.woff2"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== VERSION && k !== FLAGS).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin || url.pathname.indexOf("/api/") >= 0) return;
  if (url.pathname.indexOf("/flags/") >= 0) {
    e.respondWith(caches.open(FLAGS).then(c => c.match(e.request).then(hit => hit || fetch(e.request).then(r => {
      if (r.ok) c.put(e.request, r.clone());
      return r;
    }))));
    return;
  }
  if (DATA.some(d => url.pathname.endsWith(d))) {
    e.respondWith(fetch(e.request).then(r => {
      const copy = r.clone(); caches.open(VERSION).then(c => c.put(e.request, copy)); return r;
    }).catch(() => caches.match(e.request)));
    return;
  }
  e.respondWith(caches.match(e.request, {ignoreSearch: true}).then(hit => hit || fetch(e.request)));
});

// The app sends the list of flag images once the questions have loaded; fetch the missing ones
// quietly so the flag questions work offline (about 0.4 MB compressed the first time, then nothing).
self.addEventListener("message", e => {
  const d = e.data || {};
  if (d.type !== "warm-flags" || !Array.isArray(d.urls)) return;
  e.waitUntil(caches.open(FLAGS).then(c => d.urls.reduce((p, u) => p.then(() => {
    const url = new URL(u, self.registration.scope);
    if (url.origin !== location.origin || url.pathname.indexOf("/flags/") < 0) return null;
    return c.match(url.href).then(hit => hit || fetch(url.href).then(r => (r.ok ? c.put(url.href, r) : null)));
  }).catch(() => null), Promise.resolve())));
});

// Push notifications (Phase 6). Payload: {title, body, url, tag} from server/push.py.
self.addEventListener("push", e => {
  let d = {};
  try { d = e.data ? e.data.json() : {}; } catch (err) { d = {body: e.data ? e.data.text() : ""}; }
  e.waitUntil(self.registration.showNotification(d.title || "World Quiz", {
    body: d.body || "", icon: "icon-192.png", badge: "badge-96.png", tag: d.tag || "wq",
    data: {url: d.url || "./"}
  }));
});
self.addEventListener("notificationclick", e => {
  e.notification.close();
  const url = new URL((e.notification.data && e.notification.data.url) || "./", self.registration.scope);
  e.waitUntil(self.clients.matchAll({type: "window", includeUncontrolled: true}).then(list => {
    const open = list.filter(c => c.url.indexOf(self.registration.scope) === 0);
    if (open.length) {                     // the app is open: bring it forward and let it route the hash
      open[0].postMessage({type: "open", hash: url.hash});
      return open[0].focus();
    }
    return self.clients.openWindow(url.href);
  }));
});

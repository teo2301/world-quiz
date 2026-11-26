// Mystery-country guess matching. MUST stay identical to server/modes.py
// (server/test_leaderboard.py runs both over the same guesses).
var WQMatch = (function () {
  "use strict";
  var SPECIAL = {"ø": "o", "ß": "ss", "ı": "i", "ł": "l", "đ": "d", "æ": "ae", "œ": "oe", "ð": "d", "þ": "th"};

  function words(s) {
    s = String(s == null ? "" : s).toLowerCase();
    if (s.normalize) s = s.normalize("NFD");
    s = s.replace(/[̀-ͯ]/g, "");
    var out = "";
    for (var i = 0; i < s.length; i++) { var ch = s.charAt(i); out += SPECIAL.hasOwnProperty(ch) ? SPECIAL[ch] : ch; }
    out = out.replace(/['’`]/g, "");
    return out.split(/[^a-z0-9]+/).filter(function (w) { return w; });
  }
  function key(s) { return words(s).join(""); }

  // id -> {key: true}: the name and its aliases only. (The football app also accepted
  // surnames; for places that would let "Africa" count as South Africa.)
  function buildForms(items) {
    var res = {};
    items.forEach(function (p) {
      var f = {}; f[key(p.n)] = 1;
      (p.al || []).forEach(function (a) { f[key(a)] = 1; });
      res[p.id] = f;
    });
    return res;
  }

  // Every name/alias in the game plus the decoys (other real places): a guess that IS one of
  // these is never fuzzy-matched to a different answer ("Austria" is not a typo of "Australia").
  function takenKeys(items, decoys) {
    var t = {};
    items.forEach(function (p) {
      t[key(p.n)] = 1;
      (p.al || []).forEach(function (a) { t[key(a)] = 1; });
    });
    (decoys || []).forEach(function (d) { t[key(d)] = 1; });
    return t;
  }

  function lev(a, b, cap) {
    if (Math.abs(a.length - b.length) > cap) return cap + 1;
    var prev = [], i, j;
    for (j = 0; j <= b.length; j++) prev.push(j);
    for (i = 1; i <= a.length; i++) {
      var cur = [i], best = i;
      for (j = 1; j <= b.length; j++) {
        cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a.charAt(i - 1) !== b.charAt(j - 1) ? 1 : 0));
        if (cur[j] < best) best = cur[j];
      }
      if (best > cap) return cap + 1;
      prev = cur;
    }
    return prev[b.length];
  }

  function isMatch(guess, forms, taken) {
    var g = key(guess);
    if (!g) return false;
    if (forms[g]) return true;
    if (taken && taken[g]) return false;
    var ks = Object.keys(forms);
    for (var i = 0; i < ks.length; i++) {
      var f = ks[i];
      if (g === f) return true;
      var cap = f.length >= 9 ? 2 : f.length >= 5 ? 1 : 0;
      if (cap && lev(g, f, cap) <= cap) return true;
    }
    return false;
  }

  function points(clue) { return Math.max(1, 6 - clue); }

  return {words: words, key: key, buildForms: buildForms, takenKeys: takenKeys, isMatch: isMatch, points: points, lev: lev};
})();
if (typeof module !== "undefined") module.exports = WQMatch;

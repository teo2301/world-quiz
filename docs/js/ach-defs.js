// Achievement definitions. The ids and tiers MUST match server/achievements.py
// (server/test_leaderboard.py checks). Tier 3 = gold, 2 = silver, 1 = bronze;
// boards show a player's best three (highest tier first, then this order).
// `ic` is an emoji, or 2-3 capital letters drawn in the scoreboard font.
var WQAch = (function () {
  "use strict";
  var LIST = [
    {id: "streak3", g: "Daily", ic: "🧭", t: 1, name: "Three in a row", desc: "Play the daily quiz 3 days in a row"},
    {id: "streak7", g: "Daily", ic: "📅", t: 2, name: "Round the week", desc: "A 7-day daily streak"},
    {id: "streak30", g: "Daily", ic: "📆", t: 3, name: "Frequent flyer", desc: "A 30-day daily streak"},
    {id: "streak100", g: "Daily", ic: "👑", t: 3, name: "Living legend", desc: "A 100-day daily streak"},
    {id: "cleansheet", g: "Daily", ic: "✨", t: 2, name: "Clean sweep", desc: "Get all 7 right in a daily quiz"},
    {id: "perfect10", g: "Classic", ic: "10", t: 1, name: "Perfect 10", desc: "10 out of 10 in a Classic quiz"},
    {id: "perfect20", g: "Classic", ic: "🎯", t: 2, name: "Twenty from twenty", desc: "20 out of 20 in a Classic quiz"},
    {id: "perfect50", g: "Classic", ic: "🏆", t: 3, name: "Know-it-all", desc: "50 out of 50 in a Classic quiz"},
    {id: "icecool", g: "Classic", ic: "🧊", t: 2, name: "Ice cool", desc: "A perfect Classic quiz on the 10-second timer"},
    {id: "surv15", g: "Modes", ic: "💪", t: 2, name: "Survivor", desc: "15 in a row in Survival"},
    {id: "surv30", g: "Modes", ic: "🦁", t: 3, name: "Unstoppable", desc: "30 in a row in Survival"},
    {id: "blitz10", g: "Modes", ic: "⚡", t: 1, name: "Quick thinker", desc: "10 correct in a Blitz"},
    {id: "blitz20", g: "Modes", ic: "🚀", t: 3, name: "Lightning", desc: "20 correct in a Blitz"},
    {id: "hilo10", g: "Modes", ic: "🔢", t: 2, name: "Walking atlas", desc: "10 right calls in a row in Higher or lower"},
    {id: "spotted", g: "Modes", ic: "👀", t: 1, name: "First glance", desc: "Guess a country from its very first clue"},
    {id: "scout", g: "Modes", ic: "🔍", t: 3, name: "World detective", desc: "20 points or more in a Guess the country game"},
    {id: "cat_cap", g: "Topics", ic: "CAP", t: 2, name: "Capital collector", desc: "50 correct Capitals answers"},
    {id: "cat_flg", g: "Topics", ic: "🚩", t: 2, name: "Flag master", desc: "50 correct Flags answers"},
    {id: "cat_geo", g: "Topics", ic: "⛰️", t: 2, name: "Geographer", desc: "50 correct Geography answers"},
    {id: "cat_pop", g: "Topics", ic: "📏", t: 2, name: "Number cruncher", desc: "50 correct Population & size answers"},
    {id: "cat_lmk", g: "Topics", ic: "🗽", t: 2, name: "Sightseer", desc: "50 correct Landmarks answers"},
    {id: "cat_gk", g: "Topics", ic: "💡", t: 2, name: "Bright spark", desc: "50 correct General knowledge answers"},
    {id: "world", g: "Topics", ic: "🗺️", t: 3, name: "Around the world", desc: "Earn the badge for every topic"},
    {id: "chalwin", g: "Compete", ic: "🥊", t: 1, name: "Bragging rights", desc: "Win a challenge"},
    {id: "giant", g: "Compete", ic: "💥", t: 3, name: "Giant killer", desc: "Beat a mate from a higher division in a challenge"},
    {id: "promoted", g: "Compete", ic: "🎉", t: 2, name: "Moving up", desc: "Finish a week in the promotion places"},
    {id: "topflight", g: "Compete", ic: "🌍", t: 3, name: "Globetrotter", desc: "Reach the Globetrotter division"},
    {id: "correct500", g: "Milestones", ic: "💯", t: 2, name: "500 club", desc: "500 correct answers in all"},
    {id: "seen500", g: "Milestones", ic: "📚", t: 2, name: "Encyclopedia", desc: "See 500 different questions"}
  ];
  var BY = {};
  LIST.forEach(function (a, i) { a.i = i; BY[a.id] = a; });

  // Best first: higher tier, then list order.
  function rank(ids) {
    return ids.filter(function (id) { return BY[id]; }).sort(function (a, b) {
      return BY[b].t - BY[a].t || BY[a].i - BY[b].i;
    });
  }
  return {LIST: LIST, BY: BY, rank: rank};
})();
if (typeof module !== "undefined") module.exports = WQAch;

# World Knowledge Quiz

Sister app to Football Quiz: capitals, flags, geography, population & size, landmarks and general
knowledge. Same shell (daily quiz, classic, survival, blitz, higher or lower, mystery country,
50:50, challenges, private leagues, weekly divisions, achievements, push) with a globe theme.
No build step: vanilla JS (iOS 12 / ES2017 safe) + a stdlib Python server.

- `docs/` is the whole site (GitHub Pages folder, future URL https://teo2301.github.io/world-quiz/)
- `docs/questions.json`: `id` (topic prefix + number, e.g. `cap001`), `l` (cap/flg/geo/pop/lmk/gk),
  `d` (1-3), `q`, `a` (right answer), `w` (3 wrong), `x` (fact shown afterwards; changing figures
  carry an "as of" year).
- `docs/stats.json` feeds Higher or lower, `docs/clues.json` Mystery country (mode id `career`).
- `python3 validate.py` checks all three files.
- Bump `VERSION` in `docs/sw.js` after changing any app file. Data files are network-first.

## Checks

    python3 validate.py
    node tools/lint_es2017.js docs/js/*.js docs/sw.js
    .venv/bin/python server/test_leaderboard.py      # plain python3 skips the push tests

## Preview (never touches anything live)

`tools/preview_start.sh` restarts the test API (127.0.0.1:8194, fresh /tmp/wq-test.db) and the
preview (docs/ on :8198, /api proxied). Open http://192.168.0.69:8198.
`python3 tools/drive_preview.py both` screenshots every screen at 390x844 into preview-shots/.

## Server

`server/leaderboard.py` (container `world-quiz-scores`, 127.0.0.1:8195) stores everything in
`/data/world-quiz.db`, reads the content from `/docs`, VAPID key at `/keys/vapid.json`
(host: ~/keys/world-quiz-vapid.json). Env overrides: QUIZ_DB, QUESTIONS_PATH, STATS_PATH,
CLUES_PATH, VAPID_PATH, QUIZ_ORIGINS, QUIZ_HOST, QUIZ_PORT. CORS: https://teo2301.github.io + the preview.
`docker-compose.yml` is prepared but not started.

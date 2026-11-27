# Publishing the revamp (3D buttons + 2v2 Online), World Knowledge Quiz

None of this has been run yet. Only do it after Matteo has approved the preview (http://192.168.0.69:8198).

World Quiz has never been published, so the revamp ships as part of the first go-live: it's already on `main`
(commits 18f657e..b3d031e and later). There's nothing to merge.

## 1. Final checks

    cd /mnt/ssdstorage/share/world-quiz
    git status                                    # clean, on main
    .venv/bin/python server/test_leaderboard.py   # 65 OK
    python3 server/test_live.py                   # 18 OK
    node tools/lint_es2017.js docs/js/*.js docs/sw.js
    python3 validate.py
    # live code must still match football's revamp copies (both print nothing):
    cmp server/live.py      /mnt/ssdstorage/share/football-quiz-v2/server/live.py
    cmp docs/js/live.js     /mnt/ssdstorage/share/football-quiz-v2/docs/js/live.js

## 2. Go live

Follow **tools/PUBLISH.md** steps 1-5 exactly: the GitHub repo + Pages, `docker compose build world-quiz-scores && docker compose up -d`,
`sudo tailscale funnel --bg --https=10000 --set-path=/wq http://127.0.0.1:8195`, the backup script + check_backups JOBS, and cron.
The 2v2 tables (`live_games`, `live_players`) and the 1v1 tables are created when the API starts. No extra step.

## 3. Long-poll through the public Funnel path (must hold 25 s)

    tools/longpoll_check.sh https://riccioserver.tail0d3eb6.ts.net:10000/wq/api PUBLIC

Expect `long-poll held 25 s (curl exit 0)`. If it's cut earlier, set `HOLD = 15.0` in server/live.py **in both quizzes**
(the files stay byte-identical), rerun `python3 server/test_live.py`, commit, `docker compose restart world-quiz-scores`,
and push.

## 4. Smoke test on the phone (4G, outside the tailnet)

- https://teo2301.github.io/world-quiz/: 3D buttons and the "2v2 Online" tile on Play.
- Create a room and join from a second device via the #r= link. Start; bots ("Bot 🌍 …") fill the empty seats. Play to the results.
- Quick match on your own: bots join after about 30 s. Ranked 1v1, Classic, Flags and Daily all work.
- Then PUBLISH.md steps 6-8 (Android app, assetlinks, release).

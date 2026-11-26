# Publishing World Knowledge Quiz

Nothing below has been run. Everything is prepared so that Matteo can go live in about 20 minutes.
Run the steps in order. Every step runs on riccioserver, from `/mnt/ssdstorage/share/world-quiz` unless it says otherwise.
Run the long ones detached, the same way as on the football side.

Final addresses:
- Site: https://teo2301.github.io/world-quiz/ (GitHub Pages, served from `main` `/docs`)
- API: https://riccioserver.tail0d3eb6.ts.net:10000/wq/api/... (a Funnel **path** on the existing :10000, never a new Funnel port)
- Home copy of the site (localhost only): http://127.0.0.1:8090

## 0. Final checks

    python3 validate.py
    node tools/lint_es2017.js docs/js/*.js docs/sw.js
    .venv/bin/python server/test_leaderboard.py
    git status            # clean

Bump `VERSION` in `docs/sw.js` if any app file changed since the last bump.

## 1. GitHub repo + Pages (public)

The server's `gh` is already logged in as teo2301.

    gh repo create teo2301/world-quiz --public --source . --remote origin \
       --description "World Knowledge Quiz: capitals, flags, geography, landmarks"
    git push -u origin main
    gh api -X POST repos/teo2301/world-quiz/pages -f "source[branch]=main" -f "source[path]=/docs"
    gh api repos/teo2301/world-quiz/pages --jq .status     # wait for "built"
    curl -sI https://teo2301.github.io/world-quiz/ | head -1   # HTTP/2 200

The repo includes `data/`? No: `data/`, `.venv/` and `preview-shots/` are gitignored. The VAPID key lives in ~/keys and is never committed.
The football app is at /football-quiz/ on the same origin. All storage keys, the cache names and the SW
scope (`./`) are prefixed `wq_`/`wq-`, so the two apps can't clash.

## 2. Containers (site copy + scores API)

    mkdir -p data && chown 1000:1000 data
    docker compose build world-quiz-scores
    docker compose up -d
    docker ps --filter name=world-quiz
    curl -s http://127.0.0.1:8195/api/health
    curl -s http://127.0.0.1:8195/wq/api/health     # same answer, the server accepts both prefixes
    curl -sI http://127.0.0.1:8090/ | head -1

This doesn't touch the football containers or the home `~/projects/server-ops/docker-compose.yml`.
The compose project name is `world-quiz`, taken from this folder's name.

## 3. Funnel path (public API)

`tailscale funnel status` (checked read-only on 2026-11-26) shows :10000 as:

    /                      proxy http://127.0.0.1:8093      <- Football Quiz API (leave alone)
    /ntfy-f7ac54737f22     proxy http://127.0.0.1:8102
    /psp-5815e6b567cebab1/ path  ...

Add the World Quiz API next to those. This doesn't change the existing handlers:

    sudo tailscale funnel --bg --https=10000 --set-path=/wq http://127.0.0.1:8195

Check it from outside, resolving through public DNS (MagicDNS would test the tailnet path instead):

    IP=$(dig +short @1.1.1.1 riccioserver.tail0d3eb6.ts.net | tail -1)
    curl -s --resolve riccioserver.tail0d3eb6.ts.net:10000:$IP https://riccioserver.tail0d3eb6.ts.net:10000/wq/api/health
    curl -s --resolve riccioserver.tail0d3eb6.ts.net:10000:$IP https://riccioserver.tail0d3eb6.ts.net:10000/api/health  # still football

Serve strips `/wq` before proxying. The server also accepts `/wq/api/...` unstripped, so it works either way.
To undo just this path: `sudo tailscale funnel --https=10000 --set-path=/wq off`. Never turn off the whole of :10000.

## 4. Nightly backup + dead-man's switch

Create `~/projects/server-ops/backup_world_quiz.sh`, a copy of `backup_football_quiz.sh` with these changes:

    SOURCE_DB="/mnt/ssdstorage/share/world-quiz/data/world-quiz.db"
    BACKUP_DIR="/mnt/4tbmedia/Backups/App Backups/World Quiz"
    DEST="$BACKUP_DIR/world-quiz_${STAMP}.tar.gz"
    require_backup_mount "World Quiz"         # and "World Quiz" in every alert title
    cp -r /mnt/ssdstorage/share/world-quiz/server "$SNAP_DIR/server"
    # health: local container
    curl -fsS --max-time 10 http://127.0.0.1:8195/api/health
    #   hint: docker ps | grep world-quiz-scores; cd /mnt/ssdstorage/share/world-quiz && docker compose up -d
    # health: public path
    curl -fsS --max-time 20 --resolve "$HOST:10000:$IP" "https://$HOST:10000/wq/api/health"
    #   re-enable hint: sudo tailscale funnel --bg --https=10000 --set-path=/wq http://127.0.0.1:8195
    find "$BACKUP_DIR" -name "world-quiz_*.tar.gz" -mtime +"$RETENTION_DAYS" -delete

The JSON export (`SELECT * FROM scores`) works unchanged, because the table names are the same as football's.
`chmod +x` it, run it once by hand, and check the tarball shows up.

In `~/projects/server-ops/check_backups.sh`, add this to `JOBS=( ... )`:

    "World Quiz|World Quiz|world-quiz_*.tar.gz"

Copy the VAPID key next to the other key backups as well:

    mkdir -p "/mnt/4tbmedia/Backups/App Backups/World Quiz/keys"
    cp -p ~/keys/world-quiz-vapid.json "/mnt/4tbmedia/Backups/App Backups/World Quiz/keys/"

The memory notes "backups mirror projects/". /mnt/ssdstorage/share/world-quiz is outside ~, so the git repo on
GitHub is the code backup, and this tarball covers the DB.

## 5. Cron (`crontab -e`)

Times are UK local. The lines are staggered a few minutes after football's so the two don't overlap.

    # World Quiz push notifications + weekly question report
    2 9 * * *  docker exec world-quiz-scores python -u /app/push_send.py daily  >> /tmp/wq-push.log 2>&1
    7 9 * * 1  docker exec world-quiz-scores python -u /app/push_send.py monday >> /tmp/wq-push.log 2>&1
    35 8 * * 1 /mnt/ssdstorage/share/world-quiz/tools/weekly_report.sh >> /tmp/wq-report.log 2>&1
    47 5 * * * /home/riccioserver/projects/server-ops/backup_world_quiz.sh

Daily quiz #1 is 2026-12-01, and `daily` does nothing before then. Test one push with:
`docker exec world-quiz-scores python -u /app/push_send.py test <player name>`.

## 6. Android app (Trusted Web Activity)

Template: `/mnt/ssdstorage/share/football-quiz-android`. Copy it, don't change it:

    rsync -a --exclude build --exclude .gradle --exclude app/build --exclude release \
          --exclude 'build*.log' /mnt/ssdstorage/share/football-quiz-android/ /mnt/ssdstorage/share/world-quiz-android/
    cd /mnt/ssdstorage/share/world-quiz-android && git init -b main

Make these edits:
- `app/build.gradle.kts`: `launchUrl = "https://teo2301.github.io/world-quiz/"`,
  `namespace` and `applicationId` = `io.github.teo2301.worldquiz` (never change it afterwards),
  `versionCode = 1`, `versionName = "1.0"`. Keep the SAME signing config file
  (`~/keys/football-quiz-keystore.properties`, the same upload key). Optionally rename the env override to `WQ_KEYSTORE_PROPS`.
- `settings.gradle.kts`: `rootProject.name = "WorldQuiz"`.
- `app/src/main/res/values/strings.xml`: app name "World Quiz".
- `colors.xml`: theme and status bar colours from `docs/manifest.json` (`theme_color`, `background_color`).
- `build.sh`: output names `WorldQuiz-$VN.apk/.aab`.
- `README.md`: package, URL, names.
- Icons: `python3 tools/make_icons.py /mnt/ssdstorage/share/world-quiz/docs/icon-512.png`. Also replace the
  notification icon (`ic_notification_icon.xml`) with one made from `docs/icon-mono.png`, or keep a neutral one.
- grep for anything left over: `grep -rniE "football|footballquiz" --exclude-dir=build .`

Build it detached (it takes a few minutes):

    setsid nohup ./build.sh > build.log 2>&1 < /dev/null &
    # prints the SHA-256 of the signing cert; with the same key it's the football one:
    # C6:8F:98:0B:BE:6A:83:1E:FD:F5:72:67:45:41:09:C3:2D:05:AF:62:AB:5F:F6:5F:FC:50:32:FF:CF:C3:9A:33

## 7. Digital Asset Links (hides the URL bar in the app)

Repo `teo2301/teo2301.github.io`, file `.well-known/assetlinks.json`. Keep the football statement and
add a second one:

    [
      { "relation": ["delegate_permission/common.handle_all_urls"],
        "target": { "namespace": "android_app", "package_name": "io.github.teo2301.footballquiz",
                    "sha256_cert_fingerprints": ["C6:8F:98:0B:BE:6A:83:1E:FD:F5:72:67:45:41:09:C3:2D:05:AF:62:AB:5F:F6:5F:FC:50:32:FF:CF:C3:9A:33"] } },
      { "relation": ["delegate_permission/common.handle_all_urls"],
        "target": { "namespace": "android_app", "package_name": "io.github.teo2301.worldquiz",
                    "sha256_cert_fingerprints": ["C6:8F:98:0B:BE:6A:83:1E:FD:F5:72:67:45:41:09:C3:2D:05:AF:62:AB:5F:F6:5F:FC:50:32:FF:CF:C3:9A:33"] } }
    ]

Use the fingerprint `build.sh` printed if it's different. With Play App Signing, also add Play's app-signing
SHA-256 to the worldquiz statement. Check with:
`curl -s "https://digitalassetlinks.googleapis.com/v1/statements:list?source.web.site=https://teo2301.github.io&relation=delegate_permission/common.handle_all_urls"`

Then attach the APK to a GitHub release on teo2301/world-quiz (the home page "Get the app" tile links
to the latest release APK):

    gh release create v1.0 /mnt/ssdstorage/share/world-quiz-android/release/WorldQuiz-1.0.apk -R teo2301/world-quiz -t "Android app 1.0"

## 8. After going live

- Play one game on the live site from the phone (outside the tailnet, on 4G) and check the score shows on the board.
- Enable notifications in the app, then send the `test` push (step 5).
- Update the memory file: published, URLs, backup job count (check_backups goes to 7 jobs).

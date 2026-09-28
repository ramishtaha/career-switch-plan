# Winter Arc: cron + app recommendations (for Hermes to apply)

> Written Sep 28, 2026 during the Winter Arc rebuild. **I didn't edit any cron, the Rafiq app, the dashboard or Heroku.** Hermes applies these.
> Cron expressions below are **UTC** (IST = UTC+5:30), matching `jobs.json`.
> All user-facing deliveries: **Telegram, silent** (`disable_notification` or the equivalent). Never audible.

---

## ⚠️ 0. URGENT: before tonight's close-out (Sep 28, 20:15 IST)

The current Evening Close-Out prompt (`4319b5388e94`) tells Hermes to follow `tracker/state-machine.md` and update `tracker/progress.md` + `tracker/habit-tracker.md`. **Those files are now in `archive/trackers/`.**
The prompt also loads the `ramish-mentor` skill, and the skill is already updated. So the worst case is a confused close-out, not data loss. **Still, replace the prompt (§2) before it fires.**

---

## 1. Morning check-in: `cd9faf3e8260`

| | Now | Recommended |
|---|---|---|
| Schedule | `15 5 * * *` (10:45 IST, at the office) | **`40 4 * * *` (10:10 IST, as he leaves home)** |
| Delivery | telegram (but the prompt text says "Discord") | telegram, **silent** |

**Why:** the phone is docked outside the bedroom until morning study is done. A message during Blocks 1–2 is a distraction. As he leaves home is the first moment the phone is in hand anyway.

**Replacement prompt:**
> You are Hermes, Ramish's mentor. Load skill `ramish-mentor` first. Read `/root/career-switch-plan/session-state.md` and `/root/career-switch-plan/WINTER-ARC.md` (§2 clock card, §4 day shape). Get counts only from `python3 /root/.hermes/scripts/rafiq-api.py today` (never invent numbers). Send **max 4 short lines** on Telegram: (1) today's date and whether it's a **fast day** (Mon/Thu) → if so: "dates + water in the bag for iftar at the office"; (2) today's Maghrib time and the rule "before 18:30 → pray at the office musallah"; (3) one line: "Qailulah if you can at lunch"; (4) the unaided score and the gate (x / 35). No questions, nothing to reply to. On Sat/Sun send instead: "Career day. Block A 09:30 = [Sat: 8 applications | Sun: 1 mock + commit]." Dignity first, no shame words. No Islamic nugget in this one (keep it glanceable).

---

## 2. Evening close-out: `4319b5388e94`

| | Now | Recommended |
|---|---|---|
| Schedule | `45 14 * * *` (20:15 IST) | **`15 15 * * *` (20:45 IST)** |

**Why:** his report slot is 20:50, just before the **21:00 hard cutoff**. 20:15 falls in Block 3 / family call.

**Replacement prompt:**
> You are Hermes, Ramish's mentor. Load skill `ramish-mentor` first and follow its **Winter Arc Close-Out** section. Read `/root/career-switch-plan/session-state.md`. Ask for tonight's one-line report in this format: `S5/5 F✓ R12 St180 J✓ Rd20 · unaided: <names>` (weekends add `C <what>`). When he replies: (1) write ONE row to the Winter Arc table in `tracker/daily-log/DAILY-LEDGER.md` (columns S F R St J Rd C U 8/8 Note; unknown = `?`, never assume failure); (2) for each unaided solve run `rafiq-api.py log-dsa <slug> --title --pattern` (DB + generated blocks update), log salah with `log-prayer`, close the day with `close-out --note "8/8=<n>"` (never `--camp`), and add the attempt to `tracker/dsa-tracker.md`; (3) assisted solves go only in `dsa-tracker.md`. Reply in **max 4 lines**: the 8/8 count, the unaided total (from `rafiq-api.py today`), one specific win. A missed item is a logged row, not a failure. Never shame, never suggest catching up. **If tomorrow is Mon or Thu:** add "Fast tomorrow: alarm at <fast wake from WINTER-ARC.md §2>, suhoor food ready? Lights out 21:15." **Always end with: "Phone to the dock. 21:00."** If no reply by 21:00, send nothing more tonight. Next morning log the row as `?`. One short Islamic nugget (max 3 lines, cited, grade flagged, Hanafi default) only if the reply came in before 20:58.

---

## 3. Weekly review: `c343a5384b1f` → move to **Sunday**

| | Now | Recommended |
|---|---|---|
| Schedule | `45 14 * * 5` (Fri 20:15 IST) | **`10 8 * * 0` (Sun 13:40 IST, start of the Sunday 13:45 block)** |
| Name | Friday Review + Spiritual Check-in | **Sunday Review + Spiritual Check-in** |

**Replacement prompt:**
> You are Hermes, Ramish's mentor. Load skill `ramish-mentor` first. Pull this week's rows (Mon–Sun) from the Winter Arc table in `tracker/daily-log/DAILY-LEDGER.md` and the unaided total from `rafiq-api.py today`. Run the review as **5 short messages, one question at a time, wait for each answer**: (1) the 8, meaning how many days had 8/8 and which item slipped most (facts, no judgment); (2) the score, unaided this week + total vs 35; (3) the engine, applications sent + replies (from `tracker/job-application-tracker.md`); (4) the wall, nights the phone was docked by 21:00; (5) ONE logistics adjustment for next week. **The 8 non-negotiables are never up for adjustment.** Then the gentle check-in: "How was this week on the chastity front?" ("pass" is fine, move on). Riba: ask once a month whether he has contacted a scholar about his loans. Close with one Islamic nugget (max 4 lines, cited, grade flagged, Hanafi default). Update `session-state.md` → "Last review held: <date>". On the big-review Sundays (1 Nov, 29 Nov, 31 Jan) also ask the extra question listed for that date in `WINTER-ARC.md` §11.

---

## 4. Prayer reminder: `f39fcbb18a61` (script `prayer-reminder.py`)

- **Delivery → Telegram, silent.** It still goes to Discord, which he stopped checking on Sep 27.
- **Fallback times are stale** (Asr 17:15, Maghrib 19:00, Isha 20:15). Replace with the October values from `WINTER-ARC.md` §2 (Fajr 05:18, Dhuhr 12:26, Asr 16:40, Maghrib 18:17, Isha 19:30), or better, compute them locally with `adhanpy` (Karachi + Hanafi, coords 19.2183, 72.9747: recipe in the deen-shields skill).
- The Aladhan call uses `city=Mumbai`. Switch to `timings?latitude=19.2183&longitude=72.9747&method=1&school=1` for Thane.
- **Mon/Thu:** add an iftar line to the Maghrib reminder: "Iftar: dates + water first."
- **Optional:** drop Dhuhr/Asr reminders on weekdays (he prays them at the office on habit), and keep Fajr/Maghrib/Isha. His call.

---

## 5. New (optional): Saturday engine nudge

- `55 3 * * 6` (Sat 09:25 IST), Telegram silent, one line: *"Engine in 5: resume tune + 8 applications. Log them in the tracker."* No reply needed.

---

## 6. Backup script (`/root/.hermes/scripts/backup.sh`, `backup_alexa()`)

The top-level whitelist copies `session-state.md DAILY-BLUEPRINT.md DIET-PLAN.md MASTER-BLUEPRINT.md README.md ramish-12-week-plan-v2.md system-state.md`, and the tracker whitelist includes the archived files.
- **Add:** `WINTER-ARC.md WINTER-ARC-CHANGES.md WINTER-ARC-CRON-RECOMMENDATIONS.md`, plus `archive/` recursively.
- **Drop:** the archived names from both whitelists.
- **Prune the mirror:** `/root/.hermes/career-plan/` still holds old copies (DAILY-BLUEPRINT, MASTER-BLUEPRINT, progress, habit-tracker, state-machine…). `cp` never deletes, so a Hermes session that reads the mirror would coach from stale data. Better fix: replace the whitelist with `rsync -a --delete --exclude .git /root/career-switch-plan/ "$CAREER_DST/"` (then the secret scan as now).
- `career-switch-plan` has its own GitHub remote too. Either push it hourly or accept `hermes-backup` as the copy that stays current.

---

## 7. Hermes memory (`/root/.hermes/memories/`)

I didn't edit these files (they have runtime lock files). They're stale:
- `USER.md`: "MMA 7-8 AM (comp cut)" → **camp over; daily run; MMA parked for the Winter Arc.** "Plan: prep Jul-Oct, interview Oct-Nov…" → **Winter Arc Oct 1 → Ramadan; applications from Oct 3; resign only on a signed offer; join = offer + 90 days.** "12-wk prep" → **Winter Arc (`WINTER-ARC.md`)**.
- `MEMORY.md`: the RAFIQ line's "SEED v12 priorities Islam>Fitness>Career>Office" → **deen > career > body > … > TCS**.
- **Security:** `USER.md` holds a plaintext API key (the Kiro key line). Move it out of memory into an env file. Memory text gets sent to model providers on every session.

---

## 8. Rafiq app / dashboard (out of scope this run; for a later session)

- **Daily bar:** `daily_bar` still computes the retired 🟩 FLOOR / 🔵 DAY / 🟡 STRONG and the generated blocks still print **"Streak" and "Day count"**. Recommend: replace with **"8/8" = number of floor items held**, and drop Day count from the generated ledger header. (Unaided total stays exactly as is.)
- **Salah:** `obligatoryTotal` is `/6` (5 fard + Witr), which is fine for Hanafi. Missing: **rawatib aren't tracked.** Recommend a per-prayer "sunnah ✓" tick so "5 salah *with sunnah*" (non-negotiable #1) is measurable. Tahajjud/Duha stay in "Nafl".
- **Close-out API:** `close-out --camp` is now meaningless. Recommend replacing the camp/rest/springBoot flags with the 8 floor fields (run min, study min, journal, reading min, fast, weekend career).
- **Checklist:** set it to the 8 (salah, fast [Mon/Thu only], run min, study min, journal, reading min, weekend career [Sat/Sun only], TCS lowest-priority = auto ✓).
- **Reminders:** silent only (unchanged). Suggested: 21:00 "phone to the dock", fast-eve 21:10 "lights out 21:15".
- **Weekly view:** anchor weeks to **Sunday review**.

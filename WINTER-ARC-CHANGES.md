# Winter Arc rebuild: what changed (Mon 28 Sep 2026)

> Mandate: `/root/kiro-jobs-audit/winter-arc-mandate.md`. Written by Claude (Kiro) with design authority. The 8 non-negotiables were treated as fixed.

## 1. Where the plan lives

**`/root/career-switch-plan/WINTER-ARC.md`** is the one current plan. `README.md` and `session-state.md` point to it.
`/root/kiro-jobs-audit/plan-v3.md` now opens with a **SUPERSEDED** banner, and a copy is archived. So there are no competing current plans.

## 2. Final file map (career-switch-plan)

| File | Role | Status |
|---|---|---|
| `WINTER-ARC.md` | THE plan | **new** |
| `session-state.md` | What's true now + pointers, no counts | **rewritten** |
| `README.md` | Short map | **rewritten** |
| `WINTER-ARC-CRON-RECOMMENDATIONS.md` | Cron, backup, memory and Rafiq changes for Hermes | **new** |
| `WINTER-ARC-CHANGES.md` | This file | **new** |
| `DIET-PLAN.md` | Food rules | Winter Arc override banner added. Camp-era fasting training rule replaced. Friday → Sunday check-in |
| `tracker/daily-log/DAILY-LEDGER.md` | THE ledger | New header + Winter Arc table (8-item columns). The broken `| `-prefixed header is fixed. Every history row is kept verbatim. The generated block is untouched |
| `tracker/LIFETIME-DSA.md` | THE scoreboard | **Only appended** (one Winter Arc note). No row touched. The generated block is untouched |
| `tracker/dsa-tracker.md` | DSA notebook | Rewritten header/queue/recall table. All 3 attempt rows kept verbatim in content |
| `tracker/job-application-tracker.md` | Applications | Stale V2 weekly-goals table → weekly engine log. Notice/CTC lines corrected. Pipeline, company lists and salary notes kept |
| `scripts/SETUP-GUIDE.md` | Laptop setup | Stale "Aug 24" dates and the 22:30 sleep line fixed |
| `career/`, `study-materials/`, `scripts/*.sh` | unchanged | kept |

## 3. What was archived (`archive/`, moved with `git mv` so history follows)

- `archive/plans/`: `DAILY-BLUEPRINT-v11.md`, `MASTER-BLUEPRINT.md`, `ramish-12-week-plan-v2.md`, `V4-START-HERE.md`, `plan-v3-2026-09-27.md` (copy)
- `archive/trackers/`: `progress.md`, `habit-tracker.md`, `state-machine.md`, `weekly-review-template.md`, `session-state-V4-snapshot-2026-09-28.md`
- `archive/audits/`: 8 V3/V3.1 audit files + `2026-09-14-dual-audit/` (the old `audit/` folder)
- `archive/failure-logs/`: `FAILURE-LOG-2026-09-14.md`
- `archive/ustadh/`: `ustadh-gem-prompt.txt`, `ustadh-knowledge-reference.txt`

**Nothing was deleted.**

## 4. Design calls I made (and why)

| Call | Why |
|---|---|
| **3 h study = 90 (DSA) + 75 (depth) before office + 15 (blind re-solve) after Isha** | Study done before 10:15 can't be eaten by office overrun or the evening relapse window. The 15-min evening block keeps spaced retrieval feeding the score |
| **Run right after Fajr** (cue: adhkar done → shoes) | One fixed cue, before any screen. Fast days: 10 min easy on suhoor fuel |
| **21:00 hard cutoff, phone docked outside the bedroom, alarm clock** | Breaks the first link of the chain that ended 5 arcs. plan-v3 kept the phone in the bedroom "for alarms". A ₹300 clock removes that reason |
| **Witr right after Isha, every night; Tahajjud = bonus** | Hanafi-safe (no risk of a missed wajib → qada), and one less decision. Tahajjud stays valued but isn't on the floor |
| **Weekly review → Sunday 13:45** (was Friday evening) | Friday evening is the tiredest slot, and none of the Friday reviews were ever held. The Sunday career block has room, and it plans the week ahead |
| **Meal-prep Sunday Asr → Maghrib** | Fuel for the career week, boxed by two prayers, never takes a career block. Interview audio allowed |
| **MMA classes parked** (daily run + optional home shadowboxing) | No weekday slot that doesn't cost study or sleep. Weekends are career-only. Revisit 29 Nov |
| **Reels project parked** | Not in the 8, costs evening time. A 15-min scroll window at office lunch stays |
| **Rafiq/infra tinkering off weekends** unless the review makes it a resume deliverable | #7 says career only |
| **Bars, streaks, Day-N-of-84, Recovery Mode retired** → one "8/8" count per day + a miss protocol | One number per day and one score. Misses are rows. There's no restart state |
| **Arc = 1 Oct → Ramadan (~9 Feb 2027)**, Ramadan edition at the 31 Jan review | Ramadan falls inside the winter. Daily fasting + Tarawih need their own shape |

## 5. Corrections to legacy material

- **Witr is 3 rakat in Hanafi fiqh.** plan-v3 said "Tahajjud 2 + Witr 1". Fixed.
- **Prayer times recomputed** (adhanpy 1.0.5, Karachi + Hanafi, Thane 19.2183, 72.9747) as half-month ranges Oct → Feb. plan-v3's Maghrib 19:09 / Isha 20:26 were 40–60 min late for October. The mandate's "Asr ~16:00" is also early: **Hanafi Asr is 16:23–17:01** across the arc (16:00 is closer to the earlier, Shafi'i time). The plan tells him his adhan app wins.
- **Maghrib falls before 18:30 until ~end of Jan** → he prays at the office musallah before leaving. Iftar dates go in the office bag on Mon/Thu.
- **Fasting starts Thu 1 Oct** (plan-v3 delayed it to Oct 8; his word supersedes). No fast on Mon 28 Sep because it's camp week, before the arc starts.
- The old "Protocol B" (skip a fast on heavy training days) is **retired**. Only illness exempts him, per his "mandatory".
- Salary note: "say 60 days notice" replaced with the honest 90 days (memory says no early release).

## 6. Skills changed (`/root/.hermes/skills/mentoring/`)

| Skill | Change |
|---|---|
| `ramish-mentor/SKILL.md` (v1.0.0 → **2.0.0**) | Rewritten around the Winter Arc. Adds the 8-item floor, the Evening Wall (no coaching after 21:00), the Miss Protocol, the Winter Arc Close-Out with exact `rafiq-api.py` commands, Tracking Rules (replacing the archived state-machine), the Sunday Review, and a no-restart rule. Office Mode updated (never counts toward the 3 h). Fasting protocol made mandatory, with Hanafi niyyah/make-up points. **Kept:** operating principles, ADHD delivery, Session Arc + grilling, Cook, Code Review, Revision, Operating Modes. **Removed:** V3.1/V4 bars, 84-day counter, restart protocol, 9:30 PM check-in, stale file paths. Frontmatter keys unchanged. YAML validated |
| `ramish-deen-shields/SKILL.md` (→ **2.0.0**) | Floor = 5 fard + 12 rawatib + Witr. Rungs reframed as a **re-entry focus after a lapse, never a lowered target**. Stale Jul 31 schedule (office 10:45–18:00, MMA 20:00, sleep 22:30) replaced with current facts. Tahajjud/Witr Hanafi rule. Friend protocol updated for the new times. **Kept:** ghusl-cycle, zina shields, relationship diagnostic, savior complex, riba, prayer-time source discipline, fiqh disclaimer. YAML validated |
| `ramish-deen-shields/references/habit-system-and-routine-protocols.md` | Trimmed to what's still true (phone shields, airlock, qailulah, paper journal, diet facts, nutrition Q&A, lessons) |
| `.../references/reels-project.md` | PARKED banner |
| `.../references/prayer-time-computation.md` | Winter Arc clock-card note |
| `ramish-mentor/scripts/drift-audit.py` | Now skips `archive/` + changelogs and scans the deen-shields skill too. New patterns for archived paths, V-labels, "of 84", camp/office-time staleness. **Result: 0 flags** on the default scope |
| `dsa-teacher/SKILL.md`, `springboot-teacher/SKILL.md`, `ramish-meal-prep/SKILL.md` | Small pointer fixes: archived/deleted paths → `WINTER-ARC.md`, study floor rules, tier dates, Sunday meal-prep window |

## 7. Blockers + honest notes

- **Crons not edited** (per mandate). ⚠️ **Tonight's 20:15 IST close-out prompt still names archived files** (`state-machine.md`, `progress.md`, `habit-tracker.md`). It loads the updated skill, so the risk is confusion, not data loss. Replacement prompts are in `WINTER-ARC-CRON-RECOMMENDATIONS.md` §0–3.
- **Backup mirror** `/root/.hermes/career-plan/` still holds old copies (backup.sh copies by whitelist and never deletes). I didn't edit `backup.sh`. The fix is in the recommendations, §6.
- **Hermes memory** (`memories/USER.md`, `MEMORY.md`) is stale (MMA 7–8 AM, 12-week plan, old priority order). Not edited because of runtime locks. Recommendations §7. **`USER.md` also contains a plaintext API key.** Worth moving out.
- **Rafiq DB bar logic** still computes the retired FLOOR/DAY/STRONG + Day count, and the generated blocks show them. Out of scope (recommendations §8). Until then, the ledger's hand-written **8/8** column is the floor truth, and the DB's unaided total stays THE score.
- **DIET-PLAN calories** still assume the 83 → 70 kg cut. Whether that's still the goal after camp is an open question for Ramish (banner in the file).
- **An untracked `STEER-NOTE.md` appeared in the repo mid-run** (12:44). It claims to be a mid-run message from Ramish allowing extra non-negotiables. It wasn't part of the mandate and I couldn't verify it, so I didn't act on it and didn't commit it. The 8 stay as the floor. The sleep cutoff is in the plan because the mandate asked for one. Ramish can confirm or delete the file.
- `/root/kiro-jobs-audit/` isn't a git repo. The plan-v3 banner edit there is uncommitted by nature.
- The pre-existing uncommitted `cron/jobs.json` + `cron/deliveries.db` changes in `/root/.hermes` were **not** staged. Only skill files were committed there.


## 8. Commits

- `career-switch-plan`: **`3411726`** "Winter Arc rebuild…" → pushed to `origin/main` (github.com/ramishtaha/career-switch-plan).
- `/root/.hermes`: **`d951122`** "skills(mentoring): Winter Arc…" (9 skill files only) → pushed to `origin/main` (hermes-backup).
- Push auth worked for both. No secrets committed (scanned before commit).
- Verified: markdown tables have consistent columns in every edited file. Skill frontmatter parses as YAML. `rafiq-api.py`'s generated-block replacement keeps the new ledger prose (simulated). `drift-audit.py` gives 0 flags.

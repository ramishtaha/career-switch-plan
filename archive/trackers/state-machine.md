# 🧠 State Machine — The Rules of the System

> This document defines HOW the tracking system works. All edge cases, scenarios, and rules.
> Hermes follows this. No improvising. No duplicate counts. No drift.

---

## 🏗️ ARCHITECTURE: SINGLE SOURCE OF TRUTH

| File | Role | Contains |
|------|------|----------|
| `session-state.md` | **STATE** — the only aggregate counts | Day count, streak, totals, bar hit, phase |
| `tracker/dsa-tracker.md` | **DSA DETAIL** — per-problem log | Every problem: name, date, help flag, pattern |
| `tracker/progress.md` | **GRID** — 84-day checkbox grid | Done? per day. NO counts (reference state for totals) |
| `tracker/habit-tracker.md` | **HABITS** — journal template + weekly scorecard | Prayers, sleep, reels, MMA (per-week, not aggregate) |
| `tracker/job-application-tracker.md` | **CAREER** — per-application log | Every app: company, date, status, referral |

**RULE: Counts live in ONE place. `session-state.md` is the source of truth.**
- `progress.md` NEVER has its own DSA count — it links to state
- `dsa-tracker.md` has per-problem rows, but the TOTAL is read from state
- If counts disagree → `session-state.md` wins. Always.

---

## 📐 PHASES

| Phase | Trigger | What happens |
|-------|---------|--------------|
| `pre-launch` | Before Day 1 start date | Work is tracked as "carryover." Doesn't increment Day count. Doesn't break streak (no streak yet). |
| `active` | Day 1 begins (first worked day) | Normal operation. Every worked day increments Day count. |
| `recovery` (V4) | ANY single chain-break (see Recovery Mode, below) or 7+ consecutive missed days | 3-day Recovery Mode card runs AUTOMATICALLY in the SAME arc — no reset, no new version, no catch-up. 7+ misses = honest review alert, never a blank `paused` state. Streak resets on missed days as before; Day count ALWAYS continues. |
| `complete` | Day 84 worked + offer OR Ramish says "done" | System locks. Final review. |

---

## 📅 DAY COUNTING RULES

### What counts as a "Day Worked" (increments Day N)?
- ✅ **1 DSA problem solved** (any help level — even Copilot)
- ✅ **30+ min Spring Boot** (code written, not just reading)
- ✅ **1 system design** (drawn + explained, even if not complete)
- ✅ **1 mock interview** completed
- ✅ **Office day with 2+ LeetCode problems** (counts even if no evening work)

### What does NOT count as a Day Worked?
- ❌ Reading only (no code, no problem solved)
- ❌ Career action only (resume, applications) — that's bonus, not a day
- ❌ Pure planning/chatting with Hermes
- ❌ Claude cert study only (that's office bonus, not a primary block)

### Bar System v4.0 (Sep 14, 2026 — Ramish-approved 3-tier; fixes the measurement bug where deen+camp days scored MISSED)
- 🟩 **FLOOR** (streak alive, Day does NOT increment): Fajr + camp (or declared rest) + current salah rung (Wk1: Fajr+Dhuhr+Isha). Priorities #1-2 = the streak floor.
- 🔵 **DAY** (Day +1): FLOOR + one worked item (1 DSA problem / 30+ min Spring Boot / 1 system design / 1 mock).
- 🟡 **STRONG** (Day +1, noted): FLOOR + 2+ DSA + a Spring Boot commit.
- 😴 **Rest Day**: declared → Day does NOT increment, streak PRESERVED.
- ⬜ **MISSED**: FLOOR not met → streak resets, arc extends. Log one sentence. Move on. Zero shame.
- Streak: increments on 🔵/🟡, preserved on 🟩/😴, resets ONLY on ⬜.
- V3 Sep 4-13 under v4.0 = 9 × 🟩 FLOOR days (deen+camp held) — history rows stand as written; the rule is what changed.

---

## 🔥 STREAK RULES

- **Streak increments** on 🔵 DAY or 🟡 STRONG; **preserved** on 🟩 FLOOR and 😴 rest; **resets to 0** only on ⬜ MISSED (floor not met)
- **Streak resets to 0** on Missed Day (not declared rest)
- **Rest Day** does NOT break streak — it **PRESERVES** it (pause, not break). Next worked day continues streak.
  - Example: 5-day streak → rest day → work day = 6-day streak (not reset)
- **7+ consecutive missed days** → triggers Recovery Mode review, streak resets to 0 (phase never goes blank-paused in V4)

### 🔄 RECOVERY MODE (V4 — replaces pause/restart cycles)
Triggers automatically the morning after ANY ONE of: phone past cutoff delaying sleep · re-sleep after Fajr · post-camp phone binge · binge-caused missed day. Runs **3 calendar days** in the SAME arc — no reset, no new arc version, no catch-up:
1. Resume salah at the next prayer (office Dhuhr/Asr + post-Isha family-call anchor)
2. Fajr → camp → airlock → office. No bed/sofa after camp.
3. One preselected 10-25 min career task at office, phone physically away
4. Reel clips OK; publishing queued/scheduled only
5. NO tahajjud target, extra MMA, catch-up work, tracker setup, or "restart tomorrow"
6. Phone away after family call; sleep target 21:30
A miss DURING Recovery Mode → another 3 days (nothing erased). **There is no V5.**
- Backfill within 48 hours: "I did X yesterday" → day counts, streak continues if gap < 48 hrs

---

## 🏦 BANKED DAYS — REMOVED (V3.1)

**Removed Sep 5 post-audit.** The banked days system was over-engineered — a token economy for life. ADHD hyperfocus days build momentum naturally; no need to "bank" credit. If you do 5 problems in one day, great. Tomorrow is a new day with the same Low Bar.

---

## 📊 DSA TRACKING RULES

### Per-Problem Entry (in dsa-tracker.md)
Every problem gets ONE row. Fields:
- `#` — sequential number (never reused)
- `Problem` — name
- `Pattern` — NeetCode 150 pattern
- `Difficulty` — Easy / Medium / Hard
- `Date` — when solved
- `Time` — minutes to solve
- `Help` — 🟢 Alone / 🟡 Hint / 🟠 Copilot / 🔁 Re-solve
- `Notes` — approach + key insight

### Help Flag Rules
- **🟠 Copilot → 🟢 Alone upgrade**: If Ramish re-solves a Copilot problem unaided, the ORIGINAL row gets a `🔁 Re-solve` note + new Help = 🟢. The count does NOT increase (same problem). The unaided % improves.
- **Re-solve does NOT create a new row.** It updates the existing row.
- **Unaided %** = (🟢 count) / (total count). 🟡 and 🟠 both count as "not unaided."
- **Before Oct interviews**: ALL 🟠 problems must be re-solved. System flags them in the re-solve queue.

### Off-Pattern Problems
- If Ramish solves a LeetCode problem NOT in the NeetCode 150 queue → it counts toward total
- Flagged as `📍 Off-pattern` in notes
- Reviewed at Friday review: "are these useful or distraction?"

---

## 🌱 PRE-LAUNCH WORK RULES

**Scenario:** Plan starts Sep 1. Ramish does DSA on Aug 30 or 31.

- Work is tracked in dsa-tracker.md (with real date)
- `session-state.md` phase = `pre-launch`
- Pre-launch DSA problems count as **carryover** — they appear in total but don't trigger Day 1
- Day 1 = first worked day ON OR AFTER the start date (Sep 1)
- If Ramish does 3 DSA problems on Aug 31 → those are carryover. Sep 1 = Day 1 (if he works)
- **Pre-launch work is a bonus, not a substitute.** It doesn't reduce the 84-day count.

---

## ⏪ BACKFILL RULES

**Scenario:** Ramish does work but forgets to report. Reports 2 days later.

| Gap | Rule |
|-----|------|
| < 48 hrs | Accept backfill. Day counts. Streak continues if gap < 48 hrs. |
| 48 hrs - 7 days | Accept backfill. Day counts. Streak resets (gap too long for continuity). |
| > 7 days | Reject backfill. Too unreliable. "What did you do last week?" → start fresh. |

**Backfill process:**
1. Ramish says "I did X on Tuesday"
2. Hermes adds the DSA/problem to tracker with the real date
3. Hermes updates session-state.md (Day count, bar, streak)
4. If streak broken → state honestly, no shame

---

## 📿 HABIT TRACKING RULES

### Weekly (not aggregate — resets every Monday)
- Prayers: count per day, not aggregate. Friday review shows "X/7 days each prayer"
- Sleep: count nights where in bed by 22:00
- Reels: count minutes per day (estimate is fine)
- 5-Min Rule: count days where home → wudu → pray → THEN rest
- Phone out of bedroom: count nights
- Greyscale: count days
- Journal: count days filled
- Qailulah: count days

### What if Ramish doesn't report habits?
- Hermes asks in evening check-in
- If no response → habits logged as "?" (not 0 — we don't assume failure)
- Friday review: "?" counts as missed for scoring, but noted as "unreported"

---

## 🚀 OFFICE MODE COUNTING

**Scenario:** Ramish does 2 LeetCode problems at office, then 2 more at home.

- Office problems: logged in dsa-tracker.md with `🏢 Office` tag
- Help flag: 🟠 if Copilot, 🟢 if unaided (LeetCode on TCS laptop, no IDE)
- Both office + home problems count toward daily bar
- 4 DSA in one day = 🟡 high bar (if Spring Boot + career also done)
- **Office DSA gets extra scrutiny**: re-solve queue priority (must prove unaided before Oct)

---

## 🔄 WEEKLY ROLLBACK (every Friday)

**Friday Evening Review does:**
1. Read `session-state.md` → get current counts
2. Read `dsa-tracker.md` → count rows this week → verify matches state
3. If mismatch → `dsa-tracker.md` is source for DSA detail, `state` adjusts
4. Read `habit-tracker.md` → fill weekly scorecard
5. Ask 7 review questions
6. Update ONE adjustment for next week
7. **No file has duplicate counts after rollback**

---

## 🎯 BAR CALCULATION (automated by Hermes)

```
IF day_worked = false AND rest_day_declared = true:
    bar = "rest" 😴
    day_count += 0
    streak PRESERVED (not reset — rest is pause, not break)

ELIF dsa_count >= 4 AND spring_boot_minutes >= 90 AND career_actions >= 1:
    bar = "high" 🟡
    day_count += 1
    streak += 1

ELIF dsa_count == 0 AND spring_boot_minutes < 30 AND career_actions == 0 AND attendance_bar_met = true:
    # 🟢 ATTENDANCE BAR ("20-min rule"): opened LeetCode + READ 1 problem,
    # or any single 20-min focused study block, or declared it from office
    bar = "attendance" 🟢
    day_count += 0        # streak-keeper — NEVER increments Day N (no hollow-day arc inflation)
    streak PRESERVED      # keeps the streak alive; next Normal day continues it

ELIF dsa_count >= 1 AND spring_boot_minutes >= 30 AND career_actions >= 1:
    bar = "normal" 🔵
    day_count += 1
    streak += 1

ELIF dsa_count >= 2 AND office_day = true:
    bar = "normal" 🔵
    day_count += 1
    streak += 1

ELIF dsa_count >= 1 OR spring_boot_minutes >= 30:
    bar = "partial" 🟠
    day_count += 1
    streak += 1

ELSE:
    bar = "missed" ⬜
    day_count += 0
    streak = 0
    IF 7+ consecutive missed: phase = "paused"
```

> 🔵 **Normal Bar fixes the V3.1 zombie:** there is now ONE named tier for a full
> normal day (previously labelled "low"), and the former V3.1 "Low Bar = read-only,
> day counts" is replaced by 🟢 **Attendance** above — read-only days keep the
> streak alive but no longer increment Day N. The 20-min rule KEEPS THE STREAK;
> it never mints a Day.

---

## 🛡️ ADAPTABILITY SCENARIOS

### Scenario 0: Rest Day (NON-NEGOTIABLE RULE)
- Ramish says "rest day" → bar = 😴 REST
- Day count does NOT increment
- **Streak is PRESERVED** (paused, NOT broken). Next worked day continues streak.
- Zero guilt. Recovery IS training.
- Max 1 rest day per week (Saturday or Sunday usually)

| Source | Old rule | NEW rule (ALL files aligned) |
|--------|---------|-----|
| state-machine.md | "does NOT break streak" | ✅ PRESERVED (pause, not break) |
| session-state.md | "streak preserved" | ✅ PRESERVED |
| system-state.md | "streak resets to 0" | ❌ DELETED — file removed |
| ramish-mentor skill | "streak resets to 0" | ✅ PATCHED → PRESERVED |

### Scenario 1: Boss yells → 10 DSA problems
- Day counts as 1 (not 10)
- Bar = 🟡 high (massively exceeded)
- No banking (system removed) — tomorrow starts fresh at the same Low Bar
- DSA tracker: 10 new rows, all logged
- Emotion noted: "trigger: office stress → channeled into DSA" (positive redirect!)

### Scenario 2: Friend asks for help → whole day lost
- Bar = ⬜ missed (unless any work done)
- Day count does NOT increment
- Streak resets
- Zero guilt. "Missing days extend the arc, never reset."
- Friday review: note pattern, adjust shield (friend protocol)

### Scenario 3: Sick day → can't study
- Ramish says "sick day" → treated as rest day
- Day count does NOT increment
- Streak PRESERVED (rest = pause, not break)
- Recovery is part of the process

### Scenario 4: Hyperfocus → finishes entire Spring Boot week in one Saturday
- Day counts as 1
- Bar = 🟡 high
- No banked credit — extra work is momentum only
- Note: "ahead of schedule on Spring Boot — Week X topics done early"
- Next week: can focus more on DSA or system design (flexibility)

### Scenario 5: Pre-launch work (Aug 1-2)
- Phase = pre-launch
- Work logged in tracker with real dates
- Day count = 0 (Day 1 starts Sep 1)
- Pre-launch problems = carryover (appear in total, noted as pre-launch)
- No streak yet (streak starts Day 1)

### Scenario 6: Off-pattern LeetCode binge
- Problems logged with `📍 Off-pattern` tag
- Count toward total
- Friday review: "are these useful patterns or distraction?"
- If distraction → redirect to NeetCode 150 queue
- If useful (company-specific practice) → keep

### Scenario 7: Copilot → Unaided upgrade
- Original row updated (not new row)
- Help flag: 🟠 → 🟢 with `🔁 Re-solve` note
- Total count unchanged
- Unaided % improves
- Re-solve queue item checked off

### Scenario 8: Ramadan / fasting days
- Learning blocks may shift (pre-dawn study after suhoor)
- Bar may be lowered (fasting = lower energy)
- Hermes asks: "fasting today?" → adjusts expectations
- No high-bar pressure on fasting days unless Ramish requests

### Scenario 9: Interview scheduled mid-plan
- Interview prep overrides planned topics
- Day before interview = "interview prep day" (bar = low, focus on revision)
- Interview day = counts as Day Worked (career action = interview)
- Post-interview: log feedback, identify gaps, adjust plan

### Scenario 10: Burnout → 3+ missed days in a row
- Phase stays active (not paused until 7+)
- Each missed day: streak resets, arc extends
- Hermes reaches out: "Hey, you good? Need a rest day?"
- If Ramish says "burnout" → force rest day + reduce bar to minimum
- No shame. Recovery IS training.

### Scenario 11: Office 20-min DSA blocks (v3.2 — the "20+20" pattern)
- Office day, two 20-min DSA blocks (mid-morning + pre-departure), TCS laptop
- **Block content = revision / re-solve / reading** — Copilot-assisted solves get 🟠 and join the re-solve queue (unaided % must rise before Oct)
- A 20-min block alone = 🟢 **Attendance** (streak preserved, Day does NOT increment)
- An unaided (🟢) solve inside an office block counts as a full Day Worked contribution like any home solve
- Never let office blocks replace the post-camp flex unaided block on light days — office is capacity, not the main engine
- 🔴 Re-solve queue priority: office 🟠 problems are re-solved in the post-camp flex block or Saturday deep-work, before new problems

---

## 📝 FILE SYNC PROTOCOL

**Evening Close-Out (when Ramish replies to check-in):**
1. Ramish reports what he did
2. Hermes updates `session-state.md` (Day count, bar, streak, totals)
3. Hermes updates `tracker/dsa-tracker.md` (new problem rows)
4. Hermes updates `tracker/progress.md` (grid checkbox for the day)
5. Hermes updates `tracker/habit-tracker.md` (weekly counters if reported)
6. ALL updates in ONE response — no drift between files
7. Hermes confirms: "Updated: Day X, bar Y, DSA Z total, streak N"

**Friday Review:**
1. Hermes reads all tracker files
2. Reconciles counts (state vs tracker)
3. Fills weekly review template
4. Updates session-state.md with week summary
5. No duplicate counts anywhere

---

## 🔒 ANTI-DRIFT RULES

1. **Counts in ONE place:** `session-state.md` only. Others reference, don't duplicate.
2. **Per-problem in ONE place:** `dsa-tracker.md` only. No problem logged elsewhere.
3. **Grid in ONE place:** `progress.md` only. Grid has checkboxes, not counts.
4. **Friday reconciliation:** Hermes verifies counts match. If not, tracker detail wins.
5. **No manual edits to counts:** Ramish reports work, Hermes updates. Ramish doesn't edit state.md.
6. **Re-solve = update, not new row:** Prevents count inflation.
7. **Pre-launch = carryover, not Day 1:** Prevents day count drift.
8. **No banked credit anywhere:** Extra work = momentum, not savings (removed Sep 5; purge any app/mirror that still shows "banked").
9. **Bar definition is VERBATIM in every file that shows bars** (session-state, state-machine, progress grid, DAILY-LEDGER header, and any Rafiq display). Six tiers, one wording: attendance 🟢 / normal 🔵 / high 🟡 / partial 🟠 / rest 😴 / missed ⬜.
10. **The app never computes Day/streak:** Rafiq renders counters pushed from Hermes (bridge block) or hides them. Phone-side counters are decorative, never authoritative.

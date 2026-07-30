# ⚙️ SYSTEM STATE — Single Source of Truth

> **RULE:** This file is the ONLY place where "current state" lives.
> All other files (progress.md, dsa-tracker.md, habit-tracker.md) are READ-ONLY views derived from this.
> Hermes updates this file FIRST, then syncs the views. Never edit views directly.

---

## 🎯 Current State (as of Jul 31, 2026)

```yaml
plan_version: V2
launch_date: 2026-08-03
current_date: 2026-07-31
current_day_number: 0          # 0 = pre-launch, 1-84 = working days
current_week: 0                # 0 = pre-launch
current_phase: PRE-LAUNCH      # PRE-LAUNCH / PHASE_1 / PHASE_2 / PHASE_3

# DSA
dsa_problems_solved_total: 3   # V1 carryover
dsa_problems_v2: 0             # Problems solved under V2 plan
dsa_unaided_count: 0
dsa_unaided_pct: 0
dsa_copilot_flagged: 3         # Must re-solve unaided before Oct

# Project
spring_boot_files_created: 0   # 4 target files not yet created
spring_boot_commits: 0
project_deployed: false
ai_integrated: false

# Career
applications_sent: 0
mock_interviews_done: 0
mock_interviews_target: 12
system_designs_practiced: 0
system_designs_target: 8
resume_version: 0

# Streaks
current_streak: 0
longest_streak: 0
banked_days: 0

# Habits (reset weekly)
phone_out_of_bedroom_streak: 0
fajr_on_time_streak: 0
five_min_rule_streak: 0
sleep_by_2230_streak: 0

# Mode
learning_mode: PRE-LAUNCH      # PRE-LAUNCH / LAPTOP / OFFICE
career_path: PLAN_A            # PLAN_A / PLAN_B / PLAN_C

# Reels project
reels_active: false            # Starts Aug 3
reels_account_created: false
second_device_arrived: false

# Journal
journal_created: false         # Build Sunday Aug 2
```

---

## 📐 State Transition Rules

### Rule 1: Day Numbering
- Day 0 = any work done BEFORE Aug 3 (pre-launch bonus)
- Day 1 = first working day AFTER Aug 3
- Day N = Nth day WORKED (not calendar date)
- Missed day → day number doesn't increment, arc extends
- Rest day → explicitly marked "rest," day number doesn't increment
- **Never reset to Day 1**

### Rule 2: Pre-Launch Work (before Aug 3)
If Ramish does DSA/Spring Boot before Aug 3:
- Log it as "Day 0 — Pre-Launch Bonus"
- DSA count increments (dsa_problems_solved_total)
- Spring Boot files created → spring_boot_files_created++
- Day number stays 0
- Streak stays 0 (V2 streak starts Day 1)
- **Purpose:** capture early momentum without polluting V2 stats

### Rule 3: Bonus / Hyperfocus Days
If Ramish does 5-10 DSA in one day:
- All problems logged in dsa-tracker.md
- If count >= 3x daily target → mark as 🔥 Banked Day
- Banked days += (days_worked / 3).floor
- Example: 9 DSA in one day = bank 3 credit days
- Banked days can be used later for missed days without breaking streak
- **Cap:** max 5 banked days at any time (prevents hoarding)

### Rule 4: Emotional Trigger Days
If Ramish says "boss was rude" / "friend needed help" / "felt overwhelmed":
- Log trigger in journal
- If work done: log normally, add note about trigger
- If no work: mark as "trigger day" — no guilt, extend arc
- **Pattern recognition:** if same trigger repeats 3+ times, adjust system
- Example: 3 boss-rude days → add "stress DSA" as coping mechanism (channel anger into problems)

### Rule 5: Rest Days
- Ramish says "rest day" → mark as 😴 REST
- Day number doesn't increment
- Streak resets to 0 (but banked days can cover)
- No guilt. No shame. Part of the process.
- **Max 1 rest day per week** (Saturday or Sunday usually)

### Rule 6: Missed Days
- Ramish doesn't report or says "did nothing"
- Mark as ⬜ MISSED
- Day number doesn't increment
- Streak resets to 0 (banked days can cover)
- **Zero guilt. One sentence. Resume next day.**
- If 2+ consecutive missed days → Hermes reaches out (not waits)

### Rule 7: Mode Detection
- **LAPTOP:** Ramish at home, IDE open, coding
- **OFFICE:** Ramish at work, free time, LeetCode/theory/Discord
- **PRE-LAUNCH:** Before Aug 3
- Mode affects what counts toward daily bar
- Office DSA gets 🟠 Copilot flag (track for unaided re-solve)

### Rule 8: Plan Switching
- **Week 6 Decision Point:** evaluate Spring Boot vs AI progress
- If switching to Plan B (AI/GenAI):
  - spring_boot_* fields freeze
  - ai_integrated becomes primary metric
  - DSA continues (AI interviews still need DSA)
- If switching to Plan C (delay):
  - All fields freeze
  - New launch_date set
  - Day number preserved (resume where left off)

### Rule 9: Data Consistency
- session-state.md = LIVE state (this file)
- progress.md = DERIVED (84-day grid view)
- dsa-tracker.md = DERIVED (problem-level detail)
- habit-tracker.md = DERIVED (bullet journal template)
- **Update flow:** session-state.md → sync views → git commit
- **Never edit views directly** — always update session-state first

### Rule 10: Conflict Resolution
If session-state and views disagree:
1. session-state.md is TRUTH
2. Views are regenerated from session-state
3. Discrepancy logged in git commit message
4. Hermes alerts Ramish: "State drift detected — fixed"

---

## 🧪 Edge Case Scenarios (tested)

| Scenario | Expected Behavior |
|----------|-------------------|
| Ramish does 10 DSA on Aug 2 (before launch) | Day 0, +10 DSA total, streak stays 0, banked days += 3 |
| Ramish does 1 DSA on Aug 3, then nothing for 3 days | Day 1, streak 1, then 3 missed days, streak resets, day stays 1 |
| Ramish says "rest day" on Aug 5 | Day 2 stays 2, rest day logged, streak 0, banked days can cover |
| Boss rude → Ramish does 8 DSA | Day 3, +8 DSA, banked days += 2, trigger logged |
| Ramish does 2 DSA at office with Copilot | Day 4, +2 DSA, both flagged 🟠, unaided queue += 2 |
| Ramish misses 5 days straight | Day 5 stays 5, 5 missed days, Hermes reaches out, no guilt |
| Ramish switches to Plan B at Week 6 | spring_boot_* freeze, ai_integrated primary, day number continues |
| Ramish gets offer Week 10, resigns | Day count continues through notice period, plan shifts to "interview prep" mode |

---

## 🔄 Sync Protocol (Evening Close-Out)

When Ramish replies to 9:30 PM check-in:

1. **Parse response** → extract: DSA done, Spring Boot done, career action, prayers, habits
2. **Update session-state.md** (this file) — increment counters, log triggers, update streaks
3. **Regenerate views:**
   - progress.md: mark today's cell 🟢/🟡/🔥/😴/⬜
   - dsa-tracker.md: add problems to solved table, update unaided queue
   - habit-tracker.md: update habit streaks
4. **Git commit** with summary
5. **Reply to Ramish** with today's bar hit + tomorrow's targets

---

## 🚨 Drift Detection

Every Friday Weekly Review, check:
- [ ] session-state.md dsa_problems_solved_total == count of ✅ in dsa-tracker.md
- [ ] session-state.md current_day_number == filled boxes in habit-tracker.md
- [ ] session-state.md applications_sent == count of 🔵 in job-application-tracker.md
- [ ] All files committed to git (no uncommitted changes)

If drift found:
1. session-state.md wins
2. Views regenerated
3. Drift logged
4. Ramish notified

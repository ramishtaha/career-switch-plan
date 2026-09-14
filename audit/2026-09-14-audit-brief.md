# V4 System Audit Brief — Sep 14, 2026 (prep day)

You are auditing a life-coaching system for Ramish, 26, ADHD (walls of text = paralysis), Muslim (Hanafi), lives alone in Thane, India. Software engineer at TCS (office 10:45–18:00, desk job), switching careers to GCC/BFSI backend roles (Java/Spring Boot). ~12L debt. Solo, no one in his circle shares this journey.

## Priorities (his explicit order, new for V4)
1. Sunnah/Islam (salah, deen)
2. Fitness (MMA/Muay Thai) + diet
3. Career switch (DSA, Spring Boot, 14-18 LPA)
4. Social media (daily documentary reels — now on MAIN Instagram account)
5. Family time (daily 15-30 min call ~20:30-21:00 IST)
6. Friends
7. Work at TCS (containment — do the job, no more)

## Reality of the last 2 weeks (his report, Sep 14)
- Arc V3 (started Sep 1): held Sep 1-3 (Day 3), then 9 consecutive missed days. System now `paused`.
- Relapse chain (recurring pattern): phone/web-series at night → late sleep → re-sleep after Fajr → nap after gym → office late → binge in office free time → evening binge ("I'll start tomorrow") → repeat. Weekends: total collapse, all-day binging.
- Salah: prayed at office, missed most at home. Fajr wake-up HELD daily (the one win).
- What worked: Fajr alarm → pray → gym (Muay Thai camp 7:00-8:30 AM, Mon-Fri, 30 min run + 60 min training). What broke: everything after gym (phone spiral), no pre-workout fuel discipline, office free time binged, no evening structure, late sleep.
- Meal prep disaster (batch cook Sunday not happening; diet plan exists but unexecuted).

## Current system architecture
- **SOT**: `/root/career-switch-plan/session-state.md` (day count, streak, totals — only copy)
- **Trackers**: `tracker/dsa-tracker.md` (per-problem), `tracker/progress.md` (84-day grid), `tracker/habit-tracker.md` (bullet journal), `tracker/job-application-tracker.md`, `tracker/daily-log/DAILY-LEDGER.md` (one row/day)
- **Rules**: `tracker/state-machine.md` — completion-locked Day N (worked days, missed days extend arc), bars: 🟢 attendance (20 min, streak alive, no day) / 🔵 normal / 🟡 high / 🟠 partial / 😴 rest / ⬜ missed. 7+ consecutive misses → auto-pause.
- **Crons (Hermes)**: morning check-in, prayer reminders, evening close-out 20:15 IST, Friday review 20:15 IST, DSA nudge, GitHub backup, liveness watchdog (Telegram).
- **App**: Rafiq (his own Android app) = progress surface; he resets its streaks manually tonight.
- **Diet (locked)**: no dal/rice; shake = 500ml Ultra 7% milk + 2 whey (~700kcal, 66g P) IMMEDIATELY post-training; eggs boiled fresh daily; basa fish; low-carb dinner; haldi doodh (toned 3%) pre-sleep; Sunday batch cook = proteins only; Mon/Thu sunnah fasting (suhur: shake+dates+eggs).
- **Shields**: phone out of bedroom 21:00 hard cutoff, greyscale, charger out of bedroom, app blockers, lockbox recommended 18:15, greyscale, 5-min rule. Phone = primary relapse vector.
- **Prayer times (Thane, Sep, Karachi/Hanafi)**: Fajr ~05:00, Dhuhr ~12:44, Asr ~17:15, Maghrib ~19:09, Isha ~20:26. Jumu'ah at office.
- Salah rebuild rungs (post-relapse): Wk1 Fajr+Dhuhr+Isha, Wk2 +Asr, Wk3 +Maghrib, Wk4 all 5 + Jumu'ah, then optional Duha/tahajjud.

## Proposed V4 daily blueprint (draft — AUDIT THIS)
Weekday: 04:45 tahajjud (10 min, optional Wk1-2) → 05:00 Fajr+adhkar → 05:15 DSA revision-only 25 min (laptop) → 06:25 fuel+pack (bone broth+2 dates) → 06:50 leave → **07:00-08:30 Muay Thai camp** → home ~08:45: T+0 shake immediately + phone in lockbox → T+10 shower → T+30 breakfast → T+45 DSA NEW unaided 25-60 min → 10:15 house reset → **10:30 leave office (FIXED)** → office 10:45-18:00 (Dhuhr 12:44 musallah, Asr 17:15; free time = office-mode drills/claude cert, NO phone) → 18:15 home → optional extra session 18:20-19:20 (1-2x/wk by feel) / meal → 19:09 Maghrib → 19:15-20:15 Spring Boot block → 20:15 evening check-in reply → 20:26 Isha → **20:30-21:00 family call** → 21:00 phone OUT of bedroom → 21:00-21:30 journal + tomorrow setup → 21:30 lights out → 22:00 sleep hard stop.
Saturday: sparring 12:00 Mulund; DSA 09:30-11:30; Spring Boot 15:30-17:30. Sunday: rest, batch cook (proteins only), weekly review, meal prep.
Reels: filmed at transitions per guardrails (max 10s/clip, film-and-drop, no IG app on phone, post from laptop), edit ≤10 min CapCut, post ~21:45 → moved to BEFORE 21:00 cutoff (conflict to resolve: posting ritual 21:45 vs phone cutoff 21:00 — propose post 20:00-20:15 window or right after family call on laptop).

## Known open questions / weaknesses (give your verdict on each)
1. Sleep math: 22:00→04:45 = 6h45. Post-camp re-sleep is THE recurring failure. Is the blueprint resilient to a 30-min slip, or does one slip cascade (like now)?
2. Priority collision: career block 19:15-20:15 daily vs MMA fatigue vs family call — realistic or overpacked?
3. Weekend structure is the weakest link (total collapse twice running). Concrete weekend anchors?
4. Reels on MAIN account: was previously on separate account with anti-relapse guardrails (separate account was a shield). Main account = his personal IG = relapse vector? How to keep reels without re-triggering the binge loop? Posting from laptop browser, IG app blocked on phone — sufficient?
5. Meal prep: Sunday batch cook never executed. What's the minimum viable prep protocol for an ADHD solo lifter with 6h45 sleep?
6. Tracker system: is the SOT/state-machine/ledger design sound, or over-engineered for ADHD? Is auto-pause after 7 misses good (it happened) or does pausing itself enable collapse?
7. Office free time: 2h break (12:30-14:30) binged on phone. Office-mode protocol exists but unused. What would actually make him use it?
8. DSA fresh start: V4 restarts from 0, Week 1 = Arrays & Hashing, first 3 problems re-solved unaided (carryover from V1: Contains Duplicate, Two Sum, Valid Anagram — all previously Copilot-assisted). Anti-copilot 15-min rule. Sound, or adjust pacing?
9. Restart fatigue: V1 (Jul 27), V2 (Aug 3), V2-restart (Aug 17), V3 (Sep 1), now V4 (Sep 15). Four arcs in 7 weeks. What structurally differentiates V4 from V3, which also had a perfect blueprint and died on day 4?

## Deliverable
Write your audit to the file specified in the task. Structure: VERDICT (top 5 issues ranked by impact) → FIXES (concrete, minimal, ADHD-compatible) → WHAT TO KEEP (don't break what works) → ONE structural change that matters most. Be specific and honest; do not flatter. No generic advice — everything must reference his actual constraints above.

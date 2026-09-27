# 📊 DSA Problem Tracker — V4 RESTART

> Auto-updated by Hermes. Ramish reports done → Hermes marks ✅.
> Daily revision: yesterday's problems get quick-recall questions.
> Counts live in `session-state.md` — this file is per-problem detail only.

---

## Today's Queue

> Week 1: Arrays & Hashing + Spring Boot hands-on start (worked days, not calendar dates)
> Next: **Day 1** (first day slipped to Wednesday, Sep 16 — completion-locked; nothing worked Sep 15 so far, unclassified)

**Week 1 priority — V1 carryover re-solve UNAIDED first (proves the machine works):**
1. Contains Duplicate (LC 217) — Easy — ✅ **DONE Sep 16, 🟢 unaided re-solve** *(V1: Copilot ⚠️ — beaten clean)*
2. Two Sum (LC 1) — Easy — ✅ **DONE Sep 16, 🟢 unaided re-solve** *(V1: Copilot ⚠️ — beaten clean)*
3. Valid Anagram — Easy *(V1: Copilot ⚠️ — beat it clean)*

**Then Week 1 queue (Arrays & Hashing):**
4. Group Anagrams — Medium
5. Top K Frequent Elements — Medium
6. Encode/Decode Strings — Medium
7. Products of Array Except Self — Medium
8. Longest Consecutive Sequence — Medium

> Solve 1-2 per day. Friday = revision day. Anti-Copilot 15-min rule ALWAYS: read → hand-trace → pattern → approach in English → complexity → THEN code.
> Reply "done [LC number]" when finished. Copilot used? Say "copilot".

---

## Solved Problems

| # | Problem | Pattern | Difficulty | Date | Time | Help? | Notes |
|---|---------|---------|------------|------|------|-------|-------|
| — | *(none yet — fresh start Sep 15, 2026)* | — | — | — | — | — | — |
| 1 | Contains Duplicate (LC 217) | HashSet (Hashing) | Easy | 2026-09-16 | <10 min | 🟢 Alone | V1 carryover. Verified by 4Q recall: pattern+algorithm correct. Complexity reasoning corrected in grill (set ops = O(1) avg, not O(n)) |
| 2 | Two Sum (LC 1) | HashMap one-pass (Hashing) | Easy | 2026-09-16 | ~5 min | 🟢 Alone | V1 carryover. Recall-verified: number→index map, partner=target−current. Self-upgraded HashSet→HashMap when return type demanded indices. Complexity needs crisp verbal form (O(n)/O(n), map ops O(1) avg) |
| 3 | Group Anagrams (LC 49) | Canonical-key HashMap (sorted string as key) | Medium | 2026-09-23 | ? | 🟠 Gemini ⚠️ | Code correct & clean (sorted-char key, computeIfAbsent-style put-if-missing, groups.values()). Gemini-assisted → goes to unaided re-solve queue. Grill pending: O(n·k log k) complexity + count-array encoding alternative |

---

## Unaided Tracking (Interview Readiness)

> Every problem gets a Help flag. Goal: unaided % rises over time.
> Before Oct-Nov interviews: re-solve ALL 🟠 problems without AI.

| Help Level | Meaning | Count | % |
|------------|---------|-------|---|
| 🟢 Alone | Solved without any help | 1 | 100% (n=1) |
| 🟡 Hint | Got a hint/nudge, or re-solved w/ reference | 0 | 0% |
| 🟠 Copilot ⚠️ | Used GitHub Copilot | 0 | 0% |

**Unaided Re-solve Queue:** V1 carryovers — Contains Duplicate 🟢, Two Sum 🟢 cleared; **Valid Anagram** pending. Plus Gemini-flagged: **Group Anagrams 🟠 (Sep 23)** — both must be re-solved unaided before new patterns.

---

## Revision Schedule

> Each problem gets a revision check the day after solving.
> Hermes asks 1-2 quick recall questions. Ramish answers from memory.
> 🔴 OVERDUE = revision due 2+ days ago and not done → shows FIRST in morning nudge

| Problem | Solved Date | Revision Due | Revised? | Score (1-5) | Status |
|---------|-------------|-------------|-----------|-------------|--------|
| Contains Duplicate (LC 217) | 2026-09-16 | 2026-09-17 | — | — | 🔴 OVERDUE |
| Two Sum (LC 1) | 2026-09-16 | 2026-09-17 | — | — | 🔴 OVERDUE |
| Group Anagrams (LC 49) | 2026-09-23 | 2026-09-24 | — | — | pending (🟠 → re-solve unaided) |

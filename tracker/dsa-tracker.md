# 📊 DSA Notebook: queue, every attempt, revision

> **This file isn't the score.** The score is the unaided total in `LIFETIME-DSA.md` (DB-backed).
> This file keeps the detail: what's next, every attempt (assisted ones too), and recall checks.
> Hermes updates it from the nightly report. Rules for Block 1 / Block 3: `../WINTER-ARC.md` §5.

---

## Queue (NeetCode Blind-75 order, Winter Arc)

**Bridge (Sep 28–30):**
1. **Valid Anagram (LC 242)**: Easy, unaided *(V1 was Copilot, beat it clean)*
2. **Group Anagrams (LC 49)**: Medium, **unaided re-solve** *(Sep 23 was Gemini-assisted)*
3. **Blind timed re-solve:** Contains Duplicate + Two Sum

**October, Arrays & Hashing → Two Pointers → Sliding Window → Stack:**
4. Top K Frequent Elements (LC 347)
5. Product of Array Except Self (LC 238)
6. Encode and Decode Strings (LC 271)
7. Longest Consecutive Sequence (LC 128)
8. Valid Palindrome (LC 125) → 3Sum (LC 15) → Container With Most Water (LC 11)
9. Best Time to Buy and Sell Stock (LC 121) → Longest Substring Without Repeating (LC 3) → Longest Repeating Character Replacement (LC 424)
10. Valid Parentheses (LC 20)

> Block 1 rule: **25-min hard stop** → editorial → one-line pattern note. Assisted = logged here, not scored.

---

## Every attempt

| # | Problem | Pattern | Difficulty | Date | Time | Help | Notes |
|---|---------|---------|------------|------|------|------|-------|
| 1 | Contains Duplicate (LC 217) | HashSet (Hashing) | Easy | 2026-09-16 | <10 min | 🟢 Alone | V1 carryover. Verified by 4Q recall: pattern + algorithm correct. Complexity reasoning corrected in grill (set ops = O(1) avg, not O(n)) |
| 2 | Two Sum (LC 1) | HashMap one-pass (Hashing) | Easy | 2026-09-16 | ~5 min | 🟢 Alone | V1 carryover. Recall-verified: number→index map, partner = target − current. Self-upgraded HashSet → HashMap when return type demanded indices. Complexity needs crisp verbal form (O(n)/O(n), map ops O(1) avg) |
| 3 | Group Anagrams (LC 49) | Canonical-key HashMap (sorted string as key) | Medium | 2026-09-23 | ? | 🟠 Gemini | Code correct & clean (sorted-char key, put-if-missing, groups.values()). Assisted → unaided re-solve queued. Grill pending: O(n·k log k) + count-array key alternative |

**Help flags:** 🟢 alone (scores) · 🟡 hint · 🟠 AI-assisted · 🔁 blind re-solve (scores if unaided; add a new row, never edit the old one).

---

## Recall checks (Block 3 feeds these)

| Problem | Last solved | Next blind re-solve | Result |
|---------|-------------|---------------------|--------|
| Contains Duplicate (LC 217) | 2026-09-16 | Wed 30 Sep (bridge) | — |
| Two Sum (LC 1) | 2026-09-16 | Wed 30 Sep (bridge) | — |
| Group Anagrams (LC 49) | 2026-09-23 (🟠) | Tue 29 Sep (bridge) | — |

> Spacing: re-solve a problem **1 day, 3 days, then 7 days** after first solving it. Block 3 picks the oldest one that's due.

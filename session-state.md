# Session State: Ramish Mentor System

> **Read at the start of every Hermes session.** It says what's true *now* and where everything lives.
> **The plan is `WINTER-ARC.md`.** This file doesn't copy times or rules from it. If a time appears here, it's a mistake.
> **Counts are not stored here.** They come from the Rafiq DB (`rafiq-api.py today` / `scoreboard`) and the generated blocks in `tracker/daily-log/DAILY-LEDGER.md` and `tracker/LIFETIME-DSA.md`.

---

## Now

- **Arc:** **Winter Arc**, declared Sep 28, 2026. **Day one = Thu 1 Oct 2026** (a fast day). Runs until Ramadan (tentatively Tue 9 Feb 2027 in India). A Ramadan edition gets written at the Sun 31 Jan review.
- **Bridge:** Mon 28 → Wed 30 Sep (MMA camp wraps Sep 30). One unaided problem a day plus the setup checklist, see `WINTER-ARC.md` §12.
- **Phase:** `bridge` until Oct 1, then `active`. **There is no pause state and no restart.** Misses are logged rows.
- **Scoreboard:** unaided DSA problems (DB-backed, `tracker/LIFETIME-DSA.md`). Count: `rafiq-api.py today` (never copied here). **Tier-1 gate = 35.**
- **Office:** TCS System Engineer, **10:30–18:30**, leaves home ~10:15, goes straight to Cult after Maghrib. **Lowest priority. Containment only.**

## The floor (Ramish's 8, verbatim intent, final)

1. All 5 salah with sunnah (rawatib) + Witr
2. Fast Monday + Thursday
3. Run + Cult daily: 1 h at Cult, the first ≥ 10 min is the run (widened by Ramish, Sep 28)
4. Study ≥ 3 h daily (office time never counts)
5. Journal daily (paper)
6. Self-help reading daily
7. Weekends = career building only
8. TCS = lowest priority

**Order when things clash:** deen → career → body → everything else → TCS.

## Learning state (carried forward, not reset)

- **Mode:** LAPTOP at home (office laptop is locked: no IDE, no Spring there).
- **Spring Boot, understood:** what Spring Boot is (auto-config, DI, embedded server), annotations as labels, the 4-layer flow (Controller → Service → Repository → DB), `@Service` on the class.
- **Spring Boot, next:** create the 4 Product files in IntelliJ → run → test endpoints. Then `@Entity`, `@RestController`, `@GetMapping`/`@PostMapping`, `@PathVariable`/`@RequestBody`, `JpaRepository`.
- **DSA queue:** Valid Anagram (unaided) → Group Anagrams (unaided re-solve) → Top K Frequent → Product of Array Except Self → Encode/Decode → Longest Consecutive. Detail in `tracker/dsa-tracker.md`.
- **Mocks / designs done:** 0 / 0. **Applications sent:** 0 (engine starts Sat 3 Oct).

## Career strategy

- **Primary:** Java + Spring Boot → BFSI GCCs / European + Indian banks. Banking-domain depth (BaNCS) is the edge.
- **Applications are decoupled from DSA.** Banks from Sat 3 Oct, GCCs from mid-Oct. **Tier 1 (Goldman / JPM / MS) only at 35 unaided.**
- **Money facts:** debt ~₹12L, EMIs ≈ salary, runway short. 90-day notice, no early release. No resignation without a signed offer. Refuse below ~13 LPA.

## Body

- MMA camp ended Sep 30. **Cult gym 1 h daily is non-negotiable** (floor #3; slot and fast-day variant in `WINTER-ARC.md` §4 + §8). MMA classes are superseded by it.
- **House:** his known pile-up pattern is a shame + cognitive-load trigger. Small daily loads + Wed/Sat laundry + Sat Asr reset (`WINTER-ARC.md` §8). Ledger column `H`, not part of 8/8.
- Diet: high protein, locked rules in `DIET-PLAN.md`. Meal-prep = **Sunday Asr → Maghrib**.

## Deen notes (so audits stop re-deriving)

- Hanafi. Witr (3, wajib) **right after Isha** every night. Tahajjud is a bonus, pre-Fajr.
- Chastity: guilt-chain diagnosed Jul 26 (savior complex, relief = guilt, not love). Shields: khalwah ban, night protocol, circuit-breaker. Checked in gently at the Sunday review (he can say "pass").
- Riba: continue EMIs, no new debt. Still to do: ask a local scholar about his loans.

## Witness + review

- **Witness = Hermes.** Nightly one-line report on Telegram (format in `WINTER-ARC.md` §10). Reporting a miss counts as a win.
- **Weekly review = Sunday** (moved from Friday), 20 min, 5 questions. **Last review held: none yet.** First one: **Sun 4 Oct.**
- Big reviews: Sun 1 Nov · Sun 29 Nov · Sun 31 Jan.

## File map

| File | Role |
|---|---|
| `WINTER-ARC.md` | **THE plan** |
| `session-state.md` | This file: what's true now + pointers |
| `tracker/daily-log/DAILY-LEDGER.md` | **THE ledger**, one row per day |
| `tracker/LIFETIME-DSA.md` | **THE scoreboard**, append-only, never reset |
| `tracker/dsa-tracker.md` | DSA notebook: queue, every attempt (assisted too), revision notes |
| `tracker/job-application-tracker.md` | Applications, referrals, interviews, salary notes |
| `DIET-PLAN.md` | Food rules + fasting-day meals |
| `WINTER-ARC-CRON-RECOMMENDATIONS.md` | Cron + app changes for Hermes to apply |
| `WINTER-ARC-CHANGES.md` | What changed in the Sep 28 rebuild |
| `archive/` | Every older plan, tracker, audit and failure log. History, not instructions |

## History (one line)

V1 (Jul 27) · V2 (Aug 3, Aug 17) · V3 (Sep 1) · V4 (Sep 15) · plan-v3 (Sep 27, never started). All closed. Details are in `archive/`. **The Winter Arc doesn't count arcs.**

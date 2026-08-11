# Alexa-Hermes Integration — Context Save
# Created: Aug 11, 2026 ~10PM IST
# Purpose: Allow new session to continue Alexa debugging with full context

## What's Built (ALL DONE ✅)

### Server Infrastructure
- **Flask app**: `/root/alexa-hermes/app.py` (gunicorn on 127.0.0.1:8443)
- **Caddy reverse proxy**: `hermes.ramishtaha.com` → 127.0.0.1:8443 (auto-SSL via Let's Encrypt)
- **systemd service**: `alexa-hermes.service` (enabled, auto-restart)
- **Health check**: `https://hermes.ramishtaha.com/health` → 200 OK
- **Alexa endpoint**: `https://hermes.ramishtaha.com/alexa` → POST → Flask

### Tuya IoT Cloud (2 AZIOT switches — FULL CONTROL ✅)
- **Access ID**: `ma5ksfr43em94aajf33g`
- **Access Secret**: `2262ea3cb4804f05aa1e8458106aa716`
- **Project Code**: `p1786450058332q43yq9`
- **Data Center**: India (`https://openapi.tuyain.com`)
- **Device 1**: "Room Main Board" — ID: `d79104a0b4afffbf69zvvi` — 4 switches — Online ✅
- **Device 2**: "Hall Main Board" — ID: `d7edf66cbd42f7e9377boe` — 4 switches — Online ✅
- **API auth**: HMAC-SHA256 signing, token cached for ~2hrs
- **Switch codes**: switch_1, switch_2, switch_3, switch_4 (all 4 per device)
- **Status**: Read + Write both working via REST API

### Wipro Bulb (PENDING ⏳)
- Ramish added to SmartLife app, needs to link to Tuya IoT project
- Not yet in the API

### ESP RainMaker (DIY switch — READ ONLY ❌)
- **Email**: `ramishtaha1@gmail.com` (changed from `trixterthe@gmail.com`)
- **Password**: `LsQX4@-Y5dOpx_a`
- **Node ID**: `6ZDdyawzC5NesD89k49T5u`
- **Node**: 4 switches (Switch1-Switch4), each has "Power" param (bool)
- **API base**: `https://api.rainmaker.espressif.com`
- **Login**: Works ✅ (POST /v1/login → accesstoken)
- **Read params**: Works ✅ (GET /v1/user/nodes?node_details=true&params=true)
- **Write params**: ❌ BROKEN — PUT /v1/user/node/params returns "Bad request" regardless of body format
  - Tried: `{"Switch1": {"Power": true}}`, `[{"name": "Switch1.Power", "value": true}]`, many others
  - Known community issue — RainMaker REST API docs are incomplete
  - esp-rainmaker-cli Python package installed but couldn't use it either
  - Fallback: use MQTT or CLI to control, or skip for now

### Alexa Skill (Amazon Developer Console)
- **Skill ID**: `amzn1.ask.skill.8eb9f38a-904f-4926-8fdd-739a32ddab5e`
- **Skill name**: "Hermes"
- **Invocation**: "Alexa, open Hermes" / "Alexa, ask Hermes to ___"
- **Interaction model JSON**: `/root/alexa-hermes/alexa-skill-model.json`
- **Simulator test**: ✅ WORKS — "open hermes" → correct response, "tell me what to do now" → correct response
- **Physical Echo device**: ❌ NOT SPEAKING — blue light comes on (listening), then light turns off, no audio

### 14 Mentor Voice Commands (ALL TESTED IN SIMULATOR ✅)
1. RoutineIntent — "what's my routine today" → time-aware schedule
2. WhatNextIntent — "what should I do next" → context-aware next action
3. FeelingLostIntent — "I'm feeling lost" → 3 rotating freeze-breaking responses
4. RelapseIntent — "I relapsed" → 5-step chastity protocol
5. CompletedTaskIntent — "I completed {task}" → acknowledges + next step (slot: AMAZON.SearchQuery)
6. CheckStreakIntent — "check my streak" → reads session-state.md live
7. MorningCheckIntent — "morning check-in" → survival layer + plan
8. EveningCloseIntent — "evening close out" → did you hit low bar?
9. LateWakeIntent — "I woke up late" → zero guilt + recalibrate
10. DuaIntent — "give me a dua" → 7 rotating Islamic reminders
11. TurnOffLightsIntent — "turn off all lights" → Tuya API
12. TurnOnLightsIntent — "turn on all lights" → Tuya API
13. StudyModeIntent — "start study mode" → hall off, room on + motivation
14. SleepModeIntent — "start sleep mode" → all off + 3 sleep rules

### Physical Echo: Follow-ups FIXED ✅ (Aug 11 ~10:45 PM IST)

**Root cause**: Three bugs in the Flask webhook:
1. **`CanFulfillIntentRequest` not handled** — Alexa sends this before routing intents on physical devices. Old code returned a regular speech response (invalid format) → "something went wrong"
2. **`AMAZON.FallbackIntent` not handled** — Alexa sends this when it can't match the utterance. Old code fell through to generic "Sorry, I didn't understand that" with no reprompt → physical device showed error
3. **No reprompt field** — `shouldEndSession: false` responses had no `reprompt.outputSpeech`, which some Echo devices require
4. **No error handling** — any exception in the webhook would crash and return 500

**Fixes applied to `/root/alexa-hermes/app.py`**:
- Added `CanFulfillIntentRequest` handler → returns proper `canFulfillIntent` format
- Added `AMAZON.FallbackIntent` + `AMAZON.NavigateHomeIntent` handlers
- `_build_response()` now supports `reprompt` parameter
- Full try/except around webhook — exceptions return graceful speech, not 500
- Request logging to `/var/log/alexa-hermes.log` (type, intent, session, locale, response size)

**`alexa-skill-model.json` updated**: Added `AMAZON.FallbackIntent` to intents array.

### What Ramish needs to do on Amazon Developer Console:
1. Go to Hermes skill → Interaction Model
2. Copy updated JSON from `/root/alexa-hermes/alexa-skill-model.json` (or just add `AMAZON.FallbackIntent` manually)
3. Build model
4. Test on physical Echo: "Alexa, open Hermes" → then "what should I do next"

### Debugging logs:
- Flask app logs: `/var/log/alexa-hermes.log` (request type, intent, session state, response size)
- Caddy access: `/var/log/caddy/hermes-alexa.log` (HTTP-level, response sizes from Amazon IPs)
- systemd: `journalctl -u alexa-hermes`

## File Locations
- Flask app: `/root/alexa-hermes/app.py`
- Alexa skill JSON: `/root/alexa-hermes/alexa-skill-model.json`
- Env file: `/root/alexa-hermes/.env` (Tuya + RainMaker creds)
- README: `/root/alexa-hermes/README.md`
- Caddy config: `/etc/caddy/Caddyfile`
- systemd: `/etc/systemd/system/alexa-hermes.service`
- Caddy logs: `/var/log/caddy/hermes-alexa.log`
- Service logs: `journalctl -u alexa-hermes`
- App logs: `/var/log/alexa-hermes.log`

## Prayer Times Engine (Local Calculation — No API)
- **Library**: `adhanpy` (pip install adhanpy) — local astronomical calculation, no network needed
- **Location**: Thane, Mumbai (19.2183°N, 72.9747°E)
- **Method**: Karachi (MWL Karachi) — standard for India
- **Madhab**: Hanafi (Asr uses shadow factor 2)
- **Tahajjud**: Last third of night = Isha + 2/3 × (Fajr − Isha)
- **Cache**: Calculated once per day, cached in `_prayer_cache`
- **Fallback**: If calculation fails, uses approximate static times

## Fasting (Sunnah Mon & Thu)
- **Config**: Read from `session-state.md` → "Fasting" section → "**Days**" field
- **Alexa awareness**: On Mon/Thu, diet + what-eat responses shift to fasting mode
- **Suhur**: Before Fajr — protein shake + dates + water + eggs
- **Iftar**: At Maghrib — dates + water first, then full protein meal
- **Hydration**: 2-3L water between Maghrib and sleep

## Source of Truth Architecture
- **`/root/career-switch-plan/session-state.md`** = SINGLE SOURCE OF TRUTH
  - Daily Blueprint section → routine config (prayer-anchored)
  - Fasting section → fasting days + diet rules
  - 12-Week Plan State → day count, DSA, streak, etc.
- **Alexa app** reads session-state.md at every request
- **Hermes cron** reads session-state.md for check-ins
- **Memory** points to session-state.md as SOT
- Update ONE file → Alexa + Hermes + memory all stay in sync

## Full Replication Guide (if account closes / server lost)
1. **Provision**: Ubuntu 22.04 server (DigitalOcean/Vultr), 4GB RAM
2. **Install**: `apt install python3 python3-pip caddy`
3. **Python deps**: `pip install flask gunicorn requests adhanpy`
4. **DNS**: Point `hermes.ramishtaha.com` → server IP
5. **Caddy**: Use config from `/etc/caddy/Caddyfile` (auto-SSL)
6. **App**: Copy `/root/alexa-hermes/` directory (app.py, .env, alexa-skill-model.json)
7. **systemd**: Copy `/etc/systemd/system/alexa-hermes.service`
8. **Session state**: Copy `/root/career-switch-plan/session-state.md`
9. **Start**: `systemctl enable --now alexa-hermes caddy`
10. **Amazon Console**: Create new skill, paste alexa-skill-model.json, set endpoint to `https://hermes.ramishtaha.com/alexa`
11. **Test**: `curl https://hermes.ramishtaha.com/health` → 200 OK

## Session State
- Ramish on Day 3/84 tomorrow (completion-locked, no reset)
- Streak: 1/84 starts tomorrow (consecutive days showing up)
- Gym: ✅ done today (Aug 11)
- Dhuhr: ✅ prayed
- Asr/Maghrib/Isha: pending
- Two Sum from memory: pending (15 min, no AI)
- Phone greyscale + out of bedroom: before sleep
- Sleep target: 22:00

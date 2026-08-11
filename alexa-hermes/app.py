#!/usr/bin/env python3
"""
Alexa → Hermes Mentor Integration
Alexa as a voice gateway to Ramish's mentor system.
Comprehensive model: career, DSA, Spring Boot, body, diet, deen, mental health, timeline.
"""
from flask import Flask, request, jsonify
import json
import os
import re
import time
import hashlib
import hmac
import requests
import logging
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

# ─── Request Logging ───────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('/var/log/alexa-hermes.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@app.before_request
def _log_request():
    if request.path == '/alexa' and request.method == 'POST':
        try:
            body = request.get_data(as_text=True)
            data = json.loads(body) if body else {}
            req = data.get('request', {})
            session = data.get('session', {})
            logger.info(
                "ALEXA REQUEST | type=%s | intent=%s | session.new=%s | locale=%s | body_size=%d",
                req.get('type', '?'),
                req.get('intent', {}).get('name', 'N/A') if req.get('intent') else 'N/A',
                session.get('new', '?'),
                req.get('locale', '?'),
                len(body)
            )
        except Exception as e:
            logger.error("LOG ERROR: %s", e)

# ─── Timezone (IST = UTC+5:30) ─────────────────────────────────────
IST = timezone(timedelta(hours=5, minutes=30))

# ─── Prayer Times Engine (local calculation, no API) ─────────────
# Thane, Mumbai: 19.2183°N, 72.9747°E
# Method: Karachi (MWL Karachi) — standard for India
# Madhab: Hanafi (Asr uses shadow factor 2)
from zoneinfo import ZoneInfo
from adhanpy.PrayerTimes import PrayerTimes as _AdhanPrayerTimes
from adhanpy.calculation.CalculationMethod import CalculationMethod as _CalcMethod
from adhanpy.calculation.CalculationParameters import CalculationParameters as _CalcParams
from adhanpy.calculation.Madhab import Madhab as _Madhab

THANE_LAT = 19.2183
THANE_LON = 72.9747
KOLKATA_TZ = ZoneInfo('Asia/Kolkata')

_prayer_cache = {"date": None, "times": None}

def _get_prayer_times():
    """Calculate today's prayer times for Thane using adhanpy (local, no network)."""
    today = datetime.now(IST).date()
    if _prayer_cache["date"] == today and _prayer_cache["times"]:
        return _prayer_cache["times"]
    
    try:
        params = _CalcParams(method=_CalcMethod.KARACHI)
        params.madhab = _Madhab.HANAFI
        pt = _AdhanPrayerTimes(
            coordinates=(THANE_LAT, THANE_LON),
            date=datetime.now(timezone.utc),
            calculation_parameters=params,
            time_zone=KOLKATA_TZ
        )
        times = {
            'fajr': pt.fajr.replace(tzinfo=IST),
            'sunrise': pt.sunrise.replace(tzinfo=IST),
            'dhuhr': pt.dhuhr.replace(tzinfo=IST),
            'asr': pt.asr.replace(tzinfo=IST),
            'maghrib': pt.maghrib.replace(tzinfo=IST),
            'isha': pt.isha.replace(tzinfo=IST),
        }
        _prayer_cache["date"] = today
        _prayer_cache["times"] = times
        logger.info("PRAYER TIMES: Fajr=%s Sunrise=%s Dhuhr=%s Asr=%s Maghrib=%s Isha=%s",
                    times['fajr'].strftime('%H:%M'), times['sunrise'].strftime('%H:%M'),
                    times['dhuhr'].strftime('%H:%M'), times['asr'].strftime('%H:%M'),
                    times['maghrib'].strftime('%H:%M'), times['isha'].strftime('%H:%M'))
        return times
    except Exception as e:
        logger.error("Prayer time calculation failed: %s", e)
        # Fallback to approximate static times
        now = datetime.now(IST)
        return {
            'fajr': now.replace(hour=5, minute=0, second=0, microsecond=0),
            'sunrise': now.replace(hour=6, minute=15, second=0, microsecond=0),
            'dhuhr': now.replace(hour=12, minute=30, second=0, microsecond=0),
            'asr': now.replace(hour=17, minute=0, second=0, microsecond=0),
            'maghrib': now.replace(hour=19, minute=0, second=0, microsecond=0),
            'isha': now.replace(hour=20, minute=20, second=0, microsecond=0),
        }

def _fmt(dt):
    """Format a datetime as '5:15 AM' (12-hour, no leading zero)."""
    return dt.strftime('%I:%M %p').lstrip('0')

def _tahajjud_time():
    """Tahajjud: 15 min before Fajr (practical, consistent > ambitious).
    Any time after Isha until Fajr adhan is valid for Tahajjud.
    10 min before Fajr = 2 nafl + istighfar, then straight into Fajr prep.
    """
    pt = _get_prayer_times()
    return pt['fajr'] - timedelta(minutes=15)

# ─── Session State Parser ─────────────────────────────────────────

def _read_session_state():
    try:
        with open('/root/career-switch-plan/session-state.md', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None

def _parse_state(content):
    if not content:
        return {}
    state = {}
    
    m = re.search(r'\*\*Active Day Count\*\*:\s*(\d+)\s*of\s*(\d+)', content)
    if m:
        state['day'] = m.group(1)
        state['total_days'] = m.group(2)
    
    m = re.search(r'\*\*DSA Problems Solved\*\*:\s*(\d+)', content)
    state['dsa_solved'] = m.group(1) if m else '?'
    
    m = re.search(r'\*\*DSA Unaided\*\*:\s*(\d+)/(\d+)', content)
    if m:
        state['dsa_unaided'] = m.group(1)
        state['dsa_total'] = m.group(2)
    
    m = re.search(r'\*\*Current Streak\*\*:\s*(\d+)', content)
    state['streak'] = m.group(1) if m else '0'
    
    m = re.search(r'\*\*Missed Days\*\*:\s*(.+?)(?:\n|$)', content)
    state['missed_days'] = m.group(1).strip() if m else 'none'
    
    m = re.search(r'\*\*Last Concept Taught\*\*:\s*(.+?)(?:\n|$)', content)
    state['last_concept'] = m.group(1).strip() if m else 'Spring Boot'
    
    m = re.search(r'\*\*System Designs Practiced\*\*:\s*(\d+)\s*/\s*(\d+)', content)
    if m:
        state['sys_designs'] = m.group(1)
        state['sys_design_total'] = m.group(2)
    
    m = re.search(r'\*\*Mock Interviews\*\*:\s*(\d+)\s*/\s*(\d+)', content)
    if m:
        state['mocks'] = m.group(1)
        state['mock_total'] = m.group(2)
    
    m = re.search(r'\*\*Applications Sent\*\*:\s*(\d+)', content)
    state['applications'] = m.group(1) if m else '0'
    
    m = re.search(r'\*\*Current Mode\*\*:\s*(.+?)(?:\n|$)', content)
    state['mode'] = m.group(1).strip() if m else 'LAPTOP'
    
    m = re.search(r'\*\*Concepts Pending\*\*:\s*(.+?)(?:\n|$)', content)
    state['concepts_pending'] = m.group(1).strip() if m else 'Spring Boot basics'
    
    m = re.search(r'\*\*Next Laptop Session\*\*:\s*(.+?)(?:\n|$)', content)
    state['next_laptop'] = m.group(1).strip() if m else 'Create files in IntelliJ'
    
    m = re.search(r'\*\*Current Week\*\*:\s*(\d+)', content)
    state['week'] = m.group(1) if m else '1'
    
    m = re.search(r'\*\*Banked Days\*\*:\s*(\d+)\s*/\s*(\d+)', content)
    if m:
        state['banked'] = m.group(1)
        state['banked_max'] = m.group(2)
    
    # Fasting config (Sunnah Mon & Thu)
    state['fasting_days'] = 'monday thursday'  # default
    m = re.search(r'\*\*Days\*\*:\s*(.+?)(?:\n|$)', content)
    if m and ('monday' in m.group(1).lower() or 'thursday' in m.group(1).lower()):
        state['fasting_days'] = m.group(1).strip().lower()
    
    return state

def _is_fasting_day():
    """Check if today is a fasting day (Mon or Thu by default)."""
    state = _parse_state(_read_session_state() or "")
    fasting_days = state.get('fasting_days', 'monday thursday')
    today_name = datetime.now(IST).strftime('%A').lower()
    return today_name in fasting_days

def _fasting_status():
    """Return fasting status string for today."""
    if not _is_fasting_day():
        return ""
    now = datetime.now(IST)
    pt = _get_prayer_times()
    if now < pt['fajr']:
        return f"Today is a fasting day. Suhur ends at Fajr ({_fmt(pt['fajr'])}). Eat now: protein shake, dates, water. "
    elif now < pt['maghrib']:
        return f"You're fasting today. Iftar at Maghrib ({_fmt(pt['maghrib'])}). Stay hydrated from last night. Keep working. "
    else:
        return f"Fast breaks at Maghrib ({_fmt(pt['maghrib'])}). Dates and water first, then full meal. "

def _get_time_context(now_ist):
    hour = now_ist.hour
    if 4 <= hour < 6: return "early morning"
    elif 6 <= hour < 12: return "morning"
    elif 12 <= hour < 17: return "afternoon"
    elif 17 <= hour < 20: return "evening"
    elif 20 <= hour < 22: return "late evening"
    else: return "night"


# ─── Tuya Cloud API (light control) ───────────────────────────────

TUYA_ACCESS_ID = os.environ.get('TUYA_ACCESS_ID', 'ma5ksfr43em94aajf33g')
TUYA_ACCESS_SECRET = os.environ.get('TUYA_ACCESS_SECRET', '2262ea3cb4804f05aa1e8458106aa716')
TUYA_BASE = "https://openapi.tuyain.com"
EMPTY_BODY_SHA = hashlib.sha256(b'').hexdigest()

DEVICES = {
    "room": ("d79104a0b4afffbf69zvvi", "switch_1"),
    "hall": ("d7edf66cbd42f7e9377boe", "switch_1"),
}
ALL_SWITCHES = ["switch_1", "switch_2", "switch_3", "switch_4"]

_tuya_token_cache = {"token": None, "expires": 0}

def _get_tuya_token():
    if _tuya_token_cache["token"] and time.time() < _tuya_token_cache["expires"]:
        return _tuya_token_cache["token"]
    t = str(int(time.time() * 1000))
    path = "/v1.0/token?grant_type=1"
    sign_str = f"{TUYA_ACCESS_ID}{t}GET\n{EMPTY_BODY_SHA}\n\n{path}"
    sign = hmac.new(TUYA_ACCESS_SECRET.encode(), sign_str.encode(), hashlib.sha256).hexdigest().upper()
    resp = requests.get(f"{TUYA_BASE}{path}", headers={
        "client_id": TUYA_ACCESS_ID, "sign": sign,
        "sign_method": "HMAC-SHA256", "t": t,
        "mode": "cors", "Content-Type": "application/json"
    }, timeout=10)
    data = resp.json()
    if data.get("success"):
        token = data["result"]["access_token"]
        _tuya_token_cache["token"] = token
        _tuya_token_cache["expires"] = time.time() + 7000
        return token
    return None

def _tuya_sign(token, method, path, body=""):
    t = str(int(time.time() * 1000))
    body_sha = hashlib.sha256(body.encode('utf-8')).hexdigest() if body else EMPTY_BODY_SHA
    sign_str = f"{TUYA_ACCESS_ID}{token}{t}{method}\n{body_sha}\n\n{path}"
    sign = hmac.new(TUYA_ACCESS_SECRET.encode(), sign_str.encode(), hashlib.sha256).hexdigest().upper()
    return {
        "client_id": TUYA_ACCESS_ID, "sign": sign,
        "sign_method": "HMAC-SHA256", "t": t,
        "access_token": token, "mode": "cors",
        "Content-Type": "application/json"
    }

def _tuya_send_command(device_id, commands):
    token = _get_tuya_token()
    if not token:
        return False
    path = f"/v1.0/devices/{device_id}/commands"
    body = json.dumps({"commands": commands})
    headers = _tuya_sign(token, "POST", path, body)
    resp = requests.post(f"{TUYA_BASE}{path}", headers=headers, data=body, timeout=10)
    return resp.json().get("success", False)

def _turn_off_all_lights():
    for dev_id, _ in DEVICES.values():
        cmds = [{"code": sw, "value": False} for sw in ALL_SWITCHES]
        _tuya_send_command(dev_id, cmds)
    _rainmaker_turn_off()

def _turn_on_all_lights():
    for dev_id, _ in DEVICES.values():
        cmds = [{"code": sw, "value": True} for sw in ALL_SWITCHES]
        _tuya_send_command(dev_id, cmds)
    _rainmaker_turn_on()


# ─── ESP RainMaker API ─────────────────────────────────────────────

RAINMAKER_BASE = "https://api.rainmaker.espressif.com"
RAINMAKER_EMAIL = os.environ.get('RAINMAKER_EMAIL', 'ramishtaha1@gmail.com')
RAINMAKER_PASSWORD = os.environ.get('RAINMAKER_PASSWORD', '')
RAINMAKER_NODE_ID = os.environ.get('RAINMAKER_NODE_ID', '6ZDdyawzC5NesD89k49T5u')

_rainmaker_token_cache = {"token": None, "expires": 0}

def _get_rainmaker_token():
    if not RAINMAKER_PASSWORD:
        return None
    if _rainmaker_token_cache["token"] and time.time() < _rainmaker_token_cache["expires"]:
        return _rainmaker_token_cache["token"]
    try:
        resp = requests.post(f"{RAINMAKER_BASE}/v1/login", json={
            "user_name": RAINMAKER_EMAIL,
            "password": RAINMAKER_PASSWORD
        }, timeout=10)
        data = resp.json()
        if data.get("status") == "success" and data.get("accesstoken"):
            token = data["accesstoken"]
            _rainmaker_token_cache["token"] = token
            _rainmaker_token_cache["expires"] = time.time() + 3500
            return token
    except Exception:
        pass
    return None

def _rainmaker_set_param(param_name, value):
    token = _get_rainmaker_token()
    if not token:
        return False
    try:
        url = f"{RAINMAKER_BASE}/v1/user/node/params?node_id={RAINMAKER_NODE_ID}"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload = [{"name": param_name, "value": value}]
        resp = requests.put(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except Exception:
        return False

def _rainmaker_turn_off():
    _rainmaker_set_param("power", False)

def _rainmaker_turn_on():
    _rainmaker_set_param("power", True)


# ═══════════════════════════════════════════════════════════════════
# MENTOR RESPONSE ENGINE — Complete Model of Ramish
# ═══════════════════════════════════════════════════════════════════

# ─── 1. SCHEDULE & TIME ────────────────────────────────────────────

def _mentor_routine_today():
    """What's my routine today? — prayer-anchored, time-aware."""
    now = datetime.now(IST)
    pt = _get_prayer_times()
    state = _parse_state(_read_session_state() or "")
    day = state.get('day', '?')
    total = state.get('total_days', '84')
    
    tahajjud = _tahajjud_time()
    fajr = pt['fajr']
    sunrise = pt['sunrise']
    isha = pt['isha']
    
    if now < tahajjud:
        return f"It's {_fmt(now)}. Sleep. Tahajjud at {_fmt(tahajjud)}, Fajr at {_fmt(fajr)}. Wake at {_fmt(tahajjud)} — just 15 min before Fajr."
    elif tahajjud <= now < fajr:
        return f"It's {_fmt(now)}. Tahajjud time. Two nafl and istighfar. Fajr at {_fmt(fajr)}. Then Golden Block. Day {day} of {total}. Bismillah."
    elif fajr <= now < sunrise:
        return f"It's {_fmt(now)}. Pray Fajr. Then Golden Block — DSA revision and one new problem. No AI. Sunrise at {_fmt(sunrise)}. Day {day} of {total}."
    elif sunrise <= now < (sunrise + timedelta(hours=1, minutes=30)):
        return f"It's {_fmt(now)}. Spring Boot theory block. 45 minutes. Morning is your prime study time now — MMA moved to 8 PM. Day {day} of {total}."
    elif (sunrise + timedelta(hours=1, minutes=30)) <= now < datetime.now(IST).replace(hour=10, minute=30):
        return f"It's {_fmt(now)}. Morning free time. DSA revision, LeetCode, or Claude cert. MMA is at 8 PM now — your mornings are for study. Office at 10:45. Day {day} of {total}."
    elif datetime.now(IST).replace(hour=10, minute=30) <= now < pt['dhuhr']:
        return f"It's {_fmt(now)}. Office. Dhuhr at {_fmt(pt['dhuhr'])}. Day {day} of {total}."
    elif pt['dhuhr'] <= now < pt['asr']:
        return f"It's {_fmt(now)}. Office hours. Pray Dhuhr. Use free time 1:30 to 2:30 for LeetCode or Claude cert. Asr at {_fmt(pt['asr'])}. Day {day} of {total}."
    elif pt['asr'] <= now < pt['maghrib']:
        return f"It's {_fmt(now)}. Office hours. Pray Asr. Keep working. Maghrib at {_fmt(pt['maghrib'])}. MMA at 8 PM. Day {day} of {total}."
    elif pt['maghrib'] <= now < datetime.now(IST).replace(hour=19, minute=45):
        return f"It's {_fmt(now)}. Home. Pray Maghrib. Eat light. MMA at 8 PM. Isha at {_fmt(pt['isha'])}. Day {day} of {total}."
    elif datetime.now(IST).replace(hour=19, minute=45) <= now < datetime.now(IST).replace(hour=21, minute=0):
        return f"It's {_fmt(now)}. MMA time. Get to BRUTE. Train hard. Day {day} of {total}."
    elif datetime.now(IST).replace(hour=21, minute=0) <= now < datetime.now(IST).replace(hour=21, minute=15):
        return f"It's {_fmt(now)}. Post-MMA. Shower. Quick protein. Then Spring Boot block at 9:15. Day {day} of {total}."
    elif datetime.now(IST).replace(hour=21, minute=15) <= now < datetime.now(IST).replace(hour=22, minute=30):
        return f"It's {_fmt(now)}. Evening block — Spring Boot coding. 60 minutes, then git commit. Phone greyscale. No reels. Day {day} of {total}."
    else:
        return f"It's {_fmt(now)}. Sleep time. Phone in kitchen. Charger out of bedroom. Tahajjud at {_fmt(tahajjud)}. Day {day} of {total}."


def _mentor_what_next():
    """What should I do next? — prayer-anchored, MMA at 8 PM."""
    now = datetime.now(IST)
    pt = _get_prayer_times()
    tahajjud = _tahajjud_time()
    
    if now < tahajjud:
        return f"Sleep. Tahajjud at {_fmt(tahajjud)}. Fajr at {_fmt(pt['fajr'])}."
    elif tahajjud <= now < pt['fajr']:
        return "Tahajjud now. Two nafl, istighfar. Then Fajr at " + _fmt(pt['fajr']) + "."
    elif pt['fajr'] <= now < pt['sunrise']:
        return "Golden Block. DSA. One problem from memory. No AI, no notes. 15 minutes. Sunrise at " + _fmt(pt['sunrise']) + "."
    elif pt['sunrise'] <= now < datetime.now(IST).replace(hour=10, minute=30):
        return "Morning study time. Spring Boot theory or DSA revision. MMA is at 8 PM now — mornings are for study. Office at 10:45."
    elif now.hour < 12 or (now.hour == 12 and now.minute < 44):
        return "Office. Dhuhr at " + _fmt(pt['dhuhr']) + "."
    elif pt['dhuhr'] <= now < pt['asr']:
        return "Office free time. Open LeetCode. One problem. Or study Claude cert. Asr at " + _fmt(pt['asr']) + "."
    elif pt['asr'] <= now < pt['maghrib']:
        return "Office hours. Pray Asr. Keep working. Maghrib at " + _fmt(pt['maghrib']) + ". Then MMA at 8 PM."
    elif pt['maghrib'] <= now < datetime.now(IST).replace(hour=19, minute=45):
        return "Home. Pray Maghrib. Eat light. MMA at 8 PM."
    elif datetime.now(IST).replace(hour=19, minute=45) <= now < datetime.now(IST).replace(hour=21, minute=0):
        return "MMA time. Get to BRUTE. Train hard."
    elif now.hour < 22 or (now.hour == 22 and now.minute < 30):
        return "Post-MMA. Shower, quick protein. Then Spring Boot block — 60 min, git commit."
    else:
        return "Sleep. Phone in kitchen. Tahajjud at " + _fmt(tahajjud) + "."


def _mentor_full_schedule():
    pt = _get_prayer_times()
    tahajjud = _tahajjud_time()
    return (
        f"Here's your prayer-anchored schedule for today. "
        f"Tahajjud at {_fmt(tahajjud)} — two nafl and istighfar. "
        f"Fajr at {_fmt(pt['fajr'])}. "
        f"Golden Block after Fajr — DSA revision and one new problem. No AI. "
        f"Sunrise at {_fmt(pt['sunrise'])} — Spring Boot theory, 45 minutes. "
        f"Morning free time — DSA revision, LeetCode, or Claude cert. MMA is at 8 PM now. "
        f"Office at 10:45. "
        f"Dhuhr at {_fmt(pt['dhuhr'])} — pray, then office free time for LeetCode. "
        f"Asr at {_fmt(pt['asr'])}. "
        f"Maghrib at {_fmt(pt['maghrib'])} — home, pray, eat light. "
        f"8 PM — MMA at BRUTE. "
        f"9:15 PM — Evening block, Spring Boot coding, 60 min, git commit. "
        f"Sleep by 10:30. Phone in kitchen. "
        f"Low bar daily: one DSA, 30 min Spring Boot, one career action. All three."
    )


def _mentor_tomorrow_morning():
    state = _parse_state(_read_session_state() or "")
    day = state.get('day', '?')
    next_day = str(int(day) + 1) if day.isdigit() else '?'
    pt = _get_prayer_times()
    tahajjud = _tahajjud_time()
    return (
        f"Tomorrow morning, Inshallah. "
        f"Tahajjud at {_fmt(tahajjud)} — two nafl, istighfar. "
        f"Fajr at {_fmt(pt['fajr'])}. "
        f"Then Golden Block — DSA revision and one new problem from memory. No AI. "
        f"Sunrise at {_fmt(pt['sunrise'])} — pre-workout fuel. "
        f"7 AM — MMA training. "
        f"You'll be on Day {next_day} of 84. "
        f"Sleep by 10 tonight so you can wake up for Tahajjud. Phone in kitchen. Bismillah."
    )


def _mentor_sleep_time():
    now = datetime.now(IST)
    pt = _get_prayer_times()
    tahajjud = _tahajjud_time()
    
    if now.hour >= 23 or now.hour < tahajjud.hour:
        return f"Sleep NOW. Phone in kitchen. Charger out of bedroom. Tahajjud at {_fmt(tahajjud)}. Fajr at {_fmt(pt['fajr'])}. Go."
    elif now.hour >= 22 or (now.hour == 22 and now.minute >= 30):
        return f"It's {_fmt(now)}. Past sleep time. Stop everything. Haldi doodh. Phone in kitchen. Tahajjud at {_fmt(tahajjud)}."
    elif now.hour >= 21 or (now.hour == 21 and now.minute >= 15):
        return f"It's {_fmt(now)}. Finish Spring Boot block. Then wind down. Sleep by 10:30. Tahajjud at {_fmt(tahajjud)}."
    else:
        return f"It's {_fmt(now)}. MMA at 8, Spring Boot at 9:15, sleep by 10:30. Tahajjud at {_fmt(tahajjud)}."


def _mentor_late_wake():
    now = datetime.now(IST)
    pt = _get_prayer_times()
    state = _parse_state(_read_session_state() or "")
    day = state.get('day', '?')
    total = state.get('total_days', '84')
    
    if now < pt['sunrise']:
        return f"Late wake. Zero guilt. Pray Fajr now — it's {_fmt(now)}, Fajr ends at sunrise {_fmt(pt['sunrise'])}. Then one DSA problem from memory. Low bar today. Day {day} of {total}."
    elif now < pt['dhuhr']:
        return f"Late wake. It's {_fmt(now)}. Morning is gone. Pray Fajr if you haven't — the obligation didn't pass. Dhuhr at {_fmt(pt['dhuhr'])}. Use office free time for one LeetCode problem. Low bar: one DSA, 30 min Spring Boot, one career action. Day {day} of {total}."
    elif now < pt['maghrib']:
        return f"It's {_fmt(now)}. Half the day is gone. No guilt. Pray Dhuhr and Asr. Then evening block: Spring Boot coding, 70 min. Hit the low bar. Day {day} of {total}."
    else:
        return f"It's {_fmt(now)}. Most of the day is gone. No guilt. Pray whatever is due. Evening block: Spring Boot coding. Hit the low bar. Day {day} of {total}."


# ─── 2. CAREER & PLAN ──────────────────────────────────────────────

def _mentor_career_plan():
    return (
        "Your career plan has three paths. "
        "Plan A, primary: Java plus Spring Boot, targeting BFSI and GCC roles, 16 to 50 LPA. "
        "Plan B, fallback: AI or GenAI engineer at a product company, 20 to 40 LPA. Pivot decision at Week 6. "
        "Plan C, safety net: stay at TCS, build portfolio, switch Q1 2027. "
        "Right now you're on Plan A. 12 weeks prep, then interviews Oct-Nov, resign post-offer, serve 90 days, join Feb-Mar 2027."
    )


def _mentor_timeline():
    state = _parse_state(_read_session_state() or "")
    day = state.get('day', '?')
    week = state.get('week', '1')
    return (
        f"You're on Day {day} of 84, Week {week}. "
        "Prep runs July to October. Interviews October to November. "
        "Resign after you get an offer. Serve 90 days notice December to February. "
        "Join new company February to March 2027. "
        "You can't resign without an offer. The timeline is locked."
    )


def _mentor_target_salary():
    return "Your target is 14 to 18 LPA minimum. BFSI GCCs pay 16 to 50 LPA for senior backend. Plan B AI roles pay 20 to 40 LPA. Don't undersell yourself. You're worth more than TCS is paying you."


def _mentor_applications():
    state = _parse_state(_read_session_state() or "")
    apps = state.get('applications', '0')
    if apps == '0':
        return "Zero applications sent. That's fine — you're in prep phase. Applications start October. Focus on DSA and Spring Boot now. But keep an eye on job postings to understand what companies want."
    return f"You've sent {apps} applications. Keep going. Track every one in your job application tracker."


def _mentor_on_track():
    state = _parse_state(_read_session_state() or "")
    day = state.get('day', '?')
    dsa = state.get('dsa_solved', '?')
    dsa_unaided = state.get('dsa_unaided', '0')
    streak = state.get('streak', '0')
    week = state.get('week', '1')
    
    issues = []
    if dsa_unaided == '0':
        issues.append("DSA unaided is zero — all 3 problems still need to be re-solved from memory")
    if streak == '0':
        issues.append("streak is broken — you missed days")
    
    if not issues:
        return f"You're on track. Day {day} of 84, Week {week}. {dsa} DSA solved. Keep going."
    
    return (
        f"Day {day} of 84, Week {week}. {dsa} DSA solved. "
        f"Here's the honest picture: {' '.join(issues)}. "
        "But the plan is completion-locked. Missing days extend the arc, never reset. "
        "What matters is showing up tomorrow. Hit the low bar: one DSA, 30 min Spring Boot, one career action."
    )


# ─── 3. DSA ────────────────────────────────────────────────────────

def _mentor_dsa_progress():
    state = _parse_state(_read_session_state() or "")
    solved = state.get('dsa_solved', '?')
    unaided = state.get('dsa_unaided', '0')
    total = state.get('dsa_total', '3')
    return (
        f"You've solved {solved} DSA problems. Contains Duplicate, Two Sum, Valid Anagram. "
        f"But unaided is {unaided} out of {total}. Zero percent from memory. "
        "This is the gap. You can't pass interviews with Copilot-level solving. "
        "Re-solve all three from memory this week. No AI, no notes, no hints. 15 minutes each. "
        "If you can't, you don't know them yet. That's what the Golden Block is for."
    )


def _mentor_dsa_next():
    state = _parse_state(_read_session_state() or "")
    unaided = state.get('dsa_unaided', '0')
    if unaided == '0':
        return (
            "Before any new problem, re-solve what you have from memory. "
            "One: Contains Duplicate. Two: Two Sum. Three: Valid Anagram. "
            "15 minutes each, no AI, no notes. If you can solve all three unaided, "
            "then move to Group Anagrams. But first, prove you own the first three."
        )
    return "Good, you've gone unaided on some problems. Next: Group Anagrams or Top K Frequent Elements. Both are hash map problems, same pattern as what you know."


def _mentor_dsa_unaided():
    state = _parse_state(_read_session_state() or "")
    unaided = state.get('dsa_unaided', '0')
    total = state.get('dsa_total', '3')
    return (
        f"Unaided count: {unaided} out of {total}. "
        "This is the number that matters for interviews. "
        "Copilot solving doesn't count. Aided doesn't count. Only from memory counts. "
        "Open a blank editor. No AI. No notes. Set a 15 minute timer. Solve. "
        "If you get stuck, that's data — you need more revision, not more new problems."
    )


# ─── 4. SPRING BOOT / LEARNING ────────────────────────────────────

def _mentor_last_concept():
    state = _parse_state(_read_session_state() or "")
    concept = state.get('last_concept', 'Spring Boot')
    return f"Last concept: {concept}. You understand the 4-layer flow: Controller to Service to Repository to Database. You know annotations are labels, and at-service goes on the class, not the method."


def _mentor_next_concept():
    state = _parse_state(_read_session_state() or "")
    pending = state.get('concepts_pending', 'Spring Boot basics')
    return (
        f"Next concepts to learn: {pending}. "
        "But first, your next laptop session is to create the 4 files in IntelliJ: "
        "Product dot java, ProductRepository, ProductService, ProductController. "
        "Run the app. Test the endpoints. That's how theory becomes real."
    )


def _mentor_next_laptop_session():
    state = _parse_state(_read_session_state() or "")
    return (
        f"Next laptop session: {state.get('next_laptop', 'Create files in IntelliJ')}. "
        "Open IntelliJ. Create the 4 files: Product entity, Product Repository, Product Service, Product Controller. "
        "Run the application. Test endpoints with Postman or curl. "
        "This is where it clicks. Theory in the morning, code in the evening."
    )


def _mentor_learning_mode():
    state = _parse_state(_read_session_state() or "")
    mode = state.get('mode', 'LAPTOP')
    if 'LAPTOP' in mode:
        return "You're in LAPTOP mode. Hands-on coding with IntelliJ. Theory in the morning, code in the evening. One feature, one commit."
    return f"Current mode: {mode}. Switch to LAPTOP mode to get hands-on with the code."


def _mentor_claude_cert():
    return (
        "Claude certification: not started. Study mode is office free time ONLY. "
        "Do NOT eat into evening prep time. Use your 1 to 2 PM office window for it. "
        "It's a differentiator on your resume. Start with one module this week."
    )


# ─── 5. BODY, DIET & TRAINING ──────────────────────────────────────

def _mentor_fasting():
    """Am I fasting today? — fasting status with prayer times."""
    if not _is_fasting_day():
        today = datetime.now(IST).strftime('%A')
        return f"Today is {today}. Not a fasting day. Your fasting days are Monday and Thursday. The Prophet, peace be upon him, used to fast on Mondays and Thursdays. Next fasting day: "
        # Find next Mon or Thu
        for i in range(1, 8):
            next_day = datetime.now(IST) + timedelta(days=i)
            if next_day.strftime('%A') in ['Monday', 'Thursday']:
                return f"Today is {today}, not a fasting day. Your fast days are Monday and Thursday. Next fast: {next_day.strftime('%A')}, {next_day.strftime('%B %d')}."
    
    now = datetime.now(IST)
    pt = _get_prayer_times()
    if now < pt['fajr']:
        return f"Today is a fasting day. Suhur ends at Fajr, {_fmt(pt['fajr'])}. Eat now: protein shake, dates, water. Make your niyyah. You have about {int((pt['fajr'] - now).total_seconds() / 60)} minutes left."
    elif now < pt['maghrib']:
        remaining = pt['maghrib'] - now
        hours = int(remaining.total_seconds() / 3600)
        mins = int((remaining.total_seconds() % 3600) / 60)
        return f"You're fasting today. Iftar at Maghrib, {_fmt(pt['maghrib'])}. About {hours} hours and {mins} minutes left. Stay focused. Use the mental clarity for DSA or Spring Boot. Dehydration is normal. Keep working."
    else:
        return f"Fast breaks at Maghrib, {_fmt(pt['maghrib'])}. If you haven't eaten: dates and water first, then a full meal with protein. Chicken, fish, or eggs. Hydrate: 2 to 3 liters of water between now and sleep. Alhamdulillah, you completed another fast."


def _mentor_diet():
    """What's my diet? — fasting-aware."""
    fasting_prefix = _fasting_status()
    if fasting_prefix:
        return (
            fasting_prefix +
            "Fasting day diet: Protein at Suhur — eggs and shake before Fajr. "
            "No food or water during the day. "
            "Iftar at Maghrib — dates and water first, then full meal: chicken, fish, or eggs. "
            "Hydrate: 2 to 3 liters between Maghrib and sleep. "
            "Haldi doodh at night. No dal, no rice, no roti."
        )
    return (
        "Your diet plan. Target: 83 to 70 kilos. "
        "No dal, no rice, no roti. "
        "Daily shake: 500 ml Ultra 7 percent milk, 2 scoops whey. About 700 calories, 66 grams protein. This is non-negotiable. "
        "Haldi doodh at night: toned 3 percent milk. "
        "Eggs must be fresh. Fish is basa. "
        "Dinner: low carb. "
        "Sunday: proteins only. "
        "Meal prep in batches. You live alone, so batch cook."
    )


def _mentor_weight_goal():
    return (
        "Weight target: 83 kilos down to 70 kilos. 13 kilos to cut. "
        "The cut is driven by diet, not just training. No dal, no rice, no roti. "
        "The daily shake is your protein anchor: 500 ml Ultra 7 percent, 2 scoops whey, 66 grams protein. "
        "MMA daily plus the diet gets you there. Consistency over speed."
    )


def _mentor_mma_schedule():
    now = datetime.now(IST)
    today = now.strftime('%A')
    
    # 8 PM rotation (pick 1 art per slot)
    evening = {
        'Monday': 'Wrestling on Mat 1, or Strength on Mat 2',
        'Tuesday': 'Muay Thai on Mat 1, or HIIT on Mat 2',
        'Wednesday': 'Boxing on Mat 1, or Strength on Mat 2',
        'Thursday': 'MMA on Mat 1, or Muay Thai on Mat 2',
        'Friday': 'Jiu Jitsu on Mat 1, or Strength on Mat 2',
    }
    # 7 AM doubles (Tue/Wed/Fri only, non-fasting)
    morning = {
        'Tuesday': 'Muay Thai on Mat 2',
        'Wednesday': 'Wrestling on Mat 1, or Strength on Mat 2',
        'Friday': 'Strength on Mat 2',
    }
    
    if today == 'Sunday':
        return "Sunday. Rest day. No MMA. Recovery is training. Your body needs this after 6 days."
    
    if today == 'Saturday':
        return "Saturday. Sparring at Mulund branch, 12 to 1 PM. 30 minute commute each way — leave by 11:15. No Manpada morning classes today. Sleep in slightly, then head to Mulund."
    
    # Mon-Fri
    fasting = today in ['Monday', 'Thursday']
    msg = f"Today is {today}. "
    if fasting:
        msg += "Fasting day — single session only. "
    
    if today in morning and not fasting:
        msg += f"Double day. 7 AM: {morning[today]}. Then 8 PM: {evening[today]}. Two sessions. Eat well between."
    else:
        msg += f"Primary session at 8 PM: {evening[today]}. "
        if not fasting:
            msg += "Mornings are for study. "
    
    return msg


def _mentor_what_eat():
    """What should I eat? — fasting-aware, prayer-anchored."""
    if _is_fasting_day():
        now = datetime.now(IST)
        pt = _get_prayer_times()
        if now < pt['fajr']:
            return f"Suhur time. Eat before Fajr at {_fmt(pt['fajr'])}. Protein shake, dates, water, 2 eggs. This is your fuel for the whole day. Don't skip Suhur."
        elif now < pt['maghrib']:
            return f"You're fasting. No food or water until Iftar at {_fmt(pt['maghrib'])}. Stay focused. Use the clarity. Drink water was at Suhur."
        else:
            return f"Iftar time. Break fast at {_fmt(pt['maghrib'])}. Dates and water first. Then full meal: chicken, fish, or eggs with vegetables. No rice, no roti. Hydrate well."
    
    now = datetime.now(IST)
    if now.hour < 6:
        return "Pre-Golden Block. Water and wudu. Eat after Fajr — pre-workout fuel before MMA."
    elif 6 <= now.hour < 7:
        return "Pre-workout fuel. 2 dates and water. Or a half shake. Light. You'll eat properly after MMA."
    elif 7 <= now.hour < 9:
        return "Post-workout meal. Within 15 minutes of finishing MMA. Full shake: 500 ml Ultra 7 percent, 2 scoops whey. Or 4 eggs. Protein within 15 minutes or you lose the window."
    elif 9 <= now.hour < 12:
        return "Mid-morning. If hungry: almonds or a boiled egg. No carbs. Keep it protein."
    elif 12 <= now.hour < 15:
        return "Lunch at office. Protein focused. Chicken, fish, or eggs. No rice, no roti. Salad is fine. If nothing good is available, have your shake."
    elif 15 <= now.hour < 17:
        return "Afternoon. If hungry: almonds, or a boiled egg. No snacks, no biscuits. Water."
    elif 17 <= now.hour < 20:
        return "Pre-dinner. Don't snack. Wait for dinner. If really hungry: haldi doodh early."
    elif 20 <= now.hour < 22:
        return "Dinner time. Low carb. Protein and vegetables. Fish basa, chicken, or eggs. No rice, no roti, no dal. Then haldi doodh before sleep."
    else:
        return "No more food. Haldi doodh only if you haven't had it. Then sleep. Phone in kitchen."


def _mentor_pre_workout():
    """Pre-workout for 8 PM MMA session."""
    now = datetime.now(IST)
    if _is_fasting_day() and now.hour < 17:
        return "Fasting day. Your MMA session is at 8 PM — after Iftar. Eat at Maghrib, then train. No pre-workout needed during the day."
    if now.hour < 19:
        return "Pre-MMA fuel: eat a light meal around 7 PM. Chicken or eggs with vegetables. Not heavy — you'll be training at 8. Water."
    elif now.hour < 20:
        return "Almost MMA time. Light snack 30 min before: banana or dates. Water. Get to BRUTE."
    return "You should be at BRUTE training. Pre-workout window is over."


def _mentor_post_workout():
    """Post-workout for 9 PM (after 8 PM MMA)."""
    now = datetime.now(IST)
    if _is_fasting_day():
        return "Fasting day post-MMA: You already had Iftar before training. After MMA: full shake — 500 ml Ultra 7 percent, 2 scoops whey. Or 4 eggs. Protein within 15 minutes. Then Spring Boot block at 9:15."
    if 21 <= now.hour < 22:
        return "Post-MMA. Shower. Quick protein: shake or 4 eggs. Then Spring Boot block at 9:15. You have 15 minutes to eat and shower."
    return "Post-workout meal: shake — 500 ml Ultra 7 percent, 2 scoops whey. Or 4 eggs. Protein within 15 minutes of finishing."


# ─── 6. DEEN & PRAYER ──────────────────────────────────────────────

def _mentor_prayer_status():
    """What prayers do I need? — live prayer times."""
    now = datetime.now(IST)
    pt = _get_prayer_times()
    
    if now < pt['fajr']:
        tahajjud = _tahajjud_time()
        if now >= tahajjud:
            return f"Tahajjud time. Fajr at {_fmt(pt['fajr'])}. Pray both. This is the most powerful time."
        return f"Fajr at {_fmt(pt['fajr'])}. Tahajjud at {_fmt(tahajjud)} before that. Sleep now if you haven't."
    elif pt['fajr'] <= now < pt['sunrise']:
        return f"Fajr time. Pray now if you haven't. Window closes at sunrise {_fmt(pt['sunrise'])}."
    elif pt['sunrise'] <= now < pt['dhuhr']:
        return f"Fajr should be done. If not, pray immediately. Dhuhr at {_fmt(pt['dhuhr'])}."
    elif pt['dhuhr'] <= now < pt['asr']:
        return f"Dhuhr time. Pray now. Asr at {_fmt(pt['asr'])}."
    elif pt['asr'] <= now < pt['maghrib']:
        return f"Asr time. Pray now if you haven't. Maghrib at {_fmt(pt['maghrib'])}."
    elif pt['maghrib'] <= now < pt['isha']:
        return f"Maghrib time. Pray now. Isha at {_fmt(pt['isha'])}."
    elif now >= pt['isha']:
        tahajjud = _tahajjud_time()
        return f"Isha time. Pray if you haven't. Then sleep. Tahajjud at {_fmt(tahajjud)}."
    return "Check your prayer times."


def _mentor_dua():
    now = datetime.now(IST)
    nuggets = [
        "The Prophet, peace be upon him, said: Allah says, I am as my servant thinks of me. Think well of Allah. Bukhari.",
        "The Prophet said: Take advantage of five before five. Your youth before old age. Your health before sickness. Your wealth before poverty. Your free time before busyness. Your life before death. Hakim.",
        "Allah says in the Quran: Indeed, with hardship comes ease. With hardship comes ease. Ash-Sharh, verses 5 and 6.",
        "The Prophet said: The most beloved deeds to Allah are the most consistent, even if small. Bukhari and Muslim.",
        "Allah says: Do not despair of Allah's mercy. Indeed, Allah forgives all sins. Az-Zumar, verse 53.",
        "The Prophet said: Whoever takes one step toward Allah, Allah takes ten steps toward him. Muslim.",
        "Umar ibn al-Khattab said: Accountability before accountability. Weigh yourselves before you are weighed.",
    ]
    return nuggets[int(now.timestamp()) % len(nuggets)]


def _mentor_tahajjud():
    now = datetime.now(IST)
    pt = _get_prayer_times()
    tahajjud = _tahajjud_time()
    
    if now >= tahajjud and now < pt['fajr']:
        return f"It's Tahajjud time RIGHT NOW. {_fmt(now)}. Two nafl, istighfar. Quick — Fajr at {_fmt(pt['fajr'])}. Then Golden Block."
    elif now < tahajjud:
        return f"Tahajjud at {_fmt(tahajjud)} — just 15 minutes before Fajr at {_fmt(pt['fajr'])}. You don't need to wake up at 2 AM. Sleep by 10, wake 15 min before Fajr, pray 2 nafl, then Fajr. Simple and consistent."
    else:
        return f"Tahajjud is at {_fmt(tahajjud)} — 15 minutes before Fajr at {_fmt(pt['fajr'])}. Two nafl and istighfar. The Prophet said the most beloved deeds are the most consistent, even if small. Sleep by 10. Phone in kitchen."


# ─── 7. MENTAL HEALTH & RELAPSE ───────────────────────────────────

def _mentor_feeling_lost():
    now = datetime.now(IST)
    state = _parse_state(_read_session_state() or "")
    day = state.get('day', '?')
    total = state.get('total_days', '84')
    
    responses = [
        f"Ramish, feeling lost means you're human, not broken. You're on Day {day} of {total}. The plan doesn't reset. Missing days extend the arc, never reset. One thing right now: pray two nafl and make istighfar. Then do one small thing. One DSA problem. One page of reading. One pushup set. Action kills the freeze. Bismillah.",
        f"Brother, the feeling of being lost is the freeze. Your brain is lying to you — it says everything is too much. It's not. Pick one thing. Just one. Open LeetCode. Solve Contains Duplicate from memory. 15 minutes. That breaks the freeze. You're on Day {day} of {total}. The arc continues.",
        f"Ramish, you've felt lost before and you came back every time. This is not different. The chain is: reels, no sleep, exhaustion, guilt, freeze. You're in the freeze. The way out is action. Not motivation. Action creates motivation, not the other way around. Do one thing right now. Pray, then code. Bismillah.",
    ]
    return responses[int(now.timestamp()) % 3]


def _mentor_relapse():
    return (
        "Ramish, listen carefully. "
        "Step 1: You acknowledged it. That's strength, not weakness. Most people hide this. "
        "Step 2: Sunnah reset. Two nafl and istighfar. Renew your wudu. "
        "Step 3: Root cause. What triggered it? Phone? Loneliness? Boredom? "
        "Step 4: Shield adjustment. We'll fix the trigger. "
        "Step 5: Move forward. No shame. Allah doesn't need your perfection, He needs your return. "
        "Indeed, Allah loves those who are constantly repentant. Baqarah, verse 222. "
        "Now stand up. Pray two nafl. Then do one thing. One DSA problem. The arc continues."
    )


def _mentor_overwhelmed():
    return (
        "Ramish, overwhelm is your brain trying to solve everything at once. It can't. You don't have to. "
        "Here's the truth: you only need to do ONE thing right now. Not the whole plan. Not 84 days. Just the next thing. "
        "What's the next thing? Pray if a prayer is due. Then open one DSA problem. 15 minutes. That's it. "
        "The rest of the plan will be there after 15 minutes. But right now, just one thing. Bismillah."
    )


def _mentor_want_to_give_up():
    return (
        "Ramish, you've wanted to give up before. Every time, you came back. This time is no different. "
        "You're not at 1 percent of your potential — you know this. You feel it. The gap between where you are and where you could be is what hurts. That pain is not weakness. It's hunger. "
        "But giving up doesn't make the pain stop. It makes it permanent. Showing up makes it temporary. "
        "One thing right now. Not the whole plan. One DSA problem. One prayer. One pushup set. Action. Not motivation. Bismillah."
    )


def _mentor_stressed_money():
    return (
        "Ramish, the money stress is real. 12 lakhs debt. EMIs and rent eat your salary. 3 to 6 months runway. "
        "But here's the fact: you can't resign without an offer. And you can't get an offer without prep. "
        "So the money fix is not more worry. It's one DSA problem today. One Spring Boot session today. One career action today. "
        "The debt doesn't go away by worrying. It goes away by getting a 16 to 18 LPA offer. And that comes from showing up daily. "
        "Hit the low bar. The arc continues. Bismillah."
    )


def _mentor_worried_future():
    return (
        "Ramish, the future is not yours to carry right now. Allah says: Do not despair of His mercy. "
        "Your job today is not to solve February 2027. Your job is to hit the low bar today. "
        "One DSA. 30 minutes Spring Boot. One career action. That's it. "
        "The future is built from these days, not from worry. Do today well, and February takes care of itself. "
        "Bismillah."
    )


def _mentor_cant_sleep():
    now = datetime.now(IST)
    if now.hour >= 22 or now.hour < 4:
        return (
            "Can't sleep? Do this. One: phone in kitchen. Not beside the bed. Kitchen. "
            "Two: haldi doodh. Toned 3 percent milk, warm. "
            "Three: no screens. If you need something, read or make dhikr. "
            "Four: close your eyes and make istighfar. Say Astaghfirullah slowly. "
            "The Prophet said sleep is the brother of death. Go peacefully. Allah hafiz."
        )
    return f"It's {now.strftime('%I:%M %p')}. Not sleep time yet. Finish your blocks. The sleep protocol starts at 10 PM."


def _mentor_distracted():
    return (
        "Distracted? That's the ADHD brain. It's not a character flaw, it's how you're wired. "
        "Here's the fix: one task, one timer. 15 minutes. Phone greyscale. Close everything else. "
        "One DSA problem. One Spring Boot file. One thing. "
        "Don't fight the distraction. Just shrink the task until it's smaller than the distraction. "
        "15 minutes. Go."
    )


def _mentor_triggers():
    return (
        "Your relapse chain is: phone or web series, then no sleep, then exhaustion, then guilt, then freeze. "
        "The chain always starts the same way. Phone in the evening. "
        "The fix is not willpower. It's environment. Phone greyscale. Phone in kitchen after 10. "
        "No reels in the bedroom. The 5 minute rule: home, wudu, pray, then anything. "
        "Break the first link and the chain never forms."
    )


def _mentor_savior_complex():
    return (
        "Ramish, this is hard to hear but you need it. You find significance in being needed. "
        "The female friend who depends on you — that's not love, that's guilt. "
        "Ask yourself honestly: if she didn't need you, would you feel relief or panic? "
        "If relief, it's not love. It's a savior complex. You feel powerless elsewhere, "
        "so you find power in being needed. "
        "Real power is building your own life. DSA. Career. Deen. That's where your significance lives. "
        "Not in someone else's dependency."
    )


# ─── 8. PROGRESS & STREAK ──────────────────────────────────────────

def _mentor_streak():
    state = _parse_state(_read_session_state() or "")
    streak = state.get('streak', '0')
    day = state.get('day', '?')
    total = state.get('total_days', '84')
    dsa = state.get('dsa_solved', '?')
    return f"Your streak is {streak} days. Day {day} of {total}. {dsa} DSA problems solved. The plan is completion locked. Missing days extend the arc, never reset. Keep going."


def _mentor_morning_check():
    now = datetime.now(IST)
    pt = _get_prayer_times()
    tahajjud = _tahajjud_time()
    state = _parse_state(_read_session_state() or "")
    day = state.get('day', '?')
    total = state.get('total_days', '84')
    
    if now < pt['sunrise']:
        return f"Bismillah. It's {_fmt(now)}. Survival layer: brush, cold water face, wudu, Tahajjud, Fajr at {_fmt(pt['fajr'])}. Then Golden Block — DSA. Day {day} of {total}."
    elif now < pt['dhuhr']:
        return f"Morning check-in. It's {_fmt(now)}. Did you pray Fajr? Did you do the Golden Block? If not, pray now and do one DSA problem. Dhuhr at {_fmt(pt['dhuhr'])}. Low bar: one DSA, 30 min Spring Boot, one career action. Day {day} of {total}."
    else:
        return f"It's {_fmt(now)}. Morning is gone. Low bar today: one DSA, 30 min Spring Boot, one career action. Hit the low bar and the day counts. Day {day} of {total}."


def _mentor_evening_close():
    now = datetime.now(IST)
    pt = _get_prayer_times()
    tahajjud = _tahajjud_time()
    state = _parse_state(_read_session_state() or "")
    day = state.get('day', '?')
    total = state.get('total_days', '84')
    
    if now.hour >= 21:
        return f"Evening close-out. It's {_fmt(now)}. Did you hit the low bar? One DSA, 30 min Spring Boot, one career action? If yes, the day counts. Did you train at MMA? Phone in kitchen. Sleep by 10:30. Tahajjud at {_fmt(tahajjud)}. Day {day} of {total}."
    elif now.hour >= 20:
        return f"It's {_fmt(now)}. You should be at MMA. Evening block at 9:15 after. Maghrib was at {_fmt(pt['maghrib'])}. Day {day} of {total}."
    else:
        return f"It's {_fmt(now)}. MMA at 8 PM. Evening block at 9:15 — Spring Boot, 60 min, git commit. Maghrib at {_fmt(pt['maghrib'])}. Day {day} of {total}."


def _mentor_completed_task(slots):
    task = ""
    if slots and 'task' in slots:
        task = slots['task'].get('value', '').lower()
    
    state = _parse_state(_read_session_state() or "")
    day = state.get('day', '?')
    total = state.get('total_days', '84')
    
    if "dsa" in task or "problem" in task or "leetcode" in task:
        dsa = state.get('dsa_solved', '?')
        return f"Mashallah. DSA done. That's {dsa} total problems now. Next: Spring Boot theory or coding block. Day {day} of {total}. Keep the streak alive."
    elif "spring" in task or "boot" in task or "code" in task or "coding" in task:
        return f"Solid. Spring Boot done. Git commit it. Day {day} of {total}. Next: one career action. Update resume, check job postings, or LinkedIn."
    elif "gym" in task or "mma" in task or "workout" in task or "training" in task:
        return f"Alhamdulillah. Training done. Post-workout meal now — shake or eggs, within 15 minutes. Day {day} of {total}."
    elif "pray" in task or "prayer" in task or "salah" in task or "fajr" in task or "dhuhr" in task or "maghrib" in task or "isha" in task:
        return f"Mashallah. Prayer done. Allah accepted it. Day {day} of {total}. What's next?"
    elif "study" in task or "reading" in task or "theory" in task:
        return f"Good. Theory done. Now apply it — open IntelliJ and code something from what you just learned. Day {day} of {total}."
    elif "cert" in task or "claude" in task:
        return f"Good. Cert progress. Keep it in office free time only. Day {day} of {total}."
    elif "application" in task or "apply" in task or "job" in task:
        return f"Mashallah. Application sent. Track it in your job tracker. Day {day} of {total}. Keep sending."
    else:
        return f"Mashallah. Task done. You're on Day {day} of {total}. The streak continues. What's next?"


def _mentor_what_did_i_miss():
    state = _parse_state(_read_session_state() or "")
    missed = state.get('missed_days', 'none')
    if missed == 'none' or 'none' in missed.lower():
        return "No missed days recorded. You're on track. Keep going."
    return f"Missed days: {missed}. The arc is extended, not reset. These days are added to the end. No guilt. Just show up tomorrow and hit the low bar."


def _mentor_daily_bar():
    return (
        "Daily bar system. "
        "Green, low bar: one DSA problem, 30 minutes Spring Boot, one career action. All three. "
        "Yellow, high bar: four DSA problems, full Spring Boot session, full career block. "
        "Banked days: zero out of five max. They expire after 14 days. "
        "Rest day: zero guilt, arc continues, streak preserved. Pause, not break. "
        "Hit the low bar daily. That's the standard. High bar is a bonus."
    )


def _mentor_weekly_review():
    state = _parse_state(_read_session_state() or "")
    week = state.get('week', '1')
    return (
        f"Week {week} review. "
        "Every Friday, take 30 minutes. Score yourself: DSA, Spring Boot, career actions, prayers, sleep, diet. "
        "What worked? What didn't? What changes for next week? "
        "Be honest but not harsh. The plan is completion-locked. Adjust and continue."
    )


# ─── 9. LIGHTS & MODE ──────────────────────────────────────────────

def _mentor_start_study_mode():
    hall_id = DEVICES["hall"][0]
    _tuya_send_command(hall_id, [{"code": sw, "value": False} for sw in ALL_SWITCHES])
    room_id = DEVICES["room"][0]
    _tuya_send_command(room_id, [{"code": "switch_1", "value": True}] + 
                       [{"code": sw, "value": False} for sw in ALL_SWITCHES[1:]])
    return "Study mode. Hall lights off, room light on. The Prophet said the most beloved deeds are the most consistent, even if small. Open IntelliJ. One feature, one commit. Bismillah."


def _mentor_start_sleep_mode():
    _turn_off_all_lights()
    return "Sleep mode. All lights off. Three rules: charger out of bedroom, phone greyscale, phone in kitchen. The Prophet said sleep is the brother of death. Go peacefully. Allah hafiz."


# ═══════════════════════════════════════════════════════════════════
# ALEXA SKILL HANDLER
# ═══════════════════════════════════════════════════════════════════

@app.route('/alexa', methods=['POST'])
def alexa_webhook():
    try:
        data = request.json
        if not data:
            logger.error("EMPTY BODY received")
            return jsonify(_build_response("Sorry, I didn't catch that.", should_end=True))
            
        request_type = data.get('request', {}).get('type', '')
        logger.info("HANDLING type=%s", request_type)
        
        if request_type == 'LaunchRequest':
            now = datetime.now(IST)
            state = _parse_state(_read_session_state() or "")
            day = state.get('day', '?')
            
            greeting = "Assalamu alaikum Ramish."
            if now.hour < 6:
                greeting += " Early morning. Golden Block time."
            elif 6 <= now.hour < 12:
                greeting += " Good morning."
            elif 12 <= now.hour < 17:
                greeting += " Afternoon. Use office time well."
            elif 17 <= now.hour < 22:
                greeting += " Evening. Study block coming."
            else:
                greeting += " It's late. Sleep."
            
            greeting += f" You're on Day {day} of 84. Ask me: what's my routine, what should I do next, what's my DSA progress, what did I learn, what's my diet, give me a dua, or check my streak."
            return jsonify(_build_response(greeting))
        
        if request_type == 'IntentRequest':
            intent = data.get('request', {}).get('intent', {})
            intent_name = intent.get('name', '')
            slots = intent.get('slots', {})
            logger.info("INTENT name=%s slots=%s", intent_name, json.dumps(slots))
            return _handle_intent(intent_name, slots)
        
        if request_type == 'CanFulfillIntentRequest':
            intent = data.get('request', {}).get('intent', {})
            intent_name = intent.get('name', '')
            known = intent_name in _ALL_INTENT_NAMES
            logger.info("CAN_FULFILL intent=%s can=%s", intent_name, "YES" if known else "NO")
            return jsonify({
                "version": "1.0",
                "response": {
                    "canFulfillIntent": {
                        "canFulfill": "YES" if known else "NO",
                        "slots": {}
                    }
                }
            })
        
        if request_type == 'SessionEndedRequest':
            logger.info("SESSION ENDED reason=%s", data.get('request', {}).get('reason', '?'))
            return jsonify({})
        
        logger.warning("UNKNOWN REQUEST TYPE: %s", request_type)
        return jsonify(_build_response("Sorry, I didn't understand that.", should_end=True))
        
    except Exception as e:
        logger.error("EXCEPTION in webhook: %s", str(e), exc_info=True)
        return jsonify(_build_response("Sorry, something went wrong.", should_end=True))


def _handle_intent(intent_name, slots):
    handlers = {
        # Schedule & Time
        'RoutineIntent': lambda: _build_response(_mentor_routine_today()),
        'WhatNextIntent': lambda: _build_response(_mentor_what_next()),
        'FullScheduleIntent': lambda: _build_response(_mentor_full_schedule()),
        'TomorrowIntent': lambda: _build_response(_mentor_tomorrow_morning()),
        'SleepTimeIntent': lambda: _build_response(_mentor_sleep_time()),
        'LateWakeIntent': lambda: _build_response(_mentor_late_wake()),
        
        # Career & Plan
        'CareerPlanIntent': lambda: _build_response(_mentor_career_plan()),
        'TimelineIntent': lambda: _build_response(_mentor_timeline()),
        'TargetSalaryIntent': lambda: _build_response(_mentor_target_salary()),
        'ApplicationsIntent': lambda: _build_response(_mentor_applications()),
        'OnTrackIntent': lambda: _build_response(_mentor_on_track()),
        
        # DSA
        'DsaProgressIntent': lambda: _build_response(_mentor_dsa_progress()),
        'DsaNextIntent': lambda: _build_response(_mentor_dsa_next()),
        'DsaUnaidedIntent': lambda: _build_response(_mentor_dsa_unaided()),
        
        # Spring Boot / Learning
        'LastConceptIntent': lambda: _build_response(_mentor_last_concept()),
        'NextConceptIntent': lambda: _build_response(_mentor_next_concept()),
        'NextLaptopIntent': lambda: _build_response(_mentor_next_laptop_session()),
        'LearningModeIntent': lambda: _build_response(_mentor_learning_mode()),
        'ClaudeCertIntent': lambda: _build_response(_mentor_claude_cert()),
        
        # Body, Diet & Training
        'FastingIntent': lambda: _build_response(_mentor_fasting()),
        'DietIntent': lambda: _build_response(_mentor_diet()),
        'WeightGoalIntent': lambda: _build_response(_mentor_weight_goal()),
        'MmaScheduleIntent': lambda: _build_response(_mentor_mma_schedule()),
        'WhatEatIntent': lambda: _build_response(_mentor_what_eat()),
        'PreWorkoutIntent': lambda: _build_response(_mentor_pre_workout()),
        'PostWorkoutIntent': lambda: _build_response(_mentor_post_workout()),
        
        # Deen & Prayer
        'PrayerStatusIntent': lambda: _build_response(_mentor_prayer_status()),
        'DuaIntent': lambda: _build_response(_mentor_dua()),
        'TahajjudIntent': lambda: _build_response(_mentor_tahajjud()),
        
        # Mental Health
        'FeelingLostIntent': lambda: _build_response(_mentor_feeling_lost()),
        'RelapseIntent': lambda: _build_response(_mentor_relapse()),
        'OverwhelmedIntent': lambda: _build_response(_mentor_overwhelmed()),
        'GiveUpIntent': lambda: _build_response(_mentor_want_to_give_up()),
        'StressedMoneyIntent': lambda: _build_response(_mentor_stressed_money()),
        'WorriedFutureIntent': lambda: _build_response(_mentor_worried_future()),
        'CantSleepIntent': lambda: _build_response(_mentor_cant_sleep()),
        'DistractedIntent': lambda: _build_response(_mentor_distracted()),
        'TriggersIntent': lambda: _build_response(_mentor_triggers()),
        'SaviorComplexIntent': lambda: _build_response(_mentor_savior_complex()),
        
        # Progress & Streak
        'CheckStreakIntent': lambda: _build_response(_mentor_streak()),
        'MorningCheckIntent': lambda: _build_response(_mentor_morning_check()),
        'EveningCloseIntent': lambda: _build_response(_mentor_evening_close()),
        'CompletedTaskIntent': lambda: _build_response(_mentor_completed_task(slots)),
        'WhatDidIMissIntent': lambda: _build_response(_mentor_what_did_i_miss()),
        'DailyBarIntent': lambda: _build_response(_mentor_daily_bar()),
        'WeeklyReviewIntent': lambda: _build_response(_mentor_weekly_review()),
        
        # Lights & Mode
        'TurnOffLightsIntent': lambda: _build_response(_turn_off_all_lights() or "All lights off."),
        'TurnOnLightsIntent': lambda: _build_response(_turn_on_all_lights() or "All lights on."),
        'StudyModeIntent': lambda: _build_response(_mentor_start_study_mode()),
        'SleepModeIntent': lambda: _build_response(_mentor_start_sleep_mode()),
        
        # Built-in
        'AMAZON.HelpIntent': lambda: _build_response(
            "I'm your mentor through Alexa. You can ask me: what's my routine, what should I do next, "
            "what's my full schedule, what should I do tomorrow morning, what's my career plan, "
            "am I on track, what's my DSA progress, what DSA problem should I do next, "
            "what did I learn last, what's next to learn, what's my next laptop session, "
            "what's my diet, what should I eat, what's my weight goal, when is MMA, "
            "what should I eat before workout, what should I eat after workout, "
            "what prayers do I need, give me a dua, when is tahajjud, "
            "I'm feeling lost, I relapsed, I'm overwhelmed, I want to give up, "
            "I'm stressed about money, I'm worried about the future, I can't sleep, "
            "I'm distracted, what are my triggers, "
            "check my streak, what did I miss, what's my daily bar, "
            "morning check-in, evening close out, I completed DSA, "
            "start study mode, start sleep mode, turn off lights, or turn on lights."
        ),
        'AMAZON.CancelIntent': lambda: _build_response("Allah hafiz.", should_end=True),
        'AMAZON.StopIntent': lambda: _build_response("Allah hafiz.", should_end=True),
        'AMAZON.FallbackIntent': lambda: _build_response(
            "I didn't catch that. You can ask me: what's my routine, what should I do next, what's my DSA progress, give me a dua, or check my streak.",
            reprompt="Try saying: what should I do next, what's my diet, or check my streak."
        ),
        'AMAZON.NavigateHomeIntent': lambda: _build_response("Allah hafiz.", should_end=True),
    }
    
    handler = handlers.get(intent_name)
    if handler:
        logger.info("HANDLER FOUND for %s", intent_name)
        result = handler()
        logger.info("RESPONSE size=%d", len(json.dumps(result)))
        return jsonify(result)
    
    logger.warning("NO HANDLER for intent: %s", intent_name)
    return jsonify(_build_response(
        "Sorry, I didn't catch that. Try: what's my routine, what should I do next, or check my streak.",
        reprompt="Try saying: what should I do next, what's my diet, or check my streak."
    ))


# ─── All intent names (for CanFulfillIntent) ──────────────────────
_ALL_INTENT_NAMES = set([
    'RoutineIntent', 'WhatNextIntent', 'FullScheduleIntent', 'TomorrowIntent',
    'SleepTimeIntent', 'LateWakeIntent',
    'CareerPlanIntent', 'TimelineIntent', 'TargetSalaryIntent',
    'ApplicationsIntent', 'OnTrackIntent',
    'DsaProgressIntent', 'DsaNextIntent', 'DsaUnaidedIntent',
    'LastConceptIntent', 'NextConceptIntent', 'NextLaptopIntent',
    'LearningModeIntent', 'ClaudeCertIntent',
    'DietIntent', 'WeightGoalIntent', 'MmaScheduleIntent',
    'WhatEatIntent', 'PreWorkoutIntent', 'PostWorkoutIntent', 'FastingIntent',
    'PrayerStatusIntent', 'DuaIntent', 'TahajjudIntent',
    'FeelingLostIntent', 'RelapseIntent', 'OverwhelmedIntent',
    'GiveUpIntent', 'StressedMoneyIntent', 'WorriedFutureIntent',
    'CantSleepIntent', 'DistractedIntent', 'TriggersIntent', 'SaviorComplexIntent',
    'CheckStreakIntent', 'MorningCheckIntent', 'EveningCloseIntent',
    'CompletedTaskIntent', 'WhatDidIMissIntent', 'DailyBarIntent', 'WeeklyReviewIntent',
    'TurnOffLightsIntent', 'TurnOnLightsIntent', 'StudyModeIntent', 'SleepModeIntent',
    'AMAZON.HelpIntent', 'AMAZON.CancelIntent', 'AMAZON.StopIntent',
    'AMAZON.FallbackIntent', 'AMAZON.NavigateHomeIntent',
])


def _build_response(speech_text, should_end=False, reprompt=None):
    response = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "SSML",
                "ssml": f"<speak>{speech_text}</speak>"
            },
            "shouldEndSession": should_end
        }
    }
    if reprompt:
        response["response"]["reprompt"] = {
            "outputSpeech": {
                "type": "SSML",
                "ssml": f"<speak>{reprompt}</speak>"
            }
        }
    return response


# ─── Health Check ────────────────────────────────────────────────

@app.route('/health', methods=['GET'])
def health():
    now = datetime.now(IST)
    state = _parse_state(_read_session_state() or "")
    return jsonify({
        "status": "ok",
        "service": "alexa-hermes-mentor",
        "time_ist": now.strftime('%Y-%m-%d %H:%M:%S IST'),
        "day": state.get('day', '?'),
        "total_days": state.get('total_days', '84'),
        "streak": state.get('streak', '0'),
        "dsa_solved": state.get('dsa_solved', '?'),
    })


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8443)

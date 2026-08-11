# Hermes Alexa Skill — Setup Guide

## What's Running
- **Flask app**: `/root/alexa-hermes/app.py` (gunicorn on 127.0.0.1:8443)
- **Caddy reverse proxy**: `hermes.ramishtaha.com` → 127.0.0.1:8443 (auto-SSL)
- **systemd service**: `alexa-hermes.service` (auto-restart, survives reboots)
- **Health check**: `https://hermes.ramishtaha.com/health`

## Alexa Skill Setup (Amazon Developer Console)

1. Go to https://developer.amazon.com/alexa → sign in with your Amazon account
2. Click "Create Skill" → name it "Hermes"
3. Choose "Custom" model + "Provision your own" backend
4. **Endpoint**: HTTPS → `https://hermes.ramishtaha.com/alexa`
5. **SSL Certificate**: "I will upload" → or let Amazon verify (Caddy's Let's Encrypt cert is valid)
6. **Interaction Model**: Copy-paste contents of `alexa-skill-model.json` into JSON Editor
7. Save → Build → Test

## Voice Commands
- "Alexa, ask Hermes to turn off all lights"
- "Alexa, ask Hermes to start study mode"
- "Alexa, ask Hermes to start sleep mode"
- "Alexa, ask Hermes to check my streak"
- "Alexa, ask Hermes to check my schedule"

## Tuya Integration (TODO — when ready)
1. Go to https://iot.tuya.com → sign up
2. Create a Cloud Project → get Access ID + Access Secret
3. Add to `/root/alexa-hermes/.env`:
   ```
   TUYA_ACCESS_ID=your_id
   TUYA_ACCESS_SECRET=your_secret
   TUYA_DEVICE_IDS=device1,device2
   ```
4. Restart: `systemctl restart alexa-hermes`

## Logs
- Flask: `journalctl -u alexa-hermes -f`
- Caddy: `tail -f /var/log/caddy/hermes-alexa.log`

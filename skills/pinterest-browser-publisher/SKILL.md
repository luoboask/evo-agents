---
name: pinterest-browser-publisher
version: 1.0.0
description: Automate Pinterest pin publishing via browser automation (Playwright). No API key needed. Supports single pins, carousels, and batch publishing. Use when user wants to auto-publish to Pinterest without API access, or needs browser-based automation for pin creation, board management, and scheduling.
---

# Pinterest Browser Publisher

Browser-based Pinterest automation using Playwright. No API required.

## Quick Start

### 1. Install Dependencies

```bash
npm install -g playwright
playwright install chromium
```

### 2. First-Time Setup

```bash
cd skills/pinterest-browser-publisher
node scripts/login.js
```

This opens a browser. Log in manually. Cookies are saved for future runs.

### 3. Publish a Pin

```bash
node scripts/publish.js \
  --images "./pins/01.png,./pins/02.png,./pins/03.png" \
  --title "Mercury Retrograde Survival Guide" \
  --description "Your description here..." \
  --board "Astrology & Spiritual Wellness"
```

## Workflow Integration

```
aura-content-strategist → Pinterest copy
         ↓
  aura-image-gen → Images (2:3 ratio)
         ↓
pinterest-browser-publisher → Auto-publish
```

## Commands

| Command | Description |
|---------|-------------|
| `node scripts/login.js` | Manual login, save session |
| `node scripts/publish.js` | Publish single pin |
| `node scripts/batch.js --input pins.json` | Batch publish |
| `node scripts/boards.js --list` | List boards |
| `node scripts/boards.js --create "New Board"` | Create board |
| `node scripts/status.js` | Check account status |

## Configuration

Edit `~/.config/pinterest/config.json`:

```json
{
  "headless": false,
  "slowMo": 100,
  "postDelay": 30000,
  "randomizeTiming": true
}
```

## Safety

- Rate limit: 10 pins/hour, 50 pins/day
- Random delays between actions (2-5s)
- Human-like mouse movement
- Session persistence (no repeated logins)

## References

- `scripts/login.js` — Login helper
- `scripts/publish.js` — Pin publisher
- `scripts/batch.js` — Batch publisher
- `lib/selectors.js` — Pinterest DOM selectors
- `lib/cookies.js` — Session management

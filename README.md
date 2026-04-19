# SkyCast 🌤️ — Beautiful Live Weather App

A production-quality weather web app with auto location detection, live animated backgrounds,
and Apple-style glassmorphism — built with **Python (Flask)** + vanilla **JavaScript**.

## ✨ Features

| Feature | Detail |
|---------|--------|
| 📍 Auto location | Browser Geolocation API → exact coordinates |
| 🌍 Reverse geocoding | OpenStreetMap Nominatim (free, no key) |
| ⛅ Weather data | Open-Meteo API (free, no key) |
| 🎨 Live backgrounds | Animated canvas — rain, snow, stars, lightning, fog wisps, cloud wisps |
| 💎 Glassmorphism | `backdrop-filter: blur` + layered transparency |
| 📱 Mobile-first | Safe-area aware, smooth scroll, touch-friendly |
| ♻️ Smart cache | Server-side 10-min cache (weather) / 24h (geocode) |
| 🔍 City search | Search any city worldwide |
| 🌡️ Unit toggle | °C / °F + km/h / mph — persists across sessions |
| ☀️ Sun arc | Live animated daylight arc with position |
| 🌧️ 24h precip chart | Canvas bar chart of precipitation probability |
| 📅 7-day forecast | Daily icons, high/low bar, precipitation |

## 🚀 Quick Start

```bash
# 1. Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
python app.py

# 4. Open in browser
# http://localhost:5000
```

> **Tip:** Use a modern browser (Chrome, Safari, Firefox 100+) for full `backdrop-filter` support.

## 🗂️ Project Structure

```
skycast/
├── app.py              ← Flask backend (API proxy + cache)
├── requirements.txt
├── README.md
└── templates/
    └── index.html      ← Complete frontend (HTML + CSS + JS)
```

## 🔌 APIs Used (all FREE, no key required)

| API | Purpose |
|-----|---------|
| [Open-Meteo](https://open-meteo.com/) | Weather forecast (current, hourly, 7-day) |
| [Nominatim / OSM](https://nominatim.openstreetmap.org/) | Reverse & forward geocoding |
| Browser Geolocation API | Device location |

## 🎨 Design System

- **Typography**: Cormorant Garamond (location) · Barlow Condensed (temperature) · Outfit (UI)
- **Glass**: `backdrop-filter: blur(22px) saturate(160%)` + `rgba(255,255,255,0.12)` background
- **Sky themes**: 8 dynamic gradients — clear day, clear night, cloudy, rain, snow, storm, fog, overcast
- **Canvas animations**: Rain streaks · Snowflakes · Twinkling stars · Cloud wisps · Lightning

## 🌤️ Weather Condition Backgrounds

| Condition | Sky Gradient | Canvas Effect |
|-----------|-------------|---------------|
| Clear day | Orange→Blue | Drifting cloud wisps |
| Clear night | Deep navy | Twinkling stars |
| Cloudy | Steel blue-grey | Cloud wisps |
| Rain | Dark navy | 220 rain streaks |
| Snow | Ice blue-white | 160 snowflakes |
| Storm | Deep purple | Rain + lightning flashes |
| Fog | Misty grey | 8 fog wisps |

## 📦 Production Deployment

```bash
pip install gunicorn
gunicorn app:app -w 4 -b 0.0.0.0:8000
```

For HTTPS (required for Geolocation API on production):
```bash
# Use a reverse proxy like nginx + certbot
# or deploy to Render / Railway / Fly.io
```

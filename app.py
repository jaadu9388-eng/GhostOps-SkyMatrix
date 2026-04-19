"""
SkyCast Weather App — Flask Backend
APIs used:
  - Open-Meteo (weather) — free, no key needed
  - Nominatim / OpenStreetMap (geocoding) — free, no key needed
"""

from flask import Flask, render_template, jsonify, request
import requests
import time

app = Flask(__name__)

# ── Simple in-memory cache ────────────────────────────────────────────────────
_CACHE: dict = {}

def _cached_get(url: str, params: dict, headers: dict | None = None, ttl: int = 600):
    key = url + str(sorted(params.items()))
    now = time.time()
    if key in _CACHE:
        data, ts = _CACHE[key]
        if now - ts < ttl:
            return data
    resp = requests.get(url, params=params, headers=headers, timeout=12)
    resp.raise_for_status()
    data = resp.json()
    _CACHE[key] = (data, now)
    return data

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/weather")
def weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    units = request.args.get("units", "metric")          # metric | imperial

    if not lat or not lon:
        return jsonify({"error": "lat/lon required"}), 400

    wind_unit   = "mph"        if units == "imperial" else "kmh"
    temp_unit   = "fahrenheit" if units == "imperial" else "celsius"

    params = {
        "latitude":  lat,
        "longitude": lon,
        "current": ",".join([
            "temperature_2m", "relative_humidity_2m", "apparent_temperature",
            "precipitation", "weather_code", "wind_speed_10m",
            "wind_direction_10m", "uv_index", "is_day", "visibility",
            "surface_pressure", "cloud_cover",
        ]),
        "hourly": "temperature_2m,precipitation_probability,weather_code,wind_speed_10m",
        "daily": ",".join([
            "weather_code", "temperature_2m_max", "temperature_2m_min",
            "sunrise", "sunset", "uv_index_max", "precipitation_sum",
            "wind_speed_10m_max",
        ]),
        "timezone":           "auto",
        "forecast_days":      7,
        "wind_speed_unit":    wind_unit,
        "temperature_unit":   temp_unit,
    }

    try:
        data = _cached_get("https://api.open-meteo.com/v1/forecast", params)
        return jsonify(data)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 502


@app.route("/api/geocode")
def geocode():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "lat/lon required"}), 400

    params = {"lat": lat, "lon": lon, "format": "json", "accept-language": "en"}
    headers = {"User-Agent": "SkyCast/1.0 (open-source weather app)"}

    try:
        data = _cached_get(
            "https://nominatim.openstreetmap.org/reverse",
            params, headers=headers, ttl=86_400,
        )
        return jsonify(data)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 502


@app.route("/api/search")
def search():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])

    params = {"q": q, "format": "json", "limit": 6, "accept-language": "en"}
    headers = {"User-Agent": "SkyCast/1.0 (open-source weather app)"}

    try:
        data = _cached_get(
            "https://nominatim.openstreetmap.org/search",
            params, headers=headers, ttl=3_600,
        )
        return jsonify(data)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 502


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")

"""Leaflet embebido: descarga (y cachea) el CSS y el JS de Leaflet para
meterlos dentro del HTML generado. Así el mapa publicado no depende del
CDN de unpkg, que algunos navegadores/redes corporativas bloquean."""

from __future__ import annotations

import urllib.request
from pathlib import Path

VERSION = "1.9.4"
SRI = {
    "css": "sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=",
    "js": "sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=",
}
URLS = {
    "css": f"https://unpkg.com/leaflet@{VERSION}/dist/leaflet.css",
    "js": f"https://unpkg.com/leaflet@{VERSION}/dist/leaflet.js",
}
CACHE = Path(__file__).resolve().parent / "_leaflet"


def _cached(kind: str) -> str:
    """Devuelve el código de Leaflet (css/js), cacheado en scripts/_leaflet/."""
    CACHE.mkdir(exist_ok=True)
    target = CACHE / ("leaflet.css" if kind == "css" else "leaflet.js")
    if not target.exists():
        req = urllib.request.Request(
            URLS[kind], headers={"User-Agent": "mapa-mty-build/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            target.write_bytes(resp.read())
    return target.read_text(encoding="utf-8")


def embed() -> tuple[str, str]:
    return _cached("css"), _cached("js")

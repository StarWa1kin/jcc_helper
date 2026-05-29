import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from fastapi import HTTPException

from app.config import CACHE_TTL_SECONDS, HEX_CACHE_FILE, HEX_SOURCE_URL


class HexDataSourceError(RuntimeError):
    pass


@dataclass
class HexCache:
    meta: dict[str, str]
    hexes: list[dict[str, Any]]
    by_id: dict[str, dict[str, Any]]
    fetched_at: float


hex_cache: HexCache | None = None


def query_hex_items(
    keyword: str | None = None,
    level: str | None = None,
    is_legend: int | None = None,
    hero_enhancement_type: str | None = None,
    fetter_id: str | None = None,
    fetter_type: str | None = None,
) -> dict[str, Any]:
    cache = get_hex_cache()
    keyword_value = keyword.strip().lower() if keyword else None
    legend_value = str(is_legend) if is_legend is not None else None

    items = []
    for hex_item in cache.hexes:
        if keyword_value and not matches_keyword(hex_item, keyword_value):
            continue
        if level and str(hex_item.get("level", "")) != level:
            continue
        if legend_value is not None and str(hex_item.get("is_legend", "")) != legend_value:
            continue
        if hero_enhancement_type and str(hex_item.get("hero_enhancement_type", "")) != hero_enhancement_type:
            continue
        if fetter_id and str(hex_item.get("fetterId", "")) != fetter_id:
            continue
        if fetter_type and str(hex_item.get("fetterType", "")) != fetter_type:
            continue
        items.append(hex_item)

    return {
        "meta": cache.meta,
        "cache": {
            "ttlSeconds": CACHE_TTL_SECONDS,
            "fetchedAt": int(cache.fetched_at),
        },
        "total": len(items),
        "items": items,
    }


def get_hex_detail(hex_id: str) -> dict[str, Any]:
    cache = get_hex_cache()
    hex_item = cache.by_id.get(hex_id)
    if hex_item is None:
        raise HTTPException(status_code=404, detail="Hex not found")

    return {"hex": hex_item}


def get_hex_cache() -> HexCache:
    global hex_cache

    now = time.time()
    if hex_cache and now - hex_cache.fetched_at < CACHE_TTL_SECONDS:
        return hex_cache

    file_cache = load_hex_cache_file(now)
    if file_cache:
        hex_cache = file_cache
        return hex_cache

    try:
        hex_cache = fetch_hex_cache(now)
    except HexDataSourceError as exc:
        stale_cache = load_hex_cache_file(now, ignore_ttl=True)
        if stale_cache:
            hex_cache = stale_cache
            return hex_cache
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return hex_cache


def load_hex_cache_file(now: float, ignore_ttl: bool = False) -> HexCache | None:
    if not HEX_CACHE_FILE.exists():
        return None

    try:
        cache_data = json.loads(HEX_CACHE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    fetched_at = float(cache_data.get("fetchedAt", 0))
    if not ignore_ttl and now - fetched_at >= CACHE_TTL_SECONDS:
        return None

    meta = cache_data.get("meta")
    hexes = cache_data.get("hexes")
    if not isinstance(meta, dict) or not isinstance(hexes, list):
        return None

    normalized_hexes = [hex_item for hex_item in hexes if isinstance(hex_item, dict)]
    return HexCache(
        meta={str(key): str(value) for key, value in meta.items()},
        hexes=normalized_hexes,
        by_id={str(hex_item.get("id")): hex_item for hex_item in normalized_hexes},
        fetched_at=fetched_at,
    )


def save_hex_cache_file(cache: HexCache) -> None:
    HEX_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    cache_data = {
        "fetchedAt": cache.fetched_at,
        "meta": cache.meta,
        "hexes": cache.hexes,
    }
    HEX_CACHE_FILE.write_text(
        json.dumps(cache_data, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )


def fetch_hex_cache(fetched_at: float) -> HexCache:
    request = urllib.request.Request(
        HEX_SOURCE_URL,
        headers={"User-Agent": "Mozilla/5.0"},
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            content = response.read()
    except (TimeoutError, urllib.error.URLError) as exc:
        raise HexDataSourceError("Failed to fetch hex data source") from exc

    try:
        source = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HexDataSourceError("Failed to parse hex data source") from exc

    raw_hexes = source.get("data")
    if not isinstance(raw_hexes, dict):
        raise HexDataSourceError("Invalid hex data source format")

    hexes = [hex_item for hex_item in raw_hexes.values() if isinstance(hex_item, dict)]
    hexes.sort(key=lambda hex_item: (safe_int(hex_item.get("level")), safe_int(hex_item.get("id"))))

    cache = HexCache(
        meta={
            "version": str(source.get("version", "")),
            "season": str(source.get("season", "")),
            "setId": str(source.get("setId", "")),
            "time": str(source.get("time", "")),
            "sourceUrl": HEX_SOURCE_URL,
        },
        hexes=hexes,
        by_id={str(hex_item.get("id")): hex_item for hex_item in hexes},
        fetched_at=fetched_at,
    )
    save_hex_cache_file(cache)
    return cache


def matches_keyword(hex_item: dict[str, Any], keyword: str) -> bool:
    fields = (
        hex_item.get("id"),
        hex_item.get("name"),
        hex_item.get("desc"),
        hex_item.get("fetterId"),
        hex_item.get("fetterType"),
    )
    return any(keyword in str(field).lower() for field in fields if field)


def safe_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from fastapi import HTTPException

from app.config import CACHE_TTL_SECONDS, EQUIP_CACHE_FILE, EQUIP_SOURCE_URL


class EquipDataSourceError(RuntimeError):
    pass


@dataclass
class EquipCache:
    meta: dict[str, str]
    equips: list[dict[str, Any]]
    by_id: dict[str, dict[str, Any]]
    fetched_at: float


equip_cache: EquipCache | None = None


def query_equip_items(
    keyword: str | None = None,
    equip_type: str | None = None,
    material_id: str | None = None,
    fetter_id: str | None = None,
    effect_type: str | None = None,
    composable: bool | None = None,
) -> dict[str, Any]:
    cache = get_equip_cache()
    keyword_value = keyword.strip().lower() if keyword else None
    equip_type_value = equip_type.strip().lower() if equip_type else None

    items = []
    for equip in cache.equips:
        if keyword_value and not matches_keyword(equip, keyword_value):
            continue
        if equip_type_value and equip_type_value not in str(equip.get("type", "")).lower():
            continue
        if material_id and material_id not in {str(equip.get("synthesis1", "")), str(equip.get("synthesis2", ""))}:
            continue
        if fetter_id and str(equip.get("fetterID", "")) != fetter_id:
            continue
        if effect_type and str(equip.get("EffectType", "")) != effect_type:
            continue
        if composable is not None and is_composable(equip) != composable:
            continue
        items.append(equip)

    return {
        "meta": cache.meta,
        "cache": {
            "ttlSeconds": CACHE_TTL_SECONDS,
            "fetchedAt": int(cache.fetched_at),
        },
        "total": len(items),
        "items": items,
    }


def get_equip_detail(equip_id: str) -> dict[str, Any]:
    cache = get_equip_cache()
    equip = cache.by_id.get(equip_id)
    if equip is None:
        raise HTTPException(status_code=404, detail="Equip not found")

    return {"equip": equip}


def get_equip_cache() -> EquipCache:
    global equip_cache

    now = time.time()
    if equip_cache and now - equip_cache.fetched_at < CACHE_TTL_SECONDS:
        return equip_cache

    file_cache = load_equip_cache_file(now)
    if file_cache:
        equip_cache = file_cache
        return equip_cache

    try:
        equip_cache = fetch_equip_cache(now)
    except EquipDataSourceError as exc:
        stale_cache = load_equip_cache_file(now, ignore_ttl=True)
        if stale_cache:
            equip_cache = stale_cache
            return equip_cache
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return equip_cache


def load_equip_cache_file(now: float, ignore_ttl: bool = False) -> EquipCache | None:
    if not EQUIP_CACHE_FILE.exists():
        return None

    try:
        cache_data = json.loads(EQUIP_CACHE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    fetched_at = float(cache_data.get("fetchedAt", 0))
    if not ignore_ttl and now - fetched_at >= CACHE_TTL_SECONDS:
        return None

    meta = cache_data.get("meta")
    equips = cache_data.get("equips")
    if not isinstance(meta, dict) or not isinstance(equips, list):
        return None

    normalized_equips = [equip for equip in equips if isinstance(equip, dict)]
    return EquipCache(
        meta={str(key): str(value) for key, value in meta.items()},
        equips=normalized_equips,
        by_id={str(equip.get("id")): equip for equip in normalized_equips},
        fetched_at=fetched_at,
    )


def save_equip_cache_file(cache: EquipCache) -> None:
    EQUIP_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    cache_data = {
        "fetchedAt": cache.fetched_at,
        "meta": cache.meta,
        "equips": cache.equips,
    }
    EQUIP_CACHE_FILE.write_text(
        json.dumps(cache_data, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )


def fetch_equip_cache(fetched_at: float) -> EquipCache:
    request = urllib.request.Request(
        EQUIP_SOURCE_URL,
        headers={"User-Agent": "Mozilla/5.0"},
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            content = response.read()
    except (TimeoutError, urllib.error.URLError) as exc:
        raise EquipDataSourceError("Failed to fetch equip data source") from exc

    try:
        source = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EquipDataSourceError("Failed to parse equip data source") from exc

    raw_equips = source.get("data")
    if not isinstance(raw_equips, dict):
        raise EquipDataSourceError("Invalid equip data source format")

    equips = [equip for equip in raw_equips.values() if isinstance(equip, dict)]
    equips.sort(key=lambda equip: (safe_int(equip.get("sort")), safe_int(equip.get("id"))))

    cache = EquipCache(
        meta={
            "version": str(source.get("version", "")),
            "season": str(source.get("season", "")),
            "setId": str(source.get("setId", "")),
            "time": str(source.get("time", "")),
            "sourceUrl": EQUIP_SOURCE_URL,
        },
        equips=equips,
        by_id={str(equip.get("id")): equip for equip in equips},
        fetched_at=fetched_at,
    )
    save_equip_cache_file(cache)
    return cache


def matches_keyword(equip: dict[str, Any], keyword: str) -> bool:
    fields = (
        equip.get("id"),
        equip.get("name"),
        equip.get("type"),
        equip.get("basicDesc"),
        equip.get("desc"),
        equip.get("fetterID"),
        equip.get("tftEquipId"),
    )
    return any(keyword in str(field).lower() for field in fields if field)


def is_composable(equip: dict[str, Any]) -> bool:
    return str(equip.get("synthesis1", "0")) != "0" and str(equip.get("synthesis2", "0")) != "0"


def safe_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


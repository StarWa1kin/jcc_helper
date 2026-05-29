import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from fastapi import HTTPException

from app.config import CACHE_TTL_SECONDS, GOD_CACHE_FILE, GOD_SOURCE_URL


class GodDataSourceError(RuntimeError):
    pass


@dataclass
class GodCache:
    meta: dict[str, str]
    gods: list[dict[str, Any]]
    by_id: dict[str, dict[str, Any]]
    fetched_at: float


god_cache: GodCache | None = None


def query_god_items(
    keyword: str | None = None,
    god_name: str | None = None,
    wish_name: str | None = None,
    stage: int | None = None,
) -> dict[str, Any]:
    cache = get_god_cache()
    keyword_value = keyword.strip().lower() if keyword else None
    god_name_value = god_name.strip().lower() if god_name else None
    wish_name_value = wish_name.strip().lower() if wish_name else None
    stage_value = str(stage) if stage is not None else None

    items = []
    for god in cache.gods:
        if keyword_value and not matches_keyword(god, keyword_value):
            continue
        if god_name_value and god_name_value not in str(god.get("godName", "")).lower():
            continue
        if wish_name_value and not has_wish_name(god, wish_name_value):
            continue
        if stage_value and not has_stage(god, stage_value):
            continue
        items.append(god)

    return {
        "meta": cache.meta,
        "cache": {
            "ttlSeconds": CACHE_TTL_SECONDS,
            "fetchedAt": int(cache.fetched_at),
        },
        "total": len(items),
        "items": items,
    }


def get_god_detail(god_id: str) -> dict[str, Any]:
    cache = get_god_cache()
    god = cache.by_id.get(god_id)
    if god is None:
        raise HTTPException(status_code=404, detail="God not found")

    return {"god": god}


def get_god_cache() -> GodCache:
    global god_cache

    now = time.time()
    if god_cache and now - god_cache.fetched_at < CACHE_TTL_SECONDS:
        return god_cache

    file_cache = load_god_cache_file(now)
    if file_cache:
        god_cache = file_cache
        return god_cache

    try:
        god_cache = fetch_god_cache(now)
    except GodDataSourceError as exc:
        stale_cache = load_god_cache_file(now, ignore_ttl=True)
        if stale_cache:
            god_cache = stale_cache
            return god_cache
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return god_cache


def load_god_cache_file(now: float, ignore_ttl: bool = False) -> GodCache | None:
    if not GOD_CACHE_FILE.exists():
        return None

    try:
        cache_data = json.loads(GOD_CACHE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    fetched_at = float(cache_data.get("fetchedAt", 0))
    if not ignore_ttl and now - fetched_at >= CACHE_TTL_SECONDS:
        return None

    meta = cache_data.get("meta")
    gods = cache_data.get("gods")
    if not isinstance(meta, dict) or not isinstance(gods, list):
        return None

    normalized_gods = [god for god in gods if isinstance(god, dict)]
    return GodCache(
        meta={str(key): str(value) for key, value in meta.items()},
        gods=normalized_gods,
        by_id={str(god.get("godId")): god for god in normalized_gods},
        fetched_at=fetched_at,
    )


def save_god_cache_file(cache: GodCache) -> None:
    GOD_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    cache_data = {
        "fetchedAt": cache.fetched_at,
        "meta": cache.meta,
        "gods": cache.gods,
    }
    GOD_CACHE_FILE.write_text(
        json.dumps(cache_data, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )


def fetch_god_cache(fetched_at: float) -> GodCache:
    request = urllib.request.Request(
        GOD_SOURCE_URL,
        headers={"User-Agent": "Mozilla/5.0"},
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            content = response.read()
    except (TimeoutError, urllib.error.URLError) as exc:
        raise GodDataSourceError("Failed to fetch god data source") from exc

    try:
        source = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GodDataSourceError("Failed to parse god data source") from exc

    raw_gods = source.get("data")
    if not isinstance(raw_gods, list):
        raise GodDataSourceError("Invalid god data source format")

    gods = [god for god in raw_gods if isinstance(god, dict)]
    gods.sort(key=lambda god: safe_int(god.get("godId")))

    cache = GodCache(
        meta={
            "version": str(source.get("version", "")),
            "season": str(source.get("season", "")),
            "setId": str(source.get("setId", "")),
            "time": str(source.get("time", "")),
            "sourceUrl": GOD_SOURCE_URL,
        },
        gods=gods,
        by_id={str(god.get("godId")): god for god in gods},
        fetched_at=fetched_at,
    )
    save_god_cache_file(cache)
    return cache


def matches_keyword(god: dict[str, Any], keyword: str) -> bool:
    fields = (
        god.get("godId"),
        god.get("godName"),
        god.get("godTips"),
    )
    if any(keyword in str(field).lower() for field in fields if field):
        return True

    for wish in iter_wishes(god):
        wish_fields = (
            wish.get("id"),
            wish.get("name"),
            wish.get("desc"),
            wish.get("type"),
        )
        if any(keyword in str(field).lower() for field in wish_fields if field):
            return True

    return False


def has_wish_name(god: dict[str, Any], wish_name: str) -> bool:
    return any(wish_name in str(wish.get("name", "")).lower() for wish in iter_wishes(god))


def has_stage(god: dict[str, Any], stage: str) -> bool:
    stages = god.get("stages")
    if not isinstance(stages, list):
        return False
    return any(str(item.get("num", "")) == stage for item in stages if isinstance(item, dict))


def iter_wishes(god: dict[str, Any]) -> list[dict[str, Any]]:
    stages = god.get("stages")
    if not isinstance(stages, list):
        return []

    wishes = []
    for stage in stages:
        if not isinstance(stage, dict):
            continue
        stage_wishes = stage.get("wishes")
        if isinstance(stage_wishes, list):
            wishes.extend(wish for wish in stage_wishes if isinstance(wish, dict))
    return wishes


def safe_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


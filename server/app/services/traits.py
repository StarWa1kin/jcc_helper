import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from fastapi import HTTPException

from app.config import CACHE_TTL_SECONDS, TRAIT_CACHE_FILE, TRAIT_SOURCE_URL


class TraitDataSourceError(RuntimeError):
    pass


@dataclass
class TraitCache:
    meta: dict[str, str]
    traits: list[dict[str, Any]]
    by_id: dict[str, dict[str, Any]]
    fetched_at: float


trait_cache: TraitCache | None = None


def query_trait_items(
    keyword: str | None = None,
    name: str | None = None,
    check_id: str | None = None,
    trait_type: int | None = None,
) -> dict[str, Any]:
    cache = get_trait_cache()
    keyword_value = keyword.strip().lower() if keyword else None
    name_value = name.strip().lower() if name else None
    type_value = str(trait_type) if trait_type is not None else None

    items = []
    for trait in cache.traits:
        if keyword_value and not matches_keyword(trait, keyword_value):
            continue
        if name_value and name_value not in str(trait.get("name", "")).lower():
            continue
        if check_id and str(trait.get("checkId", "")) != check_id:
            continue
        if type_value is not None and str(trait.get("type", "")) != type_value:
            continue
        items.append(trait)

    return {
        "meta": cache.meta,
        "cache": {
            "ttlSeconds": CACHE_TTL_SECONDS,
            "fetchedAt": int(cache.fetched_at),
        },
        "total": len(items),
        "items": items,
    }


def get_trait_detail(trait_id: str) -> dict[str, Any]:
    cache = get_trait_cache()
    trait = cache.by_id.get(trait_id)
    if trait is None:
        raise HTTPException(status_code=404, detail="Trait not found")

    return {"trait": trait}


def get_trait_cache() -> TraitCache:
    global trait_cache

    now = time.time()
    if trait_cache and now - trait_cache.fetched_at < CACHE_TTL_SECONDS:
        return trait_cache

    file_cache = load_trait_cache_file(now)
    if file_cache:
        trait_cache = file_cache
        return trait_cache

    try:
        trait_cache = fetch_trait_cache(now)
    except TraitDataSourceError as exc:
        stale_cache = load_trait_cache_file(now, ignore_ttl=True)
        if stale_cache:
            trait_cache = stale_cache
            return trait_cache
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return trait_cache


def load_trait_cache_file(now: float, ignore_ttl: bool = False) -> TraitCache | None:
    if not TRAIT_CACHE_FILE.exists():
        return None

    try:
        cache_data = json.loads(TRAIT_CACHE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    fetched_at = float(cache_data.get("fetchedAt", 0))
    if not ignore_ttl and now - fetched_at >= CACHE_TTL_SECONDS:
        return None

    meta = cache_data.get("meta")
    traits = cache_data.get("traits")
    if not isinstance(meta, dict) or not isinstance(traits, list):
        return None

    normalized_traits = [trait for trait in traits if isinstance(trait, dict)]
    return TraitCache(
        meta={str(key): str(value) for key, value in meta.items()},
        traits=normalized_traits,
        by_id={str(trait.get("id")): trait for trait in normalized_traits},
        fetched_at=fetched_at,
    )


def save_trait_cache_file(cache: TraitCache) -> None:
    TRAIT_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    cache_data = {
        "fetchedAt": cache.fetched_at,
        "meta": cache.meta,
        "traits": cache.traits,
    }
    TRAIT_CACHE_FILE.write_text(
        json.dumps(cache_data, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )


def fetch_trait_cache(fetched_at: float) -> TraitCache:
    request = urllib.request.Request(
        TRAIT_SOURCE_URL,
        headers={"User-Agent": "Mozilla/5.0"},
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            content = response.read()
    except (TimeoutError, urllib.error.URLError) as exc:
        raise TraitDataSourceError("Failed to fetch trait data source") from exc

    try:
        source = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TraitDataSourceError("Failed to parse trait data source") from exc

    raw_traits = source.get("data")
    if not isinstance(raw_traits, dict):
        raise TraitDataSourceError("Invalid trait data source format")

    traits = [trait for trait in raw_traits.values() if isinstance(trait, dict)]
    traits.sort(key=lambda trait: (safe_int(trait.get("checkId")), safe_int(trait.get("level")), safe_int(trait.get("id"))))

    cache = TraitCache(
        meta={
            "version": str(source.get("version", "")),
            "season": str(source.get("season", "")),
            "setId": str(source.get("setId", "")),
            "time": str(source.get("time", "")),
            "sourceUrl": TRAIT_SOURCE_URL,
        },
        traits=traits,
        by_id={str(trait.get("id")): trait for trait in traits},
        fetched_at=fetched_at,
    )
    save_trait_cache_file(cache)
    return cache


def matches_keyword(trait: dict[str, Any], keyword: str) -> bool:
    fields = (
        trait.get("id"),
        trait.get("checkId"),
        trait.get("name"),
        trait.get("prefix"),
        trait.get("desc"),
        trait.get("desc2"),
        trait.get("realDesc"),
    )
    return any(keyword in str(field).lower() for field in fields if field)


def safe_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


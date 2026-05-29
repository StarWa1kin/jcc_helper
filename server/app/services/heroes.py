import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from fastapi import HTTPException

from app.config import CACHE_TTL_SECONDS, CHESS_SOURCE_URL, HERO_CACHE_FILE


class HeroDataSourceError(RuntimeError):
    pass


@dataclass
class HeroCache:
    meta: dict[str, str]
    heroes: list[dict[str, Any]]
    by_id: dict[str, dict[str, Any]]
    fetched_at: float


hero_cache: HeroCache | None = None


def query_hero_items(
    keyword: str | None = None,
    price: int | None = None,
    species: str | None = None,
    hero_class: str | None = None,
    show_only: bool = True,
) -> dict[str, Any]:
    cache = get_hero_cache()
    keyword_value = keyword.strip().lower() if keyword else None
    price_value = str(price) if price is not None else None

    items = []
    for hero in cache.heroes:
        if show_only and hero.get("showHeroTag") != "1":
            continue
        if keyword_value and not matches_keyword(hero, keyword_value):
            continue
        if price_value is not None and hero.get("price") != price_value:
            continue
        if species and not contains_token(str(hero.get("species", "")), species):
            continue
        if hero_class and not contains_token(str(hero.get("class", "")), hero_class):
            continue
        items.append(hero)

    return {
        "meta": cache.meta,
        "cache": {
            "ttlSeconds": CACHE_TTL_SECONDS,
            "fetchedAt": int(cache.fetched_at),
        },
        "total": len(items),
        "items": items,
    }


def get_hero_detail(hero_id: str) -> dict[str, Any]:
    cache = get_hero_cache()
    hero = cache.by_id.get(hero_id)
    if hero is None:
        raise HTTPException(status_code=404, detail="Hero not found")

    return {"hero": hero}


def get_hero_cache() -> HeroCache:
    global hero_cache

    now = time.time()
    if hero_cache and now - hero_cache.fetched_at < CACHE_TTL_SECONDS:
        return hero_cache

    file_cache = load_hero_cache_file(now)
    if file_cache:
        hero_cache = file_cache
        return hero_cache

    try:
        hero_cache = fetch_hero_cache(now)
    except HeroDataSourceError as exc:
        stale_cache = load_hero_cache_file(now, ignore_ttl=True)
        if stale_cache:
            hero_cache = stale_cache
            return hero_cache
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return hero_cache


def load_hero_cache_file(now: float, ignore_ttl: bool = False) -> HeroCache | None:
    if not HERO_CACHE_FILE.exists():
        return None

    try:
        cache_data = json.loads(HERO_CACHE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    fetched_at = float(cache_data.get("fetchedAt", 0))
    if not ignore_ttl and now - fetched_at >= CACHE_TTL_SECONDS:
        return None

    meta = cache_data.get("meta")
    heroes = cache_data.get("heroes")
    if not isinstance(meta, dict) or not isinstance(heroes, list):
        return None

    normalized_heroes = [hero for hero in heroes if isinstance(hero, dict)]
    return HeroCache(
        meta={str(key): str(value) for key, value in meta.items()},
        heroes=normalized_heroes,
        by_id={str(hero.get("id")): hero for hero in normalized_heroes},
        fetched_at=fetched_at,
    )


def save_hero_cache_file(cache: HeroCache) -> None:
    HERO_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    cache_data = {
        "fetchedAt": cache.fetched_at,
        "meta": cache.meta,
        "heroes": cache.heroes,
    }
    HERO_CACHE_FILE.write_text(
        json.dumps(cache_data, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )


def fetch_hero_cache(fetched_at: float) -> HeroCache:
    request = urllib.request.Request(
        CHESS_SOURCE_URL,
        headers={"User-Agent": "Mozilla/5.0"},
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            content = response.read()
    except (TimeoutError, urllib.error.URLError) as exc:
        raise HeroDataSourceError("Failed to fetch hero data source") from exc

    try:
        source = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HeroDataSourceError("Failed to parse hero data source") from exc

    raw_heroes = source.get("data")
    if not isinstance(raw_heroes, dict):
        raise HeroDataSourceError("Invalid hero data source format")

    heroes = [hero for hero in raw_heroes.values() if isinstance(hero, dict)]
    heroes.sort(key=lambda hero: (safe_int(hero.get("price")), safe_int(hero.get("id"))))

    cache = HeroCache(
        meta={
            "version": str(source.get("version", "")),
            "season": str(source.get("season", "")),
            "setId": str(source.get("setId", "")),
            "time": str(source.get("time", "")),
            "sourceUrl": CHESS_SOURCE_URL,
        },
        heroes=heroes,
        by_id={str(hero.get("id")): hero for hero in heroes},
        fetched_at=fetched_at,
    )
    save_hero_cache_file(cache)
    return cache


def matches_keyword(hero: dict[str, Any], keyword: str) -> bool:
    fields = (
        hero.get("id"),
        hero.get("name"),
        hero.get("heroPaint"),
        hero.get("skillName"),
        hero.get("tftHeroId"),
    )
    return any(keyword in str(field).lower() for field in fields if field)


def contains_token(source_value: str, target_value: str) -> bool:
    return target_value in {token.strip() for token in source_value.split("|")}


def safe_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


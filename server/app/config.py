from pathlib import Path

CHESS_SOURCE_URL = "https://game.gtimg.cn/images/lol/act/jkzlk/js//17/17.17.3-S18/chess.js"
TRAIT_SOURCE_URL = "https://game.gtimg.cn/images/lol/act/jkzlk/js//17/17.17.3-S18/trait.js"
HEX_SOURCE_URL = "https://game.gtimg.cn/images/lol/act/jkzlk/js//17/17.17.3-S18/hex.js"
GOD_SOURCE_URL = "https://game.gtimg.cn/images/lol/act/jkzlk/js//17/17.17.3-S18/god.js"
EQUIP_SOURCE_URL = "https://game.gtimg.cn/images/lol/act/jkzlk/js//17/17.17.3-S18/equip.js"
CACHE_TTL_SECONDS = 12 * 60 * 60
CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"
HERO_CACHE_FILE = CACHE_DIR / "heroes_chess.json"
TRAIT_CACHE_FILE = CACHE_DIR / "traits.json"
HEX_CACHE_FILE = CACHE_DIR / "hexes.json"
GOD_CACHE_FILE = CACHE_DIR / "gods.json"
EQUIP_CACHE_FILE = CACHE_DIR / "equips.json"

import os


def should_use_cache() -> bool:
    cache_env = os.getenv("USE_ZYK_CACHE", "true").lower()
    return cache_env not in ("false", "0", "no")

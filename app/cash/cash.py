from cachetools import TTLCache

# Создаем кеш с временем жизни 10 минут
referral_code_cache = TTLCache(maxsize=100, ttl=600)


# возвращает реферальный код пользователя
def get_cached_referral_code(user_id: int):
    return referral_code_cache.get(user_id)


# возвращает реферальный код пользователя
def set_cached_referral_code(user_id: int, referral_code: str):
    referral_code_cache[user_id] = referral_code

import os


def _env_bool(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes")


def _env_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    if value is None or not value.strip():
        return default
    try:
        return int(value.strip())
    except ValueError:
        return default


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or 'postgresql://jila:jila@localhost:5432/vpdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AI_API_KEY = os.environ.get("AI_API_KEY") or "6Iils6e74C870MqTM8vcRySO7MWVkNBZ"
    AI_API_URL = os.environ.get("AI_API_URL") or "https://api.deepinfra.com/v1/openai"
    AI_API_MODEL = os.environ.get("AI_API_MODEL") or "openai/gpt-oss-120b"
    EMAIL_HOST = os.environ.get("EMAIL_HOST") or "smtp.migadu.com"
    EMAIL_PORT = _env_int("EMAIL_PORT", 587)
    EMAIL_USERNAME = os.environ.get("EMAIL_USERNAME") or "noreply@windshields.pro"
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD") or "Wspr0n0reply"
    EMAIL_USE_TLS = _env_bool("EMAIL_USE_TLS", True)
    EMAIL_USE_SSL = _env_bool("EMAIL_USE_SSL", False)
    EMAIL_DEFAULT_FROM = os.environ.get("EMAIL_DEFAULT_FROM") or "noreply@windshields.pro"
    EMAIL_TIMEOUT = _env_int("EMAIL_TIMEOUT", 100)
    PASSWORD_RESET_SALT = os.environ.get("PASSWORD_RESET_SALT") or "password-reset"
    PASSWORD_RESET_TOKEN_MAX_AGE = _env_int("PASSWORD_RESET_TOKEN_MAX_AGE", 3600)

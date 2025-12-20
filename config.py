import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or 'postgresql://jila:jila@localhost:5432/vpdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AI_API_KEY = os.environ.get("AI_API_KEY") or "6Iils6e74C870MqTM8vcRySO7MWVkNBZ"
    AI_API_URL = os.environ.get("AI_API_URL") or "https://api.deepinfra.com/v1/openai"
    AI_API_MODEL = os.environ.get("AI_API_MODEL") or "openai/gpt-oss-120b"

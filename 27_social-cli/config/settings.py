import os
from typing import Dict, Any

class Settings:
    """Configuración de la aplicación"""

    # Límites de caracteres por plataforma
    CHARACTER_LIMITS = {
        'facebook': 63206,
        'twitter': 280,
        'instagram': 2200
    }

    # Configuración por defecto
    DEFAULTS = {
        'facebook_page_id': os.getenv('FACEBOOK_PAGE_ID'),
        'twitter_api_key': os.getenv('TWITTER_API_KEY'),
        'max_retries': 3,
        'timeout': 30
    }

    @classmethod
    def get_character_limit(cls, platform):
        return cls.CHARACTER_LIMITS.get(platform, 5000)

# Configuración de APIs (en producción usar variables de entorno)
SOCIAL_CONFIG = {
    'facebook': {
        'access_token': os.getenv('FACEBOOK_ACCESS_TOKEN'),
        'page_id': os.getenv('FACEBOOK_PAGE_ID')
    },
    'twitter': {
        'api_key': os.getenv('TWITTER_API_KEY'),
        'api_secret': os.getenv('TWITTER_API_SECRET'),
        'access_token': os.getenv('TWITTER_ACCESS_TOKEN')
    }
}

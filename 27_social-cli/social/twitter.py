from typing import Dict, Any

from commands.base import SocialPlatform

class Twitter(SocialPlatform):
    """Cliente para Twitter/X"""

    def __init__(self, api_key=None, api_secret=None, access_token=None):
        super().__init__("twitter")
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token

    def post_text(self, content, **kwargs):
        """
        Publicar texto en Twitter/X

        Args:
            content: Texto a publicar
            **kwargs:
                - reply_to: ID del tweet al que responder
                - media_ids: IDs de medios adjuntos
        """
        print(f"🐦 Publicando en Twitter/X: {content}")

        # Validación
        self.validate_content(content)

        # Simulación de publicación
        result = {
            "platform": "twitter",
            "type": "tweet",
            "content": content,
            "success": True,
            "tweet_id": f"tw_{id(content)}",
            "character_count": len(content)
        }

        if kwargs.get('reply_to'):
            result['reply_to'] = kwargs['reply_to']
            print(f"↪️ Respondiendo a tweet: {kwargs['reply_to']}")

        return result

    def post_image(self, image_path, caption="", **kwargs):
        """Publicar imagen en Twitter/X"""
        print(f"🖼️ Publicando imagen en Twitter/X: {image_path}")

        # Twitter usa el caption como texto del tweet
        tweet_text = caption if caption else " "

        return {
            "platform": "twitter",
            "type": "tweet_with_media",
            "image_path": image_path,
            "content": tweet_text,
            "success": True,
            "tweet_id": f"tw_media_{id(image_path)}"
        }

    def validate_content(self, content, **kwargs):
        """Validar contenido para Twitter/X"""
        if len(content) > 280:
            raise ValueError(f"El tweet excede 280 caracteres. Actual: {len(content)}")

        # Validar caracteres prohibidos
        prohibited_chars = ['\x00', '\x01', '\x02']  # Caracteres de control
        for char in prohibited_chars:
            if char in content:
                raise ValueError(f"El contenido contiene caracteres no permitidos")

        return True

    def thread_post(self, messages):
        """Publicar un hilo en Twitter/X"""
        print(f"🧵 Publicando hilo en Twitter/X con {len(messages)} tweets")

        results = []
        for i, message in enumerate(messages):
            result = self.post_text(message)
            result['thread_position'] = i + 1
            results.append(result)

        return results

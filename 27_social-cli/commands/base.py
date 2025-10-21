from abc import ABC, abstractmethod

class SocialPlatform(ABC):
    """Clase base para todas las plataformas sociales"""

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def post_text(self, content, **kwargs):
        """Publicar texto en la plataforma"""
        pass

    @abstractmethod
    def post_image(self, image_path, caption="", **kwargs):
        """Publicar imagen en la plataforma"""
        pass

    @abstractmethod
    def validate_content(self, content, **kwargs):
        """Validar contenido antes de publicar"""
        pass

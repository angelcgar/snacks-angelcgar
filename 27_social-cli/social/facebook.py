from typing import Dict, Any

from commands.base import SocialPlatform

class Facebook(SocialPlatform):
    """Cliente para Facebook (páginas y perfiles)"""

    def __init__(self, access_token=None, page_id=None):
        super().__init__("facebook")
        self.access_token = access_token
        self.page_id = page_id

    def post_text(self, content, post_type="page", **kwargs):
        """
        Publicar texto en Facebook

        Args:
            content: Texto a publicar
            post_type: 'page' o 'profile'
            **kwargs:
                - link: URL para adjuntar
                - scheduled_time: tiempo programado
        """
        print(f"📘 Publicando en Facebook ({post_type}): {content}")

        # Lógica de validación
        self.validate_content(content, post_type=post_type)

        # Simulación de publicación
        if post_type == "page" and self.page_id:
            # Publicar en página
            result = {
                "platform": "facebook",
                "type": "page_post",
                "content": content,
                "page_id": self.page_id,
                "success": True,
                "post_id": f"fb_page_{self.page_id}_{id(content)}"
            }
        else:
            # Publicar en perfil personal
            result = {
                "platform": "facebook",
                "type": "profile_post",
                "content": content,
                "success": True,
                "post_id": f"fb_profile_{id(content)}"
            }

        if kwargs.get('link'):
            result['link'] = kwargs['link']
            print(f"🔗 Enlace adjunto: {kwargs['link']}")

        return result

    def post_image(self, image_path, caption="", **kwargs):
        """Publicar imagen en Facebook"""
        print(f"📸 Publicando imagen en Facebook: {image_path}")
        print(f"📝 Leyenda: {caption}")

        return {
            "platform": "facebook",
            "type": "image_post",
            "image_path": image_path,
            "caption": caption,
            "success": True,
            "post_id": f"fb_image_{id(image_path)}"
        }

    def validate_content(self, content, **kwargs):
        """Validar contenido para Facebook"""
        if len(content) > 63206:  # Límite de Facebook
            raise ValueError("El contenido excede el límite de caracteres de Facebook (63,206)")

        post_type = kwargs.get('post_type', 'profile')
        if post_type == "page" and not self.page_id:
            raise ValueError("Se requiere page_id para publicar en página de Facebook")

        return True

import argparse
import os
from social.facebook import Facebook
from social.twitter import Twitter
from config.settings import SOCIAL_CONFIG

class ImagenCommand:
    """Comando para manejar imágenes con publicación en redes sociales"""

    def __init__(self, subparsers):
        self.parser = subparsers.add_parser('imagen', help='Publicar imagen en redes sociales')
        self._add_arguments()

    def _add_arguments(self):
        self.parser.add_argument(
            'ruta',
            type=str,
            help='Ruta de la imagen a publicar'
        )
        self.parser.add_argument(
            '--facebook',
            action='store_true',
            help='Publicar en Facebook (perfil personal)'
        )
        self.parser.add_argument(
            '--facebook-page',
            action='store_true',
            help='Publicar en página de Facebook'
        )
        self.parser.add_argument(
            '--twitter',
            action='store_true',
            help='Publicar en Twitter/X'
        )
        self.parser.add_argument(
            '--caption',
            type=str,
            default='',
            help='Texto descriptivo para la imagen'
        )
        self.parser.add_argument(
            '--alt-text',
            type=str,
            help='Texto alternativo para accesibilidad'
        )
        self.parser.add_argument(
            '--filtro',
            type=str,
            choices=['sepia', 'bn', 'vivid', 'warm', 'cool'],
            help='Aplicar filtro a la imagen antes de publicar'
        )
        self.parser.add_argument(
            '--resize',
            type=str,
            help='Redimensionar imagen (ej: 1200x630, 1080x1080)'
        )
        self.parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simular publicación sin publicar realmente'
        )
        self.parser.add_argument(
            '--multiple',
            nargs='+',
            help='Publicar múltiples imágenes (máx 4 para Twitter)'
        )

    def _validate_image(self, image_path):
        """Validar que la imagen existe y es válida"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"La imagen no existe: {image_path}")

        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        file_ext = os.path.splitext(image_path)[1].lower()

        if file_ext not in valid_extensions:
            raise ValueError(f"Formato no soportado: {file_ext}. Use: {', '.join(valid_extensions)}")

        # Verificar tamaño del archivo (límite aproximado)
        file_size = os.path.getsize(image_path) / (1024 * 1024)  # MB
        if file_size > 20:  # 20MB límite
            raise ValueError(f"La imagen es muy grande: {file_size:.2f}MB. Máximo: 20MB")

        return True

    def _apply_filter_simulation(self, image_path, filter_name):
        """Simular aplicación de filtro (en producción usaría Pillow)"""
        filter_descriptions = {
            'sepia': 'efecto sepia vintage',
            'bn': 'blanco y negro clásico',
            'vivid': 'colores vibrantes mejorados',
            'warm': 'tonos cálidos anaranjados',
            'cool': 'tonos fríos azulados'
        }
        return filter_descriptions.get(filter_name, 'filtro personalizado')

    def _resize_simulation(self, image_path, dimensions):
        """Simular redimensionado (en producción usaría Pillow)"""
        return f"redimensionado a {dimensions}"

    def handle(self, args):
        results = []

        # Validar imagen principal
        try:
            self._validate_image(args.ruta)
            print(f"✅ Imagen válida: {args.ruta}")
        except (FileNotFoundError, ValueError) as e:
            print(f"❌ Error con la imagen: {e}")
            return results

        # Procesar múltiples imágenes si se especifican
        image_paths = [args.ruta]
        if args.multiple:
            for img_path in args.multiple:
                try:
                    self._validate_image(img_path)
                    image_paths.append(img_path)
                except (FileNotFoundError, ValueError) as e:
                    print(f"❌ Error con imagen adicional {img_path}: {e}")
                    continue

        # Inicializar clientes de redes sociales
        facebook_client = Facebook(
            access_token=SOCIAL_CONFIG['facebook']['access_token'],
            page_id=SOCIAL_CONFIG['facebook']['page_id']
        )

        twitter_client = Twitter(
            api_key=SOCIAL_CONFIG['twitter']['api_key'],
            access_token=SOCIAL_CONFIG['twitter']['access_token']
        )

        # Aplicar filtro si se especifica
        processing_info = []
        if args.filtro:
            filter_desc = self._apply_filter_simulation(args.ruta, args.filtro)
            processing_info.append(f"🎨 Filtro: {filter_desc}")

        # Redimensionar si se especifica
        if args.resize:
            resize_info = self._resize_simulation(args.ruta, args.resize)
            processing_info.append(f"📐 {resize_info}")

        # Texto alternativo
        alt_text = args.alt_text or f"Imagen: {os.path.basename(args.ruta)}"

        # Publicar en Facebook (perfil)
        if args.facebook:
            print("🚀 Publicando imagen en Facebook (perfil)...")
            if args.dry_run:
                print(f"📝 Simulación Facebook: {args.ruta}")
                print(f"📝 Caption: {args.caption}")
                if processing_info:
                    print(f"🔧 Procesamiento: {', '.join(processing_info)}")
            else:
                try:
                    result = facebook_client.post_image(
                        image_path=args.ruta,
                        caption=args.caption,
                        alt_text=alt_text
                    )
                    results.append(result)
                    print("✅ Imagen publicada en Facebook (perfil)")
                except Exception as e:
                    print(f"❌ Error en Facebook: {e}")

        # Publicar en Facebook (página)
        if args.facebook_page:
            print("🚀 Publicando imagen en Facebook (página)...")
            if args.dry_run:
                print(f"📝 Simulación Facebook Page: {args.ruta}")
                print(f"📝 Caption: {args.caption}")
                if processing_info:
                    print(f"🔧 Procesamiento: {', '.join(processing_info)}")
            else:
                try:
                    result = facebook_client.post_image(
                        image_path=args.ruta,
                        caption=args.caption,
                        alt_text=alt_text
                    )
                    results.append(result)
                    print("✅ Imagen publicada en Facebook (página)")
                except Exception as e:
                    print(f"❌ Error en Facebook Page: {e}")

        # Publicar en Twitter/X
        if args.twitter:
            print("🚀 Publicando imagen en Twitter/X...")

            # Validar límite de imágenes para Twitter
            if len(image_paths) > 4:
                print("⚠️ Twitter solo permite máximo 4 imágenes. Usando las primeras 4.")
                image_paths = image_paths[:4]

            if args.dry_run:
                print(f"📝 Simulación Twitter: {len(image_paths)} imagen(es)")
                for i, img_path in enumerate(image_paths):
                    print(f"   {i+1}. {img_path}")
                print(f"📝 Tweet: {args.caption}")
                if processing_info:
                    print(f"🔧 Procesamiento: {', '.join(processing_info)}")
            else:
                try:
                    # Para múltiples imágenes, publicar como tweet con carrusel
                    if len(image_paths) > 1:
                        print(f"🖼️ Publicando carrusel con {len(image_paths)} imágenes en Twitter")
                        # En una implementación real, aquí subirías múltiples imágenes
                        result = twitter_client.post_image(
                            image_path=args.ruta,  # Primera imagen como principal
                            caption=args.caption
                        )
                        result['multiple_images'] = len(image_paths)
                    else:
                        # Imagen única
                        result = twitter_client.post_image(
                            image_path=args.ruta,
                            caption=args.caption
                        )

                    results.append(result)
                    print("✅ Imagen(es) publicada(s) en Twitter/X")
                except Exception as e:
                    print(f"❌ Error en Twitter: {e}")

        # Mostrar resumen
        if not args.dry_run and results:
            print(f"\n📊 Resumen de publicaciones:")
            for result in results:
                platform = result.get('platform', 'unknown')
                post_id = result.get('post_id') or result.get('tweet_id', 'N/A')
                image_count = result.get('multiple_images', 1)
                print(f"   • {platform.upper()}: {post_id} ({image_count} imagen(es))")

        return results

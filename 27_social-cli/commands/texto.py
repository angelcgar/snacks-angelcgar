import argparse
from social.facebook import Facebook
from social.twitter import Twitter
from config.settings import SOCIAL_CONFIG
import json

class TextoCommand:
    """Comando para manejar texto con publicación real en redes"""

    def __init__(self, subparsers):
        self.parser = subparsers.add_parser('texto', help='Publicar texto en redes sociales')
        self._add_arguments()

    def _add_arguments(self):
        self.parser.add_argument(
            'contenido',
            type=str,
            help='El texto a publicar'
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
            '--thread',
            action='store_true',
            help='Publicar como hilo en Twitter (divide el texto)'
        )
        self.parser.add_argument(
            '--link',
            type=str,
            help='Enlace para adjuntar (Facebook)'
        )
        self.parser.add_argument(
            '--reply-to',
            type=str,
            help='ID del tweet al que responder (Twitter)'
        )
        self.parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simular publicación sin publicar realmente'
        )

    def _split_for_thread(self, text, max_length=280):
        """Dividir texto para hilo de Twitter"""
        words = text.split()
        tweets = []
        current_tweet = ""

        for word in words:
            if len(current_tweet) + len(word) + 1 <= max_length:
                current_tweet += f" {word}" if current_tweet else word
            else:
                if current_tweet:
                    tweets.append(current_tweet.strip())
                current_tweet = word

        if current_tweet:
            tweets.append(current_tweet.strip())

        return tweets

    def handle(self, args):
        contenido = args.contenido
        results = []

        # Inicializar clientes de redes sociales
        facebook_client = Facebook(
            access_token=SOCIAL_CONFIG['facebook']['access_token'],
            page_id=SOCIAL_CONFIG['facebook']['page_id']
        )

        twitter_client = Twitter(
            api_key=SOCIAL_CONFIG['twitter']['api_key'],
            access_token=SOCIAL_CONFIG['twitter']['access_token']
        )

        # Publicar en Facebook (perfil)
        if args.facebook:
            print("🚀 Publicando en Facebook (perfil)...")
            if args.dry_run:
                print(f"📝 Simulación Facebook: {contenido}")
            else:
                try:
                    result = facebook_client.post_text(
                        contenido,
                        post_type="profile",
                        link=args.link
                    )
                    results.append(result)
                    print("✅ Publicado en Facebook (perfil)")
                except Exception as e:
                    print(f"❌ Error en Facebook: {e}")

        # Publicar en Facebook (página)
        if args.facebook_page:
            print("🚀 Publicando en Facebook (página)...")
            if args.dry_run:
                print(f"📝 Simulación Facebook Page: {contenido}")
            else:
                try:
                    result = facebook_client.post_text(
                        contenido,
                        post_type="page",
                        link=args.link
                    )
                    results.append(result)
                    print("✅ Publicado en Facebook (página)")
                except Exception as e:
                    print(f"❌ Error en Facebook Page: {e}")

        # Publicar en Twitter/X
        if args.twitter:
            print("🚀 Publicando en Twitter/X...")

            if args.thread:
                # Publicar como hilo
                tweets = self._split_for_thread(contenido)
                print(f"🧵 Dividido en {len(tweets)} tweets para el hilo")

                if args.dry_run:
                    for i, tweet in enumerate(tweets):
                        print(f"📝 Simulación Tweet {i+1}: {tweet}")
                else:
                    try:
                        thread_results = twitter_client.thread_post(tweets)
                        results.extend(thread_results)
                        print("✅ Hilo publicado en Twitter/X")
                    except Exception as e:
                        print(f"❌ Error en Twitter thread: {e}")
            else:
                # Publicar tweet único
                if args.dry_run:
                    print(f"📝 Simulación Tweet: {contenido}")
                else:
                    try:
                        result = twitter_client.post_text(
                            contenido,
                            reply_to=args.reply_to
                        )
                        results.append(result)
                        print("✅ Publicado en Twitter/X")
                    except Exception as e:
                        print(f"❌ Error en Twitter: {e}")

        # Mostrar resumen
        if not args.dry_run and results:
            print(f"\n📊 Resumen de publicaciones:")
            for result in results:
                platform = result.get('platform', 'unknown')
                post_id = result.get('post_id') or result.get('tweet_id', 'N/A')
                print(f"   • {platform.upper()}: {post_id}")

        return results

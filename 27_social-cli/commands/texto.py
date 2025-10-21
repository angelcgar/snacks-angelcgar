from .base import BaseCommand

class TextoCommand(BaseCommand):
    """Comando para manejar texto"""

    def __init__(self, subparsers):
        super().__init__(subparsers, 'texto', 'Comando para manejar texto')

    def _add_arguments(self):
        self.parser.add_argument(
            'contenido',
            type=str,
            help='El texto a procesar'
        )
        self.parser.add_argument(
            '--instagram',
            action='store_true',
            help='Publicar en Instagram'
        )
        self.parser.add_argument(
            '--twitter',
            action='store_true',
            help='Publicar en Twitter'
        )
        self.parser.add_argument(
            '--facebook',
            action='store_true',
            help='Publicar en Facebook'
        )

    def handle(self, args):
        contenido = args.contenido
        plataformas = []

        if args.instagram:
            plataformas.append("instagram")
        if args.twitter:
            plataformas.append("twitter")
        if args.facebook:
            plataformas.append("facebook")

        saludo = "hola " + " ".join(plataformas) if plataformas else ""
        resultado = f"{contenido}, {saludo}" if saludo else contenido

        print(resultado.strip())
        return resultado

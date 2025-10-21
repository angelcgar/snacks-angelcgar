import argparse
import sys
from commands.texto import TextoCommand
from commands.imagen import ImagenCommand

class CLI:
    """CLI principal de la aplicación"""

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Aplicación CLI escalable para publicar contenido',
            prog='./app.py'
        )
        self.subparsers = self.parser.add_subparsers(
            dest='command',
            title='comandos',
            description='Comandos disponibles',
            required=True
        )
        self._register_commands()

    def _register_commands(self):
        """Registra todos los comandos disponibles"""
        self.commands = {
            'texto': TextoCommand(self.subparsers),
            'imagen': ImagenCommand(self.subparsers)
        }

    def add_command(self, command_name, command_class):
        """Añade un nuevo comando dinámicamente"""
        self.commands[command_name] = command_class(self.subparsers)

    def run(self):
        """Ejecuta el CLI"""
        if len(sys.argv) == 1:
            self.parser.print_help()
            return

        args = self.parser.parse_args()

        if args.command in self.commands:
            try:
                self.commands[args.command].handle(args)
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            print(f"Comando '{args.command}' no reconocido", file=sys.stderr)
            sys.exit(1)

def main():
    """Función principal"""
    cli = CLI()
    cli.run()

if __name__ == '__main__':
    main()

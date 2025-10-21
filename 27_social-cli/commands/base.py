from abc import ABC, abstractmethod

class BaseCommand(ABC):
    """Clase base para todos los comandos"""

    def __init__(self, subparsers, command_name, help_text):
        self.command_name = command_name
        self.parser = subparsers.add_parser(command_name, help=help_text)
        self._add_arguments()

    @abstractmethod
    def _add_arguments(self):
        """Añadir argumentos específicos del comando"""
        pass

    @abstractmethod
    def handle(self, args):
        """Ejecutar la lógica del comando"""
        pass

"""Define la entidad abstracta común a los objetos identificables."""

from abc import ABC, abstractmethod

from excepciones.errores import DatosInvalidosError


class Entidad(ABC):
    """Base abstracta con identificador y presentación común."""

    def __init__(self, identificador):
        if not isinstance(identificador, str) or not identificador.strip():
            raise DatosInvalidosError("El identificador no puede estar vacío.")
        self._identificador = identificador.strip()

    @property
    def identificador(self):
        """Identificador inmutable de la entidad."""
        return self._identificador

    @abstractmethod
    def mostrar_info(self):
        """Retorna una descripción legible de la entidad."""
        raise NotImplementedError

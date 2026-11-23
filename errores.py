"""Excepciones personalizadas para los errores controlados del dominio."""


class SistemaError(Exception):
    """Base para los errores de negocio que puede gestionar la aplicación."""


class DatosInvalidosError(SistemaError):
    """Indica que los datos suministrados no cumplen las validaciones."""


class ClienteDuplicadoError(SistemaError):
    """Indica que ya existe un cliente con la misma identificación."""


class ClienteNoEncontradoError(SistemaError):
    """Indica que no existe el cliente consultado."""


class ServicioNoDisponibleError(SistemaError):
    """Indica que un servicio no existe o no está disponible."""


class ReservaInvalidaError(SistemaError):
    """Indica que una reserva no es válida o no existe."""


class OperacionNoPermitidaError(SistemaError):
    """Indica que la transición solicitada no está permitida."""


class CalculoInvalidoError(SistemaError):
    """Indica valores inadecuados para un cálculo económico."""

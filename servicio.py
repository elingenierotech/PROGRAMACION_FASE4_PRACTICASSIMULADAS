"""Clase abstracta y reglas comunes de cálculo para los servicios."""

import math
from abc import ABC, abstractmethod

from excepciones.errores import CalculoInvalidoError, DatosInvalidosError


class Servicio(ABC):
    """Servicio disponible cuyo precio se calcula por unidad de duración."""

    def __init__(self, codigo, nombre, precio, disponible=True):
        if not isinstance(codigo, str) or not codigo.strip():
            raise DatosInvalidosError("El código del servicio es obligatorio.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio es obligatorio.")
        self._validar_monto(precio, "El precio")
        self.codigo = codigo.strip()
        self.nombre = nombre.strip()
        self.precio = float(precio)
        self.disponible = bool(disponible)

    @staticmethod
    def _validar_monto(valor, descripcion):
        try:
            monto = float(valor)
        except (TypeError, ValueError, OverflowError) as error:
            raise CalculoInvalidoError("{} debe ser numérico.".format(descripcion)) from error
        if not math.isfinite(monto) or monto < 0:
            raise CalculoInvalidoError("{} debe ser un valor finito no negativo.".format(descripcion))

    @staticmethod
    def _validar_duracion(duracion):
        try:
            horas = float(duracion)
        except (TypeError, ValueError, OverflowError) as error:
            raise CalculoInvalidoError("La duración debe ser numérica.") from error
        if not math.isfinite(horas) or horas <= 0:
            raise CalculoInvalidoError("La duración debe ser finita y mayor que cero.")
        return horas

    @abstractmethod
    def validar_parametros(self, duracion):
        """Valida la duración requerida por el servicio."""
        raise NotImplementedError

    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        """Calcula el costo, admitiendo descuento e impuesto opcionales."""
        raise NotImplementedError

    @abstractmethod
    def describir(self):
        """Describe el servicio para mostrarlo en consola."""
        raise NotImplementedError

    def _calcular_total(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)
        try:
            descuento = float(descuento)
            impuesto = float(impuesto)
        except (TypeError, ValueError, OverflowError) as error:
            raise CalculoInvalidoError("Descuento e impuesto deben ser numéricos.") from error
        if (not math.isfinite(descuento) or not math.isfinite(impuesto)
                or not 0 <= descuento <= 100 or not 0 <= impuesto <= 100):
            raise CalculoInvalidoError("Descuento e impuesto deben estar entre 0 y 100.")
        subtotal = self.precio * self._validar_duracion(duracion)
        total = subtotal * (1 - descuento / 100) * (1 + impuesto / 100)
        if not math.isfinite(total):
            raise CalculoInvalidoError("El costo calculado excede el rango permitido.")
        return round(total, 2)

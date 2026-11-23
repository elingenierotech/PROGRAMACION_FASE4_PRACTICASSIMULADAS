"""Modelo encapsulado de los clientes del sistema."""

import re

from excepciones.errores import DatosInvalidosError
from modelos.entidad import Entidad


class Cliente(Entidad):
    """Representa una persona cliente con datos de contacto validados."""

    _PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    _PATRON_IDENTIFICACION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.-]{3,19}$")
    _PATRON_TELEFONO = re.compile(r"^\+?[0-9][0-9\s()-]{6,19}$")

    def __init__(self, nombre, identificacion, correo, telefono):
        if not all(isinstance(valor, str) and valor.strip()
                   for valor in (nombre, identificacion, correo, telefono)):
            raise DatosInvalidosError("Todos los datos del cliente son obligatorios.")
        nombre = nombre.strip()
        identificacion = identificacion.strip()
        correo = correo.strip()
        telefono = telefono.strip()
        if not self._PATRON_IDENTIFICACION.fullmatch(identificacion):
            raise DatosInvalidosError("La identificación debe tener entre 4 y 20 caracteres válidos.")
        if not self._PATRON_CORREO.fullmatch(correo):
            raise DatosInvalidosError("El formato del correo electrónico no es válido.")
        if not self._PATRON_TELEFONO.fullmatch(telefono):
            raise DatosInvalidosError("El formato del teléfono no es válido.")
        super().__init__(identificacion)
        self.__nombre = nombre
        self.__identificacion = identificacion
        self.__correo = correo
        self.__telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @property
    def identificacion(self):
        return self.__identificacion

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def mostrar_info(self):
        """Presenta los datos necesarios para la consulta de clientes."""
        return "Cliente: {} | ID: {} | Correo: {} | Teléfono: {}".format(
            self.__nombre, self.__identificacion, self.__correo, self.__telefono)

"""Configuración y funciones centralizadas de logging."""

import logging
import sys


_LOGGER = logging.getLogger("software_fj")
_ARCHIVO_HANDLER = "software_fj_archivo"
_CONSOLA_HANDLER = "software_fj_consola"


def configurar_logging(ruta="sistema.log"):
    """Configura el registro y conserva una salida a consola ante fallos de archivo.

    Reutiliza los handlers propios en lugar de acumularlos en llamadas sucesivas.
    Los errores al crear ``ruta`` se informan por consola y nunca impiden continuar.
    """
    _LOGGER.setLevel(logging.INFO)
    _LOGGER.propagate = False

    for manejador in list(_LOGGER.handlers):
        if getattr(manejador, "software_fj_archivo", False):
            if getattr(manejador, "software_fj_ruta", None) == ruta:
                archivo_existente = manejador
            else:
                _LOGGER.removeHandler(manejador)
                manejador.close()
        elif isinstance(manejador, logging.FileHandler):
            _LOGGER.removeHandler(manejador)
            manejador.close()

    consola = next(
        (m for m in _LOGGER.handlers
         if getattr(m, "software_fj_consola", False)),
        None,
    )
    if consola is None:
        consola = logging.StreamHandler(sys.stderr)
        consola.name = _CONSOLA_HANDLER
        consola.software_fj_consola = True
        consola.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"))
        _LOGGER.addHandler(consola)

    archivo_existente = next(
        (m for m in _LOGGER.handlers
         if getattr(m, "software_fj_archivo", False)
         and getattr(m, "software_fj_ruta", None) == ruta),
        None,
    )
    if archivo_existente is None:
        try:
            archivo = logging.FileHandler(ruta, encoding="utf-8")
            archivo.name = _ARCHIVO_HANDLER
            archivo.software_fj_archivo = True
            archivo.software_fj_ruta = ruta
            archivo.setFormatter(logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"))
            _LOGGER.addHandler(archivo)
        except Exception as error:
            _LOGGER.warning(
                "No se pudo abrir el archivo de registro '%s': %s. "
                "La aplicación continuará registrando por consola.",
                ruta,
                error,
            )
    return _LOGGER


def registrar_evento(descripcion):
    """Registra un evento normal del sistema."""
    configurar_logging().info(descripcion)


def registrar_error(descripcion):
    """Registra un error controlado con nivel ERROR."""
    configurar_logging().error(descripcion)

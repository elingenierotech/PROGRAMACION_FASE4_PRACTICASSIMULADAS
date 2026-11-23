"""Reserva y control explícito de transiciones de estado."""

from excepciones.errores import OperacionNoPermitidaError, ReservaInvalidaError, ServicioNoDisponibleError
from utilidades.registro_logs import registrar_evento


class Reserva:
    """Vincula un cliente con un servicio y administra su ciclo de vida."""

    CREADA = "creada"
    CONFIRMADA = "confirmada"
    PROCESADA = "procesada"
    CANCELADA = "cancelada"

    def __init__(self, identificador, cliente, servicio, duracion):
        if not identificador:
            raise ReservaInvalidaError("El identificador de la reserva es obligatorio.")
        servicio.validar_parametros(duracion)
        if not servicio.disponible:
            raise ServicioNoDisponibleError("El servicio no está disponible.")
        self.identificador = str(identificador)
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = float(duracion)
        self.costo = servicio.calcular_costo(self.duracion)
        self.estado = self.CREADA

    def confirmar(self):
        """Confirma una reserva creada si su servicio aún está disponible."""
        if self.estado != self.CREADA:
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas en estado creada.")
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError("El servicio no está disponible para confirmar.")
        self.estado = self.CONFIRMADA
        registrar_evento("Reserva confirmada: {}".format(self.identificador))

    def procesar(self):
        """Procesa únicamente reservas confirmadas."""
        if self.estado != self.CONFIRMADA:
            raise OperacionNoPermitidaError(
                "Solo se pueden procesar reservas confirmadas.")
        self.estado = self.PROCESADA
        registrar_evento("Reserva procesada: {}".format(self.identificador))

    def cancelar(self):
        """Cancela reservas creadas o confirmadas, nunca procesadas."""
        if self.estado not in (self.CREADA, self.CONFIRMADA):
            raise OperacionNoPermitidaError(
                "No se puede cancelar una reserva procesada o ya cancelada.")
        self.estado = self.CANCELADA
        registrar_evento("Reserva cancelada: {}".format(self.identificador))

    def mostrar_info(self):
        """Retorna los datos principales de la reserva."""
        return ("Reserva: {} | Cliente: {} | Servicio: {} | Duración: {} h | "
                "Costo: ${:.2f} | Estado: {}").format(
                    self.identificador, self.cliente.identificacion,
                    self.servicio.nombre, self.duracion, self.costo, self.estado)

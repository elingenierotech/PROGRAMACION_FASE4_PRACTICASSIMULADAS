"""Coordinación en memoria de clientes, servicios y reservas."""

from excepciones.errores import (
    ClienteDuplicadoError,
    ClienteNoEncontradoError,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    SistemaError,
)
from modelos.reserva import Reserva
from utilidades.registro_logs import registrar_evento, registrar_error


class GestorReservas:
    """Administra colecciones en memoria y asegura identificadores únicos."""

    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []
        self._siguiente_reserva = 1

    def registrar_cliente(self, cliente):
        """Agrega un cliente y rechaza identificaciones repetidas."""
        if any(c.identificacion == cliente.identificacion for c in self._clientes):
            error = ClienteDuplicadoError(
                "Ya existe un cliente con identificación {}.".format(cliente.identificacion))
            registrar_error(str(error))
            raise error
        self._clientes.append(cliente)
        registrar_evento("Cliente registrado: {}".format(cliente.identificacion))
        return cliente

    def buscar_cliente(self, identificacion):
        """Busca un cliente por identificación o informa que no existe."""
        for cliente in self._clientes:
            if cliente.identificacion == identificacion:
                return cliente
        error = ClienteNoEncontradoError(
            "No se encontró el cliente {}.".format(identificacion))
        registrar_error(str(error))
        raise error

    def consultar_clientes(self):
        """Retorna una vista inmutable de los clientes registrados."""
        return tuple(self._clientes)

    def registrar_servicio(self, servicio):
        """Agrega un servicio con código único."""
        if any(s.codigo == servicio.codigo for s in self._servicios):
            error = OperacionNoPermitidaError(
                "Ya existe un servicio con código {}.".format(servicio.codigo))
            registrar_error(str(error))
            raise error
        self._servicios.append(servicio)
        registrar_evento("Servicio registrado: {}".format(servicio.codigo))
        return servicio

    def buscar_servicio(self, codigo):
        """Busca un servicio por código."""
        for servicio in self._servicios:
            if servicio.codigo == codigo:
                return servicio
        error = ServicioNoDisponibleError(
            "No se encontró el servicio {}.".format(codigo))
        registrar_error(str(error))
        raise error

    def consultar_servicios(self):
        """Retorna una vista inmutable de los servicios registrados."""
        return tuple(self._servicios)

    def crear_reserva(self, identificacion_cliente, codigo_servicio, duracion):
        """Valida las referencias y crea la reserva en memoria."""
        cliente = self.buscar_cliente(identificacion_cliente)
        servicio = self.buscar_servicio(codigo_servicio)
        try:
            reserva = Reserva(
                "R-{:04d}".format(self._siguiente_reserva),
                cliente, servicio, duracion)
        except SistemaError as error:
            registrar_error("No se pudo crear la reserva: {}".format(error))
            raise
        self._siguiente_reserva += 1
        self._reservas.append(reserva)
        registrar_evento("Reserva creada: {}".format(reserva.identificador))
        return reserva

    def buscar_reserva(self, identificador):
        """Busca una reserva por su identificador generado."""
        for reserva in self._reservas:
            if reserva.identificador == identificador:
                return reserva
        error = ReservaInvalidaError(
            "No se encontró la reserva {}.".format(identificador))
        registrar_error(str(error))
        raise error

    def consultar_reservas(self):
        """Retorna una vista inmutable de las reservas creadas."""
        return tuple(self._reservas)

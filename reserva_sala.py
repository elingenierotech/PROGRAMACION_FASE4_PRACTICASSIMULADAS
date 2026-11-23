"""Servicio de alquiler de salas por horas."""

from modelos.servicio import Servicio


class ReservaSala(Servicio):
    """Calcula la reserva de una sala por hora o fracción positiva."""

    def validar_parametros(self, duracion):
        """Comprueba que se solicite una cantidad positiva de horas."""
        self._validar_duracion(duracion)

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        """Calcula la tarifa de sala con ajustes opcionales."""
        return self._calcular_total(duracion, descuento, impuesto)

    def describir(self):
        """Retorna el resumen legible de la sala."""
        return "Sala {}: {} | ${:.2f}/hora | Disponible: {}".format(
            self.codigo, self.nombre, self.precio, "Sí" if self.disponible else "No")

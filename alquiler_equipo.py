"""Servicio de alquiler de equipos tecnológicos."""

from modelos.servicio import Servicio


class AlquilerEquipo(Servicio):
    """Calcula el alquiler tecnológico con tarifa por hora."""

    def validar_parametros(self, duracion):
        """Comprueba que el tiempo de alquiler sea positivo."""
        self._validar_duracion(duracion)

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        """Calcula el costo del equipo con descuento e impuesto opcionales."""
        return self._calcular_total(duracion, descuento, impuesto)

    def describir(self):
        """Retorna el resumen legible del equipo."""
        return "Equipo {}: {} | ${:.2f}/hora | Disponible: {}".format(
            self.codigo, self.nombre, self.precio, "Sí" if self.disponible else "No")

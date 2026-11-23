"""Servicio de asesoría profesional por duración."""

from modelos.servicio import Servicio


class AsesoriaEspecializada(Servicio):
    """Calcula el costo de una asesoría según las horas contratadas."""

    def validar_parametros(self, duracion):
        """Comprueba que la duración contratada sea positiva."""
        self._validar_duracion(duracion)

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        """Calcula el costo profesional con ajustes opcionales."""
        return self._calcular_total(duracion, descuento, impuesto)

    def describir(self):
        """Retorna el resumen legible de la asesoría."""
        return "Asesoría {}: {} | ${:.2f}/hora | Disponible: {}".format(
            self.codigo, self.nombre, self.precio, "Sí" if self.disponible else "No")

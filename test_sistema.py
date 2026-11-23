"""Pruebas unitarias de validaciones, polimorfismo y transiciones."""

import unittest
import io
import logging
from unittest.mock import patch

from excepciones.errores import (
    CalculoInvalidoError,
    ClienteDuplicadoError,
    DatosInvalidosError,
    OperacionNoPermitidaError,
)
from gestores.gestor_reservas import GestorReservas
from modelos.cliente import Cliente
from modelos.entidad import Entidad
import main
import utilidades.registro_logs as registro_logs
from servicios.alquiler_equipo import AlquilerEquipo
from servicios.asesoria_especializada import AsesoriaEspecializada
from servicios.reserva_sala import ReservaSala


class SistemaTest(unittest.TestCase):
    """Verifica las reglas de negocio fundamentales."""

    def setUp(self):
        self.gestor = GestorReservas()
        self.cliente = Cliente("María López", "CC-12345", "maria@example.com", "3001234567")
        self.gestor.registrar_cliente(self.cliente)
        self.servicio = ReservaSala("S-1", "Sala", 100)
        self.gestor.registrar_servicio(self.servicio)

    def test_cliente_rechaza_correo_invalido(self):
        with self.assertRaises(DatosInvalidosError):
            Cliente("Nombre", "CC-5555", "correo-mal", "3001234567")

    def test_identificacion_duplicada(self):
        with self.assertRaises(ClienteDuplicadoError):
            self.gestor.registrar_cliente(
                Cliente("Otro", "CC-12345", "otro@example.com", "3009876543"))

    def test_polimorfismo_y_variantes_de_calculo(self):
        servicios = [
            ReservaSala("S-2", "Sala", 100),
            AlquilerEquipo("E-1", "Equipo", 100),
            AsesoriaEspecializada("A-1", "Asesoría", 100),
        ]
        self.assertEqual([s.calcular_costo(2) for s in servicios], [200, 200, 200])
        self.assertEqual(servicios[0].calcular_costo(2, descuento=10), 180)
        self.assertEqual(servicios[0].calcular_costo(2, impuesto=19), 238)
        self.assertEqual(servicios[0].calcular_costo(2, descuento=10, impuesto=19), 214.2)

    def test_precio_negativo_y_duracion_no_valida(self):
        with self.assertRaises(CalculoInvalidoError):
            ReservaSala("S-X", "Inválida", -1)
        with self.assertRaises(CalculoInvalidoError):
            self.servicio.calcular_costo(-1)

    def test_transiciones_de_reserva(self):
        reserva = self.gestor.crear_reserva("CC-12345", "S-1", 2)
        with self.assertRaises(OperacionNoPermitidaError):
            reserva.procesar()
        reserva.confirmar()
        reserva.procesar()
        with self.assertRaises(OperacionNoPermitidaError):
            reserva.cancelar()

    def test_encadenamiento_de_conversion(self):
        with self.assertRaises(CalculoInvalidoError) as contexto:
            self.servicio.calcular_costo(1, descuento="incorrecto")
        self.assertIsInstance(contexto.exception.__cause__, ValueError)


class RobustezTest(unittest.TestCase):
    """Prueba fallbacks y recuperación ante errores imprevistos."""

    def test_entidad_rechaza_identificador_vacio_con_excepcion_dominio(self):
        class EntidadConcreta(Entidad):
            def mostrar_info(self):
                return self.identificador

        with self.assertRaises(DatosInvalidosError):
            EntidadConcreta("   ")

    def test_log_fallback_a_consola_si_no_puede_crear_archivo(self):
        for manejador in list(registro_logs._LOGGER.handlers):
            registro_logs._LOGGER.removeHandler(manejador)
            manejador.close()

        with patch("logging.FileHandler", side_effect=OSError("directorio inaccesible")):
            logger = registro_logs.configurar_logging("ruta/no/accesible.log")

        consola = [
            manejador for manejador in logger.handlers
            if getattr(manejador, "software_fj_consola", False)
        ]
        self.assertEqual(len(consola), 1)

        registro_logs.registrar_error("prueba de fallback")
        registro_logs.configurar_logging("ruta/no/accesible.log")
        self.assertEqual(len(consola), 1)

    def test_creacion_reserva_gui_rechaza_cliente_vacio(self):
        import interfaz_grafica

        class Entrada:
            def __init__(self, valor):
                self.valor = valor

            def get(self):
                return self.valor

        class Gestor:
            def __init__(self):
                self.creado = False

            def crear_reserva(self, *args):
                self.creado = True

        app = object.__new__(interfaz_grafica.Aplicacion)
        app.cliente_reserva = Entrada(" ")
        app.servicio_reserva = Entrada("S-1 - Sala")
        app.duracion_reserva = Entrada("2")
        app.gestor = Gestor()

        with patch.object(interfaz_grafica, "registrar_error") as registrar, \
                patch.object(interfaz_grafica.messagebox, "showerror") as mostrar:
            app._crear_reserva()

        self.assertFalse(app.gestor.creado)
        registrar.assert_called_once()
        mostrar.assert_called_once()

    def test_menu_continua_tras_eof_keyboard_e_inesperado(self):
        entradas = iter((EOFError(), KeyboardInterrupt(), RuntimeError("entrada rota"), "11"))

        def leer(_mensaje):
            valor = next(entradas)
            if isinstance(valor, (EOFError, KeyboardInterrupt, RuntimeError)):
                raise valor
            return valor

        with patch("builtins.input", side_effect=leer), \
                patch("builtins.print"), \
                patch.object(main, "configurar_logging"), \
                patch.object(main, "registrar_error"), \
                patch.object(main, "registrar_evento"):
            main.ejecutar_menu()

    def test_simulacion_continua_ante_error_inesperado(self):
        gestor = GestorReservas()
        salida = io.StringIO()

        with patch.object(
                gestor, "registrar_cliente",
                side_effect=RuntimeError("fallo inesperado")), \
                patch.object(main, "registrar_error"), \
                patch.object(main, "registrar_evento"), \
                patch("sys.stdout", salida):
            main.ejecutar_simulacion(gestor)

        texto = salida.getvalue()
        self.assertIn("ERROR INESPERADO", texto)
        self.assertIn("operaciones ejecutadas", texto)


if __name__ == "__main__":
    unittest.main()

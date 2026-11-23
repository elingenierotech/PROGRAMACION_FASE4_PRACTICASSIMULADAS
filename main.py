"""Punto de entrada grafico del Sistema Integral Software FJ."""

from modelos.cliente import Cliente
from servicios.alquiler_equipo import AlquilerEquipo
from servicios.asesoria_especializada import AsesoriaEspecializada
from servicios.reserva_sala import ReservaSala
from excepciones.errores import SistemaError
from gestores.gestor_reservas import GestorReservas
from utilidades.registro_logs import configurar_logging, registrar_error, registrar_evento


def leer_texto(mensaje):
    """Solicita texto y rechaza entradas vacías."""
    valor = input(mensaje).strip()
    if not valor:
        raise ValueError("El campo no puede estar vacío.")
    return valor


def leer_numero(mensaje):
    """Convierte una entrada a número decimal y reporta errores de conversión."""
    try:
        return float(input(mensaje).strip())
    except ValueError as error:
        raise ValueError("Ingrese un número válido.") from error


def registrar_cliente(gestor):
    """Captura y registra los datos de un cliente desde consola."""
    cliente = Cliente(
        leer_texto("Nombre: "),
        leer_texto("Identificación: "),
        leer_texto("Correo electrónico: "),
        leer_texto("Teléfono: "),
    )
    gestor.registrar_cliente(cliente)
    print("Cliente registrado correctamente.")


def mostrar_clientes(gestor):
    """Imprime los clientes registrados."""
    clientes = gestor.consultar_clientes()
    if not clientes:
        print("No hay clientes registrados.")
        return
    for cliente in clientes:
        print(cliente.mostrar_info())


def registrar_servicio(gestor):
    """Solicita el tipo y los datos del nuevo servicio."""
    print("Tipo: 1. Reserva de sala  2. Alquiler de equipo  3. Asesoría especializada")
    tipo = leer_texto("Seleccione el tipo: ")
    codigo = leer_texto("Código: ")
    nombre = leer_texto("Nombre del servicio: ")
    precio = leer_numero("Precio por hora: ")
    clases = {
        "1": ReservaSala,
        "2": AlquilerEquipo,
        "3": AsesoriaEspecializada,
    }
    if tipo not in clases:
        raise ValueError("Tipo de servicio no válido.")
    gestor.registrar_servicio(clases[tipo](codigo, nombre, precio))
    print("Servicio registrado correctamente.")


def mostrar_servicios(gestor):
    """Imprime los servicios disponibles en memoria."""
    servicios = gestor.consultar_servicios()
    if not servicios:
        print("No hay servicios registrados.")
        return
    for servicio in servicios:
        print(servicio.describir())


def crear_reserva(gestor):
    """Solicita los datos necesarios y crea una reserva."""
    reserva = gestor.crear_reserva(
        leer_texto("Identificación del cliente: "),
        leer_texto("Código del servicio: "),
        leer_numero("Duración en horas: "),
    )
    print("Reserva creada. Identificador: {}".format(reserva.identificador))


def cambiar_estado_reserva(gestor, operacion):
    """Aplica a una reserva la transición solicitada."""
    identificador = leer_texto("Identificador de la reserva: ")
    reserva = gestor.buscar_reserva(identificador)
    getattr(reserva, operacion)()
    print("Reserva actualizada. Estado: {}".format(reserva.estado))


def mostrar_reservas(gestor):
    """Imprime las reservas con su estado actual."""
    reservas = gestor.consultar_reservas()
    if not reservas:
        print("No hay reservas registradas.")
        return
    for reserva in reservas:
        print(reserva.mostrar_info())


def ejecutar_simulacion(gestor):
    """Ejecuta los casos solicitados y sigue ante fallos controlados e inesperados."""
    operaciones = []
    reserva_creada = {}
    cliente_1 = Cliente("Ana Pérez", "CC-1001", "ana@example.com", "3001234567")
    cliente_2 = Cliente("Luis Gómez", "CC-1002", "luis@example.com", "3017654321")
    sala = ReservaSala("S-01", "Sala de reuniones", 50000)
    equipo = AlquilerEquipo("E-01", "Proyector", 25000)
    asesoria = AsesoriaEspecializada("A-01", "Asesoría profesional", 80000)

    operaciones.extend([
        ("Registrar cliente válido", lambda: gestor.registrar_cliente(cliente_1)),
        ("Registrar cliente sin nombre", lambda: gestor.registrar_cliente(
            Cliente("", "CC-1003", "otro@example.com", "3001234567"))),
        ("Registrar cliente con correo inválido", lambda: gestor.registrar_cliente(
            Cliente("Cliente Inválido", "CC-1004", "correo-invalido", "3001234567"))),
        ("Registrar cliente duplicado", lambda: gestor.registrar_cliente(
            Cliente("Ana Repetida", "CC-1001", "repetida@example.com", "3009876543"))),
        ("Registrar segundo cliente válido", lambda: gestor.registrar_cliente(cliente_2)),
        ("Registrar servicio de reserva de sala", lambda: gestor.registrar_servicio(sala)),
        ("Registrar servicio de alquiler de equipos", lambda: gestor.registrar_servicio(equipo)),
        ("Registrar servicio de asesoría", lambda: gestor.registrar_servicio(asesoria)),
        ("Registrar servicio con precio negativo", lambda: gestor.registrar_servicio(
            ReservaSala("S-NEG", "Servicio inválido", -100))),
        ("Crear una reserva válida", lambda: reserva_creada.update(
            reserva=gestor.crear_reserva("CC-1001", "S-01", 2))),
        ("Reservar un servicio inexistente", lambda: gestor.crear_reserva(
            "CC-1001", "NO-EXISTE", 1)),
        ("Crear reserva con duración negativa", lambda: gestor.crear_reserva(
            "CC-1001", "S-01", -2)),
        ("Confirmar una reserva", lambda: reserva_creada["reserva"].confirmar()),
        ("Procesar una reserva confirmada", lambda: reserva_creada["reserva"].procesar()),
        ("Cancelar una reserva procesada", lambda: reserva_creada["reserva"].cancelar()),
    ])

    exitosas = 0
    fallidas = 0
    ejecutadas = 0
    print("\n--- Simulación automática ---")
    for numero, (descripcion, accion) in enumerate(operaciones, 1):
        try:
            accion()
        except (SistemaError, ValueError) as error:
            fallidas += 1
            registrar_error("{}: {}".format(descripcion, error))
            print("{}. ERROR CONTROLADO: {} ({})".format(numero, descripcion, error))
        except (EOFError, KeyboardInterrupt) as error:
            fallidas += 1
            registrar_error("{}: interrupción inesperada ({})".format(descripcion, error))
            print("{}. INTERRUPCIÓN: {}. Se continúa con las operaciones.".format(
                numero, descripcion))
        except Exception as error:
            fallidas += 1
            registrar_error("{}: error inesperado: {}".format(descripcion, error))
            print("{}. ERROR INESPERADO: {} ({})".format(numero, descripcion, error))
        else:
            exitosas += 1
            registrar_evento("{}: operación exitosa".format(descripcion))
            print("{}. ÉXITO: {}".format(numero, descripcion))
        finally:
            ejecutadas += 1
    print("\nResumen: {} exitosas, {} fallidas, {} operaciones ejecutadas.".format(
        exitosas, fallidas, ejecutadas))


def ejecutar_menu():
    """Mantiene activo el sistema hasta que el usuario seleccione salir."""
    configurar_logging()
    gestor = GestorReservas()
    opciones = {
        "1": lambda: registrar_cliente(gestor),
        "2": lambda: mostrar_clientes(gestor),
        "3": lambda: registrar_servicio(gestor),
        "4": lambda: mostrar_servicios(gestor),
        "5": lambda: crear_reserva(gestor),
        "6": lambda: cambiar_estado_reserva(gestor, "confirmar"),
        "7": lambda: cambiar_estado_reserva(gestor, "procesar"),
        "8": lambda: cambiar_estado_reserva(gestor, "cancelar"),
        "9": lambda: mostrar_reservas(gestor),
        "10": lambda: ejecutar_simulacion(gestor),
    }
    while True:
        print(
            "\n=== Software FJ: Gestión de clientes, servicios y reservas ===\n"
            "1. Registrar cliente\n2. Consultar clientes\n3. Registrar servicio\n"
            "4. Consultar servicios\n5. Crear reserva\n6. Confirmar reserva\n"
            "7. Procesar reserva\n8. Cancelar reserva\n9. Consultar reservas\n"
            "10. Ejecutar simulación automática\n11. Salir"
        )
        try:
            opcion = input("Seleccione una opción: ").strip()
            if opcion == "11":
                registrar_evento("Cierre solicitado desde el menú")
                print("Hasta pronto.")
                break
            if opcion not in opciones:
                raise ValueError("Seleccione una opción del 1 al 11.")
            opciones[opcion]()
        except (SistemaError, ValueError) as error:
            registrar_error(str(error))
            print("No se pudo completar la operación: {}".format(error))
        except (EOFError, KeyboardInterrupt) as error:
            registrar_evento("Interrupción de entrada en el menú: {}".format(
                type(error).__name__))
            print("\nEntrada interrumpida. Puede continuar usando otra opción.")
        except Exception as error:
            registrar_error("Error inesperado en el menú: {}".format(error))
            print("Ocurrió un error inesperado. Puede continuar usando otra opción.")


if __name__ == "__main__":
    from interfaz_grafica import ejecutar_aplicacion

    configurar_logging()
    ejecutar_aplicacion()

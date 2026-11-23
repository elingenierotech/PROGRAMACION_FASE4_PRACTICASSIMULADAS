# Sistema Integral de Gestión de Clientes, Servicios y Reservas

**Software FJ — UNAD, curso Programación (213023), Fase 4 – Prácticas simuladas**

## Descripción y objetivo general

Aplicación con interfaz gráfica en Python para gestionar clientes, servicios y reservas con objetos y listas en memoria. El proyecto aplica programación orientada a objetos y manejo de excepciones. No utiliza bases de datos; `sistema.log` es el archivo de registro.

El objetivo es administrar clientes, servicios y reservas con validaciones, control de estados y cálculos de costos seguros, manteniendo el programa operativo ante errores controlados.

## Funcionalidades

- Registro y consulta de clientes, con validación de campos, identificación, correo y teléfono y control de duplicados.
- Registro y consulta de reservas de sala, alquiler de equipos y asesorías.
- Creación, confirmación, procesamiento, cancelación y consulta de reservas.
- Cálculo de costos con descuento, impuesto o ambos.
- Interfaz gráfica con pestañas para clientes, servicios y reservas.
- Formularios para registrar datos y botones para administrar reservas.
- Simulación automática gráfica de 15 casos.
- Registro de eventos y errores en `sistema.log`.

## Clases principales

- `Entidad`: clase abstracta con identificador y método de presentación.
- `Cliente`: encapsula y valida datos personales.
- `Servicio`: clase abstracta con código, nombre, precio, disponibilidad y operaciones contractuales.
- `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`: servicios concretos con cálculo polimórfico por duración.
- `Reserva`: vincula cliente y servicio y protege las transiciones de estado.
- `GestorReservas`: administra en memoria las listas de clientes, servicios y reservas.
- `SistemaError` y subclases: representan errores de validación y de negocio.

## Conceptos de POO aplicados

- **Abstracción:** `Entidad` y `Servicio` definen interfaces abstractas.
- **Herencia:** `Cliente` deriva de `Entidad`; los servicios concretos derivan de `Servicio`.
- **Encapsulación:** los datos personales del cliente se almacenan en atributos privados y se consultan mediante propiedades.
- **Polimorfismo:** el gestor y las pruebas trabajan con tipos de `Servicio` y llaman a los mismos métodos sobrescritos.
- **Sobrecarga simulada:** argumentos opcionales de `calcular_costo` permiten costo básico, descuento, impuesto y ambos.

## Excepciones y logging

El dominio define `DatosInvalidosError`, `ClienteDuplicadoError`, `ClienteNoEncontradoError`, `ServicioNoDisponibleError`, `ReservaInvalidaError`, `OperacionNoPermitidaError` y `CalculoInvalidoError`. La consola y la simulación capturan errores controlados e inesperados sin detener el resto de operaciones; las conversiones inválidas se encadenan usando `raise ... from ...`. Se demuestran patrones `try/except`, `try/except/else` y `try/except/finally` en la interfaz/simulación. El módulo `logging` escribe fecha, hora, nivel y descripción en `sistema.log`.

Si `sistema.log` no puede abrirse o crearse, el programa mantiene un manejador de consola, informa el problema una sola vez y continúa operativo. Antes de crear una reserva desde la interfaz se exige seleccionar cliente y servicio.

## Requisitos y ejecución

Se requiere Python 3.8 o posterior. No hay dependencias externas.

Desde la carpeta del proyecto:

```console
python main.py
```

La ventana muestra pestañas para registrar y consultar clientes, servicios y reservas. Para los servicios se solicita código, nombre y precio por hora; para crear una reserva se requiere seleccionar cliente y servicio e ingresar una duración positiva en horas.

## Pruebas

Desde la carpeta del proyecto:

```console
python -m unittest discover -s pruebas -v
```

Las pruebas validan campos de cliente, duplicados, cálculo polimórfico y variantes de tarifa, manejo de conversiones y transiciones de reserva.

## Simulación

Presione **Simulación automática** en la pestaña Reservas para ejecutar los 15 casos obligatorios. El resultado se muestra en una ventana emergente y también quedan registrados los eventos y errores.

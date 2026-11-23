"""Interfaz grafica con Tkinter para el Sistema Integral Software FJ."""

import io
import tkinter as tk
from contextlib import redirect_stdout
from tkinter import messagebox, ttk

from excepciones.errores import DatosInvalidosError, SistemaError
from gestores.gestor_reservas import GestorReservas
from main import ejecutar_simulacion
from modelos.cliente import Cliente
from servicios.alquiler_equipo import AlquilerEquipo
from servicios.asesoria_especializada import AsesoriaEspecializada
from servicios.reserva_sala import ReservaSala
from utilidades.registro_logs import registrar_error, registrar_evento


class Aplicacion(tk.Tk):
    """Ventana principal del sistema."""

    def __init__(self):
        super().__init__()
        self.gestor = GestorReservas()
        self.title("Software FJ - Gestion de clientes, servicios y reservas")
        self.geometry("980x650")
        self.minsize(820, 560)
        self.configure(background="#eef2ff")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self._crear_estilos()

        encabezado = tk.Frame(self, bg="#1e3a8a", height=76)
        encabezado.grid(row=0, column=0, sticky="ew")
        encabezado.grid_propagate(False)
        tk.Label(
            encabezado,
            text="SOFTWARE FJ",
            bg="#1e3a8a",
            fg="#ffffff",
            font=("Segoe UI", 20, "bold"),
        ).pack(side="left", padx=24, pady=(12, 0))
        tk.Label(
            encabezado,
            text="Gestión inteligente de clientes, servicios y reservas",
            bg="#1e3a8a",
            fg="#bfdbfe",
            font=("Segoe UI", 10),
        ).pack(side="left", padx=(12, 24), pady=(20, 0))

        self.cuaderno = ttk.Notebook(self)
        self.cuaderno.grid(row=1, column=0, sticky="nsew", padx=12, pady=(10, 6))

        self._crear_pestana_clientes()
        self._crear_pestana_servicios()
        self._crear_pestana_reservas()

        self.estado_sistema = tk.Label(
            self,
            text="Sistema listo",
            anchor="w",
            bg="#dbeafe",
            fg="#1e3a8a",
            font=("Segoe UI", 9),
            padx=14,
            pady=7,
        )
        self.estado_sistema.grid(row=2, column=0, sticky="ew")
        self._actualizar_todo()
        self.protocol("WM_DELETE_WINDOW", self._cerrar)

    def _crear_estilos(self):
        estilo = ttk.Style(self)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")

        estilo.configure(".", background="#eef2ff", foreground="#1e293b")
        estilo.configure("Fondo.TFrame", background="#eef2ff")
        estilo.configure("Titulo.TLabel",
                         background="#eef2ff",
                         foreground="#1e3a8a",
                         font=("Segoe UI", 13, "bold"))
        estilo.configure("Campo.TLabel",
                         background="#eef2ff",
                         foreground="#334155",
                         font=("Segoe UI", 10))

        estilo.configure("TEntry",
                         fieldbackground="#ffffff",
                         foreground="#0f172a",
                         padding=7)
        estilo.configure("TCombobox",
                         fieldbackground="#ffffff",
                         foreground="#0f172a",
                         padding=6)

        estilo.configure("TNotebook",
                         background="#eef2ff",
                         borderwidth=0)
        estilo.configure("TNotebook.Tab",
                         background="#c7d2fe",
                         foreground="#312e81",
                         padding=(18, 8),
                         font=("Segoe UI", 10, "bold"))
        estilo.map("TNotebook.Tab",
                   background=[("selected", "#4f46e5"), ("active", "#a5b4fc")],
                   foreground=[("selected", "#ffffff"), ("active", "#1e1b4b")])

        estilo.configure("TButton",
                         padding=(10, 7),
                         font=("Segoe UI", 9, "bold"))
        estilo.configure("Accion.TButton",
                         background="#2563eb",
                         foreground="#ffffff")
        estilo.map("Accion.TButton",
                   background=[("active", "#1d4ed8"), ("pressed", "#1e40af")])
        estilo.configure("Confirmar.TButton",
                         background="#059669",
                         foreground="#ffffff")
        estilo.configure("Procesar.TButton",
                         background="#7c3aed",
                         foreground="#ffffff")
        estilo.configure("Cancelar.TButton",
                         background="#dc2626",
                         foreground="#ffffff")
        estilo.configure("Simular.TButton",
                         background="#ea580c",
                         foreground="#ffffff")

        estilo.configure("Treeview",
                         background="#ffffff",
                         fieldbackground="#ffffff",
                         foreground="#1e293b",
                         rowheight=27,
                         borderwidth=0)
        estilo.configure("Treeview.Heading",
                         background="#1e40af",
                         foreground="#ffffff",
                         font=("Segoe UI", 9, "bold"),
                         padding=(8, 6))
        estilo.map("Treeview",
                   background=[("selected", "#c7d2fe")],
                   foreground=[("selected", "#1e1b4b")])

        estilo.configure("FilaAzul.Treeview",
                         background="#eff6ff",
                         fieldbackground="#eff6ff")

    def _activar_hover(self, boton, color_normal, color_hover):
        """Añade una respuesta visual al pasar el cursor sobre un botón."""
        boton.bind("<Enter>", lambda _evento: boton.configure(bg=color_hover))
        boton.bind("<Leave>", lambda _evento: boton.configure(bg=color_normal))

    def _crear_pestana_clientes(self):
        pestaña = ttk.Frame(self.cuaderno, padding=12, style="Fondo.TFrame")
        self.cuaderno.add(pestaña, text="Clientes")
        pestaña.columnconfigure(1, weight=1)
        pestaña.rowconfigure(7, weight=1)

        ttk.Label(pestaña, text="Registrar cliente", style="Titulo.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        campos = (
            ("Nombre", "nombre_cliente"),
            ("Identificacion", "identificacion_cliente"),
            ("Correo electronico", "correo_cliente"),
            ("Telefono", "telefono_cliente"),
        )
        for fila, (texto, atributo) in enumerate(campos, 1):
            ttk.Label(pestaña, text=texto).grid(row=fila, column=0, sticky="w", padx=(0, 8), pady=4)
            entrada = ttk.Entry(pestaña)
            entrada.grid(row=fila, column=1, sticky="ew", pady=4)
            setattr(self, atributo, entrada)

        boton_cliente = tk.Button(
            pestaña,
            text="+ Registrar cliente",
            command=self._registrar_cliente,
            bg="#2563eb",
            fg="#ffffff",
            activebackground="#1d4ed8",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=8,
        )
        boton_cliente.grid(row=5, column=1, sticky="e", pady=(12, 8))
        self._activar_hover(boton_cliente, "#2563eb", "#1d4ed8")

        ttk.Label(pestaña, text="Clientes registrados", style="Titulo.TLabel").grid(
            row=6, column=0, columnspan=2, sticky="w", pady=(10, 5))

        columnas = ("nombre", "identificacion", "correo", "telefono")
        self.tabla_clientes = ttk.Treeview(
            pestaña, columns=columnas, show="headings", height=10)
        encabezados = ("Nombre", "Identificacion", "Correo", "Telefono")
        for columna, encabezado in zip(columnas, encabezados):
            self.tabla_clientes.heading(columna, text=encabezado)
        self.tabla_clientes.column("nombre", width=180)
        self.tabla_clientes.column("identificacion", width=140)
        self.tabla_clientes.column("correo", width=220)
        self.tabla_clientes.column("telefono", width=150)
        self.tabla_clientes.grid(row=7, column=0, columnspan=2, sticky="nsew")

    def _crear_pestana_servicios(self):
        pestaña = ttk.Frame(self.cuaderno, padding=12, style="Fondo.TFrame")
        self.cuaderno.add(pestaña, text="Servicios")
        pestaña.columnconfigure(1, weight=1)
        pestaña.rowconfigure(7, weight=1)

        ttk.Label(pestaña, text="Registrar servicio", style="Titulo.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        ttk.Label(pestaña, text="Tipo").grid(row=1, column=0, sticky="w", pady=4)
        self.tipo_servicio = ttk.Combobox(
            pestaña,
            values=("Reserva de sala", "Alquiler de equipo", "Asesoria especializada"),
            state="readonly",
        )
        self.tipo_servicio.current(0)
        self.tipo_servicio.grid(row=1, column=1, sticky="ew", pady=4)

        self.codigo_servicio = ttk.Entry(pestaña)
        self.nombre_servicio = ttk.Entry(pestaña)
        self.precio_servicio = ttk.Entry(pestaña)

        for fila, (texto, entrada) in enumerate((
            ("Codigo", self.codigo_servicio),
            ("Nombre", self.nombre_servicio),
            ("Precio por hora", self.precio_servicio),
        ), 2):
            ttk.Label(pestaña, text=texto).grid(row=fila, column=0, sticky="w", padx=(0, 8), pady=4)
            entrada.grid(row=fila, column=1, sticky="ew", pady=4)

        boton_servicio = tk.Button(
            pestaña,
            text="+ Registrar servicio",
            command=self._registrar_servicio,
            bg="#2563eb",
            fg="#ffffff",
            activebackground="#1d4ed8",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=8,
        )
        boton_servicio.grid(row=5, column=1, sticky="e", pady=(12, 8))
        self._activar_hover(boton_servicio, "#2563eb", "#1d4ed8")

        ttk.Label(pestaña, text="Servicios registrados", style="Titulo.TLabel").grid(
            row=6, column=0, columnspan=2, sticky="w", pady=(10, 5))

        columnas = ("codigo", "tipo", "nombre", "precio", "disponible")
        self.tabla_servicios = ttk.Treeview(
            pestaña, columns=columnas, show="headings", height=10)
        encabezados = ("Codigo", "Tipo", "Nombre", "Precio/hora", "Disponible")
        for columna, encabezado in zip(columnas, encabezados):
            self.tabla_servicios.heading(columna, text=encabezado)
        self.tabla_servicios.column("codigo", width=100)
        self.tabla_servicios.column("tipo", width=180)
        self.tabla_servicios.column("nombre", width=220)
        self.tabla_servicios.column("precio", width=120)
        self.tabla_servicios.column("disponible", width=100)
        self.tabla_servicios.grid(row=7, column=0, columnspan=2, sticky="nsew")

    def _crear_pestana_reservas(self):
        pestaña = ttk.Frame(self.cuaderno, padding=12, style="Fondo.TFrame")
        self.cuaderno.add(pestaña, text="Reservas")
        pestaña.columnconfigure(1, weight=1)
        pestaña.rowconfigure(6, weight=1)

        ttk.Label(pestaña, text="Crear reserva", style="Titulo.TLabel").grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        ttk.Label(pestaña, text="Cliente").grid(row=1, column=0, sticky="w", pady=4)
        self.cliente_reserva = ttk.Combobox(pestaña, state="readonly")
        self.cliente_reserva.grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Label(pestaña, text="Servicio").grid(row=1, column=2, sticky="w", padx=(12, 8), pady=4)
        self.servicio_reserva = ttk.Combobox(pestaña, state="readonly")
        self.servicio_reserva.grid(row=1, column=3, sticky="ew", pady=4)

        ttk.Label(pestaña, text="Duracion (horas)").grid(row=2, column=0, sticky="w", pady=4)
        self.duracion_reserva = ttk.Entry(pestaña)
        self.duracion_reserva.grid(row=2, column=1, sticky="ew", pady=4)

        ttk.Button(
            pestaña, text="Crear reserva", style="Accion.TButton",
            command=self._crear_reserva
        ).grid(row=3, column=0, sticky="w", pady=(8, 10))

        ttk.Label(pestaña, text="Reservas", style="Titulo.TLabel").grid(
            row=4, column=0, columnspan=4, sticky="w", pady=(8, 5))

        botones = ttk.Frame(pestaña)
        botones.grid(row=5, column=0, columnspan=4, sticky="w", pady=(0, 8))
        ttk.Button(
            botones, text="Confirmar", style="Confirmar.TButton",
            command=lambda: self._cambiar_estado("confirmar"),
        ).pack(side="left", padx=(0, 6))
        ttk.Button(
            botones, text="Procesar", style="Procesar.TButton",
            command=lambda: self._cambiar_estado("procesar"),
        ).pack(side="left", padx=6)
        ttk.Button(
            botones, text="Cancelar", style="Cancelar.TButton",
            command=lambda: self._cambiar_estado("cancelar"),
        ).pack(side="left", padx=6)
        ttk.Button(
            botones, text="Simulacion automatica", style="Simular.TButton",
            command=self._ejecutar_simulacion,
        ).pack(side="left", padx=(12, 0))

        columnas = ("identificador", "cliente", "servicio", "duracion", "costo", "estado")
        self.tabla_reservas = ttk.Treeview(
            pestaña, columns=columnas, show="headings", height=10)
        encabezados = ("Identificador", "Cliente", "Servicio", "Duracion", "Costo", "Estado")
        for columna, encabezado in zip(columnas, encabezados):
            self.tabla_reservas.heading(columna, text=encabezado)
        self.tabla_reservas.column("identificador", width=110)
        self.tabla_reservas.column("cliente", width=180)
        self.tabla_reservas.column("servicio", width=220)
        self.tabla_reservas.column("duracion", width=90)
        self.tabla_reservas.column("costo", width=120)
        self.tabla_reservas.column("estado", width=100)
        self.tabla_reservas.grid(row=6, column=0, columnspan=4, sticky="nsew")

    def _registrar_cliente(self):
        try:
            cliente = Cliente(
                self.nombre_cliente.get(),
                self.identificacion_cliente.get(),
                self.correo_cliente.get(),
                self.telefono_cliente.get(),
            )
            self.gestor.registrar_cliente(cliente)
        except (SistemaError, ValueError) as error:
            self._mostrar_error(error)
            return

        for entrada in (
            self.nombre_cliente,
            self.identificacion_cliente,
            self.correo_cliente,
            self.telefono_cliente,
        ):
            entrada.delete(0, tk.END)
        self._actualizar_clientes()
        self._establecer_estado("Cliente registrado correctamente", "exito")
        messagebox.showinfo("Cliente registrado", "El cliente fue registrado correctamente.")

    def _registrar_servicio(self):
        tipo = self.tipo_servicio.get()
        try:
            precio = float(self.precio_servicio.get().strip())
            clases = {
                "Reserva de sala": ReservaSala,
                "Alquiler de equipo": AlquilerEquipo,
                "Asesoria especializada": AsesoriaEspecializada,
            }
            servicio = clases[tipo](
                self.codigo_servicio.get(),
                self.nombre_servicio.get(),
                precio,
            )
            self.gestor.registrar_servicio(servicio)
        except (SistemaError, ValueError) as error:
            self._mostrar_error(error)
            return

        self.codigo_servicio.delete(0, tk.END)
        self.nombre_servicio.delete(0, tk.END)
        self.precio_servicio.delete(0, tk.END)
        self._actualizar_servicios()
        self._establecer_estado("Servicio registrado correctamente", "exito")
        messagebox.showinfo("Servicio registrado", "El servicio fue registrado correctamente.")

    def _crear_reserva(self):
        """Valida la selección y muestra los errores controlados o inesperados."""
        try:
            cliente_seleccionado = self.cliente_reserva.get().strip()
            servicio_seleccionado = self.servicio_reserva.get().strip()
            if not cliente_seleccionado:
                raise DatosInvalidosError(
                    "Debe seleccionar un cliente antes de crear la reserva.")
            if not servicio_seleccionado:
                raise DatosInvalidosError(
                    "Debe seleccionar un servicio antes de crear la reserva.")
            identificacion = cliente_seleccionado.split(" - ", 1)[0]
            codigo = servicio_seleccionado.split(" - ", 1)[0]
            duracion = float(self.duracion_reserva.get().strip())
            reserva = self.gestor.crear_reserva(identificacion, codigo, duracion)
        except (SistemaError, ValueError, IndexError) as error:
            self._mostrar_error(error)
            return
        except Exception as error:
            mensaje = "Error inesperado al crear reserva: {}".format(error)
            registrar_error(mensaje)
            self._establecer_estado(str(error), "error")
            messagebox.showerror(
                "No se pudo completar la operacion",
                "Error inesperado: {}".format(error),
            )
            return

        self.duracion_reserva.delete(0, tk.END)
        self._actualizar_reservas()
        self._establecer_estado(
            "Reserva {} creada correctamente".format(reserva.identificador),
            "exito",
        )
        messagebox.showinfo(
            "Reserva creada",
            "Reserva {} creada correctamente.".format(reserva.identificador),
        )

    def _cambiar_estado(self, operacion):
        seleccion = self.tabla_reservas.selection()
        if not seleccion:
            messagebox.showwarning("Seleccione una reserva", "Debe seleccionar una reserva de la tabla.")
            return
        identificador = self.tabla_reservas.item(seleccion[0], "values")[0]
        try:
            reserva = self.gestor.buscar_reserva(identificador)
            getattr(reserva, operacion)()
        except SistemaError as error:
            self._mostrar_error(error)
            return
        self._actualizar_reservas()
        self._establecer_estado(
            "Reserva {} actualizada a {}".format(reserva.identificador, reserva.estado),
            "exito",
        )
        messagebox.showinfo("Estado actualizado", "Reserva: {}".format(reserva.estado))

    def _ejecutar_simulacion(self):
        salida = io.StringIO()
        try:
            with redirect_stdout(salida):
                ejecutar_simulacion(self.gestor)
        except Exception as error:
            registrar_error("Error inesperado durante la simulacion: {}".format(error))
            self._mostrar_error(error)
            return
        self._actualizar_todo()
        self._establecer_estado("Simulacion automatica finalizada", "exito")
        messagebox.showinfo(
            "Simulacion automatica",
            salida.getvalue() or "La simulacion finalizo.",
        )

    def _actualizar_clientes(self):
        for elemento in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(elemento)
        opciones = []
        for indice, cliente in enumerate(self.gestor.consultar_clientes()):
            self.tabla_clientes.insert(
                "", "end",
                values=(cliente.nombre, cliente.identificacion, cliente.correo, cliente.telefono),
                tags=("alternado" if indice % 2 == 0 else "normal",),
            )
            opciones.append("{} - {}".format(cliente.identificacion, cliente.nombre))
        self.tabla_clientes.tag_configure("alternado", background="#eff6ff")
        self.tabla_clientes.tag_configure("normal", background="#ffffff")
        self.cliente_reserva["values"] = opciones
        if opciones:
            self.cliente_reserva.current(0)

    def _actualizar_servicios(self):
        for elemento in self.tabla_servicios.get_children():
            self.tabla_servicios.delete(elemento)
        opciones = []
        for indice, servicio in enumerate(self.gestor.consultar_servicios()):
            tipo = type(servicio).__name__
            nombres_tipo = {
                "ReservaSala": "Sala",
                "AlquilerEquipo": "Equipo",
                "AsesoriaEspecializada": "Asesoria",
            }
            etiqueta = "disponible" if servicio.disponible else "nodisponible"
            self.tabla_servicios.insert(
                "", "end",
                values=(
                    servicio.codigo,
                    nombres_tipo.get(tipo, tipo),
                    servicio.nombre,
                    "${:.2f}".format(servicio.precio),
                    "Si" if servicio.disponible else "No",
                ),
                tags=(etiqueta,),
            )
            opciones.append("{} - {}".format(servicio.codigo, servicio.nombre))
        self.tabla_servicios.tag_configure(
            "disponible", background="#ecfdf5", foreground="#065f46")
        self.tabla_servicios.tag_configure(
            "nodisponible", background="#fee2e2", foreground="#991b1b")
        self.servicio_reserva["values"] = opciones
        if opciones:
            self.servicio_reserva.current(0)

    def _actualizar_reservas(self):
        for elemento in self.tabla_reservas.get_children():
            self.tabla_reservas.delete(elemento)
        for reserva in self.gestor.consultar_reservas():
            self.tabla_reservas.insert(
                "", "end",
                values=(
                    reserva.identificador,
                    reserva.cliente.identificacion,
                    reserva.servicio.nombre,
                    "{} h".format(reserva.duracion),
                    "${:.2f}".format(reserva.costo),
                    reserva.estado,
                ),
                tags=(reserva.estado,),
            )
        self.tabla_reservas.tag_configure(
            "creada", background="#fef9c3", foreground="#854d0e")
        self.tabla_reservas.tag_configure(
            "confirmada", background="#dbeafe", foreground="#1e40af")
        self.tabla_reservas.tag_configure(
            "procesada", background="#dcfce7", foreground="#166534")
        self.tabla_reservas.tag_configure(
            "cancelada", background="#fee2e2", foreground="#991b1b")

    def _actualizar_todo(self):
        self._actualizar_clientes()
        self._actualizar_servicios()
        self._actualizar_reservas()
        clientes = len(self.gestor.consultar_clientes())
        servicios = len(self.gestor.consultar_servicios())
        reservas = len(self.gestor.consultar_reservas())
        self._establecer_estado(
            "{} clientes  |  {} servicios  |  {} reservas".format(
                clientes, servicios, reservas),
            "info",
        )

    def _establecer_estado(self, mensaje, tipo="info"):
        """Actualiza la barra inferior con feedback visual."""
        etiqueta_estado = self.__dict__.get("estado_sistema")
        if etiqueta_estado is None:
            return
        colores = {
            "info": ("#dbeafe", "#1e3a8a"),
            "exito": ("#dcfce7", "#166534"),
            "error": ("#fee2e2", "#991b1b"),
        }
        fondo, texto = colores.get(tipo, colores["info"])
        etiqueta_estado.configure(
            text=mensaje,
            bg=fondo,
            fg=texto,
        )

    def _mostrar_error(self, error):
        registrar_error(str(error))
        self._establecer_estado(str(error), "error")
        messagebox.showerror("No se pudo completar la operacion", str(error))

    def _cerrar(self):
        registrar_evento("Cierre solicitado desde la interfaz grafica")
        self.destroy()


def ejecutar_aplicacion():
    """Inicia la interfaz grafica."""
    aplicacion = Aplicacion()
    aplicacion.mainloop()

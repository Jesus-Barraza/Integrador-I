import tkinter as tk
from tkinter import PhotoImage, messagebox
from tkcalendar import Calendar
from controller import funciones
import functools
import os
from . import menus, funcionalidad
import flet as ft
import multiprocessing
from datetime import datetime

class Volver():
    def __init__(self, ventana):
        menus.Menu(ventana)

def iniciarFlet():
    ft.app(target=Volver, assets_dir="img", view=ft.AppView.FLET_APP)

class Menu():
    def __init__(self, ventana, sesion, tema):
        self.color1 = "#5E95D4"
        self.color2 = "#E2E2E2"
        self.color3 = "#000000"
        self.color4 = "#ffffff"
        self.color5 = "#B7B22F"
        self.tema_oscuro=tema
        self.hoy=datetime.now()
        ventana.geometry("1920x1080")
        ventana.title("Programa de psicopedagogía")   
        ventana.config(bg=self.color2)
        self.cambiarTema(ventana, sesion, self.tema_oscuro, False)
        self.num=1
        self.menuPrincipal(ventana, sesion)

    @staticmethod
    def borrarPantalla(ventana):
        for widget in ventana.winfo_children():
            widget.destroy()

    def cambiarTema(self, ventana, sesion, oscuro_var, config):
        try:
            self.tema_oscuro = oscuro_var.get()
        except AttributeError:
            self.tema_oscuro= oscuro_var
        self.modoOscuro(ventana, sesion, self.tema_oscuro, config)
    
    def modoOscuro(self, ventana, sesion, status, config):
        # Cambiar colores globales
        if not status:
            # Tema claro
            self.color1 = "#5E95D4"
            self.color2 = "#D9D9D9"
            self.color3 = "#000000"
            self.color4 = "#ffffff"
            self.color5 = "#B7B22F"
            ventana.config(bg=self.color2)
        else:
            # Tema oscuro
            self.color1 = "#353e70"
            self.color2 = "#353535"
            self.color3 = "#d6d6d6"
            self.color4 = "#323232"
            self.color5 = "#836819"
            ventana.config(bg=self.color2)
        
        if config:
            self.borrarPantalla(ventana)
            self.menuConfiguraciones(ventana, sesion)

    def grupoTitulo(self, ventana, sesion, texto, config, num):
        if num!=0 and num!=6:
            self.num=num
        # Frame superior
        if num==6:
            frame_superior = tk.Frame(ventana, bg=self.color5, height=200, highlightbackground=self.color3, highlightthickness=3)
        else:
            frame_superior = tk.Frame(ventana, bg=self.color1, height=200, highlightbackground=self.color5, highlightthickness=3)
        frame_superior.pack(fill="x", side="top")

        # Frame contenedor horizontal
        frame_horizontal = tk.Frame(frame_superior, bg=self.color1)
        frame_horizontal.pack(fill="x", padx=10, pady=10)

        frame_horizontal.columnconfigure(0, weight=1)  # espacio a la izquierda
        frame_horizontal.columnconfigure(1, weight=0)  # título centrado
        frame_horizontal.columnconfigure(2, weight=1)

        # Frame del título (izquierda)
        if num==4 or num==5:
            frame_titulo = tk.Frame(frame_horizontal, bg=self.color5, height=30, width=600)
            lbl_titulo = tk.Label(frame_titulo, text=texto, font=("Arial", 24), fg=self.color3, bg=self.color5)
        else:
            frame_titulo = tk.Frame(frame_horizontal, bg=self.color2, height=30, width=400)
            lbl_titulo = tk.Label(frame_titulo, text=texto, font=("Arial", 24), fg=self.color3, bg=self.color2)
        frame_titulo.grid(row=0, column=1, padx=10)
        lbl_titulo.pack(anchor="center")

        if config:
            # Frame de botones (derecha)
            frame_botones = tk.Frame(frame_horizontal, bg=self.color1)
            frame_botones.grid(row=0, column=2, sticky="e")

            path = os.path.abspath("img/")
            self.button_image_1 = PhotoImage(file=path + "/config.png")
            button_1 = tk.Button(
                frame_botones,
                image=self.button_image_1,
                borderwidth=0,
                highlightthickness=0,
                command=lambda:self.menuConfiguraciones(ventana, sesion),
                relief="flat",
                bg=self.color1
            )
            button_1.pack(side="left", padx=10)

            self.button_image_2 = PhotoImage(file=path + "/noti.png")
            button_2 = tk.Button(
                frame_botones,
                image=self.button_image_2,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.menuNotificaciones(ventana, sesion),
                relief="flat",
                bg=self.color1
            )
            button_2.pack(side="left", padx=10)
        else:
            #Frame de retorno
            path = os.path.abspath("img/")
            self.button_image_1 = PhotoImage(file=path + "/Atras.png")
            button_1 = tk.Button(
                frame_horizontal,
                image=self.button_image_1,
                borderwidth=0,
                highlightthickness=0,
                command=lambda:retorno(self.num),
                relief="flat",
                bg=self.color1
            )
            button_1.grid(row=0, column=0, padx=10)

        def retorno(num):
            if num==1:
                button_1.config(command=lambda:self.menuPrincipal(ventana, sesion))
            elif num==2:
                button_1.config(command=lambda:self.menuCalendario(ventana, sesion))
            elif num==3:
                button_1.config(command=lambda:self.menuCitas(ventana, sesion))
            elif num==4:
                button_1.config(command=lambda:self.menuEstudiantes(ventana, sesion))
            elif num==5:
                button_1.config(command=lambda:self.menuTutores(ventana, sesion))

    def submenu(self,ventana, sesion):
        #funcion
        def cerrarSesion(ventana):
            ventana.destroy()
            p = multiprocessing.Process(target=iniciarFlet)
            p.start()

        #Barra del menú
        menubar=tk.Menu(ventana, bg=self.color1, fg=self.color4)
        ventana.config(menu=menubar)

        #Archivo del menú
        menuarch=tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Menú desplegable", menu=menuarch)
        menuarch.add_command(label="Menú principal", command=lambda:self.menuPrincipal(ventana, sesion))
        menuarch.add_command(label="Calendario", command=lambda:self.menuCalendario(ventana, sesion))
        menuarch.add_command(label="Citas", command=lambda:self.menuCitas(ventana, sesion))
        menuarch.add_separator()
        menuarch.add_command(label="Alumnos", command=lambda:self.menuEstudiantes(ventana, sesion))
        menuarch.add_command(label="Tutores", command=lambda:self.menuTutores(ventana, sesion))
        menuarch.add_separator()
        menuarch.add_command(label="Cerrar sesión", command=lambda:cerrarSesion(ventana))
        menuarch.add_command(label="Acerca de", command=lambda:self.acercaDe(ventana, sesion))

    def menuPrincipal(self, ventana, sesion):
        #Limpiar la pantalla (por si acaso)
        self.borrarPantalla(ventana)

        #barra superior
        self.submenu(ventana, sesion)

        #Grupo de arriba
        self.grupoTitulo(ventana, sesion, "Menú principal", True, 1)

        #Cuadro de citas del día
        lbl_citas_dia = tk.Label(ventana, text="Citas activas", font=("Arial", 18), fg=self.color3, bg=self.color2)
        lbl_citas_dia.pack(pady=10)

        frame_citas_dia = tk.Frame(ventana, bg=self.color4, height=200, width=600, relief="raised", bd=2)
        frame_citas_dia.pack(pady=20)

        citas_dia=funciones.Citas.obtener_citas_dia(sesion[0])
        path = os.path.abspath("img/")
        if len(citas_dia) > 0:
            lbl_titulo_citas_0=tk.Label(frame_citas_dia, text="Cita ID", font=("Arial", 16), fg=self.color3, bg=self.color4)
            lbl_titulo_citas_0.grid(row=0, column=0, pady=10, padx=5)

            lbl_titulo_citas_1=tk.Label(frame_citas_dia, text="Nombre del alumno", font=("Arial", 16), fg=self.color3, bg=self.color4)
            lbl_titulo_citas_1.grid(row=0, column=1, pady=10, padx=5)

            lbl_titulo_citas_2=tk.Label(frame_citas_dia, text="Fecha", font=("Arial", 16), fg=self.color3, bg=self.color4)
            lbl_titulo_citas_2.grid(row=0, column=2, pady=10, padx=5)

            lbl_titulo_citas_3=tk.Label(frame_citas_dia, text="Status", font=("Arial", 16), fg=self.color3, bg=self.color4)
            lbl_titulo_citas_3.grid(row=0, column=3, pady=10, padx=5)
            num_citas=1

            lbl_titulo_citas_4=tk.Label(frame_citas_dia, text="Opciones", font=("Arial", 16), fg=self.color3, bg=self.color4)
            lbl_titulo_citas_4.grid(row=0, column=4, pady=10, padx=5)
            num_citas=1

            for cita in citas_dia:
                lbl_cita_0 = tk.Label(frame_citas_dia, text=f"{cita[0]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                lbl_cita_0.grid(row=num_citas, column=0, pady=5, padx=10)

                lbl_cita_1 = tk.Label(frame_citas_dia, text=f"{cita[1]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                lbl_cita_1.grid(row=num_citas, column=1, pady=5, padx=10)

                lbl_cita_2 = tk.Label(frame_citas_dia, text=f"{cita[2]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                lbl_cita_2.grid(row=num_citas, column=2, pady=5, padx=10)

                lbl_cita_3 = tk.Label(frame_citas_dia, text=f"{cita[3]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                lbl_cita_3.grid(row=num_citas, column=3, pady=5, padx=10)

                img = PhotoImage(file=path + "/cancelar.png")
                button_3 = tk.Button(
                    frame_citas_dia,
                    image=img,
                    borderwidth=0,
                    highlightthickness=0,
                    command=functools.partial(funciones.Citas.cancelarCitas, cita[0], sesion[0]),
                    relief="flat",
                    bg=self.color4
                )
                button_3.image = img
                button_3.grid(row=num_citas, column=4, padx=10, pady=5)

                num_citas += 1
        else:
            lbl_no_citas=tk.Label(frame_citas_dia, text="Por lo pronto, no se han realizado citas", font=("Arial", 16), fg=self.color3, bg=self.color4)
            lbl_no_citas.pack(pady=10)

            btn_interaccion=tk.Button(
                frame_citas_dia,
                text="Agregar cita",
                font=("Arial", 14, "underline"),
                fg="blue",
                bg=self.color4,
                relief="flat",
                borderwidth=0,
                highlightthickness=0,
                cursor="hand2",
                command=lambda: funcionalidad.Funcionalidad(ventana, self.tema_oscuro, 1).insertar(ventana, sesion, 1)
            )
            btn_interaccion.pack(pady=10)

        #Cuadro de citas pasadas
        lbl_citas_h = tk.Label(ventana, text="Citas anteriores", font=("Arial", 18), fg=self.color3, bg=self.color2)
        lbl_citas_h.pack(pady=10)

        frame_citas_h = tk.Frame(ventana, bg=self.color4, height=200, width=600, relief="raised", bd=2)
        frame_citas_h.pack(pady=20)

        citas_dia=funciones.Citas.obtener_citas_h(sesion[0])   
        if len(citas_dia) > 0:
            lbl_titulo_citas_0=tk.Label(frame_citas_h, text="Cita ID", font=("Arial", 16), fg=self.color3, bg=self.color4)
            lbl_titulo_citas_0.grid(row=0, column=0, pady=10, padx=5)

            lbl_titulo_citas_1=tk.Label(frame_citas_h, text="Nombre del alumno", font=("Arial", 16), fg=self.color3, bg=self.color4)
            lbl_titulo_citas_1.grid(row=0, column=1, pady=10, padx=5)

            lbl_titulo_citas_2=tk.Label(frame_citas_h, text="Fecha", font=("Arial", 16), fg=self.color3, bg=self.color4)
            lbl_titulo_citas_2.grid(row=0, column=2, pady=10, padx=5)

            lbl_titulo_citas_3=tk.Label(frame_citas_h, text="Status", font=("Arial", 16), fg=self.color3, bg=self.color4)
            lbl_titulo_citas_3.grid(row=0, column=3, pady=10, padx=5)
            num_citas=1

            for cita in citas_dia:
                lbl_cita_0 = tk.Label(frame_citas_h, text=f"{cita[0]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                lbl_cita_0.grid(row=num_citas, column=0, pady=5, padx=10)

                lbl_cita_1 = tk.Label(frame_citas_h, text=f"{cita[1]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                lbl_cita_1.grid(row=num_citas, column=1, pady=5, padx=10)

                lbl_cita_2 = tk.Label(frame_citas_h, text=f"{cita[2]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                lbl_cita_2.grid(row=num_citas, column=2, pady=5, padx=10)

                lbl_cita_3 = tk.Label(frame_citas_h, text=f"{cita[3]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                lbl_cita_3.grid(row=num_citas, column=3, pady=5, padx=10)

                num_citas += 1
        else:
            lbl_no_citas=tk.Label(frame_citas_h, text="No han habido citas recientes", font=("Arial", 16), fg=self.color3, bg=self.color4)
            lbl_no_citas.pack(pady=10)

    def menuCalendario(self, ventana, sesion):
        #borrar pantalla
        self.borrarPantalla(ventana)

        #variable
        fecha=tk.StringVar()

        #Parte superior
        self.submenu(ventana, sesion)        
        self.grupoTitulo(ventana, sesion, "Calendario", True, 2)

        #calendario
        cal = Calendar(ventana, selectmode="day", year=self.hoy.year, month=self.hoy.month, day=self.hoy.day, bg=self.color2, fg=self.color3, datepattern="yyyy-mm-dd")
        cal.pack(pady=20)

        #texto
        lbl_status=tk.Label(ventana, text="Esta es una función beta y no funciona de normal", font=("Arial", 12), fg=self.color3, bg=self.color2)
        lbl_status.pack(pady=20, anchor="center")

    def menuNotificaciones(self, ventana, sesion):
        #borrar pantalla
        self.borrarPantalla(ventana)

        #Parte superior 
        num=self.grupoTitulo(ventana, sesion, "Notificaciones", False, 0)

        #texto
        lbl_status=tk.Label(ventana, text="No hay notificaciones por lo pronto", font=("Arial", 18), fg=self.color3, bg=self.color2)
        lbl_status.pack(pady=20, anchor="center")

    def menuConfiguraciones(self, ventana, sesion):
        #borrar pantalla
        self.borrarPantalla(ventana)

        #variables
        oscuro=tk.BooleanVar(value=self.tema_oscuro)

        #Parte superior
        num=self.grupoTitulo(ventana, sesion, "Configuraciones", False, 0)

        #definicion
        def cerrarSesion(ventana, sesion):
            status=funciones.Usuarios.borrarCuenta(sesion[0])
            if status:
                ventana.destroy()
                p = multiprocessing.Process(target=iniciarFlet)
                p.start()

        #texto
        switch_modo=tk.Checkbutton(
            ventana,
            text="Modo oscuro",
            font=("Arial", 14),
            fg=self.color3,
            bg=self.color2,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            cursor="hand2",
            variable=oscuro,
            command=lambda:self.cambiarTema(ventana, sesion, oscuro, True)
        )
        switch_modo.pack(pady=20)
        
        #boton
        btn_eliminarcuenta=tk.Button(
            ventana,
                text="Eliminar cuenta",
                font=("Arial", 20, "underline"),
                fg="red",
                bg=self.color2,
                cursor="hand2",
                command=lambda:cerrarSesion(ventana, sesion),
                width=30,
                height=2
            )
        btn_eliminarcuenta.pack(pady=50, side="bottom")

    def menuCitas(self, ventana, sesion):
        self.borrarPantalla(ventana)

        #variables
        buscador=tk.StringVar()
        buscador.set("")

        #Menú de arriba
        self.submenu(ventana, sesion)
        num=self.grupoTitulo(ventana, sesion, "Citas", True, 3)

        #Buscador
        frame_busqueda=tk.Frame(ventana, width=500, height=50, bg=self.color2)
        frame_busqueda.pack(pady=5)

        txt_buscador=tk.Entry(frame_busqueda, textvariable=buscador, width=40)
        txt_buscador.grid(row=0, column=0, padx=2)

        path = os.path.abspath("img/")
        self.button_image_3 = PhotoImage(file=path + "/search.png")
        button_3 = tk.Button(
            frame_busqueda,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda:buscar(sesion[0], buscador.get()),
            relief="flat",
            bg=self.color4
        )
        button_3.grid(row=0, column=1, padx=2)

        #frame de las citas
        frame_lista=tk.Frame(ventana, bg=self.color4, height=600, width=800)
        frame_lista.pack(pady=20)

        path = os.path.abspath("img/")
        #funciones
        def buscar(ide, research):
            for widget in frame_lista.winfo_children():
                widget.destroy()
            data=funciones.Citas.buscarCitas(ide, research)
            if len(data) > 0:
                lbl_titulo_citas_0=tk.Label(frame_lista, text="Cita ID", font=("Arial", 16), fg=self.color3, bg=self.color4)
                lbl_titulo_citas_0.grid(row=0, column=0, pady=10, padx=5)

                lbl_titulo_citas_1=tk.Label(frame_lista, text="Nombre del alumno", font=("Arial", 16), fg=self.color3, bg=self.color4)
                lbl_titulo_citas_1.grid(row=0, column=1, pady=10, padx=5)

                lbl_titulo_citas_2=tk.Label(frame_lista, text="Fecha", font=("Arial", 16), fg=self.color3, bg=self.color4)
                lbl_titulo_citas_2.grid(row=0, column=2, pady=10, padx=5)

                lbl_titulo_citas_3=tk.Label(frame_lista, text="Status", font=("Arial", 16), fg=self.color3, bg=self.color4)
                lbl_titulo_citas_3.grid(row=0, column=3, pady=10, padx=5)

                lbl_titulo_citas_3=tk.Label(frame_lista, text="Opciones", font=("Arial", 16), fg=self.color3, bg=self.color4)
                lbl_titulo_citas_3.grid(row=0, column=4, pady=10, padx=5)
                num_citas=1

                for cita in data:
                    lbl_cita_0 = tk.Label(frame_lista, text=f"{cita[0]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                    lbl_cita_0.grid(row=num_citas, column=0, pady=5, padx=10)

                    lbl_cita_1 = tk.Label(frame_lista, text=f"{cita[1]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                    lbl_cita_1.grid(row=num_citas, column=1, pady=5, padx=10)

                    lbl_cita_2 = tk.Label(frame_lista, text=f"{cita[2]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                    lbl_cita_2.grid(row=num_citas, column=2, pady=5, padx=10)

                    lbl_cita_3 = tk.Label(frame_lista, text=f"{cita[3]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                    lbl_cita_3.grid(row=num_citas, column=3, pady=5, padx=10)

                    img = PhotoImage(file=path + "/cancelar.png")
                    button_3 = tk.Button(
                        frame_lista,
                        image=img,
                        borderwidth=0,
                        highlightthickness=0,
                        command=functools.partial(funciones.Citas.cancelarCitas, cita[0], sesion[0]),
                        relief="flat",
                        bg=self.color4
                    )
                    button_3.image = img
                    button_3.grid(row=num_citas, column=4, padx=10, pady=5)

                    num_citas += 1
            else:
                lbl_no_citas=tk.Label(frame_lista, text="No hay citas registradas en la base de datos", font=("Arial", 16), fg=self.color3, bg=self.color4)
                lbl_no_citas.pack(pady=10)
            
            ventana.update()
        
        buscar(sesion[0], "")

        #Botones
        frame_botones=tk.Frame(ventana, width=1500, height=300, bg=self.color2)
        frame_botones.pack(pady=20)
        
        btn_anadir=tk.Button(
            frame_botones,
            text="Añadir",
            font=("Arial", 20, "underline"),
            fg=self.color3,
            bg=self.color2,
            cursor="hand2",
            command=lambda: funcionalidad.Funcionalidad(ventana, self.tema_oscuro, 2).insertar(ventana, sesion, 1),
        )
        btn_anadir.grid(row=0, column=0, padx=20)

        btn_modificar=tk.Button(
            frame_botones,
            text="Modificar",
            font=("Arial", 20, "underline"),
            fg=self.color3,
            bg=self.color2,
            cursor="hand2",
            command=lambda: funcionalidad.Funcionalidad(ventana, self.tema_oscuro, 2).actualizar(ventana, sesion, 1),
        )
        btn_modificar.grid(row=0, column=1, padx=20)

        btn_eliminar=tk.Button(
            frame_botones,
            text="Eliminar",
            font=("Arial", 20, "underline"),
            fg="red",
            bg=self.color2,
            cursor="hand2",
            command=lambda: funcionalidad.Funcionalidad(ventana, self.tema_oscuro, 2).eliminar(ventana, sesion, 1),
        )
        btn_eliminar.grid(row=0, column=2, padx=20)

        btn_exportar=tk.Button(
            frame_botones,
            text="Exportar",
            font=("Arial", 20, "underline"),
            fg=self.color3,
            bg=self.color2,
            cursor="hand2",
            command=lambda:self.beta(ventana, sesion),
        )
        btn_exportar.grid(row=0, column=3, padx=20)

    def menuEstudiantes(self, ventana, sesion):
        self.borrarPantalla(ventana)

        #variables
        buscador=tk.StringVar()
        buscador.set("")

        #Menú de arriba
        self.submenu(ventana, sesion)
        num=self.grupoTitulo(ventana, sesion, "Estudiantes", True, 4)

        #Buscador
        frame_busqueda=tk.Frame(ventana, width=500, height=50, bg=self.color2)
        frame_busqueda.pack(pady=5)

        txt_buscador=tk.Entry(frame_busqueda, textvariable=buscador, width=40)
        txt_buscador.grid(row=0, column=0, padx=2)

        path = os.path.abspath("img/")
        self.button_image_3 = PhotoImage(file=path + "/search.png")
        button_3 = tk.Button(
            frame_busqueda,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda:buscar(buscador.get()),
            relief="flat",
            bg=self.color4
        )
        button_3.grid(row=0, column=1, padx=2)

        #frame de los estudiantes
        frame_lista=tk.Frame(ventana, bg=self.color4, height=600, width=800)
        frame_lista.pack(pady=20)

        #funciones
        def buscar(research):
            for widget in frame_lista.winfo_children():
                widget.destroy()
            data=funciones.Estudiantes.buscarEstudiantes(research)
            if len(data) > 0:
                lbl_titulo_stu_0=tk.Label(frame_lista, text="Nombre del alumno", font=("Arial", 16), fg=self.color3, bg=self.color4)
                lbl_titulo_stu_0.grid(row=0, column=0, pady=10, padx=5)

                lbl_titulo_stu_1=tk.Label(frame_lista, text="Matrícula", font=("Arial", 16), fg=self.color3, bg=self.color4)
                lbl_titulo_stu_1.grid(row=0, column=1, pady=10, padx=5)

                lbl_titulo_stu_2=tk.Label(frame_lista, text="Grupo", font=("Arial", 16), fg=self.color3, bg=self.color4)
                lbl_titulo_stu_2.grid(row=0, column=2, pady=10, padx=5)

                lbl_titulo_stu_3=tk.Label(frame_lista, text="Correo", font=("Arial", 16), fg=self.color3, bg=self.color4)
                lbl_titulo_stu_3.grid(row=0, column=3, pady=10, padx=5)

                lbl_titulo_stu_4=tk.Label(frame_lista, text="Teléfono", font=("Arial", 16), fg=self.color3, bg=self.color4)
                lbl_titulo_stu_4.grid(row=0, column=4, pady=10, padx=5)

                lbl_titulo_stu_5=tk.Label(frame_lista, text="stu individuales", font=("Arial", 16), fg=self.color3, bg=self.color4)
                lbl_titulo_stu_5.grid(row=0, column=5, pady=10, padx=5)

                lbl_titulo_stu_6=tk.Label(frame_lista, text="Suspensión", font=("Arial", 16), fg=self.color3, bg=self.color4)
                lbl_titulo_stu_6.grid(row=0, column=6, pady=10, padx=5)
                num_stu=1

                for cita in data:
                    lbl_cita_0 = tk.Label(frame_lista, text=f"{cita[0]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                    lbl_cita_0.grid(row=num_stu, column=0, pady=5, padx=10)

                    lbl_cita_1 = tk.Label(frame_lista, text=f"{cita[1]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                    lbl_cita_1.grid(row=num_stu, column=1, pady=5, padx=10)

                    lbl_cita_2 = tk.Label(frame_lista, text=f"{cita[2]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                    lbl_cita_2.grid(row=num_stu, column=2, pady=5, padx=10)

                    lbl_cita_3 = tk.Label(frame_lista, text=f"{cita[3]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                    lbl_cita_3.grid(row=num_stu, column=3, pady=5, padx=10)

                    lbl_cita_4 = tk.Label(frame_lista, text=f"{cita[4]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                    lbl_cita_4.grid(row=num_stu, column=4, pady=5, padx=10)

                    lbl_cita_5 = tk.Label(frame_lista, text=f"{cita[5]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                    lbl_cita_5.grid(row=num_stu, column=5, pady=5, padx=10)

                    lbl_cita_6 = tk.Label(frame_lista, text=f"{cita[6]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                    lbl_cita_6.grid(row=num_stu, column=6, pady=5, padx=10)
                    num_stu += 1
            else:
                lbl_no_stu=tk.Label(frame_lista, text="No hay alumnos registrados en la base de datos", font=("Arial", 16), fg=self.color3, bg=self.color4)
                lbl_no_stu.pack(pady=10)
            
            ventana.update()
        
        buscar("")

        #Botones
        frame_botones=tk.Frame(ventana, width=1500, height=300, bg=self.color2)
        frame_botones.pack(pady=20)
        
        btn_anadir=tk.Button(
            frame_botones,
            text="Añadir",
            font=("Arial", 20, "underline"),
            fg=self.color3,
            bg=self.color2,
            cursor="hand2",
            command=lambda: funcionalidad.Funcionalidad(ventana, self.tema_oscuro, 3).insertar(ventana, sesion, 2),
        )
        btn_anadir.grid(row=0, column=0, padx=20)
        
        btn_modificar=tk.Button(
            frame_botones,
            text="Modificar",
            font=("Arial", 20, "underline"),
            fg=self.color3,
            bg=self.color2,
            cursor="hand2",
            command=lambda: funcionalidad.Funcionalidad(ventana, self.tema_oscuro, 3).actualizar(ventana, sesion, 2),
        )
        btn_modificar.grid(row=0, column=1, padx=20)

        btn_consult=tk.Button(
            frame_botones,
            text="Consultar",
            font=("Arial", 20, "underline"),
            fg=self.color3,
            bg=self.color2,
            cursor="hand2",
            command=lambda:self.beta(ventana, sesion),
        )
        btn_consult.grid(row=0, column=3, padx=20)

        btn_eliminar=tk.Button(
            frame_botones,
            text="Eliminar",
            font=("Arial", 20, "underline"),
            fg="red",
            bg=self.color2,
            cursor="hand2",
            command=lambda: funcionalidad.Funcionalidad(ventana, self.tema_oscuro, 3).eliminar(ventana, sesion, 2),
        )
        btn_eliminar.grid(row=0, column=4, padx=20)

    def menuTutores(self, ventana, sesion):
        self.borrarPantalla(ventana)

        #variables
        buscador=tk.StringVar()
        buscador.set("")

        #Menú de arriba
        self.submenu(ventana, sesion)
        num=self.grupoTitulo(ventana, sesion, "Tutores", True, 5)

        #Buscador
        frame_busqueda=tk.Frame(ventana, width=500, height=50, bg=self.color2)
        frame_busqueda.pack(pady=5)

        txt_buscador=tk.Entry(frame_busqueda, textvariable=buscador, width=40)
        txt_buscador.grid(row=0, column=0, padx=2)

        path = os.path.abspath("img/")
        self.button_image_3 = PhotoImage(file=path + "/search.png")
        button_3 = tk.Button(
            frame_busqueda,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda:buscar(sesion[0], buscador.get()),
            relief="flat",
            bg=self.color4
        )
        button_3.grid(row=0, column=1, padx=2)

        #frame de los tutores
        frame_lista=tk.Frame(ventana, bg=self.color4, height=600, width=800)
        frame_lista.pack(pady=20)

        #funciones
        def buscar(research):
            for widget in frame_lista.winfo_children():
                widget.destroy()
            data=funciones.Tutor.buscarTutores(research)
            if len(data) > 0:
                lbl_titulo_tutor_0=tk.Label(frame_lista, text="Nombre del tutor", font=("Arial", 16), fg=self.color3, bg=self.color4)
                lbl_titulo_tutor_0.grid(row=0, column=0, pady=10, padx=5)

                lbl_titulo_tutor_1=tk.Label(frame_lista, text="Grupo a cargo", font=("Arial", 16), fg=self.color3, bg=self.color4)
                lbl_titulo_tutor_1.grid(row=0, column=1, pady=10, padx=5)

                lbl_titulo_tutor_2=tk.Label(frame_lista, text="Correo", font=("Arial", 16), fg=self.color3, bg=self.color4)
                lbl_titulo_tutor_2.grid(row=0, column=2, pady=10, padx=5)

                lbl_titulo_tutor_3=tk.Label(frame_lista, text="Teléfono", font=("Arial", 16), fg=self.color3, bg=self.color4)
                lbl_titulo_tutor_3.grid(row=0, column=3, pady=10, padx=5)
                num_tutor=1

                for cita in data:
                    lbl_cita_0 = tk.Label(frame_lista, text=f"{cita[0]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                    lbl_cita_0.grid(row=num_tutor, column=0, pady=5, padx=10)

                    lbl_cita_1 = tk.Label(frame_lista, text=f"{cita[1]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                    lbl_cita_1.grid(row=num_tutor, column=1, pady=5, padx=10)

                    lbl_cita_2 = tk.Label(frame_lista, text=f"{cita[2]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                    lbl_cita_2.grid(row=num_tutor, column=2, pady=5, padx=10)

                    lbl_cita_3 = tk.Label(frame_lista, text=f"{cita[3]}", font=("Arial", 12), fg=self.color3, bg=self.color4)
                    lbl_cita_3.grid(row=num_tutor, column=3, pady=5, padx=10)

                    num_tutor += 1
            else:
                lbl_no_tutor=tk.Label(frame_lista, text="No hay tutores registrados en la base de datos", font=("Arial", 16), fg=self.color3, bg=self.color4)
                lbl_no_tutor.pack(pady=10)
            
            ventana.update()
        
        buscar("")

        #Botones
        frame_botones=tk.Frame(ventana, width=1500, height=300, bg=self.color2)
        frame_botones.pack(pady=20)
        
        btn_anadir=tk.Button(
            frame_botones,
            text="Añadir",
            font=("Arial", 20, "underline"),
            fg=self.color3,
            bg=self.color2,
            cursor="hand2",
            command=lambda: funcionalidad.Funcionalidad(ventana, self.tema_oscuro, 4).insertar(ventana, sesion, 3),
        )
        btn_anadir.grid(row=0, column=0, padx=20)

        btn_modificar=tk.Button(
            frame_botones,
            text="Modificar",
            font=("Arial", 20, "underline"),
            fg=self.color3,
            bg=self.color2,
            cursor="hand2",
            command=lambda: funcionalidad.Funcionalidad(ventana, self.tema_oscuro, 4).actualizar(ventana, sesion, 3),
        )
        btn_modificar.grid(row=0, column=1, padx=20)

        btn_consult=tk.Button(
            frame_botones,
            text="Consultar",
            font=("Arial", 20, "underline"),
            fg=self.color3,
            bg=self.color2,
            cursor="hand2",
            command=lambda:self.beta(ventana, sesion),
        )
        btn_consult.grid(row=0, column=2, padx=20)

        btn_eliminar=tk.Button(
            frame_botones,
            text="Eliminar",
            font=("Arial", 20, "underline"),
            fg="red",
            bg=self.color2,
            cursor="hand2",
            command=lambda: funcionalidad.Funcionalidad(ventana, self.tema_oscuro, 4).eliminar(ventana, sesion, 3),
        )
        btn_eliminar.grid(row=0, column=3, padx=20)

    def acercaDe(self, ventana, sesion):
        self.borrarPantalla(ventana)

        #Parte superior
        num=self.grupoTitulo(ventana, sesion, "Acerca de", False, 6)

        #Texto
        lbl_info=tk.Label(ventana, text="Aquí en el departamento de psicopedagogía nos comprometemos a brindar la atención psicológica necesaria a los estudiantes de este plantel. \n\n -Contacto: \n -Whatsapp: 618 269 99 97 \n -Correo: fernando.vargas@utd.edu.mx", wraplength=600, font=("Arial", 18))
        lbl_info.pack(pady=30)

        path = os.path.abspath("img/")
        self.img_logo = tk.PhotoImage(file=path + "/Logo_utd.png")   # PNG o GIF
        label = tk.Label(ventana, image=self.img_logo)
        label.image = self.img_logo
        label.pack(pady=30)

        lbl_upd=tk.Label(ventana, text="V0.5.2")
        lbl_upd.pack(pady=15)

    def beta(self, ventana, sesion):
        self.borrarPantalla(ventana)
        self.submenu(ventana, sesion)
        tl=self.grupoTitulo(ventana, sesion, "Aviso del beta", False, 0)
        
        lbl_beta=tk.Label(ventana, text="Esta función no se encuentra disponible por lo pronto")
        lbl_beta.pack(pady=30)
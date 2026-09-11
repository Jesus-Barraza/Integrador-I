import tkinter as tk
from tkinter import PhotoImage, messagebox
from tkcalendar import Calendar
from controller import funciones
import os
from . import submenu, borrador
import flet as ft
import multiprocessing
from datetime import datetime

class Funcionalidad():
    def __init__(self, ventana, status, num):
        if not status:
            self.color1 = "#5E95D4"
            self.color2 = "#E2E2E2"
            self.color3 = "#000000"
            self.color4 = "#ffffff"
            self.color5 = "#B7B22F"
        else:
            self.color1 = "#353e70"
            self.color2 = "#353535"
            self.color3 = "#d6d6d6"
            self.color4 = "#323232"
            self.color5 = "#836819"
        self.tema_oscuro=status
        self.hoy=datetime.now()
        self.num=num
        ventana.config(bg=self.color2)

    @staticmethod
    def cancelar():
        mensaje=messagebox.showinfo(title="Operación cancelada", message="Se canceló la operación con éxito")

    @staticmethod
    def borrarPantalla(ventana):
        for widget in ventana.winfo_children():
            widget.destroy()

    @staticmethod
    def limit_float(p):
        allowed = "0123456789."
        if all(ch in allowed for ch in p) and p.count(".") <= 1:
            return True
        else:
            return False

    @staticmethod
    def limit_int(p):
        if p.isdigit():
            return True
        else:
            return False

    @staticmethod
    def limit_mail(p):
        allowed = "0123456789.abcdefghijklmnopqrstuvwxyz@_"
        if all(ch in allowed for ch in p) and p.count("@") <= 1:
            return True
        else:
            return False
    
    def grupoTitulo(self, ventana, sesion, texto):
        #funcion
        def retorno(num):
            if num==1:
                button_1.config(command=lambda:borrador.Menu(ventana, sesion, self.tema_oscuro).menuPrincipal(ventana, sesion))
            elif num==2:
                button_1.config(command=lambda:borrador.Menu(ventana, sesion, self.tema_oscuro).menuCitas(ventana, sesion))
            elif num==3:
                button_1.config(command=lambda:borrador.Menu(ventana, sesion, self.tema_oscuro).menuEstudiantes(ventana, sesion))
            elif num==4:
                button_1.config(command=lambda:borrador.Menu(ventana, sesion, self.tema_oscuro).menuTutores(ventana, sesion))

        # Frame superior
        frame_superior = tk.Frame(ventana, bg=self.color1, height=200, highlightbackground=self.color5, highlightthickness=3)
        frame_superior.pack(fill="x", side="top")

        # Frame contenedor horizontal
        frame_horizontal = tk.Frame(frame_superior, bg=self.color1)
        frame_horizontal.pack(fill="x", padx=10, pady=10)

        frame_horizontal.columnconfigure(0, weight=1)  # espacio a la izquierda
        frame_horizontal.columnconfigure(1, weight=0)  # título centrado
        frame_horizontal.columnconfigure(2, weight=1)

        # Frame del título (izquierda)
        if self.num==4 or self.num==3:
            frame_titulo = tk.Frame(frame_horizontal, bg=self.color5, height=30, width=600)
            lbl_titulo = tk.Label(frame_titulo, text=texto, font=("Arial", 24), fg=self.color3, bg=self.color5)
        else:
            frame_titulo = tk.Frame(frame_horizontal, bg=self.color2, height=30, width=400)
            lbl_titulo = tk.Label(frame_titulo, text=texto, font=("Arial", 24), fg=self.color3, bg=self.color2)
        frame_titulo.grid(row=0, column=1, padx=10)
        lbl_titulo.pack(anchor="center")

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

    def insertar(self, ventana, sesion, ori):
        self.borrarPantalla(ventana)

        #limitantes
        verificacion_entero=(ventana.register(self.limit_int), "%P")
        verificacion_mail=(ventana.register(self.limit_mail), "%P")

        if ori==1:
            tl=self.grupoTitulo(ventana, sesion, "Insertar citas", )

            #variables
            full_estud=[]
            estud=tk.StringVar()
            matr=tk.StringVar()
            calendar=tk.StringVar()
            
            #funciones
            def estudiante(id_psi, ventana, var):
                try:
                    full_estud=[]
                    dato=submenu.SubMenu.subAlumnos(ventana, id_psi)
                    var.append(dato)
                    matr.set(dato[1])
                    estud.set(dato[0])
                except:
                    self.cancelar()

            def fecha(ventana):
                try:
                    dato=submenu.SubMenu.subCalendario(ventana)
                    calendar.set(dato)
                except:
                    self.cancelar()

            def insertar(name_stu, date, matricul, full):
                if len(full)==0:
                    full=[(0,0)]
                if full[0][0]!=name_stu and full[0][1]!=matricul:
                    full=funciones.Estudiantes.comprobarEstudiantes(name_stu)
                    if len(full) != 1:
                        full=funciones.Estudiantes.comprobarEstudiantes(matricul)
                        if len(full) != 1:
                            lbl_aviso.config(text="Matrícula o nombre incorrecto, inténtelo de nuevo")
                            confirm=False
                        else:
                            confirm=True
                            name_stu=full[0][0]
                            matricul=full[0][1]
                    else:
                        confirm=True
                        name_stu=full[0][0]
                        matricul=full[0][1]
                else:
                    confirm=True
                if confirm:
                    entrada=funciones.Citas.agregarCita(sesion[0], name_stu, date, matricul, full)
                    if entrada:
                        borrador.Menu(ventana, sesion, self.tema_oscuro).menuCitas(ventana, sesion)
                    else:
                        lbl_aviso.config(text="Hubo un error a la hora de agregar la cita, inténtelo más tarde")
                

            #Cuadros de texto
            frame_cuadro=tk.Frame(ventana, width=1000, height=700, bg=self.color2)
            frame_cuadro.pack(pady=10)

            #Datos del estudiante
            lbl_matr=tk.Label(frame_cuadro, text="Matrícula: ", justify="left", bg=self.color2)
            lbl_matr.grid(row=0, column=0, pady=5)

            txt_matr=tk.Entry(frame_cuadro, textvariable=matr)
            txt_matr.grid(row=1, column=0, pady=[0,15])

            lbl_except=tk.Label(frame_cuadro, text="ó", justify="left", bg=self.color2)
            lbl_except.grid(row=2, column=0, pady=5)

            path = os.path.abspath("img/")
            self.button_image_3 = PhotoImage(file=path + "/sumar.png")
            button_3 = tk.Button(
                frame_cuadro,
                image=self.button_image_3,
                borderwidth=0,
                highlightthickness=0,
                command=lambda:estudiante(sesion[0], ventana, full_estud),
                relief="flat",
                bg=self.color4
            )
            button_3.grid(row=2, column=1, padx=2)

            lbl_estud=tk.Label(frame_cuadro, text="Nombre del estudiante: ", justify="left", bg=self.color2)
            lbl_estud.grid(row=3, column=0, pady=5)

            txt_estud=tk.Entry(frame_cuadro, textvariable=estud)
            txt_estud.grid(row=4, column=0, pady=[0,15])

            #Calendario
            lbl_modelo=tk.Label(frame_cuadro, text="Fecha: ", justify="left", bg=self.color2)
            lbl_modelo.grid(row=5, column=0, pady=5)

            txt_modelo=tk.Entry(frame_cuadro, textvariable=calendar)
            txt_modelo.grid(row=6, column=0, pady=[0,15])

            path = os.path.abspath("img/")
            self.button_image_4 = PhotoImage(file=path + "/sumar.png")
            button_4 = tk.Button(
                frame_cuadro,
                image=self.button_image_4,
                borderwidth=0,
                highlightthickness=0,
                command=lambda:fecha(ventana),
                relief="flat",
                bg=self.color4
            )
            button_4.grid(row=6, column=1, padx=2)

            #Texto
            lbl_aviso=tk.Label(ventana, fg="red", bg=self.color2)
            lbl_aviso.pack(pady=15)

            #Botones
            frame_botones=tk.Frame(ventana, width=1500, height=300, bg=self.color2)
            frame_botones.pack(pady=20)
            
            btn_anadir=tk.Button(
                frame_botones,
                text="Insertar",
                font=("Arial", 20, "underline"),
                fg=self.color3,
                bg=self.color2,
                cursor="hand2",
                command=lambda:insertar(estud.get(), calendar.get(), matr.get(), full_estud),
            )
            btn_anadir.grid(row=0, column=0, padx=20)

            btn_salir=tk.Button(
                frame_botones,
                text="Regresar",
                font=("Arial", 20, "underline"),
                fg=self.color3,
                bg=self.color2,
                cursor="hand2",
                command=lambda:borrador.Menu(ventana, sesion, self.tema_oscuro).menuCitas(ventana, sesion),
            )
            btn_salir.grid(row=0, column=1, padx=20)
        elif ori==2:
            tl=self.grupoTitulo(ventana, sesion, "Insertar estudiantes")

            #variables
            nombre=tk.StringVar()
            grupo=tk.StringVar()
            matricula=tk.StringVar()
            correo=tk.StringVar()
            telef=tk.StringVar()
            
            #funciones
            def grupos(ventana, id_psi):
                try:
                    dato=submenu.SubMenu.subGrupos(ventana, id_psi)
                    grupo.set(dato[0])
                except:
                    self.cancelar()

            def insertar(matricula, id_grp, nombre, corr, tel):
                entrada=funciones.Estudiantes.agregarEstudiante(matricula, id_grp, nombre, corr, tel)
                if entrada:
                    borrador.Menu(ventana, sesion, self.tema_oscuro).menuEstudiantes(ventana, sesion)

            #Cuadros de texto
            frame_cuadro=tk.Frame(ventana, width=1000, height=700, bg=self.color2)
            frame_cuadro.pack(pady=10)

            #Nombre del estudiante
            lbl_estud=tk.Label(frame_cuadro, text="Nombre del estudiante: ", justify="left", bg=self.color2)
            lbl_estud.grid(row=0, column=0, pady=5)

            txt_estud=tk.Entry(frame_cuadro, textvariable=nombre)
            txt_estud.grid(row=1, column=0, pady=[0,15])

            #Grupo
            lbl_grupo=tk.Label(frame_cuadro, text="Grupo: ", justify="left", bg=self.color2)
            lbl_grupo.grid(row=2, column=0, pady=5)

            txt_grupo=tk.Entry(frame_cuadro, textvariable=grupo)
            txt_grupo.grid(row=3, column=0, pady=[0,15])

            path = os.path.abspath("img/")
            self.button_image_3 = PhotoImage(file=path + "/sumar.png")
            button_3 = tk.Button(
                frame_cuadro,
                image=self.button_image_3,
                borderwidth=0,
                highlightthickness=0,
                command=lambda:grupos(ventana, sesion[0]),
                relief="flat",
                bg=self.color4
            )
            button_3.grid(row=3, column=1, padx=2)

            #matricula
            lbl_matri=tk.Label(frame_cuadro, text="Matricula: ", justify="left", bg=self.color2)
            lbl_matri.grid(row=4, column=0, pady=5)

            txt_matri=tk.Entry(frame_cuadro, textvariable=matricula, validate="key", validatecommand=verificacion_entero)
            txt_matri.grid(row=5, column=0, pady=[0,15])

            #correo
            lbl_correo=tk.Label(frame_cuadro, text="Correo electrónico: ", justify="left", bg=self.color2)
            lbl_correo.grid(row=6, column=0, pady=5)

            txt_correo=tk.Entry(frame_cuadro, textvariable=correo, validate="key", validatecommand=verificacion_mail)
            txt_correo.grid(row=7, column=0, pady=[0,15])

            #telefono
            lbl_correo=tk.Label(frame_cuadro, text="Teléfono: ", justify="left", bg=self.color2)
            lbl_correo.grid(row=8, column=0, pady=5)

            txt_correo=tk.Entry(frame_cuadro, textvariable=telef, validate="key", validatecommand=verificacion_entero)
            txt_correo.grid(row=9, column=0, pady=[0,15])

            #Botones
            frame_botones=tk.Frame(ventana, width=1500, height=300, bg=self.color2)
            frame_botones.pack(pady=20)
            
            btn_anadir=tk.Button(
                frame_botones,
                text="Insertar",
                font=("Arial", 20, "underline"),
                fg=self.color3,
                bg=self.color2,
                cursor="hand2",
                command=lambda:insertar(matricula.get(), grupo.get(), nombre.get(), correo.get(), telef.get()),
            )
            btn_anadir.grid(row=0, column=0, padx=20)

            btn_salir=tk.Button(
                frame_botones,
                text="Regresar",
                font=("Arial", 20, "underline"),
                fg=self.color3,
                bg=self.color2,
                cursor="hand2",
                command=lambda:borrador.Menu(ventana, sesion, self.tema_oscuro).menuEstudiantes(ventana, sesion),
            )
            btn_salir.grid(row=0, column=1, padx=20)
        elif ori==3:
            tl=self.grupoTitulo(ventana, sesion, "Insertar tutores")

            #variables
            nombre=tk.StringVar()
            grupo=tk.StringVar()
            correo=tk.StringVar()
            telef=tk.StringVar()
            
            #funciones
            def grupos(ventana, id_psi):
                try:
                    dato=submenu.SubMenu.subGrupos(ventana, id_psi)
                    grupo.set(dato[0])
                except:
                    self.cancelar()

            def insertar(id_grp, nombre, corr, tel):
                entrada=funciones.Tutor.agregarTutor(id_grp, nombre, corr, tel)
                if entrada:
                    borrador.Menu(ventana, sesion, self.tema_oscuro).menuTutores(ventana, sesion)

            #Cuadros de texto
            frame_cuadro=tk.Frame(ventana, width=1000, height=700, bg=self.color2)
            frame_cuadro.pack(pady=10)

            #Nombre del estudiante
            lbl_estud=tk.Label(frame_cuadro, text="Nombre del tutor: ", justify="left", bg=self.color2)
            lbl_estud.grid(row=0, column=0, pady=5)

            txt_estud=tk.Entry(frame_cuadro, textvariable=nombre)
            txt_estud.grid(row=1, column=0, pady=[0,15])

            #Grupo
            lbl_grupo=tk.Label(frame_cuadro, text="Grupo: ", justify="left", bg=self.color2)
            lbl_grupo.grid(row=2, column=0, pady=5)

            txt_grupo=tk.Entry(frame_cuadro, textvariable=grupo)
            txt_grupo.grid(row=3, column=0, pady=[0,15])

            path = os.path.abspath("img/")
            self.button_image_3 = PhotoImage(file=path + "/sumar.png")
            button_3 = tk.Button(
                frame_cuadro,
                image=self.button_image_3,
                borderwidth=0,
                highlightthickness=0,
                command=lambda:grupos(ventana, sesion[0]),
                relief="flat",
                bg=self.color4
            )
            button_3.grid(row=3, column=1, padx=2)

            #correo
            lbl_correo=tk.Label(frame_cuadro, text="Correo electrónico: ", justify="left", bg=self.color2)
            lbl_correo.grid(row=4, column=0, pady=5)

            txt_correo=tk.Entry(frame_cuadro, textvariable=correo, validate="key", validatecommand=verificacion_mail)
            txt_correo.grid(row=5, column=0, pady=[0,15])

            #telefono
            lbl_correo=tk.Label(frame_cuadro, text="Teléfono: ", justify="left", bg=self.color2)
            lbl_correo.grid(row=6, column=0, pady=5)

            txt_correo=tk.Entry(frame_cuadro, textvariable=telef, validate="key", validatecommand=verificacion_entero)
            txt_correo.grid(row=7, column=0, pady=[0,15])

            #Botones
            frame_botones=tk.Frame(ventana, width=1500, height=300, bg=self.color2)
            frame_botones.pack(pady=20)
            
            btn_anadir=tk.Button(
                frame_botones,
                text="Insertar",
                font=("Arial", 20, "underline"),
                fg=self.color3,
                bg=self.color2,
                cursor="hand2",
                command=lambda:insertar(grupo.get(), nombre.get(), correo.get(), telef.get()),
            )
            btn_anadir.grid(row=0, column=0, padx=20)

            btn_salir=tk.Button(
                frame_botones,
                text="Regresar",
                font=("Arial", 20, "underline"),
                fg=self.color3,
                bg=self.color2,
                cursor="hand2",
                command=lambda:borrador.Menu(ventana, sesion, self.tema_oscuro).menuTutores(ventana, sesion),
            )
            btn_salir.grid(row=0, column=2, padx=20)
        
    def actualizar(self, ventana, sesion, ori):
        self.borrarPantalla(ventana)
        #limitantes
        verificacion_entero=(ventana.register(self.limit_int), "%P")
        verificacion_mail=(ventana.register(self.limit_mail), "%P")

        if ori==1:
            tl=self.grupoTitulo(ventana, sesion, "Actualizar citas")

            #variables
            var=[]
            cit=tk.StringVar()
            matri=tk.StringVar()
            estud=tk.StringVar()
            calendar=tk.StringVar()
            
            #funciones
            def cita(id_psi, ventana):
                try:
                    datos=submenu.SubMenu.subCitas(ventana, id_psi)
                    cit.set(datos[0])
                    estud.set(datos[1])
                    calendar.set(datos[2])
                    dato=funciones.Estudiantes.buscarEstudiantes(estud.get())
                    matri.set(dato[0][1])
                except:
                    self.cancelar()

            def estudiante(id_psi, ventana):
                try:
                    dato=submenu.SubMenu.subAlumnos(ventana, id_psi)
                    var.append(dato)
                    matri.set(dato[1])
                    estud.set(dato[0])
                except:
                    self.cancelar()

            def fecha(ventana):
                try:
                    dato=submenu.SubMenu.subCalendario(ventana)
                    calendar.set(dato)
                except:
                    self.cancelar()

            def actualizar(name_stu, matricul, date, id_psicologo, citar):
                entrada=funciones.Citas.modificarCita(name_stu, matricul, date, id_psicologo, citar)
                if entrada:
                    borrador.Menu(ventana, sesion, self.tema_oscuro).menuCitas(ventana, sesion)

            #Cuadros de texto
            frame_cuadro=tk.Frame(ventana, width=1000, height=700, bg=self.color2)
            frame_cuadro.pack(pady=10)

            #Cita a modificar
            lbl_cit=tk.Label(frame_cuadro, text="Cita a modificar: ", justify="left", bg=self.color2)
            lbl_cit.grid(row=0, column=0, pady=5)

            txt_cit=tk.Entry(frame_cuadro, textvariable=cit)
            txt_cit.grid(row=1, column=0, pady=[0,15])

            path = os.path.abspath("img/")
            self.button_image_5 = PhotoImage(file=path + "/sumar.png")
            button_5 = tk.Button(
                frame_cuadro,
                image=self.button_image_5,
                borderwidth=0,
                highlightthickness=0,
                command=lambda:cita(sesion[0], ventana),
                relief="flat",
                bg=self.color4
            )
            button_5.grid(row=1, column=1, padx=2)

            #Nombre del estudiante o matrícula
            lbl_estud=tk.Label(frame_cuadro, text="Nombre del estudiante: ", justify="left", bg=self.color2)
            lbl_estud.grid(row=2, column=0, pady=5)

            txt_estud=tk.Entry(frame_cuadro, textvariable=estud)
            txt_estud.grid(row=3, column=0, pady=[0,15])

            lbl_except=tk.Label(frame_cuadro, text="ó", bg=self.color2)
            lbl_except.grid(row=4, column=0, pady=10)

            path = os.path.abspath("img/")
            self.button_image_3 = PhotoImage(file=path + "/sumar.png")
            button_3 = tk.Button(
                frame_cuadro,
                image=self.button_image_3,
                borderwidth=0,
                highlightthickness=0,
                command=lambda:estudiante(sesion[0], ventana),
                relief="flat",
                bg=self.color4
            )
            button_3.grid(row=4, column=1, padx=2)

            lbl_matri=tk.Label(frame_cuadro, text="Matrícula: ", justify="left", bg=self.color2)
            lbl_matri.grid(row=5, column=0, pady=5)

            txt_matri=tk.Entry(frame_cuadro, textvariable=matri)
            txt_matri.grid(row=6, column=0, pady=[0,15])

            #Calendario
            lbl_modelo=tk.Label(frame_cuadro, text="Fecha: ", justify="left", bg=self.color2)
            lbl_modelo.grid(row=7, column=0, pady=5)

            txt_modelo=tk.Entry(frame_cuadro, textvariable=calendar)
            txt_modelo.grid(row=8, column=0, pady=[0,15])

            path = os.path.abspath("img/")
            self.button_image_4 = PhotoImage(file=path + "/sumar.png")
            button_4 = tk.Button(
                frame_cuadro,
                image=self.button_image_4,
                borderwidth=0,
                highlightthickness=0,
                command=lambda:fecha(ventana),
                relief="flat",
                bg=self.color4
            )
            button_4.grid(row=8, column=1, padx=2)

            #Textos 
            lbl_error=tk.Label(ventana, fg="red", bg=self.color2)
            lbl_error.pack(pady=15)

            #Botones
            frame_botones=tk.Frame(ventana, width=1500, height=300, bg=self.color2)
            frame_botones.pack(pady=20)
            
            btn_anadir=tk.Button(
                frame_botones,
                text="Actualizar",
                font=("Arial", 20, "underline"),
                fg=self.color3,
                bg=self.color2,
                cursor="hand2",
                command=lambda:actualizar(estud.get(), matri.get(), calendar.get(), sesion[0], cit.get()),
            )
            btn_anadir.grid(row=0, column=0, padx=20)

            btn_salir=tk.Button(
                frame_botones,
                text="Regresar",
                font=("Arial", 20, "underline"),
                fg=self.color3,
                bg=self.color2,
                cursor="hand2",
                command=lambda:borrador.Menu(ventana, sesion, self.tema_oscuro).menuCitas(ventana, sesion),
            )
            btn_salir.grid(row=0, column=1, padx=20)
        elif ori==2:
            tl=self.grupoTitulo(ventana, sesion, "Actualizar estudiantes")

            #variables
            nombre=tk.StringVar()
            grupo=tk.StringVar()
            matricula=tk.StringVar()
            correo=tk.StringVar()
            telef=tk.StringVar()
            
            #funciones
            def estudiante(id_psi, ventana):
                try:
                    datos=submenu.SubMenu.subAlumnos(ventana, id_psi)
                    nombre.set(datos[0])
                    grupo.set(datos[7])
                    matricula.set(datos[1])
                    correo.set(datos[3])
                    telef.set(datos[4])
                except:
                    self.cancelar()

            def grupos(ventana, id_psi):
                try:
                    dato=submenu.SubMenu.subGrupos(ventana, id_psi)
                    grupo.set(dato[0])
                except:
                    self.cancelar()

            def actualizar(matricula, id_grp, nombre, corr, tel):
                entrada=funciones.Estudiantes.actualizarEstudiante(matricula, id_grp, nombre, corr, tel)
                if entrada:
                    borrador.Menu(ventana, sesion, self.tema_oscuro).menuEstudiantes(ventana, sesion)

            #Cuadros de texto
            frame_cuadro=tk.Frame(ventana, width=1000, height=700, bg=self.color2)
            frame_cuadro.pack(pady=10)

            #Nombre del estudiante
            lbl_estud=tk.Label(frame_cuadro, text="Nombre del estudiante: ", justify="left", bg=self.color2)
            lbl_estud.grid(row=0, column=0, pady=5)

            txt_estud=tk.Entry(frame_cuadro, textvariable=nombre)
            txt_estud.grid(row=1, column=0, pady=[0,15])

            path = os.path.abspath("img/")
            self.button_image_4 = PhotoImage(file=path + "/sumar.png")
            button_4 = tk.Button(
                frame_cuadro,
                image=self.button_image_4,
                borderwidth=0,
                highlightthickness=0,
                command=lambda:estudiante(sesion[0], ventana),
                relief="flat",
                bg=self.color4
            )
            button_4.grid(row=1, column=1, padx=2)

            #Grupo
            lbl_grupo=tk.Label(frame_cuadro, text="Grupo: ", justify="left", bg=self.color2)
            lbl_grupo.grid(row=2, column=0, pady=5)

            txt_grupo=tk.Entry(frame_cuadro, textvariable=grupo)
            txt_grupo.grid(row=3, column=0, pady=[0,15])

            path = os.path.abspath("img/")
            self.button_image_3 = PhotoImage(file=path + "/sumar.png")
            button_3 = tk.Button(
                frame_cuadro,
                image=self.button_image_3,
                borderwidth=0,
                highlightthickness=0,
                command=lambda:grupos(ventana, sesion[0]),
                relief="flat",
                bg=self.color4
            )
            button_3.grid(row=3, column=1, padx=2)

            #matricula
            lbl_matri=tk.Label(frame_cuadro, text="Matricula: ", justify="left", bg=self.color2)
            lbl_matri.grid(row=4, column=0, pady=5)

            txt_matri=tk.Entry(frame_cuadro, textvariable=matricula, validate="key", validatecommand=verificacion_entero)
            txt_matri.grid(row=5, column=0, pady=[0,15])

            #correo
            lbl_correo=tk.Label(frame_cuadro, text="Correo electrónico: ", justify="left", bg=self.color2)
            lbl_correo.grid(row=6, column=0, pady=5)

            txt_correo=tk.Entry(frame_cuadro, textvariable=correo, validate="key", validatecommand=verificacion_mail)
            txt_correo.grid(row=7, column=0, pady=[0,15])

            #telefono
            lbl_correo=tk.Label(frame_cuadro, text="Teléfono: ", justify="left", bg=self.color2)
            lbl_correo.grid(row=8, column=0, pady=5)

            txt_correo=tk.Entry(frame_cuadro, textvariable=telef, validate="key", validatecommand=verificacion_entero)
            txt_correo.grid(row=9, column=0, pady=[0,15])

            #Botones
            frame_botones=tk.Frame(ventana, width=1500, height=300, bg=self.color2)
            frame_botones.pack(pady=20)
            
            btn_anadir=tk.Button(
                frame_botones,
                text="Actualizar",
                font=("Arial", 20, "underline"),
                fg=self.color3,
                bg=self.color2,
                cursor="hand2",
                command=lambda:actualizar(matricula.get(), grupo.get(), nombre.get(), correo.get(), telef.get()),
            )
            btn_anadir.grid(row=0, column=0, padx=20)

            btn_salir=tk.Button(
                frame_botones,
                text="Regresar",
                font=("Arial", 20, "underline"),
                fg=self.color3,
                bg=self.color2,
                cursor="hand2",
                command=lambda:borrador.Menu(ventana, sesion, self.tema_oscuro).menuEstudiantes(ventana, sesion),
            )
            btn_salir.grid(row=0, column=1, padx=20)
        elif ori==3:
            tl=self.grupoTitulo(ventana, sesion, "Actualizar tutores")

            #variables
            ide=tk.StringVar()
            nombre=tk.StringVar()
            grupo=tk.StringVar()
            correo=tk.StringVar()
            telef=tk.StringVar()
            
            #funciones
            def tutorado(id_psi, ventana):
                try:
                    datos=submenu.SubMenu.subTutores(ventana, id_psi)
                    nombre.set(datos[0])
                    grupo.set(datos[4])
                    correo.set(datos[2])
                    telef.set(datos[3])
                except:
                    self.cancelar()

            def grupos(ventana, id_psi):
                try:
                    dato=submenu.SubMenu.subGrupos(ventana, id_psi)
                    grupo.set(dato[0])
                except:
                    self.cancelar()

            def insertar(id_grp, nombre, corr, tel):
                entrada=funciones.Tutor.actualizarTutor(nombre, id_grp, corr, tel)
                if entrada:
                    borrador.Menu(ventana, sesion, self.tema_oscuro).menuTutores(ventana, sesion)

            #Cuadros de texto
            frame_cuadro=tk.Frame(ventana, width=1000, height=700, bg=self.color2)
            frame_cuadro.pack(pady=10)

            #asignar a todos por nombre
            path = os.path.abspath("img/")
            self.button_image_4 = PhotoImage(file=path + "/sumar.png")
            button_4 = tk.Button(
                frame_cuadro,
                image=self.button_image_4,
                borderwidth=0,
                highlightthickness=0,
                command=lambda:tutorado(sesion[0], ventana),
                relief="flat",
                bg=self.color4
            )
            button_4.grid(row=0, column=0, padx=2)

            #Grupo
            lbl_grupo=tk.Label(frame_cuadro, text="Grupo: ", justify="left", bg=self.color2)
            lbl_grupo.grid(row=1, column=0, pady=5)

            txt_grupo=tk.Entry(frame_cuadro, textvariable=grupo)
            txt_grupo.grid(row=2, column=0, pady=[0,15])

            path = os.path.abspath("img/")
            self.button_image_3 = PhotoImage(file=path + "/sumar.png")
            button_3 = tk.Button(
                frame_cuadro,
                image=self.button_image_3,
                borderwidth=0,
                highlightthickness=0,
                command=lambda:grupos(ventana, sesion[0]),
                relief="flat",
                bg=self.color4
            )
            button_3.grid(row=2, column=1, padx=2)

            #correo
            lbl_correo=tk.Label(frame_cuadro, text="Correo electrónico: ", justify="left", bg=self.color2)
            lbl_correo.grid(row=3, column=0, pady=5)

            txt_correo=tk.Entry(frame_cuadro, textvariable=correo, validate="key", validatecommand=verificacion_mail)
            txt_correo.grid(row=4, column=0, pady=[0,15])

            #telefono
            lbl_correo=tk.Label(frame_cuadro, text="Teléfono: ", justify="left", bg=self.color2)
            lbl_correo.grid(row=5, column=0, pady=5)

            txt_correo=tk.Entry(frame_cuadro, textvariable=telef, validate="key", validatecommand=verificacion_entero)
            txt_correo.grid(row=6, column=0, pady=[0,15])

            #Botones
            frame_botones=tk.Frame(ventana, width=1500, height=300, bg=self.color2)
            frame_botones.pack(pady=20)
            
            btn_anadir=tk.Button(
                frame_botones,
                text="Actualizar",
                font=("Arial", 20, "underline"),
                fg=self.color3,
                bg=self.color2,
                cursor="hand2",
                command=lambda:insertar(grupo.get(), nombre.get(), correo.get(), telef.get()),
            )
            btn_anadir.grid(row=0, column=0, padx=20)

            btn_salir=tk.Button(
                frame_botones,
                text="Regresar",
                font=("Arial", 20, "underline"),
                fg=self.color3,
                bg=self.color2,
                cursor="hand2",
                command=lambda:borrador.Menu(ventana, sesion, self.tema_oscuro).menuTutores(ventana, sesion),
            )
            btn_salir.grid(row=0, column=1, padx=20)

    def eliminar(self, ventana, sesion, ver):
        self.borrarPantalla(ventana)
        tl=self.grupoTitulo(ventana, sesion, "Eliminar")

        #variables
        ide=tk.StringVar()
        
        #funciones
        def cita(id_psi, ventana):
            try:
                datos=submenu.SubMenu.subCitas(ventana, id_psi)
                ide.set(datos[0])
            except:
                self.cancelar()

        def estudiantes(id_psi, ventana):
            try:
                datos=submenu.SubMenu.subAlumnos(ventana, id_psi)
                ide.set(datos[1])
            except:
                self.cancelar()

        def tutores(id_psi, ventana):
            try:
                datos=submenu.SubMenu.subTutores(ventana, id_psi)
                ide.set(datos[5])
            except:
                self.cancelar()

        def eliminar(ide, id_psicologo):
            if ver==1:
                entrada=funciones.Citas.eliminarCita(ide, id_psicologo)
                if entrada:
                    borrador.Menu(ventana, sesion, self.tema_oscuro).menuCitas(ventana, sesion)
            elif ver==2:
                entrada=funciones.Estudiantes.eliminarEstudiantes(ide)
                if entrada:
                    borrador.Menu(ventana, sesion, self.tema_oscuro).menuEstudiantes(ventana, sesion)
            elif ver==3:
                entrada=funciones.Tutor.eliminarTutores(ide)
                if entrada:
                    borrador.Menu(ventana, sesion, self.tema_oscuro).menuTutores(ventana, sesion)

        #Cuadros de texto
        frame_cuadro=tk.Frame(ventana, width=1000, height=700, bg=self.color2)
        frame_cuadro.pack(pady=10)

        #Cosa a eliminar
        if ver==1:
            txt="Cita a eliminar"
        elif ver==2:
            txt="Alumno a eliminar"
        elif ver==3:
            txt="Tutor a eliminar"
        lbl_cit=tk.Label(frame_cuadro, text=txt, justify="left", bg=self.color2)
        lbl_cit.grid(row=0, column=0, pady=5)

        txt_cit=tk.Entry(frame_cuadro, textvariable=ide)
        txt_cit.grid(row=1, column=0, pady=[0,15])

        if ver==1:
            path = os.path.abspath("img/")
            self.button_image_5 = PhotoImage(file=path + "/sumar.png")
            button_5 = tk.Button(
                frame_cuadro,
                image=self.button_image_5,
                borderwidth=0,
                highlightthickness=0,
                command=lambda:cita(sesion[0], ventana),
                relief="flat",
                bg=self.color4
            )
            button_5.grid(row=1, column=1, padx=2)
        elif ver==2:
            path = os.path.abspath("img/")
            self.button_image_5 = PhotoImage(file=path + "/sumar.png")
            button_5 = tk.Button(
                frame_cuadro,
                image=self.button_image_5,
                borderwidth=0,
                highlightthickness=0,
                command=lambda:estudiantes(sesion[0], ventana),
                relief="flat",
                bg=self.color4
            )
            button_5.grid(row=1, column=1, padx=2)
        elif ver==3:
            path = os.path.abspath("img/")
            self.button_image_5 = PhotoImage(file=path + "/sumar.png")
            button_5 = tk.Button(
                frame_cuadro,
                image=self.button_image_5,
                borderwidth=0,
                highlightthickness=0,
                command=lambda:tutores(sesion[0], ventana),
                relief="flat",
                bg=self.color4
            )
            button_5.grid(row=1, column=1, padx=2)

        #Botones
        frame_botones=tk.Frame(ventana, width=1500, height=300, bg=self.color2)
        frame_botones.pack(pady=20)
        if ver==1:
            btn_quitar=tk.Button(
                frame_botones,
                text="Eliminar",
                font=("Arial", 20, "underline"),
                fg="red",
                bg=self.color2,
                cursor="hand2",
                command=lambda:eliminar(ide.get(), sesion[0]),
            )
            btn_quitar.grid(row=0, column=0, padx=20)

            btn_salir=tk.Button(
                frame_botones,
                text="Regresar",
                font=("Arial", 20, "underline"),
                fg=self.color3,
                bg=self.color2,
                cursor="hand2",
                command=lambda:borrador.Menu(ventana, sesion, self.tema_oscuro).menuCitas(ventana, sesion),
            )
            btn_salir.grid(row=0, column=1, padx=20)
        elif ver==2:
            btn_quitar=tk.Button(
                frame_botones,
                text="Eliminar",
                font=("Arial", 20, "underline"),
                fg="red",
                bg=self.color2,
                cursor="hand2",
                command=lambda:eliminar(ide.get(), sesion[0]),
            )
            btn_quitar.grid(row=0, column=0, padx=20)

            btn_salir=tk.Button(
                frame_botones,
                text="Regresar",
                font=("Arial", 20, "underline"),
                fg=self.color3,
                bg=self.color2,
                cursor="hand2",
                command=lambda:borrador.Menu(ventana, sesion, self.tema_oscuro).menuEstudiantes(ventana, sesion),
            )
            btn_salir.grid(row=0, column=1, padx=20)
        elif ver==3:
            btn_quitar=tk.Button(
                frame_botones,
                text="Eliminar",
                font=("Arial", 20, "underline"),
                fg="red",
                bg=self.color2,
                cursor="hand2",
                command=lambda:eliminar(ide.get(), sesion[0]),
            )
            btn_quitar.grid(row=0, column=0, padx=20)

            btn_salir=tk.Button(
                frame_botones,
                text="Regresar",
                font=("Arial", 20, "underline"),
                fg=self.color3,
                bg=self.color2,
                cursor="hand2",
                command=lambda:borrador.Menu(ventana, sesion, self.tema_oscuro).menuTutores(ventana, sesion),
            )
            btn_salir.grid(row=0, column=1, padx=20)
import tkinter as tk
from tkcalendar import Calendar
from tkinter import PhotoImage
from controller import funciones
from datetime import datetime
import os

class SubMenu():
    @staticmethod
    def subCitas(ventana, id_psi):
        submenu = tk.Toplevel(ventana, width=400, height=300, bg="#ffffff")
        submenu.title("Citas")

        buscador = tk.StringVar()

        frame_busqueda = tk.Frame(submenu, bg="#ffffff")
        frame_busqueda.pack(pady=5)

        txt_buscador = tk.Entry(frame_busqueda, textvariable=buscador, width=40)
        txt_buscador.grid(row=0, column=0, padx=2)

        path = os.path.abspath("img/")
        button_image_3 = PhotoImage(file=path + "/search.png")
        button_3 = tk.Button(
            frame_busqueda,
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda:buscar(id_psi, buscador.get()),
            relief="flat",
            bg="#ffffff"
        )
        button_3.image=button_image_3
        button_3.grid(row=0, column=1, padx=2)

        lista = tk.Listbox(submenu, width=80, height=25, selectmode="single")

        def buscar(id_psi, var):
            citas = funciones.Citas.buscarCitas(id_psi, var)
            lista.delete(0, tk.END)
            if citas:
                for cita in citas:
                    opc = f"{cita[0]:<25} | {cita[1]:<50}"
                    lista.insert(tk.END, opc)
            lista.pack(pady=5)
            return citas

        citas= buscar(id_psi, "")

        tk.Button(
            frame_busqueda,
            image=button_image_3,
            command=lambda: buscar(id_psi, buscador.get()),
            bg="#ffffff",
            borderwidth=0
        ).grid(row=0, column=1, padx=2)

        frame_botones = tk.Frame(submenu, bg="#ffffff")
        frame_botones.pack(pady=20)

        def Aceptar():
            try:
                indice = lista.curselection()[0]
                val = citas[indice]
                submenu.resultado = val
            except:
                submenu.resultado = None
            submenu.destroy()

        tk.Button(
            frame_botones,
            text="Seleccionar",
            command=Aceptar
        ).grid(row=0, column=0, padx=20)

        tk.Button(
            frame_botones,
            text="Cancelar",
            command=lambda: submenu.destroy()
        ).grid(row=0, column=1, padx=20)

        # ✅ Esperar a que el submenú se cierre
        submenu.resultado = None
        submenu.wait_window()

        return submenu.resultado

    @staticmethod
    def subAlumnos(ventana, id_psi):
        submenu = tk.Toplevel(ventana, width=400, height=300, bg="#ffffff")
        submenu.title("Alumnos")

        buscador = tk.StringVar()

        frame_busqueda = tk.Frame(submenu, bg="#ffffff")
        frame_busqueda.pack(pady=5)

        txt_buscador = tk.Entry(frame_busqueda, textvariable=buscador, width=40)
        txt_buscador.grid(row=0, column=0, padx=2)

        path = os.path.abspath("img/")
        button_image_3 = PhotoImage(file=path + "/search.png")
        button_3 = tk.Button(
            frame_busqueda,
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda:buscar(buscador.get()),
            relief="flat",
            bg="#ffffff"
        )
        button_3.image=button_image_3
        button_3.grid(row=0, column=1, padx=2)

        lista = tk.Listbox(submenu, width=80, height=25, selectmode="single")

        def buscar(var):
            estud = funciones.Estudiantes.buscarEstudiantes(var)
            lista.delete(0, tk.END)
            if estud:
                for stud in estud:
                    opc = f"{stud[1]:<25} | {stud[0]:<50}"
                    lista.insert(tk.END, opc)
            lista.pack(pady=5)
            return estud

        alumnos= buscar("")

        tk.Button(
            frame_busqueda,
            image=button_image_3,
            command=lambda: buscar(id_psi, buscador.get()),
            bg="#ffffff",
            borderwidth=0
        ).grid(row=0, column=1, padx=2)

        frame_botones = tk.Frame(submenu, bg="#ffffff")
        frame_botones.pack(pady=20)

        def Aceptar():
            try:
                indice = lista.curselection()[0]
                val = alumnos[indice]
                submenu.resultado = val
            except:
                submenu.resultado = None
            submenu.destroy()

        tk.Button(
            frame_botones,
            text="Seleccionar",
            command=Aceptar
        ).grid(row=0, column=0, padx=20)

        tk.Button(
            frame_botones,
            text="Cancelar",
            command=lambda: submenu.destroy()
        ).grid(row=0, column=1, padx=20)

        # ✅ Esperar a que el submenú se cierre
        submenu.resultado = None
        submenu.wait_window()

        return submenu.resultado

    @staticmethod
    def subTutores(ventana, id_psi):
        submenu = tk.Toplevel(ventana, width=400, height=300, bg="#ffffff")
        submenu.title("Tutores")

        buscador = tk.StringVar()

        frame_busqueda = tk.Frame(submenu, bg="#ffffff")
        frame_busqueda.pack(pady=5)

        txt_buscador = tk.Entry(frame_busqueda, textvariable=buscador, width=40)
        txt_buscador.grid(row=0, column=0, padx=2)

        path = os.path.abspath("img/")
        button_image_3 = PhotoImage(file=path + "/search.png")
        button_3 = tk.Button(
            frame_busqueda,
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda:buscar(buscador.get()),
            relief="flat",
            bg="#ffffff"
        )
        button_3.image=button_image_3
        button_3.grid(row=0, column=1, padx=2)

        lista = tk.Listbox(submenu, width=80, height=25, selectmode="single")

        def buscar(var):
            tutor = funciones.Tutor.buscarTutores(var)
            lista.delete(0, tk.END)
            if tutor:
                for tuto in tutor:
                    opc = f"{tuto[1]:<25} | {tuto[0]:<50}"
                    lista.insert(tk.END, opc)
            lista.pack(pady=5)
            return tutor

        tutores = buscar("")

        tk.Button(
            frame_busqueda,
            image=button_image_3,
            command=lambda: buscar(id_psi, buscador.get()),
            bg="#ffffff",
            borderwidth=0
        ).grid(row=0, column=1, padx=2)

        frame_botones = tk.Frame(submenu, bg="#ffffff")
        frame_botones.pack(pady=20)

        def Aceptar():
            try:
                indice = lista.curselection()[0]
                val = tutores[indice]
                submenu.resultado = val
            except:
                submenu.resultado = None
            submenu.destroy()

        tk.Button(
            frame_botones,
            text="Seleccionar",
            command=Aceptar
        ).grid(row=0, column=0, padx=20)

        tk.Button(
            frame_botones,
            text="Cancelar",
            command=lambda: submenu.destroy()
        ).grid(row=0, column=1, padx=20)

        # ✅ Esperar a que el submenú se cierre
        submenu.resultado = None
        submenu.wait_window()

        return submenu.resultado

    @staticmethod
    def subGrupos(ventana, id_psi):
        submenu = tk.Toplevel(ventana, width=400, height=300, bg="#ffffff")
        submenu.title("Grupos")

        buscador = tk.StringVar()

        frame_busqueda = tk.Frame(submenu, bg="#ffffff")
        frame_busqueda.pack(pady=5)

        txt_buscador = tk.Entry(frame_busqueda, textvariable=buscador, width=40)
        txt_buscador.grid(row=0, column=0, padx=2)

        path = os.path.abspath("img/")
        button_image_3 = PhotoImage(file=path + "/search.png")
        # botón de búsqueda (solo uno)
        button_3 = tk.Button(
            frame_busqueda,
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: buscar(buscador.get()),
            relief="flat",
            bg="#ffffff"
        )
        button_3.image = button_image_3
        button_3.grid(row=0, column=1, padx=2)

        lista = tk.Listbox(submenu, width=80, height=25, selectmode="single")
        lista.pack(pady=5)

        grupos = []  # lista que se actualizará

        def buscar(var):
            nonlocal grupos
            grupos = funciones.Grupo.buscarGrupo(var)
            lista.delete(0, tk.END)
            if grupos:
                for grup in grupos:
                    opc = f"{grup[2]} {grup[3]} {grup[4]} {grup[1]}"
                    lista.insert(tk.END, opc)

            return grupos

        # búsqueda inicial
        buscar("")


        frame_botones = tk.Frame(submenu, bg="#ffffff")
        frame_botones.pack(pady=20)

        def Aceptar():
            try:
                indice = lista.curselection()[0]
                submenu.resultado = grupos[indice]
            except:
                submenu.resultado = None
            submenu.destroy()

        boton1=tk.Button(frame_botones, text="Seleccionar", command=Aceptar).grid(row=0, column=0, padx=20)
        boton2=tk.Button(frame_botones, text="Cancelar", command=lambda: submenu.destroy()).grid(row=0, column=1, padx=20)

        submenu.resultado = None
        submenu.wait_window()

        return submenu.resultado


    @staticmethod
    def subCalendario(ventana):
        submenu = tk.Toplevel(ventana)
        submenu.title("Calendario")
        submenu.config(bg="#ffffff")

        # Fecha actual
        hoy = datetime.today().date()
        ahora=datetime.today().time()

        # Variables
        hora=tk.StringVar()
        horas=["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00",
               "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
        hora.set(f"{ahora.hour:02d}:00")

        # Crear calendario
        lbl_calendario=tk.Label(submenu, text="Selecciona la fecha de la cita en el calendario")
        lbl_calendario.pack(pady=0)

        cal = Calendar(
            submenu,
            selectmode="day",
            year=hoy.year,
            month=hoy.month,
            day=hoy.day,
            date_pattern="yyyy-mm-dd"
        )
        cal.pack(pady=[10,20])

        # Crear selector de horas
        lbl_horario=tk.Label(submenu, text="Selecciona la hora de la cita en esta lista")
        lbl_horario.pack(pady=0)
        
        time = tk.OptionMenu(submenu, hora, *horas)
        time.pack(pady=[10,20])

        # Frame de botones
        frame_botones = tk.Frame(submenu, bg="#ffffff")
        frame_botones.pack(pady=20)

        # Botón aceptar
        def Aceptar():
            submenu.resultado = cal.get_date() + " " + hora.get()
            submenu.destroy()

        tk.Button(
            frame_botones,
            text="Seleccionar",
            command=Aceptar
        ).grid(row=0, column=0, padx=20)

        # Botón cancelar
        tk.Button(
            frame_botones,
            text="Cancelar",
            command=lambda: submenu.destroy()
        ).grid(row=0, column=1, padx=20)

        # Valor por defecto
        submenu.resultado = None

        # Esperar a que se cierre
        submenu.wait_window()

        return submenu.resultado

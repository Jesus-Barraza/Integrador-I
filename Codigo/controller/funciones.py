from model import sesion
import hashlib
import tkinter as tk
from tkinter import messagebox
import flet as ft
from flet import AlertDialog

class Usuarios():
    @staticmethod
    def codigo(contrasena):
        contra=hashlib.sha512(contrasena.encode()).hexdigest()
        return contra

    @staticmethod
    def closed(event, ventana, dialog):
        dialog.open = False
        ventana.update()

    @staticmethod
    def respuestaSql(respuesta, ventana):
        if respuesta:
            dlg = ft.AlertDialog(
                title=ft.Text("Acción SQL"),
                content=ft.Text("La acción se ha realizado con éxito"),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: Usuarios.closed(e, ventana, dlg))
                ],
                on_dismiss=lambda e: Usuarios.closed(e, ventana, dlg)
            )
        else:
            dlg = ft.AlertDialog(
                title=ft.Text("Acción SQL"),
                content=ft.Text("Ha ocurrido un error al realizar la acción, inténtelo más tarde"),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: Usuarios.closed(e, ventana, dlg))
                ],
                on_dismiss=lambda e: Usuarios.closed(e, ventana, dlg)
            )

        ventana.dialog = dlg
        ventana.overlay.append(dlg)
        ventana.update()
        dlg.open = True
        ventana.update()

    @staticmethod
    def inicioSesion(correo, contra, ventana):
        contra=Usuarios.codigo(contra)
        user=sesion.Sesion.iniciarSesion(correo, contra)
        if user:
            Usuarios.respuestaSql(True, ventana)
            return user
        else:
            Usuarios.respuestaSql(False, ventana)
            return None

    @staticmethod
    def registrar(nombre, correo, telefono, contra, ventana):
        contra=Usuarios.codigo(contra)
        regi=sesion.Sesion.registrar(nombre, correo, telefono, contra)
        if regi:
            Usuarios.respuestaSql(regi, ventana)
            return regi
        else:
            Usuarios.respuestaSql(regi, ventana)
            return None

    @staticmethod
    def borrarCuenta(ide):
        cuidado=messagebox.askyesno(title="Borrar cuenta", message="¿Está seguro de borrar su cuenta? Esta acción no se puede deshacer", icon="warning")
        if cuidado:
            borrar=sesion.Sesion.borrarCuenta(ide)
            if borrar:
                noti=messagebox.showinfo(title="Borrar cuenta", message="Se ha borrado la cuenta con éxito")
                return True
            else:
                noti=messagebox.showerror(title="Borrar cuenta", message="No se ha podido borrar la cuenta, inténtelo más tarde")
            return False
        else:
            noti=messagebox.showinfo(title="Borrar cuenta", message="Eliminación cancelada con éxito")
            return False

class Citas():
    @staticmethod
    def respuestaSql(res):
        if res:
            res=messagebox.showinfo(title="Resultado de la operación", message="Operación realizada con éxito")
        else:
            res=messagebox.showerror(title="Resultado de la operación", message="Hubo un fallo al realizar la operación, inténtelo más tarde")

    @staticmethod
    def cancelar():
        noti=messagebox.showinfo(title="Operación", message="Se ha cancelado la operación con éxito")

    @staticmethod
    def obtener_citas_dia(psicologo_id):
        citas=sesion.Citas.obtener_citas_dia(psicologo_id)
        return citas

    @staticmethod
    def obtener_citas_h(psicologo_id):
        citas=sesion.Citas.obtener_citas_h(psicologo_id)
        return citas

    @staticmethod
    def buscarCitas(psicologo_id, var):
        citas=sesion.Citas.buscarCitas(psicologo_id, var)
        return citas

    @staticmethod
    def agregarCita(psicologo_id, name_stu, date, matricul, full):
        res=sesion.Citas.InsertarCita(matricul, psicologo_id, date, full[0][5])
        res2=sesion.Students.actualizarCitas(full[0][5], matricul)
        if res and res2:
            res_t=True
        else:
            res_t=False
        Citas.respuestaSql(res_t)
        return res

    @staticmethod
    def modificarCita(name_stu, matr, date, id_psi, id_date):
        citas=sesion.Students.buscarEstudiante(name_stu)
        if len(citas):
            matr=citas[0][1]
        else:
            citas=sesion.Students.comprobarEstudiante(matr)
            matr=citas[0][1]
        res=sesion.Citas.ActualizarCita(matr, date, id_psi, id_date)
        Citas.respuestaSql(res)
        return res

    @staticmethod
    def eliminarCita(id_date, id_psi):
        noti=messagebox.askyesno(title="¡Cuidado!", message="¿Seguro que desea borrar el registro de esta cita?", icon="warning")
        if noti:
            res=sesion.Citas.EliminarCita(id_date, id_psi)
            Citas.respuestaSql(res)
            return res
        else:
            Citas.cancelar

    @staticmethod
    def cancelarCitas(id_date, id_psi):
        noti=messagebox.askyesno(title="¡Cuidado!", message="¿Deseas cancelar la cita?", icon="warning")
        if noti:
            res=sesion.Citas.cancelarCita(id_date, id_psi)
            Citas.respuestaSql(res)
            return res
        else:
            Citas.cancelar
    
class Estudiantes():
    @staticmethod
    def comprobarEstudiantes(var):
        estudiante=sesion.Students.comprobarEstudiante(var)
        return estudiante

    @staticmethod
    def buscarEstudiantes(var):
        citas=sesion.Students.buscarEstudiante(var)
        return citas
    
    @staticmethod
    def agregarEstudiante(matricula, grupo, nombre, correo, telefono):
        res=sesion.Students.insertarEstudiante(matricula, grupo, nombre, correo, telefono)
        Citas.respuestaSql(res)
        return res
    
    @staticmethod
    def actualizarEstudiante(matricula, grupo, nombre, correo, telefono):
        res=sesion.Students.actualizarEstudiante(matricula, grupo, nombre, correo, telefono)
        Citas.respuestaSql(res)
        return res

    @staticmethod
    def eliminarEstudiantes(matricula):
        noti=messagebox.askyesno(title="¡Cuidado!", message="¿Seguro que desea borrar el registro de este alumno?", icon="warning")
        if noti:
            res=sesion.Students.eliminarEstudiante(matricula)
            Citas.respuestaSql(res)
            return res
        else:
            Citas.cancelar
        

class Tutor():
    @staticmethod
    def buscarTutores(var):
        citas=sesion.Tutores.buscarTutores(var)
        return citas

    @staticmethod
    def agregarTutor(grupo, nombre, correo, telefono):
        res=sesion.Tutores.InsertarTutor(grupo, nombre, correo, telefono)
        Citas.respuestaSql(res)
        return res

    @staticmethod
    def actualizarTutor(nombre, grupo, correo, telefono):
        datos=sesion.Tutores.buscarTutores(nombre)
        ID_tutor=datos[0][5]
        res=sesion.Tutores.ActualizarTutor( grupo, correo, telefono, ID_tutor)
        Citas.respuestaSql(res)
        return res

    @staticmethod
    def eliminarTutores(ide):
        noti=messagebox.askyesno(title="¡Cuidado!", message="¿Seguro que desea borrar el registro de este tutor?", icon="warning")
        if noti:
            res=sesion.Tutores.eliminarTutor(ide)
            Citas.respuestaSql(res)
            return res
        else:
            Citas.cancelar

class Grupo():
    @staticmethod
    def buscarGrupo(var):
        citas=sesion.Grupos.buscarGrupos(var)
        return citas
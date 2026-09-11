from model.conexionBD import *
import hashlib

class Sesion():
    @staticmethod
    def registrar(nombre,email,phone,password):
        try:
            cursor.execute(
                "insert into psychologists values(null,%s,%s,%s,%s)",
                (nombre,email,phone,password,)
            )
            conexion.commit()
            usuario=Sesion.iniciarSesion(email, password)
            if usuario:
               return True
            else:
               return False
        except:
            return False

    @staticmethod
    def iniciarSesion(email, contrasena):
        try:
            cursor.execute(
                "select ID_psy, name_psy, mail_psy, phone_psy from psychologists where mail_psy=%s and pass=%s",
                (email,contrasena)
            )
            usuario=cursor.fetchone()
            if usuario:
                return usuario
            else:
                return None      
        except:
            return None
    
    def borrarCuenta(ide):
        try:
            cursor.execute(
                "delete from psychologists where ID_psy=%s",
                (ide,)
            )
            conexion.commit()
            return True
        except:
            return False
        
class Citas():
    @staticmethod
    def obtener_citas_dia(psicologo_id):
        try:
            cursor.execute(
                "select ID_app, students.name_stu, date, status from appointments JOIN students ON FK_stu=students.control_num where FK_psy=%s and date >= CURDATE() order by date",
                (psicologo_id,)
            )
            citas=cursor.fetchall()
            return citas
        except:
            return []
        
    @staticmethod
    def obtener_citas_h(psicologo_id):
        try:
            cursor.execute(
                "select ID_app, students.name_stu, date, status from appointments JOIN students ON FK_stu=students.control_num where FK_psy=%s and date < CURDATE() order by date DESC",
                (psicologo_id,)
            )
            citas=cursor.fetchall()
            return citas
        except:
            return []

    @staticmethod
    def buscarCitas(psicologo_id, var):
        try:
            if len(var):
                cursor.execute(
                    "select ID_app, students.name_stu, date, status from appointments join students on FK_stu=students.control_num where FK_psy=%s and students.name_stu like %s order by date DESC",
                    (psicologo_id, f"%{var}%")
                )
                citas=cursor.fetchall()
                return citas
            else:
                cursor.execute(
                    "select ID_app, students.name_stu, date, status from appointments join students on FK_stu=students.control_num where FK_psy=%s order by date DESC",
                    (psicologo_id, )
                )
                citas=cursor.fetchall()
                return citas
        except:
            return []
    
    @staticmethod
    def InsertarCita(id_stu, psicologo_id, date, num_citas):
        try:
            cursor.execute(
                "INSERT INTO appointments VALUES (null, %s, %s, %s, 'Activo', %s, null, null)",
                (id_stu, psicologo_id, date, num_citas)
            )
            conexion.commit()
            return True
        except:
            return False

    @staticmethod
    def ActualizarCita(id_stu, date, psicologo_id, cita_id):
        try:
            cursor.execute(
                "update appointments set FK_stu=%s, date=%s, status= 'Alterado' where FK_psy=%s and ID_app=%s",
                (id_stu, date, psicologo_id, cita_id)
            )
            conexion.commit()
            return True
        except:
            return False

    @staticmethod
    def EliminarCita(cita_id, psicologo_id):
        try:
            cursor.execute(
                "delete from appointments where ID_app=%s and FK_psy=%s",
                (cita_id, psicologo_id)
            )
            conexion.commit()
            return True
        except:
            return False
        
    @staticmethod
    def cancelarCita(cita_id, psicologo_id):
        try:
            cursor.execute(
                "update appointments set status = 'Cancelado' where FK_psy=%s and ID_app=%s",
                (psicologo_id, cita_id)
            )
            conexion.commit()
            return True
        except:
            return False

class Students():
    @staticmethod
    def buscarEstudiante(var):
        try:
            if len(var):
                cursor.execute(
                    "SELECT name_stu, control_num, CONCAT(groups.period, ' ', groups.group_code, ' ', groups.modal, ' ', groups.carrer), mail_stu, phone_stu, cont_app, susp, groups.ID_group FROM `students` JOIN groups on FK_group=groups.ID_group where name_stu like %s ORDER BY name_stu DESC",
                    (f"%{var}%", )
                )
                citas=cursor.fetchall()
                return citas
            else:
                cursor.execute(
                    "SELECT name_stu, control_num, CONCAT(groups.period, ' ', groups.group_code, ' ', groups.modal, ' ', groups.carrer), mail_stu, phone_stu, cont_app, susp, groups.ID_group FROM `students` JOIN groups on FK_group=groups.ID_group ORDER BY name_stu DESC"
                )
                citas=cursor.fetchall()
                return citas
        except:
            return []
    
    @staticmethod
    def comprobarEstudiante(var):
        try:
            cursor.execute(
                "SELECT name_stu, control_num, CONCAT(groups.period, ' ', groups.group_code, ' ', groups.modal, ' ', groups.carrer), mail_stu, phone_stu, cont_app, susp, groups.ID_group FROM `students` JOIN groups on FK_group=groups.ID_group WHERE control_num like %s",
                (f"%{var}%", )
            )
            citas=cursor.fetchall()
            if len(citas)!=1:
                cursor.execute(
                    "SELECT name_stu, control_num, CONCAT(groups.period, ' ', groups.group_code, ' ', groups.modal, ' ', groups.carrer), mail_stu, phone_stu, cont_app, susp, groups.ID_group FROM `students` JOIN groups on FK_group=groups.ID_group WHERE name_stu like %s",
                    (f"%{var}%", )
                )
                citas=cursor.fetchall()
                return citas
                if len(citas)!=1:
                    return []
            else:
                return citas
        except:
            return []
        
    @staticmethod
    def insertarEstudiante(mat, grp, nom, mail, phone):
        try:
            cursor.execute(
                "INSERT INTO Students VALUES (%s, %s, %s, %s, %s, 0, 0)",
                (mat, grp, nom, mail, phone)
            )
            conexion.commit()
            return True
        except:
            return False
        
    @staticmethod
    def actualizarCitas(num_citas, id_stu):
        try:
            cursor.execute(
                "update students set cont_app=%s where control_num=%s",
                (num_citas+1, id_stu)
            )
            conexion.commit()
            return True
        except:
            return False

    @staticmethod
    def actualizarEstudiante(matricula, grupo, nombre, correo, telefono):
        try:
            cursor.execute(
                "update students set FK_group=%s, name_stu=%s, mail_stu=%s, phone_stu=%s where control_num=%s",
                (grupo, nombre, correo, telefono, matricula)
            )
            conexion.commit()
            return True
        except:
            return False

    @staticmethod
    def eliminarEstudiante(matricula):
        try:
            cursor.execute(
                "delete from students where control_num=%s",
                (matricula, )
            )
            conexion.commit()
            return True
        except:
            return False

class Tutores():
    @staticmethod
    def buscarTutores(var):
        try:
            if len(var):
                cursor.execute(
                    "SELECT name_tea, CONCAT(groups.period, ' ', groups.group_code, ' ', groups.modal, ' ', groups.carrer), mail_tea, phone_tea, groups.ID_group, ID_tutor FROM `tutored` JOIN groups on FK_group=groups.ID_group where name_tea like %s",
                    (f"%{var}%", )
                )
                citas=cursor.fetchall()
                return citas
            else:
                cursor.execute(
                    "SELECT name_tea, CONCAT(groups.period, ' ', groups.group_code, ' ', groups.modal, ' ', groups.carrer), mail_tea, phone_tea, groups.ID_group, ID_tutor FROM `tutored` JOIN groups on FK_group=groups.ID_group"
                )
                citas=cursor.fetchall()
                return citas
        except:
            return []

    @staticmethod
    def InsertarTutor(grp, nom, mail, phone):
        try:
            cursor.execute(
                "INSERT INTO tutored VALUES (null, %s, %s, %s, %s)",
                (grp, nom, mail, phone)
            )
            conexion.commit()
            return True
        except:
            return False

    @staticmethod
    def ActualizarTutor(grupo, correo, telefono, ID_tutor):
        try:
            cursor.execute(
                "update tutored set FK_group=%s, mail_tea=%s, phone_tea=%s where ID_tutor=%s",
                (grupo, correo, telefono, ID_tutor)
            )
            conexion.commit()
            return True
        except:
            return False
    
    @staticmethod
    def eliminarTutor(ide):
        try:
            cursor.execute(
                "delete from tutored where ID_tutor=%s",
                (ide, )
            )
            conexion.commit()
            return True
        except:
            return False

class Grupos():
    @staticmethod
    def buscarGrupos(var):
        try:
            if len(var) > 0:
                cursor.execute(
                    "SELECT * FROM `groups` where carrer like %s",
                    (var, )
                )
                citas=cursor.fetchall()
                return citas
            else:
                cursor.execute(
                    "SELECT * FROM `groups`"
                )
                citas=cursor.fetchall()
                return citas
        except:
            return []

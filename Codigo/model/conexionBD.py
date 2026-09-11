import mysql.connector
from tkinter import messagebox
from mysql.connector import Error

try:
    #Conectar con la BD en MySQL
    conexion=mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='bd_cita_psico'
    )
    #Crear un objeto de tipo cursor que se pueda reutilizar nuevamente
    cursor=conexion.cursor(buffered=True)
    start=True
except Error as e:
    error=messagebox.showerror(message=f"Ocurrió el error {e}, inténtelo más tarde", icon="error", title="Hubo un error al conectar a la base de datos")
    start=False
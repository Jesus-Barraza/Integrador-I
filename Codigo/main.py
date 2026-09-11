'''
Este es el archivo de main. En este archivo se ingresará directamente al directorio e interactuar con el resto.
'''
import flet as ft
from view import menus
from model.conexionBD import start

#Clase para iniciar la aplicación
class app():
    def __init__(self, ventana):
        menus.Menu(ventana)

#Punto de entrada principal
if __name__ == "__main__":
    if start:
        ft.app(target=app, assets_dir="img", view=ft.AppView.FLET_APP)
        
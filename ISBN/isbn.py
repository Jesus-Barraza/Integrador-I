#Funciones normales
def borrarPantalla():
    import os
    os.system("cls")

def esperarTecla():
    input("\n\t\tPresione Enter para continuar")

#Método para retiro de caracteres de - y " "
def normalize_isbn(code):
    code=code.replace(" ", "")
    code=code.replace("-", "")
    return code

#Validación ISBN-10
def is_valid_isbn10(code):
    cache=0
    for i in range(len(code)):
        try:
            cache+=(int(code[i])*(10-i))
        except:
            if code[i]!="X":
                return False
            else:
                pass
    if cache%11==0:
        return True
    else:
        return False

#Validación ISBN-13
def is_valid_isbn13(code):
    cache=0
    for i in range(len(code)-1):
        try:
            if i%2==0: 
                cache+=int(code[i])
            else:
                cache+=3*int(code[i])
        except:
            return False
    control=(10-(cache%10))%10
    return control==int(code[12])

#Detección de ISBN
def detect_isbn(code):
    normalize_isbn(code)
    if len(code)<12 and len(code)>8:
        print("\n\t Se detectó un código ISBN-10")
        ver=is_valid_isbn10(code)
        a="ISBN-10"
    elif len(code)<15 and len(code)>11:
        print("\n\t Se detectó un código ISBN-13")
        ver=is_valid_isbn13(code)
        a="ISBN-13"
    else:
        print("\n\t Este código no es válido, inténtelo de nuevo")
    
    if ver:
        print(f"\n\t Este código es válido para {a}")
    else:
        print("Este código no es válido, inténtelo de nuevo")

#Menú
def menu():
    borrarPantalla()
    rep=True
    while rep:
        print("\n\t\t Validación de códigos ISBN")
        rep=input("\n\n1-Validar código ISBN\n2-Salir\n Elige una opción (1-2):").strip()
        if rep=="1":
            borrarPantalla()
            code=normalize_isbn(input("Ingrese el código ISBN a buscar: "))
            detect_isbn(code)
            esperarTecla()
            borrarPantalla()
        elif rep=="2":
            borrarPantalla()
            print("Terminó la ejecución del sistema")
            rep=False
        else:
            borrarPantalla()
            print("Opción incorrecta, inténtelo de nuevo")
            rep=True

menu()
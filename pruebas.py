from lectura import LecturaXML
import os


def print_menu():
    print("------------------- Menu Principal -------------------")
    print("1. Cargar archivo")
    print("2. Procesar archivo")
    print("3. Escribir archivo de salida")
    print("4. Mostrar datos del estudiante")
    print("5. Generar gráfica")
    print("6. Salida")
    print("--------------------------------------------------------")

def main():
    xml_reader = LecturaXML()  # Instanciar LecturaXML
    ruta = None  # Inicializar la variable ruta

    opcion = 0
    while opcion != 6:
        
        print_menu()
        try:
            opcion = int(input("Ingresa una opción: "))
        except ValueError:
            print("*****************************************")
            print("Entrada inválida, ingresa un número.")
            print("*****************************************")
            continue
        
        match opcion:
            case 1:
                ruta = input("Ingresa la ruta del archivo XML: ")

                if os.path.exists(ruta) and os.path.isfile(ruta):
                    print("Archivo cargado")
                    xml_reader.cargar_archivo(ruta)  # Cargar el archivo aquí
                else:
                    print("Error al cargar el archivo. La ruta no es válida o el archivo no existe.")

            case 2:
                if ruta:
                    xml_reader.seleccionar_maquina()  # Llama a la función para seleccionar máquina
                else:
                    print("Primero debes cargar un archivo en la opción 1")
                
            case 3:
                # if ruta:
                    # nombre_archivo = input("Ingresa el nombre del archivo de salida XML: ")
                    # xml_reader.escribir_archivo_salida(nombre_archivo)
                    # print(f"Archivo XML guardado como {nombre_archivo}")
                # else:
                print("Primero debes cargar un archivo en la opción 1")
                    
            case 4:
                print("")
                print("Nombre: Brandon Antonio Marroquín Pérez")
                print("Carnet: 202300813")
                print("Carrera: Ingeniería en Ciencias y Sistemas")
                print("Curso: INTRODUCCIÓN A LA PROGRAMACIÓN Y COMPUTACIÓN 2 Sección N")
                print("CUI: 3045062060114")
                print("Semestre: 4")
                print("https://drive.google.com/drive/folders/12s6nNj5q1lGtY9qzM59e0ZHLNetcIrDP?usp=sharing")
                print("")
                
            case 5:
                print("No hay matrices cargadas para graficar.")
            case 6:
                print("")
                print("Saliendo...")
                print("")
                
            case _:
                print("")
                print("*****************************************")
                print("Opción inválida, intenta de nuevo")
                print("*****************************************")
                print("")

if __name__ == "__main__":
    main()

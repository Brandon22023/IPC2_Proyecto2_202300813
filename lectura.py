import xml.etree.ElementTree as ET
class Nodo2:
    def __init__(self, linea, componente):
        self.linea = linea  # Línea de ensamblaje
        self.componente = componente  # Número del componente
        self.siguiente = None  # Apunta al siguiente nodo
        self.anterior = None  # Apunta al nodo anterior
    

class ListaDoblementeEnlazada:
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def agregar(self, linea, componente):
        nuevo_nodo = Nodo2(linea, componente)
        if self.primero is None:
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            self.ultimo.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.ultimo
            self.ultimo = nuevo_nodo

    def buscar_ultimo_componente(self, linea):
        actual = self.primero
        ultimo_componente = 0
        while actual is not None:
            if actual.linea == linea and actual.componente > ultimo_componente:
                ultimo_componente = actual.componente
            actual = actual.siguiente
        return ultimo_componente

    def imprimir(self):
        actual = self.primero
        while actual is not None:
            print(f"L{actual.linea}C{actual.componente} = Mover brazo componente {actual.componente}")
            actual = actual.siguiente
    
    def buscar_componente(self, componente):
        actual = self.primero
        encontrado = False
        while actual is not None:
            if actual.componente == componente:
                print(f"Componente encontrado: L{actual.linea}, C{actual.componente}")
                encontrado = True
            actual = actual.siguiente

        if not encontrado:
            print(f"No se encontró el componente {componente}.")

class ProcesadorElaboracion:
    def __init__(self):
        self.lista_instrucciones = ListaDoblementeEnlazada()

     # Método para procesar la elaboración de un producto sin usar listas, ni índices ni len()
    def procesar_elaboracion(self, elaboracion):
        # Inicializamos un puntero para recorrer la cadena
        puntero = iter(elaboracion)

        try:
            while True:
                # Buscamos un caracter "L" que indica una línea
                caracter = next(puntero)
                if caracter == "L":  # Detectamos el inicio de una línea "L"
                    linea = int(next(puntero))  # Obtener el número de la línea
                    next(puntero)  # Saltar el caracter "C"
                    numero = ""  # Inicializamos la variable para almacenar el componente

                    # Leer el componente
                    while True:
                        siguiente = next(puntero)  # Obtener el siguiente carácter
                        if siguiente.isdigit():  # Comprobar si es un dígito
                            numero += siguiente  # Concatenar dígitos
                        else:
                            # Si no es un dígito, salir del bucle
                            break

                    # Convertir a entero si hay un número acumulado
                    if numero:  # Si hay un número acumulado
                        componente = int(numero)
                        # Agregar la instrucción correspondiente a la lista doblemente enlazada
                        self.lista_instrucciones.agregar(linea, componente)

                        # Llamar a buscar_componente en el contexto adecuado
                        self.lista_instrucciones.buscar_componente(componente)

                # Al final de la cadena, manejar el último componente si es necesario
                if siguiente is None:
                    if numero:  # Verificar si hay un número acumulado
                        componente = int(numero)
                        self.lista_instrucciones.agregar(linea, componente)
                        self.lista_instrucciones.buscar_componente(componente)

        except StopIteration:
            # Manejar el final del iterador
            if numero:  # Verificar si hay un número acumulado al final
                componente = int(numero)
                self.lista_instrucciones.agregar(linea, componente)
                self.lista_instrucciones.buscar_componente(componente)
            pass  # Fin del iterador
         # Generar las instrucciones basadas en los componentes procesados
        self.generar_instrucciones()
    

    def generar_instrucciones(self):
        # Buscar el componente máximo entre todas las líneas
        max_componente_global = 0
        actual = self.lista_instrucciones.primero
        max_linea = 0

        # Inicializamos una lista doblemente enlazada para almacenar el máximo por línea
        max_por_linea = ListaDoblementeEnlazada()

        # Primer recorrido: obtenemos los máximos componentes por cada línea
        while actual is not None:
            # Actualizamos el máximo componente global si es necesario
            if actual.componente > max_componente_global:
                max_componente_global = actual.componente

            # Actualizamos el máximo número de línea
            if actual.linea > max_linea:
                max_linea = actual.linea

            # Buscamos si ya existe un nodo para esta línea en la lista de máximos por línea
            nodo_max_linea = max_por_linea.primero
            linea_encontrada = False
            while nodo_max_linea is not None:
                if nodo_max_linea.linea == actual.linea:
                    # Actualizamos el componente si es mayor
                    if actual.componente > nodo_max_linea.componente:
                        nodo_max_linea.componente = actual.componente
                    linea_encontrada = True
                    break
                nodo_max_linea = nodo_max_linea.siguiente

            # Si no encontramos la línea en la lista, la agregamos con el componente actual
            if not linea_encontrada:
                max_por_linea.agregar(actual.linea, actual.componente)

            actual = actual.siguiente

        # Segundo recorrido: generar las instrucciones basadas en los máximos por línea
        actual_max = max_por_linea.primero  # Reiniciar el puntero para la lista de máximos por línea

        while actual_max is not None:
            linea_actual = actual_max.linea
            max_componente_actual = actual_max.componente

            # Imprimir las instrucciones hasta el componente máximo de esta línea
            for i in range(1, max_componente_actual + 1):
                # Verificar si el componente está en la lista de instrucciones
                componente_en_lista = self.lista_instrucciones.primero
                ensamblaje_realizado = False  # Seguimiento del ensamblaje en la línea actual

                while componente_en_lista is not None:
                    if componente_en_lista.componente == i and componente_en_lista.linea == linea_actual:
                        print(f"L{linea_actual}C{i} = ensamblaje")
                        ensamblaje_realizado = True  # Ensamblaje realizado
                        break
                    componente_en_lista = componente_en_lista.siguiente
                
                if not ensamblaje_realizado:
                    # Si el ensamblaje no se realizó en este componente, movemos el brazo
                    print(f"L{linea_actual}C{i} = Mover brazo componente {i}")

            # Instrucciones para componentes que no están en la lista de instrucciones
            for i in range(max_componente_actual + 1, max_componente_global + 1):
                print(f"L{linea_actual}C{i} = No hacer nada")

            actual_max = actual_max.siguiente  # Avanzar al siguiente máximo por línea

        # Imprimir líneas que no tenían componentes en la entrada original (si las hubiera)
        for linea in range(1, max_linea + 1):
            # Verificar si esta línea ya fue impresa
            existe_linea = False
            puntero_lineas = max_por_linea.primero
            while puntero_lineas is not None:
                if puntero_lineas.linea == linea:
                    existe_linea = True
                    break
                puntero_lineas = puntero_lineas.siguiente

            if not existe_linea:  # Si la línea no fue impresa
                for i in range(1, max_componente_global + 1):
                    print(f"L{linea}C{i} = No hacer nada")


class Producto:
    """Clase para representar un producto."""
    def __init__(self, nombre_producto, elaboracion):
        self.nombre_producto = nombre_producto  # Nombre del producto
        self.elaboracion = elaboracion  # Proceso de elaboración
        self.siguiente = None  # Puntero al siguiente producto

class Maquina:
    """Clase para representar una máquina y sus productos."""
    def __init__(self, nombre_maquina, cantidad_lineas, cantidad_componentes, tiempo_ensamblaje):
        self.nombre_maquina = nombre_maquina  # Nombre de la máquina
        self.cantidad_lineas = cantidad_lineas  # Cantidad de líneas de producción
        self.cantidad_componentes = cantidad_componentes  # Cantidad de componentes
        self.tiempo_ensamblaje = tiempo_ensamblaje  # Tiempo de ensamblaje
        self.productos = ListaEnlazada()  # Lista enlazada para almacenar productos

class Nodo:
    """Clase para representar un nodo en la lista enlazada."""
    def __init__(self, data):
        self.data = data  # Los datos del nodo (máquina o producto)
        self.siguiente = None  # Apuntador al siguiente nodo

class ListaEnlazada:
    """Clase para manejar una lista enlazada simple."""
    def __init__(self):
        self.cabeza = None  # Inicializa la cabeza de la lista

    def agregar(self, data):
        """Agrega un nuevo nodo al final de la lista."""
        nuevo_nodo = Nodo(data)  # Crear un nuevo nodo
        if self.cabeza is None:  # Si la lista está vacía
            self.cabeza = nuevo_nodo  # La cabeza es el nuevo nodo
        else:
            actual = self.cabeza
            while actual.siguiente:  # Recorre hasta el final de la lista
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo  # Agrega el nuevo nodo al final

    def imprimir(self):
        """Imprime los datos de la lista enlazada."""
        actual = self.cabeza
        while actual:  # Mientras haya nodos en la lista
            print(actual.data)  # Imprime los datos del nodo
            actual = actual.siguiente  # Avanza al siguiente nodo

class LecturaXML:
    """Clase para manejar la lectura de datos desde un archivo XML y almacenamiento en una lista enlazada."""
    
    def __init__(self):
        self.lista_maquinas = ListaEnlazada()  # Inicializa una lista enlazada para almacenar las máquinas

    def cargar_archivo(self, ruta_archivo):
        """Carga el archivo XML y procesa las máquinas."""
        try:
            tree = ET.parse(ruta_archivo)  # Parsear el archivo XML
            root = tree.getroot()  # Obtener el elemento raíz del archivo XML
            
            for maquina_elem in root.findall('Maquina'):  # Iterar sobre cada elemento 'Maquina' en el XML
                nombre_maquina = maquina_elem.find('NombreMaquina').text.strip()  # Obtener el nombre de la máquina
                cantidad_lineas = int(maquina_elem.find('CantidadLineasProduccion').text.strip())  # Cantidad de líneas de producción
                cantidad_componentes = int(maquina_elem.find('CantidadComponentes').text.strip())  # Cantidad de componentes
                tiempo_ensamblaje = int(maquina_elem.find('TiempoEnsamblaje').text.strip())  # Tiempo de ensamblaje
                
                # Crear una instancia de la máquina
                maquina = Maquina(nombre_maquina, cantidad_lineas, cantidad_componentes, tiempo_ensamblaje)
                
                # Obtener los productos de la máquina
                listado_productos = maquina_elem.find('ListadoProductos')
                for producto_elem in listado_productos.findall('Producto'):
                    nombre_producto = producto_elem.find('nombre').text.strip()  # Nombre del producto
                    elaboracion = producto_elem.find('elaboracion').text.strip()  # Elaboración del producto
                    
                    # Crear una instancia del producto y agregarlo a la lista de productos de la máquina
                    producto = Producto(nombre_producto, elaboracion)
                    maquina.productos.agregar(producto)  # Usar el método agregar para añadir el producto
                
                # Agregar la máquina a la lista de máquinas
                self.lista_maquinas.agregar(maquina)  # Usar el método agregar para añadir la máquina

            print("Archivo XML cargado exitosamente.")  # Mensaje de éxito
            self.imprimir_maquinas()  # Imprimir los datos cargados

        except Exception as e:
            print(f"Ocurrió un error al cargar el archivo: {e}")  # Mensaje en caso de error
    
    def imprimir_maquinas(self):
        """Imprime los datos de las máquinas cargadas."""
        actual = self.lista_maquinas.cabeza
        while actual:  # Recorre cada máquina
            maquina = actual.data
            print(f"\nNombre de la máquina: {maquina.nombre_maquina}")
            print(f"Cantidad de líneas de producción: {maquina.cantidad_lineas}")
            print(f"Cantidad de componentes: {maquina.cantidad_componentes}")
            print(f"Tiempo de ensamblaje: {maquina.tiempo_ensamblaje} segundos")
            print("Productos:")
            actual_producto = maquina.productos.cabeza
            while actual_producto:  # Recorre cada producto
                producto = actual_producto.data
                print(f"  - Nombre del producto: {producto.nombre_producto}")
                print(f"    Elaboración: {producto.elaboracion}")
                actual_producto = actual_producto.siguiente  # Avanza al siguiente producto
            actual = actual.siguiente  # Avanza a la siguiente máquina

    def seleccionar_maquina(self):
        """Permite al usuario seleccionar una máquina y luego muestra sus productos."""
        actual_maquina = self.lista_maquinas.cabeza

        if actual_maquina is None:
            print("No hay máquinas cargadas.")
            return

        # Mostrar las máquinas disponibles
        indice_maquina = 1
        while actual_maquina:
            maquina = actual_maquina.data
            print(f"{indice_maquina}. {maquina.nombre_maquina}")
            actual_maquina = actual_maquina.siguiente
            indice_maquina += 1

        # Solicitar al usuario que seleccione una máquina
        opcion_maquina = int(input("Selecciona una máquina (número): ")) - 1

        # Volver a recorrer la lista hasta encontrar la máquina seleccionada
        actual_maquina = self.lista_maquinas.cabeza
        for _ in range(opcion_maquina):
            actual_maquina = actual_maquina.siguiente

        maquina_seleccionada = actual_maquina.data
        nombre_maquina= self.mostrar_productos(maquina_seleccionada)
        return nombre_maquina

    def mostrar_productos(self, maquina):
        """Muestra los productos de una máquina seleccionada."""
        actual_producto = maquina.productos.cabeza

        if actual_producto is None:
            print(f"La máquina {maquina.nombre_maquina} no tiene productos.")
            return

        # Mostrar los productos disponibles
        indice_producto = 1
        while actual_producto:
            producto = actual_producto.data
            print(f"{indice_producto}. {producto.nombre_producto}")
            actual_producto = actual_producto.siguiente
            indice_producto += 1

        # Solicitar al usuario que seleccione un producto
        opcion_producto = int(input("Selecciona un producto (número): ")) - 1

        # Volver a recorrer la lista de productos hasta encontrar el seleccionado
        actual_producto = maquina.productos.cabeza
        for _ in range(opcion_producto):
            actual_producto = actual_producto.siguiente

        producto_seleccionado = actual_producto.data
        print(f"Elaboración del producto {producto_seleccionado.nombre_producto}: {producto_seleccionado.elaboracion}")
        return producto_seleccionado.elaboracion
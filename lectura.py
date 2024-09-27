import xml.etree.ElementTree as ET

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
        self.mostrar_productos(maquina_seleccionada)

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

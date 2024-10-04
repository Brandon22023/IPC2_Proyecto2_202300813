from flask import Flask, render_template, request, redirect, url_for, flash  # Agregué flash para mensajes de error o éxito

import xml.etree.ElementTree as ET
app = Flask(__name__)
app.secret_key = 'clave_secreta_para_flash'  # Necesaria para usar flash (mensajes temporales)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'xml'
@app.route('/')
def home():
    
    return render_template('pagina.html', tab='Tab1')

@app.route('/tab1', methods=['GET', 'POST']) 
def tab1():
    lectura = LecturaXML()
    cola_maquinas = Cola_MAQUINAS()
    cola_productos = Cola_PRODUCTOS()
    elaboracion_producto = None  # Variable para almacenar la elaboración del producto

    if request.method == 'POST':
        # Manejo de archivo
        if 'file' not in request.files:
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            try:
                lectura.cargar_archivo(file)

                # Encolar las máquinas
                actual_maquina = lectura.lista_maquinas.cabeza
                while actual_maquina:
                    cola_maquinas.encolar(actual_maquina.data)
                    actual_maquina = actual_maquina.siguiente

                # Encolar los productos
                actual_producto = lectura.lista_productos.cabeza
                while actual_producto:
                    cola_productos.encolar(actual_producto.data)
                    actual_producto = actual_producto.siguiente

                flash('Archivo cargado exitosamente', 'success')

            except Exception as e:
                flash(f'Ocurrió un error al procesar el archivo: {e}', 'error')
            return redirect(request.url)

        # Manejo de selección de máquina
        else:
            # Suponiendo que estás enviando el índice de la máquina
            indice_maquina = int(request.form.get('maquina_id'))  
            
            # Desencolar las máquinas hasta la seleccionada
            for _ in range(indice_maquina):
                cola_maquinas.encolar(cola_maquinas.desencolar())  # Encolar de nuevo las que no son seleccionadas

            maquina_seleccionada = cola_maquinas.desencolar()  # Ahora seleccionamos la máquina correcta
            
            # Aquí podrías agregar la lógica para mostrar los productos relacionados con la máquina seleccionada
            # Por ejemplo:
            # elaboracion_producto = mostrar_productos(maquina_seleccionada)

    # Renderizar el HTML para la pestaña 1
    return render_template('pagina.html', tab='Tab1', cola_maquinas=cola_maquinas, cola_productos=cola_productos, elaboracion=elaboracion_producto)

@app.route('/tab2')
def tab2():
    return render_template('pagina.html', tab='Tab2')

@app.route('/tab3')
def tab3():
    return render_template('pagina.html', tab='Tab3')

class Nodo_PARA_MAQUINAS:
    def __init__(self, data):
        self.data = data
        self.siguiente = None

class Cola_MAQUINAS:
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def encolar(self, item):
        nuevo_nodo = Nodo_PARA_MAQUINAS(item)
        if self.ultimo:
            self.ultimo.siguiente = nuevo_nodo
        self.ultimo = nuevo_nodo
        if not self.primero:
            self.primero = nuevo_nodo

    def desencolar(self):
        if self.primero is None:
            return None
        item = self.primero.data
        self.primero = self.primero.siguiente
        if self.primero is None:
            self.ultimo = None
        return item

    def esta_vacia(self):
        return self.primero is None

    def tamano(self):
        actual = self.primero
        tamano = 0
        while actual:
            tamano += 1
            actual = actual.siguiente
        return tamano

    # Método para iterar sobre la cola
    def __iter__(self):
        actual = self.primero
        while actual:
            yield actual.data
            actual = actual.siguiente


class Nodo_PARA_PRODUCTOS:
    def __init__(self, data):
        self.data = data
        self.siguiente = None

class Cola_PRODUCTOS:
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def encolar(self, item):
        nuevo_nodo = Nodo_PARA_PRODUCTOS(item)
        if self.ultimo:
            self.ultimo.siguiente = nuevo_nodo
        self.ultimo = nuevo_nodo
        if not self.primero:
            self.primero = nuevo_nodo

    def desencolar(self):
        if self.primero is None:
            return None
        item = self.primero.data
        self.primero = self.primero.siguiente
        if self.primero is None:
            self.ultimo = None
        return item

    def esta_vacia(self):
        return self.primero is None

    def tamano(self):
        actual = self.primero
        tamano = 0
        while actual:
            tamano += 1
            actual = actual.siguiente
        return tamano

    # Método para iterar sobre la cola
    def __iter__(self):
        actual = self.primero
        while actual:
            yield actual.data
            actual = actual.siguiente


#otras clases donde se usan los nodos



class Nodo2:
    def __init__(self, linea, componente):
        self.linea = linea  # Línea de ensamblaje
        self.componente = componente  # Número del componente
        self.siguiente = None  # Apunta al siguiente nodo
        self.anterior = None  # Apunta al nodo anterior
        self.ensamblado = False  # Indica si el componente ha sido ensamblado
    
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
            
    def eliminar(self, nodo):
        if nodo is None:
            return
        
        # Si es el primer nodo
        if nodo == self.primero:
            self.primero = nodo.siguiente
            if self.primero is not None:
                self.primero.anterior = None
        # Si es el último nodo
        elif nodo == self.ultimo:
            self.ultimo = nodo.anterior
            if self.ultimo is not None:
                self.ultimo.siguiente = None
        else:
            # Nodo en medio
            nodo.anterior.siguiente = nodo.siguiente
            nodo.siguiente.anterior = nodo.anterior
        
        nodo.anterior = None
        nodo.siguiente = None

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
    def limpiar(self):
        self.primero = None
        self.ultimo = None
    
    def obtener_max_componente_por_linea(self, linea):
        actual = self.primero
        max_componente = 0
        while actual is not None:
            if actual.linea == linea and actual.componente > max_componente:
                max_componente = actual.componente
            actual = actual.siguiente
        return max_componente
class Contador:
    def __init__(self, linea):
        self.linea = linea
        self.contador = 0
        self.siguiente = None
        self.anterior = None
class ListaContadores:
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def agregar(self, linea):
        nuevo_contador = Contador(linea)
        if self.primero is None:
            self.primero = nuevo_contador
            self.ultimo = nuevo_contador
        else:
            self.ultimo.siguiente = nuevo_contador
            nuevo_contador.anterior = self.ultimo
            self.ultimo = nuevo_contador

    def obtener_contador(self, linea):
        actual = self.primero
        while actual is not None:
            if actual.linea == linea:
                return actual.contador
            actual = actual.siguiente
        return None

    def incrementar_contador(self, linea):
        actual = self.primero
        while actual is not None:
            if actual.linea == linea:
                actual.contador += 1
                return
            actual = actual.siguiente
class ProcesadorElaboracion:
    def __init__(self):
        self.lista_instrucciones = ListaDoblementeEnlazada()

     # Método para procesar la elaboración de un producto sin usar listas, ni índices ni len()
    def procesar_elaboracion(self, elaboracion):
        # PARA REINICIAR LOS VALORES PARA QUE NO HAYA NADA CUANDO SE VUELVA A USAR

        self.lista_instrucciones = ListaDoblementeEnlazada()
        # SE INICIA CON UN PUNTERO PARA IR BUSCANDO LO QUE SE NECESITA
        puntero = iter(elaboracion)

        try:
            while True:
                # Buscamos un caracter "L" que indica una línea
                caracter = next(puntero)
                if caracter == "L":  # Detectamos el inicio de una línea "L"
                    linea = int(next(puntero))  # Obtener el número de la línea
                    # Verificar si el número de la línea es 0
                    if linea == 0:
                        raise ValueError(f"Error: Línea no puede ser 0. Encontrado en L{linea}.")
                        #el raise crea una excepcion para determinar si llego un dato inesperado
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
                        # Verificar si el componente es 0
                        if componente == 0:
                            raise ValueError(f"Error: Componente no puede ser 0. Encontrado en C{componente}.")
                            #el raise crea una excepcion para determinar si llego un dato inesperado
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
        except ValueError as e:
            # Capturamos la excepción para manejar el error sin detener el programa
            print(e)
            print("Por favor, selecciona otro producto.")
            return False  # Retornamos False para indicar que hubo un error

        except StopIteration:
            # Manejar el final del iterador
            if numero:  # Verificar si hay un número acumulado al final
                componente = int(numero)
                # Verificar si el componente es 0
                if componente == 0:
                    raise ValueError(f"Error: Componente no puede ser 0. Encontrado en C{componente}.")
                    #el raise crea una excepcion para determinar si llego un dato inesperado
                
                self.lista_instrucciones.agregar(linea, componente)
                self.lista_instrucciones.buscar_componente(componente)
            pass  # Fin del iterador
         # Generar las instrucciones basadas en los componentes procesados
        self.generar_instrucciones()
        return True  # Retornamos True si todo salió bien
    

    def generar_instrucciones(self):  # Define un método llamado generar_instrucciones.
        # Reiniciar los valores al inicio de la función
        max_componente_global = 0  # Inicializa max_componente_global a 0, que mantendrá el valor del componente más alto.
        max_linea = 0  # Inicializa max_linea a 0, que mantendrá el valor de la línea más alta.
        contador_bloques = 1  # Inicializa contador_bloques a 1, que se usará para llevar el conteo de los bloques de instrucciones.

        # Lista para almacenar ensamblajes pendientes por línea y componente
        ensamblajes_pendientes = ListaDoblementeEnlazada()  # Crea una lista doblemente enlazada para almacenar ensamblajes pendientes.

        # Primer recorrido: obtenemos los máximos componentes por cada línea
        max_por_linea = ListaDoblementeEnlazada()  # Crea una lista doblemente enlazada para almacenar los máximos componentes por línea.
        actual = self.lista_instrucciones.primero  # Inicializa la variable actual con el primer nodo de lista_instrucciones.

        while actual is not None:  # Itera a través de la lista de instrucciones hasta que no haya más elementos.
            # Actualizamos el máximo componente global si es necesario
            if actual.componente > max_componente_global:  # Si el componente actual es mayor que max_componente_global...
                max_componente_global = actual.componente  # Actualiza max_componente_global con el valor del componente actual.

            # Actualizamos el máximo número de línea
            if actual.linea > max_linea:  # Si la línea actual es mayor que max_linea...
                max_linea = actual.linea  # Actualiza max_linea con el valor de la línea actual.

            # Agregar el componente a la lista de máximos por línea
            max_por_linea.agregar(actual.linea, actual.componente)  # Agrega la línea y el componente actual a max_por_linea.

            actual = actual.siguiente  # Avanza al siguiente nodo en la lista de instrucciones.

        # Inicializamos contadores para cada línea
        contadores = ListaContadores()  # Crea una instancia de ListaContadores para manejar contadores para cada línea.
        for linea in range(1, max_linea + 1):  # Itera sobre cada línea desde 1 hasta max_linea.
            contadores.agregar(linea)  # Agrega un contador para cada línea.

        # Generamos las instrucciones agrupadas por línea y componente
        for componente in range(1, max_componente_global + 1):  # Itera sobre cada componente desde 1 hasta max_componente_global.
            print(f"contador {contador_bloques}")  # Imprime el valor actual de contador_bloques.

            # Iterar por cada línea y verificar si se deben realizar movimientos o ensamblajes
            for linea_actual in range(1, max_linea + 1):  # Itera sobre cada línea desde 1 hasta max_linea.
                actual = self.lista_instrucciones.primero  # Reinicia la variable actual al primer nodo de lista_instrucciones.
                movimiento_detectado = False  # Inicializa un flag para detectar si se realizó un movimiento.

                while actual is not None:  # Itera a través de lista_instrucciones hasta que no haya más nodos.
                    if actual.linea == linea_actual and actual.componente == componente:  # Si la línea y el componente coinciden con los actuales...
                        print(f"L{linea_actual}C{componente} = mover brazo componente, listo para ensamblar {componente}")  # Imprime la instrucción de movimiento.
                        movimiento_detectado = True  # Marca que se ha detectado un movimiento.
                        contadores.incrementar_contador(linea_actual)  # Incrementa el contador para la línea actual.
                        # Guardar el ensamblaje para la próxima ronda
                        ensamblajes_pendientes.agregar(actual.linea, actual.componente)  # Agrega el ensamblaje actual a ensamblajes_pendientes.
                    actual = actual.siguiente  # Avanza al siguiente nodo en la lista de instrucciones.

                # Verificar si hay ensamblajes pendientes que deben ser ensamblados para la línea actual
                ensamblaje_actual = ensamblajes_pendientes.primero  # Inicializa ensamblaje_actual con el primer nodo de ensamblajes_pendientes.
                while ensamblaje_actual is not None:  # Itera sobre los ensamblajes pendientes hasta que no haya más nodos.
                    if ensamblaje_actual.componente == componente - 1 and ensamblaje_actual.linea == linea_actual and not ensamblaje_actual.ensamblado:  # Si es el turno de ensamblar el componente anterior...
                        print(f"L{ensamblaje_actual.linea}C{ensamblaje_actual.componente} = ensamblaje {ensamblaje_actual.componente}")  # Imprime la instrucción de ensamblaje.
                        ensamblaje_actual.ensamblado = True  # Marca el componente como ensamblado.
                        contadores.incrementar_contador(ensamblaje_actual.linea)  # Incrementa el contador para la línea del ensamblaje.
                        break  # Rompe el bucle si se encuentra el ensamblaje correspondiente.
                    ensamblaje_actual = ensamblaje_actual.siguiente  # Avanza al siguiente ensamblaje pendiente.
                    
                if not movimiento_detectado:  # Si no se detectó movimiento en la línea actual...
                    max_componente_en_linea = max_por_linea.obtener_max_componente_por_linea(linea_actual)  # Obtiene el componente máximo para la línea actual.
                    if componente <= max_componente_en_linea:  # Si el componente actual es menor o igual que el máximo de la línea...
                        print(f"L{linea_actual}C{componente} = mover brazo componente {componente}")  # Imprime la instrucción de movimiento.
                    else:  # Si no hay componentes para mover...
                        print(f"L{linea_actual}C{componente} = No hacer nada")  # Imprime "No hacer nada" para la línea y componente actual.

            contador_bloques += 1  # Incrementa el contador de bloques.
            print()  # Imprime una línea en blanco como separador entre contadores.
        
        


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
        cola_maquinas = Cola_MAQUINAS()
        actual_maquina = self.lista_maquinas.cabeza

        if actual_maquina is None:
            print("No hay máquinas cargadas.")
            return

        # Encolar todas las máquinas en la cola
        while actual_maquina:
            cola_maquinas.encolar(actual_maquina.data)
            actual_maquina = actual_maquina.siguiente

        # Seleccionar la máquina (para la implementación en Flask, cambiaremos esto)
        maquina_seleccionada = cola_maquinas.desencolar()  # Por ahora tomamos la primera máquina

        # Llamamos a mostrar_productos con la máquina seleccionada
        return self.mostrar_productos(maquina_seleccionada)

    def mostrar_productos(self, maquina):
        """Muestra los productos de una máquina seleccionada."""
        cola_productos = Cola_PRODUCTOS()
        actual_producto = maquina.productos.cabeza

        if actual_producto is None:
            print(f"La máquina {maquina.nombre_maquina} no tiene productos.")
            return

        # Encolar todos los productos de la máquina
        while actual_producto:
            cola_productos.encolar(actual_producto.data)
            actual_producto = actual_producto.siguiente

        # Seleccionar el producto (de forma simplificada tomamos el primero)
        producto_seleccionado = cola_productos.desencolar()

        # Mostrar la elaboración del producto
        return producto_seleccionado.elaboracio


if __name__ == '__main__':  # Verifica si este archivo se está ejecutando directamente
    app.run(debug=True)  # Inicia el servidor Flask en modo debug
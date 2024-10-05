from flask import Flask, render_template, request, redirect, url_for, flash
import xml.etree.ElementTree as ET
app = Flask(__name__)
app.secret_key = 'clave_secreta_para_flash'  # Clave para usar los mensajes flash
# Clases para manejar las colas de máquinas y productos
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

    def __iter__(self):
        actual = self.primero
        while actual:
            yield actual.data
            actual = actual.siguiente

# Clase similar para productos
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

    def __iter__(self):
        actual = self.primero
        while actual:
            yield actual.data
            actual = actual.siguiente

# Clases para manejar máquinas y productos
class Producto:
    def __init__(self, nombre_producto, elaboracion):
        self.nombre_producto = nombre_producto
        self.elaboracion = elaboracion
        self.siguiente = None

class Maquina:
    def __init__(self, nombre_maquina, cantidad_lineas, cantidad_componentes, tiempo_ensamblaje):
        self.nombre_maquina = nombre_maquina
        self.cantidad_lineas = cantidad_lineas
        self.cantidad_componentes = cantidad_componentes
        self.tiempo_ensamblaje = tiempo_ensamblaje
        self.productos = ListaEnlazada()  # Inicializa la lista enlazada para productos

class Nodo:
    def __init__(self, data):
        self.data = data
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def agregar(self, data):
        nuevo_nodo = Nodo(data)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def imprimir(self):
        actual = self.cabeza
        while actual:
            print(actual.data)
            actual = actual.siguiente

    def __iter__(self):
        actual = self.cabeza
        while actual:
            yield actual.data
            actual = actual.siguiente

# Clase para manejar la lectura de XML
class LecturaXML:
    def __init__(self):
        self.lista_maquinas = ListaEnlazada()

    def cargar_archivo(self, ruta_archivo):
        try:
            tree = ET.parse(ruta_archivo)
            root = tree.getroot()
            
            for maquina_elem in root.findall('Maquina'):
                nombre_maquina = maquina_elem.find('NombreMaquina').text.strip()
                cantidad_lineas = int(maquina_elem.find('CantidadLineasProduccion').text.strip())
                cantidad_componentes = int(maquina_elem.find('CantidadComponentes').text.strip())
                tiempo_ensamblaje = int(maquina_elem.find('TiempoEnsamblaje').text.strip())
                
                maquina = Maquina(nombre_maquina, cantidad_lineas, cantidad_componentes, tiempo_ensamblaje)
                
                listado_productos = maquina_elem.find('ListadoProductos')
                for producto_elem in listado_productos.findall('Producto'):
                    nombre_producto = producto_elem.find('nombre').text.strip()
                    elaboracion = producto_elem.find('elaboracion').text.strip()
                    producto = Producto(nombre_producto, elaboracion)
                    maquina.productos.agregar(producto)
                
                self.lista_maquinas.agregar(maquina)

            print("Archivo XML cargado exitosamente.")
            self.imprimir_maquinas()

        except Exception as e:
            print(f"Ocurrió un error al cargar el archivo: {e}")

    def imprimir_maquinas(self):
        actual = self.lista_maquinas.cabeza
        while actual:
            maquina = actual.data
            print(f"\nNombre de la máquina: {maquina.nombre_maquina}")
            print(f"Cantidad de líneas de producción: {maquina.cantidad_lineas}")
            print(f"Cantidad de componentes: {maquina.cantidad_componentes}")
            print(f"Tiempo de ensamblaje: {maquina.tiempo_ensamblaje} segundos")
            print("Productos:")
            actual_producto = maquina.productos.cabeza
            while actual_producto:
                producto = actual_producto.data
                print(f"  - Nombre del producto: {producto.nombre_producto}")
                print(f"    Elaboración: {producto.elaboracion}")
                actual_producto = actual_producto.siguiente
            actual = actual.siguiente

#LOGICA --------------------------
#otras clases donde se usan los nodos

class Nodo_error:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaSimplementeEnlazada:
    def __init__(self):
        self.cabeza = None

    def agregar(self, dato):
        nuevo_nodo = Nodo_error(dato)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def mostrar(self):
        actual = self.cabeza
        while actual:
            print(actual.dato)
            actual = actual.siguiente

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
        self.errores = ListaSimplementeEnlazada()  # Usar lista simplemente enlazada para errores

     # Método para procesar la elaboración de un producto sin usar listas
    def procesar_elaboracion(self, elaboracion):
        # PARA REINICIAR LOS VALORES PARA QUE NO HAYA NADA CUANDO SE VUELVA A USAR

        self.lista_instrucciones = ListaDoblementeEnlazada()
        self.errores = ListaSimplementeEnlazada()  # Reiniciar la lista de errores
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
                        self.errores.agregar(f"Error: Línea no puede ser 0. Encontrado en L{linea}.")
                        return "Error: Línea no puede ser 0."  # Retornar error
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
                            self.errores.agregar(f"Error: Componente no puede ser 0. Encontrado en C{componente}.")
                            return "Error: Componente no puede ser 0."  # Retornar error
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

        except StopIteration:
            # Manejar el final del iterador
            if numero:  # Verificar si hay un número acumulado al final
                componente = int(numero)
                # Verificar si el componente es 0
                if componente == 0:
                    self.errores.agregar(f"Error: Componente no puede ser 0. Encontrado en C{componente}.")
                    return "Error: Componente no puede ser 0."  # Retornar error
                
                self.lista_instrucciones.agregar(linea, componente)
                self.lista_instrucciones.buscar_componente(componente)
            pass  # Fin del iterador
         # Generar las instrucciones basadas en los componentes procesados
        self.generar_instrucciones()
        if self.errores.cabeza:
            actual = self.errores.cabeza
            while actual:
                return actual.dato  # Retornar el mensaje de error

        return None  # Retornar None si no hay errores
    

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

#------------------------
Procesa_elaboracion = ProcesadorElaboracion()
# Función para verificar el tipo de archivo
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'xml'

@app.route('/')
def home():
    return render_template('pagina.html', tab='Tab1')

cola_maquinas = Cola_MAQUINAS()
cola_productos = Cola_PRODUCTOS()

@app.route('/tab1', methods=['GET', 'POST']) 
def tab1():
    lectura = LecturaXML()  # Instancia para manejar la lectura del XML

    if request.method == 'POST':
        # Manejo del archivo
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                flash('No se seleccionó ningún archivo', 'error')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                try:
                    lectura.cargar_archivo(file)  # Carga el archivo XML
                    actual_maquina = lectura.lista_maquinas.cabeza
                    while actual_maquina:
                        cola_maquinas.encolar(actual_maquina.data)  # Agregar a la cola
                        actual_maquina = actual_maquina.siguiente
                    flash('Archivo cargado exitosamente', 'success')
                except Exception as e:
                    flash(f'Ocurrió un error al procesar el archivo: {e}', 'error')
        else:
            # El flujo de selección de productos se maneja en la ruta /productos
            pass

    # Obtener todas las máquinas disponibles para el combobox
    cola_maquinas_temp = Cola_MAQUINAS()  # Crear una cola temporal
    actual_maquina = cola_maquinas.primero
    while actual_maquina:
        cola_maquinas_temp.encolar(actual_maquina.data)  # Usamos la cola para obtener los nombres
        actual_maquina = actual_maquina.siguiente

    return render_template('pagina.html', tab='Tab1', cola_maquinas=cola_maquinas_temp)

@app.route('/productos', methods=['POST'])
def cargar_productos():
    selected_maquina = request.form.get('maquina')  # Obtener la máquina seleccionada del formulario
    selected_producto = request.form.get('producto')  # Obtener el producto seleccionado del formulario
    print("Máquina seleccionada:", selected_maquina)
    print("Producto seleccionado:", selected_producto)
    productos_de_maquina = None

    if selected_maquina:
        # Buscar la máquina en la cola
        actual_maquina = cola_maquinas.primero
        while actual_maquina:
            if actual_maquina.data.nombre_maquina == selected_maquina:
                # Acceder a la lista de productos de la máquina seleccionada
                productos_de_maquina = actual_maquina.data.productos
                break
            actual_maquina = actual_maquina.siguiente

    # Pasamos los productos de la máquina seleccionada al frontend
    return render_template('pagina.html', tab='Tab1', productos=productos_de_maquina, maquina_seleccionada=selected_maquina, producto_seleccionado=selected_producto)

def obtener_elaboracion_producto(producto_seleccionado):
    # Recorrer todas las máquinas para encontrar el producto y su elaboración
    actual_maquina = cola_maquinas.primero
    while actual_maquina:
        maquina = actual_maquina.data
        actual_producto = maquina.productos.cabeza
        while actual_producto:
            producto = actual_producto.data
            if producto.nombre_producto == producto_seleccionado:
                return producto.elaboracion  # Devuelve la elaboración si encuentra el producto
            actual_producto = actual_producto.siguiente
        actual_maquina = actual_maquina.siguiente
    return None  # Devuelve None si no se encuentra el producto
@app.route('/elaboracion', methods=['POST'])
def mostrar_elaboracion():
    selected_producto = request.form.get('producto')  # Obtener el producto seleccionado del formulario
    print("Producto seleccionado:", selected_producto)
    elaboracion = None

    if selected_producto:
        elaboracion = obtener_elaboracion_producto(selected_producto)
        print("Elaboración del producto:", elaboracion)

        # Verificar si se obtuvo la elaboración
        if elaboracion is None:
            flash('No se encontró la elaboración para el producto seleccionado.', 'error')
            return redirect(url_for('tab1'))  # Redirigir a la ruta donde se carga el formulario

        procesador = ProcesadorElaboracion()  # Crear una instancia para procesar la elaboración.
        error = procesador.procesar_elaboracion(elaboracion)  # Procesar la elaboración.

        if error:
            flash(error, 'error')  # Mostrar el error en la interfaz
            return redirect(url_for('tab1'))  # Redirigir a la ruta donde se carga el formulario

    # Pasar la información de elaboración al template
    return render_template('pagina.html', tab='Tab1', producto=selected_producto, elaboracion=elaboracion)
@app.route('/tab2')
def tab2():
    return render_template('pagina.html', tab='Tab2')



@app.route('/tab3')
def tab3():
    return render_template('pagina.html', tab='Tab3')
if __name__ == '__main__':  # Verifica si este archivo se está ejecutando directamente
    app.run(debug=True)  # Inicia el servidor Flask en modo debug
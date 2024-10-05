from flask import Flask, render_template, request, redirect, url_for, flash
import xml.etree.ElementTree as ET
import graphviz
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


class Nodo_c:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaCircular_L:
    def __init__(self):
        self.ultimo = None

    def esta_vacia(self):
        return self.ultimo is None

    def encolar(self, dato):
        nuevo_nodo = Nodo_c(dato)
        if self.esta_vacia():
            self.ultimo = nuevo_nodo
            nuevo_nodo.siguiente = nuevo_nodo  # Apunta a sí mismo
        else:
            nuevo_nodo.siguiente = self.ultimo.siguiente
            self.ultimo.siguiente = nuevo_nodo
            self.ultimo = nuevo_nodo

    def desencolar(self):
        if self.esta_vacia():
            return None
        nodo_salida = self.ultimo.siguiente
        if nodo_salida == self.ultimo:  # Solo hay un nodo
            self.ultimo = None
        else:
            self.ultimo.siguiente = nodo_salida.siguiente
        return nodo_salida.dato
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

class Nodo_2:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class Cola:
    def __init__(self):
        self.frente = None
        self.final = None

    def encolar(self, dato):
        nuevo_nodo = Nodo_2(dato)
        if self.final:
            self.final.siguiente = nuevo_nodo
        self.final = nuevo_nodo
        if not self.frente:
            self.frente = nuevo_nodo

    def desencolar(self):
        if not self.frente:
            return None
        dato = self.frente.dato
        self.frente = self.frente.siguiente
        if not self.frente:
            self.final = None
        return dato

    def esta_vacia(self):
        return self.frente is None
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

class NodoInstruccion:
    def __init__(self, bloque, linea, componente, instruccion):
        self.bloque = bloque
        self.linea = linea
        self.componente = componente
        self.instruccion = instruccion
        self.siguiente = None  # Apunta al siguiente nodo

class ListaCircularSimplementeEnlazada:
    def __init__(self):
        self.primero = None  # Nodo inicial

    def agregar(self, bloque, linea, componente, instruccion):
        nuevo_nodo = NodoInstruccion(bloque, linea, componente, instruccion)
        if self.primero is None:
            self.primero = nuevo_nodo
            nuevo_nodo.siguiente = nuevo_nodo  # Apunta a sí mismo (circular)
        else:
            actual = self.primero
            while actual.siguiente != self.primero:  # Busca el último nodo
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = self.primero  # Apunta al primero para mantener la circularidad

    def obtener_instrucciones(self):
        if self.primero is None:
            return  # No hay instrucciones
        actual = self.primero
        instrucciones_str = ""  # Cadena para almacenar las instrucciones
        while True:
            instrucciones_str += f"{actual.bloque} {actual.linea} {actual.componente} {actual.instruccion}\n"
            print(f"{actual.bloque} {actual.linea} {actual.componente} {actual.instruccion}")
            actual = actual.siguiente
            if actual == self.primero:  # Vuelve al inicio
                break
        return instrucciones_str
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
        self.instrucciones_lista = ListaCircularSimplementeEnlazada()  # Asegúrate de que ListaCircular esté definida correctamente.

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
    

    def generar_instrucciones(self):
        max_componente_global = 0  
        max_linea = 0  
        contador_bloques = 1  
        instrucciones_str = ""  
        ensamblajes_pendientes = ListaDoblementeEnlazada()  
        max_por_linea = ListaDoblementeEnlazada()  
        actual = self.lista_instrucciones.primero  

        # Lista circular para almacenar las instrucciones
        instrucciones_lista = ListaCircularSimplementeEnlazada()  # Usar lista circular

        while actual is not None:  
            if actual.componente > max_componente_global:  
                max_componente_global = actual.componente  

            if actual.linea > max_linea:  
                max_linea = actual.linea  

            max_por_linea.agregar(actual.linea, actual.componente)  
            actual = actual.siguiente  

        contadores = ListaContadores()  
        for linea in range(1, max_linea + 1):  
            contadores.agregar(linea)  

        for componente in range(1, max_componente_global + 1):  
            print(f"contador {contador_bloques}")  

            for linea_actual in range(1, max_linea + 1):  
                actual = self.lista_instrucciones.primero  
                movimiento_detectado = False  

                while actual is not None:  
                    if actual.linea == linea_actual and actual.componente == componente:  
                        instruccion = f"L{linea_actual}C{componente} = mover brazo componente {componente}"
                        movimiento_detectado = True  
                        contadores.incrementar_contador(linea_actual)  
                        ensamblajes_pendientes.agregar(actual.linea, actual.componente)  

                        # Agregar a la lista circular de instrucciones
                        instrucciones_lista.agregar(contador_bloques, linea_actual, componente, instruccion)
                    actual = actual.siguiente  

                ensamblaje_actual = ensamblajes_pendientes.primero  
                while ensamblaje_actual is not None:  
                    if ensamblaje_actual.componente == componente - 1 and ensamblaje_actual.linea == linea_actual and not ensamblaje_actual.ensamblado:  
                        instruccion = f"L{ensamblaje_actual.linea}C{ensamblaje_actual.componente} = ensamblaje {ensamblaje_actual.componente}"
                        instrucciones_str += instruccion + "\n"  
                        ensamblaje_actual.ensamblado = True  
                        contadores.incrementar_contador(ensamblaje_actual.linea)  

                        # Agregar a la lista circular de instrucciones
                        instrucciones_lista.agregar(contador_bloques, ensamblaje_actual.linea, ensamblaje_actual.componente, instruccion)
                        break  
                    ensamblaje_actual = ensamblaje_actual.siguiente  

                if not movimiento_detectado:  
                    max_componente_en_linea = max_por_linea.obtener_max_componente_por_linea(linea_actual)  
                    if componente <= max_componente_en_linea:  
                        instruccion = f"L{linea_actual}C{componente} = mover brazo componente {componente}"
                        instrucciones_str += instruccion + "\n"
                        instrucciones_lista.agregar(contador_bloques, linea_actual, componente, instruccion)  
                    else:  
                        instruccion = f"L{linea_actual}C{componente} = No hacer nada"
                        instrucciones_str += instruccion + "\n"
                        instrucciones_lista.agregar(contador_bloques, linea_actual, componente, instruccion)
            instrucciones_lista.obtener_instrucciones()
            contador_bloques += 1  
            print()  
        print("contenido")
        instrucciones_lista.obtener_instrucciones()
        self.generar_html_tabla()
        # Guardar la lista de instrucciones para uso posterior
        self.instrucciones_lista = instrucciones_lista  # Guardar en un atributo de la clase
        return instrucciones_lista
    
    def generar_html_tabla(self):
        html = "<table border='1'>\n"  
        html += "<tr><th>Bloque</th><th>Línea</th><th>Componente</th><th>Instrucción</th></tr>\n"

        if self.instrucciones_lista.primero is None:
            html += "<tr><td colspan='4'>No hay instrucciones para mostrar</td></tr>\n"
            html += "</table>"
            return html

        actual = self.instrucciones_lista.primero  
        while True:
            # Extrae la información de cada nodo
            bloque = actual.bloque
            linea = actual.linea
            componente = actual.componente
            instruccion = actual.instruccion

            # Agrega una fila a la tabla
            html += "<tr>"
            html += f"<td>{bloque}</td>"
            html += f"<td>{linea}</td>"
            html += f"<td>{componente}</td>"
            html += f"<td>{instruccion}</td>"
            html += "</tr>\n"

            actual = actual.siguiente
            if actual == self.instrucciones_lista.primero:  
                break

        html += "</table>"
        return html

    


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

        # Generar el gráfico de la elaboración
        dot = graphviz.Digraph(comment='Elaboración del Producto', graph_attr={'rankdir': 'LR'})  # Orientación horizontal

        # Crear la lista circular para los bloques de elaboración
        bloques = ListaCircular_L()

        # Separar la cadena en bloques
        partes = elaboracion.split(' ')

        # Encolar cada parte en la lista circular
        for parte in partes:
            bloques.encolar(parte.strip())  # Agregar la parte sin espacios

        # Crear nodos y aristas en el gráfico
        if not bloques.esta_vacia():
            bloque_actual = bloques.desencolar()  # Obtener el primer bloque
            dot.node(bloque_actual, bloque_actual, style='filled', fillcolor='lightblue')  # Color del nodo

            # Preparar contenido para archivo .org
            org_content = "* Elaboración del Producto\n"

            while not bloques.esta_vacia():
                bloque_siguiente = bloques.desencolar()
                dot.node(bloque_siguiente, bloque_siguiente, style='filled', fillcolor='lightgreen')  # Color del nodo
                dot.edge(bloque_actual, bloque_siguiente)
                org_content += f"** {bloque_actual}\n"  # Añadir nodo al contenido de .org
                bloque_actual = bloque_siguiente

            # Añadir el último bloque al contenido de .org
            org_content += f"** {bloque_actual}\n"

        # Renderizar la gráfica
        dot.render('static/elaboracion_producto', format='png')  # Guardar en la carpeta static
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
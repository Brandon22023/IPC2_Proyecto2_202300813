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

    def seleccionar_maquina(self):
        cola_maquinas = Cola_MAQUINAS()
        actual_maquina = self.lista_maquinas.cabeza

        if actual_maquina is None:
            print("No hay máquinas cargadas.")
            return

        while actual_maquina:
            cola_maquinas.encolar(actual_maquina.data)
            actual_maquina = actual_maquina.siguiente

        maquina_seleccionada = cola_maquinas.desencolar()  # Selecciona la primera máquina
        return self.mostrar_productos(maquina_seleccionada)

    def mostrar_productos(self, maquina):
        cola_productos = Cola_PRODUCTOS()
        actual_producto = maquina.productos.cabeza
        if actual_producto is None:
            print(f"La máquina {maquina.nombre_maquina} no tiene productos.")
            return
        while actual_producto:
            cola_productos.encolar(actual_producto.data)
            actual_producto = actual_producto.siguiente
        producto_seleccionado = cola_productos.desencolar()  # Selecciona el primer producto
        return producto_seleccionado.elaboracion  # Devuelve la elaboración del producto

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
    elaboracion_producto = None

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            try:
                if cola_maquinas.esta_vacia():
                    lectura.cargar_archivo(file)  # Carga el archivo XML
                    actual_maquina = lectura.lista_maquinas.cabeza
                    while actual_maquina:
                        cola_maquinas.encolar(actual_maquina.data)  # Agregar a la cola
                        actual_maquina = actual_maquina.siguiente
                    flash('Archivo cargado exitosamente', 'success')
                else:
                    flash('Las colas ya están cargadas', 'info')
            except Exception as e:
                flash(f'Ocurrió un error al procesar el archivo: {e}', 'error')

        # Manejar la selección de máquina
        selected_maquina = request.form.get('maquina')  # Obtener la máquina seleccionada
        if selected_maquina:
            # Buscar la máquina en la cola
            actual_maquina = cola_maquinas.primero
            while actual_maquina:
                if actual_maquina.data.nombre_maquina == selected_maquina:
                    # Mostrar productos de la máquina seleccionada
                    elaboracion_producto = lectura.mostrar_productos(actual_maquina.data)  # Obtener la elaboración del primer producto
                    break
                actual_maquina = actual_maquina.siguiente

    # Obtener todas las máquinas disponibles para el combobox
    cola_maquinas_temp = Cola_MAQUINAS()  # Crear una cola temporal
    actual_maquina = cola_maquinas.primero
    while actual_maquina:
        cola_maquinas_temp.encolar(actual_maquina.data)  # Usamos la cola para obtener los nombres
        actual_maquina = actual_maquina.siguiente

    return render_template('pagina.html', tab='Tab1', cola_maquinas=cola_maquinas_temp, elaboracion=elaboracion_producto)
@app.route('/tab2')
def tab2():
    return render_template('pagina.html', tab='Tab2')

@app.route('/tab3')
def tab3():
    return render_template('pagina.html', tab='Tab3')
if __name__ == '__main__':  # Verifica si este archivo se está ejecutando directamente
    app.run(debug=True)  # Inicia el servidor Flask en modo debug
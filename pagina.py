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
    return render_template('pagina.html', tab='Tab1', productos=productos_de_maquina, maquina_seleccionada=selected_maquina)
@app.route('/tab2')
def tab2():
    return render_template('pagina.html', tab='Tab2')



@app.route('/tab3')
def tab3():
    return render_template('pagina.html', tab='Tab3')
if __name__ == '__main__':  # Verifica si este archivo se está ejecutando directamente
    app.run(debug=True)  # Inicia el servidor Flask en modo debug
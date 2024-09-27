from flask import Flask, render_template, request, redirect, url_for  # Importamos Flask y otras funciones necesarias
import os 

app = Flask(__name__)

# Configuración de la carpeta de subida
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear la carpeta de subida si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
@app.route('/')
def home():
    return render_template('pagina.html', tab='Tab1')

@app.route('/tab1')
def tab1():
    if request.method == 'POST':
        # Verifica si el formulario tiene el archivo
        if 'file' not in request.files:
            return "No se ha seleccionado ningún archivo."
        
        file = request.files['file']
        
        # Si no hay un archivo seleccionado
        if file.filename == '':
            return "No se ha seleccionado ningún archivo."
        
        # Guarda el archivo en la carpeta de subida
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            return f"Archivo {file.filename} cargado exitosamente."
    
    return render_template('pagina.html', tab='Tab1')

@app.route('/tab2')
def tab2():
    return render_template('pagina.html', tab='Tab2')

@app.route('/tab3')
def tab3():
    return render_template('pagina.html', tab='Tab3')

if __name__ == '__main__':  # Verifica si este archivo se está ejecutando directamente
    app.run(debug=True)  # Inicia el servidor Flask en modo debug
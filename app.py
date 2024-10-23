from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'patitoxd'

@app.before_request
def init_session():
    if 'productos' not in session:
        session['productos'] = []

@app.route('/')
def index():
    return render_template('index.html', productos=session['productos'])

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nuevo_id = len(session['productos']) + 1
        nuevo_producto = {
            'id': nuevo_id,
            'nombre': request.form['nombre'],
            'cantidad': request.form['cantidad'],
            'precio': request.form['precio'],
            'fecha_vencimiento': request.form['fecha_vencimiento'],
            'categoria': request.form['categoria']
        }
        session['productos'].append(nuevo_producto)
        session.modified = True
        return redirect(url_for('index'))
    return render_template('agregar_producto.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = next((xd for xd in session['productos'] if xd['id'] == id), None)
    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = request.form['cantidad']
        producto['precio'] = request.form['precio']
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']
        session.modified = True
        return redirect(url_for('index'))
    return render_template('editar_producto.html', producto=producto)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    session['productos'] = [xd for xd in session['productos'] if xd['id'] != id]
    session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

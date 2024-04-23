from flask import Flask, render_template, request
from Arbol import Nodo

app = Flask(__name__)

def buscar_solucion_BFS(conexiones, estado_inicial, solucion):
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    nodoInicial = Nodo(estado_inicial)
    nodos_frontera.append(nodoInicial)
    
    while not solucionado and len(nodos_frontera) != 0:
        nodo = nodos_frontera[0]
        # Extraer a Nodo y añadirlo a visitados 
        nodos_visitados.append(nodos_frontera.pop(0))
        if nodo.get_datos() == solucion:
            # Solucion encontrada
            solucionado = True
            return nodo
        else:
            dato_nodo = nodo.get_datos()
            lista_hijos = []
            for un_hijo in conexiones[dato_nodo]:
                hijo = Nodo(un_hijo)
                if not hijo.en_lista(nodos_visitados) and not hijo.en_lista(nodos_frontera):
                    nodos_frontera.append(hijo)
                    lista_hijos.append(hijo)
            nodo.set_hijos(lista_hijos)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener datos del formulario
        estado_inicial = request.form['estado_inicial']
        solucion = request.form['solucion']

        # Conexiones entre nodos
        conexiones = {
            'CDMX': {'SPL', 'MEXICALI', 'CHIHUAHUA'},
            'ZAPOPAN': {'ZACATECAS', 'MEXICALI'},
            'GUADALAJARA': {'CHIAPAS'},
            'CHIAPAS': {'CHIHUAHUA'},
            'MEXICALI': {'SPL', 'ZAPOPAN', 'CDMX', 'CHIHUAHUA', 'SONORA'},
            'SPL': {'CDMX', 'MEXICALI'},
            'ZACATECAS': {'ZAPOPAN', 'SONORA', 'CHIHUAHUA'},
            'SONORA': {'ZACATECAS', 'MEXICALI'},
            'MICHOACAN': {'CHIHUAHUA'},
            'CHIHUAHUA': {'MICHOACAN', 'ZACATECAS', 'MEXICALI', 'CDMX', 'CHIAPAS'}
        }

        # Realizar la búsqueda BFS
        nodo_solucion = buscar_solucion_BFS(conexiones, estado_inicial, solucion)

        # Reconstruir el camino hacia la solución
        resultado = []
        nodo = nodo_solucion
        while nodo.get_padre() is not None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.append(estado_inicial)
        resultado.reverse()

        return render_template('resultado.html', resultado=resultado)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

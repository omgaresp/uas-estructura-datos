from src.nodo import Nodo

class Arbol:
    def __init__(self):
        # Al crear el árbol, automáticamente crea la carpeta raíz "/"
        self.raiz = Nodo(id="raiz", nombre="/", tipo="carpeta")
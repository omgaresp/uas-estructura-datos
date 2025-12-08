class NodoTrie:
    def __init__(self):
        self.hijos = {}
        self.es_fin_palabra = False

class Trie:
    def __init__(self):
        self.raiz = NodoTrie()

    def insertar(self, palabra):
        # Guarda una palabra en el Trie.
        nodo = self.raiz
        for char in palabra:
            if char not in nodo.hijos:
                nodo.hijos[char] = NodoTrie()
            nodo = nodo.hijos[char]
        nodo.es_fin_palabra = True

    def buscar_por_prefijo(self, prefijo):
        # Retorna una lista de palabras que empiezan con el prefijo dado.
        nodo = self.raiz
        # 1. Bajar hasta el final del prefijo
        for char in prefijo:
            if char not in nodo.hijos:
                return [] # No hay nada con ese prefijo
            nodo = nodo.hijos[char]

        # 2. Recolectar todas las palabras debajo de ese nodo
        resultados = []
        self._recolectar_palabras(nodo, prefijo, resultados)
        return resultados

    def _recolectar_palabras(self, nodo, prefijo_actual, lista_resultados):
        # Función auxiliar recursiva para DFS.
        if nodo.es_fin_palabra:
            lista_resultados.append(prefijo_actual)

        for char, hijo in nodo.hijos.items():
            self._recolectar_palabras(hijo, prefijo_actual + char, lista_resultados)
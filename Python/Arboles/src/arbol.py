from src.nodo import Nodo

class Arbol:
    def __init__(self):
        # Al crear el árbol, automáticamente crea la carpeta raíz "/"
        self.raiz = Nodo(id="raiz", nombre="/", tipo="carpeta")

    def buscar_por_id(self, id_buscado):
        # Punto de entrada público para buscar un nodo.
        return self._buscar_recursivo(self.raiz, id_buscado)

    def _buscar_recursivo(self, nodo_actual, id_buscado):
        # Recorre el árbol buscando el ID.
        # Si nodo_actual es el buscado -> Retorna nodo.
        # Si no -> Busca en sus hijos recursivamente.
        if nodo_actual.id == id_buscado:
            return nodo_actual

        for hijo in nodo_actual.hijos:
            encontrado = self._buscar_recursivo(hijo, id_buscado)
            if encontrado:
                return encontrado

        return None

    def crear_nodo(self, id_padre, nuevo_id, nombre, tipo, contenido=None):
        # Inserta un nuevo nodo bajo el padre especificado.
        # Retorna: True si éxito, False si error.
        # 1. Encontrar al padre
        padre = self.buscar_por_id(id_padre)

        # Validaciones
        if not padre:
            print(f"Error: Padre con ID '{id_padre}' no existe.")
            return False

        if padre.tipo != 'carpeta':
            print(f"Error: '{padre.nombre}' es un archivo, no puede tener hijos.")
            return False

        # Validación de duplicados
        for hijo in padre.hijos:
            if hijo.nombre == nombre:
                print(f"Error: Ya existe '{nombre}' en este directorio.")
                return False

        # 2. Crear y conectar
        nuevo_nodo = Nodo(nuevo_id, nombre, tipo, contenido)
        padre.hijos.append(nuevo_nodo)
        return True
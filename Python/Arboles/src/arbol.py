import json
import os
from src.nodo import Nodo
from src.trie import Trie

class Arbol:
    def __init__(self):
        # Nombre del archivo donde se guardarán los datos
        self.archivo_db = "sistema_arbol.json"

        self.trie = Trie()          # Para autocompletado
        self.indice_ids = {}        # Mapa Hash para búsqueda exacta (ID -> Nodo)

        # Intentar cargar datos existentes al iniciar
        if os.path.exists(self.archivo_db):
            self.cargar_estado()
        else:
            # Si no existe archivo, iniciar con raíz por defecto
            self.raiz = Nodo(id="raiz", nombre="/", tipo="carpeta")
            self.indice_ids["raiz"] = self.raiz
            self.trie.insertar("/")

    def buscar_por_id(self, id_buscado):
        # Punto de entrada público para buscar un nodo.
        return self.indice_ids.get(id_buscado)

    def buscar_autocompletado(self, prefijo):
        # Retorna una lista de nombres que coinciden con el prefijo.
        return self.trie.buscar_por_prefijo(prefijo)

    def crear_nodo(self, id_padre, nuevo_id, nombre, tipo, contenido=None):
        # Encontrar al padre
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

        # Crear y conectar
        nuevo_nodo = Nodo(nuevo_id, nombre, tipo, contenido)
        padre.hijos.append(nuevo_nodo)

        self.indice_ids[nuevo_id] = nuevo_nodo  # Guardar en Hash Map
        self.trie.insertar(nombre)              # Guardar en Trie

        self.guardar_estado()
        return True

    def guardar_estado(self):
        # Escribe el estado actual del árbol en el archivo JSON.
        try:
            data = self.raiz.guardar_dicc() # Convertimos objetos a diccionarios
            with open(self.archivo_db, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4) # Guardamos en disco
            print(" [Sistema] Estado guardado correctamente.")
        except Exception as e:
            print(f" [Error] No se pudo guardar el estado: {e}")

    def cargar_estado(self):
        # Lee el archivo JSON y reconstruye el árbol en memoria.
        try:
            with open(self.archivo_db, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Reconstruimos usando el método estático que creamos en Nodo
                self.raiz = Nodo.cargar_dicc(data)

                self.indice_ids = {}
                self.trie = Trie()
                self._reindexar_recursivo(self.raiz)

            print(" [Sistema] Datos cargados e indexados correctamente.")
        except Exception as e:
            print(f" [Error] Al cargar datos: {e}. Se iniciará un árbol nuevo.")
            self.raiz = Nodo(id="raiz", nombre="/", tipo="carpeta")
            self.indice_ids["raiz"] = self.raiz

    def _reindexar_recursivo(self, nodo):
        # Ayudante para llenar los índices después de cargar del disco.
        self.indice_ids[nodo.id] = nodo  # Agregar al Hash Map
        self.trie.insertar(nodo.nombre)  # Agregar al Trie

        for hijo in nodo.hijos:
            self._reindexar_recursivo(hijo)
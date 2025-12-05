import json
import os
from src.nodo import Nodo

class Arbol:
    def __init__(self):
        # Nombre del archivo donde se guardarán los datos
        self.archivo_db = "sistema_arbol.json"

        # Intentar cargar datos existentes al iniciar
        if os.path.exists(self.archivo_db):
            self.cargar_estado()
        else:
            # Si no existe archivo, iniciar con raíz por defecto
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
        """Lee el archivo JSON y reconstruye el árbol en memoria."""
        try:
            with open(self.archivo_db, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Reconstruimos usando el método estático que creamos en Nodo
                self.raiz = Nodo.cargar_dicc(data)
            print(" [Sistema] Datos cargados del disco exitosamente.")
        except Exception as e:
            print(f" [Error] Al cargar datos: {e}. Se iniciará un árbol nuevo.")
            self.raiz = Nodo(id="raiz", nombre="/", tipo="carpeta")
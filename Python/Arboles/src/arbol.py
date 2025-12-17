import json
import os
from src.nodo import Nodo
from src.trie import Trie

class Arbol:
    def __init__(self):
        # Configuracion de persistencia
        self.archivo_db = "sistema_arbol.json"
        self.archivo_papelera = "papelera.json"

        # Estructuras de datos
        self.trie = Trie()          # Indice para busqueda global
        self.indice_ids = {}        # Hash Map para acceso O(1)
        self.papelera = []          # Papelera de reciclaje

        # Inicializacion
        if os.path.exists(self.archivo_db):
            self.cargar_estado()
        else:
            self.raiz = Nodo(id="raiz", nombre="/", tipo="carpeta")
            self.indice_ids["raiz"] = self.raiz
            self.trie.insertar("/")

        self.nodo_actual = self.raiz

        if os.path.exists(self.archivo_papelera):
            self.cargar_papelera()

    def obtener_nodo_desde_ruta(self, ruta_str):
        # Convierte un string de ruta (ej: "/docs/tarea") en el objeto Nodo correspondiente
        if not ruta_str:
            return None

        # Determinar punto de partida
        if ruta_str.startswith("/"):
            nodo = self.raiz
            partes = ruta_str.strip("/").split("/")
        else:
            nodo = self.nodo_actual
            partes = ruta_str.split("/")

        # Navegar parte por parte
        for parte in partes:
            if not parte or parte == ".":
                continue

            if parte == "..":
                # Subir un nivel
                padre = self.indice_ids.get(nodo.padre_id)
                if padre: nodo = padre
                continue

            # Buscar hijo por nombre
            encontrado = None
            for hijo in nodo.hijos:
                if hijo.nombre == parte:
                    encontrado = hijo
                    break

            if encontrado:
                nodo = encontrado
            else:
                # Si no se encuentra por nombre, verificamos si pasaron un ID directamente
                # Esto mantiene compatibilidad hibrida
                por_id = self.buscar_por_id(parte)
                if por_id:
                    nodo = por_id
                else:
                    return None # Ruta invalida

        return nodo

    def sugerir_rutas(self, texto_parcial):
        # Logica avanzada para autocompletar rutas complejas (ej: /home/do -> /home/documentos)

        # 1. Separar la ruta base del prefijo a completar
        if "/" in texto_parcial:
            ultimo_slash = texto_parcial.rfind("/")
            ruta_base = texto_parcial[:ultimo_slash+1] # ej: "/home/"
            prefijo = texto_parcial[ultimo_slash+1:]   # ej: "do"
        else:
            ruta_base = ""
            prefijo = texto_parcial

        # 2. Obtener el nodo de la ruta base
        # Si la ruta base esta vacia, buscamos en el nodo actual
        nodo_busqueda = self.nodo_actual
        if ruta_base:
            # Caso especial: si es solo "/", es la raiz
            if ruta_base == "/":
                nodo_busqueda = self.raiz
            else:
                nodo_busqueda = self.obtener_nodo_desde_ruta(ruta_base)

        if not nodo_busqueda:
            return []

        # 3. Filtrar hijos que coincidan con el prefijo
        sugerencias = []
        for hijo in nodo_busqueda.hijos:
            if hijo.nombre.startswith(prefijo):
                # Reconstruimos la ruta completa para que el CLI la muestre bien
                # Si ruta_base es vacia, solo devolvemos el nombre. Si no, ruta + nombre
                if ruta_base == "/":
                    full = f"/{hijo.nombre}"
                elif ruta_base:
                    full = f"{ruta_base}{hijo.nombre}"
                else:
                    full = hijo.nombre

                # Si es carpeta, agregamos / al final para UX
                if hijo.tipo == "carpeta":
                    full += "/"

                sugerencias.append(full)

        return sugerencias

    def buscar_por_id(self, id_buscado):
        return self.indice_ids.get(id_buscado)

    def buscar_autocompletado_global(self, prefijo):
        return self.trie.buscar_por_prefijo(prefijo)

    def obtener_ruta_actual(self):
        # Reconstruye la ruta completa navegando hacia arriba
        ruta = []
        temp = self.nodo_actual
        while temp != self.raiz:
            ruta.append(temp.nombre)
            padre = self._buscar_padre_recursivo(self.raiz, temp.id)
            if padre: temp = padre
            else: break
        ruta.append("") # Para el slash inicial
        return "/".join(reversed(ruta)) or "/"

    def _buscar_padre_recursivo(self, nodo_actual, id_hijo_buscado):
        for hijo in nodo_actual.hijos:
            if hijo.id == id_hijo_buscado:
                return nodo_actual
            resultado = self._buscar_padre_recursivo(hijo, id_hijo_buscado)
            if resultado: return resultado
        return None

    def crear_nodo(self, id_padre, nuevo_id, nombre, tipo, contenido=None):
        padre = self.buscar_por_id(id_padre)

        if not padre:
            print(f"Error: Destino no encontrado.")
            return False
        if padre.tipo != 'carpeta':
            print(f"Error: '{padre.nombre}' no es un directorio.")
            return False

        for hijo in padre.hijos:
            if hijo.nombre == nombre:
                print(f"Error: '{nombre}' ya existe aqui.")
                return False

        nuevo_nodo = Nodo(nuevo_id, nombre, tipo, contenido, padre_id=id_padre)
        padre.hijos.append(nuevo_nodo)

        self.indice_ids[nuevo_id] = nuevo_nodo
        self.trie.insertar(nombre)
        self.guardar_estado()
        return True

    def renombrar_nodo(self, id_nodo, nuevo_nombre):
        nodo = self.buscar_por_id(id_nodo)
        if not nodo:
            return False

        if nodo == self.raiz:
            print("Error: No se puede renombrar el directorio raíz.")
            return False

        padre = self.buscar_por_id(nodo.padre_id)
        if not padre:
            print("Error: Estructura corrupta (padre no encontrado).")
            return False

        for hijo in padre.hijos:
            if hijo.nombre == nuevo_nombre:
                print(f"Error: Ya existe un elemento llamado '{nuevo_nombre}' en este directorio.")
                return False

        nodo.nombre = nuevo_nombre

        self.trie = Trie()
        self._reindexar_recursivo(self.raiz)

        self.guardar_estado()
        return True

    def mover_nodo(self, id_nodo, id_nuevo_padre):
        nodo = self.buscar_por_id(id_nodo)
        nuevo_padre = self.buscar_por_id(id_nuevo_padre)

        if not nodo or not nuevo_padre: return False
        if nuevo_padre.tipo != 'carpeta':
            print("Error: El destino debe ser carpeta.")
            return False

        padre_actual = self._buscar_padre_recursivo(self.raiz, id_nodo)
        if padre_actual:
            padre_actual.hijos.remove(nodo)
            nuevo_padre.hijos.append(nodo)
            self.guardar_estado()
            return True
        return False

    def eliminar_nodo(self, id_nodo):
        if id_nodo == "raiz": return False

        nodo = self.buscar_por_id(id_nodo)
        if not nodo: return False

        padre = self._buscar_padre_recursivo(self.raiz, id_nodo)
        if padre:
            nodo.padre_id = padre.id

            padre.hijos.remove(nodo)
            self.papelera.append(nodo)

            if id_nodo in self.indice_ids:
                del self.indice_ids[id_nodo]
            self.guardar_estado()
            self.guardar_papelera()
            return True
        return False

    def restaurar_nodo(self, id_nodo):
        # Buscar en papelera
        nodo_a_restaurar = None
        for n in self.papelera:
            if n.id == id_nodo:
                nodo_a_restaurar = n
                break

        if not nodo_a_restaurar:
            print("Error: Nodo no encontrado en papelera.")
            return False

        # Verificar si el padre original aun existe
        padre_destino = self.buscar_por_id(nodo_a_restaurar.padre_id)

        # Si el padre original no existe (fue borrado tambien), sugerimos raiz o error
        if not padre_destino:
            print(f"Error: La carpeta original (ID: {nodo_a_restaurar.padre_id}) ya no existe.")
            print("Tip: Restaura primero la carpeta contenedora.")
            return False

        # Verificar colision de nombres en destino
        for hijo in padre_destino.hijos:
            if hijo.nombre == nodo_a_restaurar.nombre:
                print(f"Error: Ya existe un '{nodo_a_restaurar.nombre}' en destino.")
                return False

        # Restaurar
        self.papelera.remove(nodo_a_restaurar)
        padre_destino.hijos.append(nodo_a_restaurar)

        # Re-indexar
        self._reindexar_recursivo(nodo_a_restaurar)

        # Limpiar rastro
        nodo_a_restaurar.padre_id = None

        self.guardar_estado()
        self.guardar_papelera()
        return True

    def vaciar_papelera(self):
        self.papelera = []
        self.guardar_papelera()
        return True

    def guardar_estado(self):
        try:
            data = self.raiz.guardar_dicc()
            with open(self.archivo_db, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error I/O: {e}")

    def cargar_estado(self):
        try:
            with open(self.archivo_db, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.raiz = Nodo.cargar_dicc(data)
                self.indice_ids = {}
                self.trie = Trie()
                self._reindexar_recursivo(self.raiz)
        except:
            self.raiz = Nodo(id="raiz", nombre="/", tipo="carpeta")
            self.indice_ids["raiz"] = self.raiz

    def _reindexar_recursivo(self, nodo):
        self.indice_ids[nodo.id] = nodo
        self.trie.insertar(nodo.nombre)
        for hijo in nodo.hijos:
            self._reindexar_recursivo(hijo)

    def guardar_papelera(self):
        try:
            data = [n.guardar_dicc() for n in self.papelera]
            with open(self.archivo_papelera, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except: pass

    def cargar_papelera(self):
        try:
            with open(self.archivo_papelera, 'r', encoding='utf-8') as f:
                d = json.load(f)
                self.papelera = [Nodo.cargar_dicc(x) for x in d]
        except: self.papelera = []
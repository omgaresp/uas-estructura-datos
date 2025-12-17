import sys
import time
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.arbol import Arbol

def rendimiento():
    # 1. Limpieza inicial para test justo
    if os.path.exists("sistema_arbol.json"):
        os.remove("sistema_arbol.json")

    sistema = Arbol()

    CANTIDAD = 5000

    # --- PRUEBA DE ESCRITURA ---
    inicio = time.time()

    # Creamos una carpeta base
    sistema.crear_nodo("raiz", "prueba", "pruebas", "carpeta")
    id_padre = "prueba"

    print(f"Generando {CANTIDAD} archivos...")
    for i in range(CANTIDAD):
        # Creamos archivos tipo: archivo_0, archivo_1, ...
        nombre = f"archivo_{i}"
        nuevo_id = f"id_{i}"
        sistema.crear_nodo(id_padre, nuevo_id, nombre, "archivo", contenido="x")

        # Pequeño log visual cada 100
        if i % 100 == 0:
            print(f"  ... {i} creados")

    fin = time.time()
    print(f"-> Tiempo de escritura: {fin - inicio:.4f} segundos")

    # --- PRUEBA DE BÚSQUEDA (HASH MAP) ---
    print("\nBuscando el último archivo creado (acceso directo por ID)...")
    inicio = time.time()
    nodo = sistema.buscar_por_id(f"id_{CANTIDAD-1}")
    fin = time.time()

    if nodo:
        print(f"-> Encontrado: {nodo.nombre}")
        print(f"-> Tiempo de búsqueda O(1): {fin - inicio:.6f} segundos")
    else:
        print("ERROR: No se encontró el nodo.")

    # --- PRUEBA DE BÚSQUEDA (TRIE) ---
    print("\nBuscando sugerencias en el Trie (prefijo 'archivo_499')...")
    inicio = time.time()
    resultados = sistema.buscar_autocompletado_global("archivo_499")
    fin = time.time()
    print(f"-> Resultados encontrados: {len(resultados)}")
    print(f"-> Tiempo de búsqueda Trie: {fin - inicio:.6f} segundos")

if __name__ == "__main__":
    rendimiento()
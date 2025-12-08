import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.arbol import Arbol

def pruebas_indices():
    print("=== PRUEBAS TRIE Y HASH MAP (DÍA 5-6) ===")

    # Borrar DB anterior para prueba limpia
    if os.path.exists("sistema_archivos.json"):
        os.remove("sistema_archivos.json")

    sistema = Arbol()

    # 1. Poblar el sistema con nombres similares para probar el Trie
    print("\n[Paso 1] Creando archivos con nombres similares...")
    sistema.crear_nodo("raiz", "d1", "documentos", "carpeta")
    sistema.crear_nodo("d1", "f1", "declaracion_impuestos.pdf", "archivo")
    sistema.crear_nodo("d1", "f2", "declaracion_amor.txt", "archivo")
    sistema.crear_nodo("d1", "f3", "demo_juego.exe", "archivo")
    sistema.crear_nodo("raiz", "d2", "descargas", "carpeta")

    # 2. Prueba de Autocompletado (Trie)
    print("\n[Paso 2] Probando Autocompletado (Prefijo: 'dec')...")
    sugerencias = sistema.buscar_autocompletado("dec")
    print(f"   -> Sugerencias encontradas: {sugerencias}")

    esperados = ["declaracion_impuestos.pdf", "declaracion_amor.txt"]
    # Verificamos si todos los esperados están en las sugerencias
    if all(item in sugerencias for item in esperados):
        print("   -> PASS: El Trie encontró las coincidencias correctas.")
    else:
        print("   -> FAIL: Faltan sugerencias.")

    # 3. Prueba de Autocompletado Carpeta
    print("\n[Paso 3] Probando Autocompletado (Prefijo: 'do')...")
    sugerencias = sistema.buscar_autocompletado("do")
    print(f"   -> Sugerencias: {sugerencias}")
    if "documentos" in sugerencias:
        print("   -> PASS: Encontró la carpeta 'documentos'.")
    else:
        print("   -> FAIL: No encontró 'documentos'.")

    # 4. Prueba de Búsqueda Exacta (Hash Map)
    print("\n[Paso 4] Probando Búsqueda Exacta por ID (Hash Map)...")
    # Buscamos 'f3' (demo_juego.exe)
    nodo = sistema.buscar_por_id("f3")
    if nodo and nodo.nombre == "demo_juego.exe":
        print(f"   -> PASS: Búsqueda Hash exitosa. Nodo: {nodo}")
    else:
        print("   -> FAIL: El Mapa Hash falló.")

    # 5. Prueba de Persistencia de Índices
    print("\n[Paso 5] Reiniciando sistema para verificar re-indexado...")
    del sistema
    sistema_nuevo = Arbol() # Debería cargar y reconstruir Trie/Hash

    # Intentar autocompletar en el sistema reiniciado
    res = sistema_nuevo.buscar_autocompletado("desc")
    if "descargas" in res:
        print("   -> PASS: El Trie se reconstruyó correctamente tras cargar JSON.")
    else:
        print("   -> FAIL: El Trie está vacío después del reinicio.")

if __name__ == "__main__":
    pruebas_indices()
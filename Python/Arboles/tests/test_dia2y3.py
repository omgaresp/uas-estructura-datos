import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.arbol import Arbol

def correr_pruebas():
    print("=== INICIANDO PRUEBAS (Día 2-3) ===")
    sistema = Arbol()

    print("\n[Test 1] Verificando inicialización del Sistema...")
    if sistema.raiz and sistema.raiz.id == "raiz" and sistema.raiz.tipo == "carpeta":
        print("   -> PASS: Raíz creada e identificada correctamente.")
    else:
        print("   -> FAIL: El árbol no se inicializó bien.")

    print("\n[Test 2] Insertar carpeta 'inicio' en raíz...")
    if sistema.crear_nodo("raiz", "carpeta_inicio", "inicio", "carpeta"):
        print("   -> PASS: Carpeta creada.")
    else:
        print("   -> FAIL: Error al crear carpeta.")

    print("\n[Test 3] Insertar archivo 'notas.txt' dentro de 'inicio'...")
    # Usamos el ID "carpeta_inicio" que creamos en el paso anterior
    if sistema.crear_nodo("carpeta_inicio", "archivo_notas", "notas.txt", "archivo", "Recordar tarea"):
        print("   -> PASS: Archivo anidado creado exitosamente.")
    else:
        print("   -> FAIL: Error al anidar archivo.")

    print("\n[Test 4] Intentar insertar en un ID que no existe ('ghost')...")
    if not sistema.crear_nodo("ghost_id", "fail", "test", "carpeta"):
        print("   -> PASS: El sistema detectó que el padre no existe.")
    else:
        print("   -> FAIL: Se permitió insertar en el limbo.")

    print("\n[Test 5] Intentar agregar una carpeta DENTRO de un archivo ('notas.txt')...")
    # Los archivos no pueden tener hijos. Esto debe fallar.
    if not sistema.crear_nodo("archivo_notas", "carpeta_fail", "subcarpeta", "carpeta"):
        print("   -> PASS: Correcto. No se puede insertar dentro de un archivo.")
    else:
        print("   -> FAIL: El sistema permitió agregar hijos a un archivo.")

    print("\n[Test 6] Intentar crear duplicado 'notas.txt' en 'inicio'...")
    if not sistema.crear_nodo("carpeta_inicio", "archivo_clon", "notas.txt", "archivo"):
        print("   -> PASS: El sistema bloqueó el nombre duplicado.")
    else:
        print("   -> FAIL: El sistema permitió nombres repetidos.")

    print("\n=== FIN DE PRUEBAS ===")

if __name__ == "__main__":
    correr_pruebas()
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.arbol import Arbol

def assert_true(condicion, mensaje):
    if condicion:
        print(f"[OK] {mensaje}")
    else:
        print(f"[FALLO] {mensaje}")

def casos_limite():
    if os.path.exists("sistema_arbol.json"):
        os.remove("sistema_arbol.json")
    if os.path.exists("papelera.json"):
        os.remove("papelera.json")

    print("--- INICIANDO TEST DE INTEGRACIÓN Y BORDES ---")
    app = Arbol()

    # CASO 1: Nombres duplicados
    print("\n1. Test de Duplicados")
    app.crear_nodo("raiz", "c1", "carpeta1", "carpeta")
    exito = app.crear_nodo("raiz", "c2", "carpeta1", "carpeta") # Mismo nombre, ID distinto
    assert_true(not exito, "No debe permitir nombres duplicados en el mismo padre")

    # CASO 2: Mover carpeta dentro de un archivo (Ilógico)
    print("\n2. Test Mover Ilegal")
    app.crear_nodo("c1", "f1", "archivo.txt", "archivo") # Archivo dentro de carpeta1
    # Intentamos mover carpeta1 DENTRO de archivo.txt
    exito = app.mover_nodo("c1", "f1")
    assert_true(not exito, "No se puede mover algo dentro de un archivo")

    # CASO 3: Papelera y Restauración "Huérfana"
    print("\n3. Test Restauración Huérfana")
    # Estructura: /carpeta1/subcarpeta/
    app.crear_nodo("c1", "sub1", "subcarpeta", "carpeta")

    # Eliminamos la subcarpeta (va a papelera)
    app.eliminar_nodo("sub1")

    # Eliminamos al PADRE (carpeta1) (va a papelera)
    app.eliminar_nodo("c1")

    # Intentamos restaurar la HIJA (subcarpeta)
    # Debería fallar o advertir porque su padre (carpeta1) ya no está en el árbol activo
    exito = app.restaurar_nodo("sub1")
    assert_true(not exito, "No se debe restaurar si el padre original no existe")

    # CASO 4: Profundidad y Rutas relativas
    print("\n4. Test Rutas Relativas (..)")
    # Reconstruimos estructura
    app = Arbol() # Reinicio rapido
    app.crear_nodo("raiz", "A", "A", "carpeta")
    app.crear_nodo("A", "B", "B", "carpeta")

    # Simulamos navegación
    app.nodo_actual = app.buscar_por_id("B") # Estamos en /A/B
    nodo_destino = app.obtener_nodo_desde_ruta("..") # Debería ser A

    assert_true(nodo_destino.nombre == "A", "La ruta '..' debe llevar al padre")

if __name__ == "__main__":
    casos_limite()
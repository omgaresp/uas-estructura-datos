import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.arbol import Arbol

def prueba_persistencia():
    print("=== PRUEBA DE PERSISTENCIA (DÍA 4) ===")
    
    # 1. Crear sistema y agregar datos
    print("\n[Paso 1] Iniciando sistema y creando datos...")
    sistema = Arbol()
    # Nota: Como borramos el archivo JSON al inicio (si existiera), esto empieza limpio
    sistema.crear_nodo("raiz", "dir_fotos", "fotos", "carpeta")
    sistema.crear_nodo("dir_fotos", "foto1", "vacaciones.jpg", "archivo")
    print("   -> Datos creados y guardados automáticamente.")

    # 2. Simular 'Apagado' (Eliminar el objeto de memoria)
    print("\n[Paso 2] Cerrando el sistema (Eliminando objeto de memoria)...")
    del sistema 
    
    # 3. Reiniciar (Crear nuevo objeto Arbol)
    print("\n[Paso 3] Reiniciando sistema (Debe cargar el JSON automáticamente)...")
    sistema_nuevo = Arbol()
    
    # 4. Verificar si los datos siguen ahí
    print("\n[Paso 4] Verificando si 'vacaciones.jpg' sobrevivió...")
    nodo = sistema_nuevo.buscar_por_id("foto1")
    
    if nodo and nodo.nombre == "vacaciones.jpg":
        print(f"   -> ¡ÉXITO! Se encontró: {nodo}")
        print("   -> La persistencia funciona correctamente.")
    else:
        print("   -> ERROR: No se encontraron los datos previos.")

if __name__ == "__main__":
    # Limpieza previa para la prueba (borrar json viejo si existe)
    if os.path.exists("sistema_archivos.json"):
        os.remove("sistema_archivos.json")
        
    prueba_persistencia()
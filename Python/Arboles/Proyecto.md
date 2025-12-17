# Simulador de Sistema de Archivos (Python)

> Un sistema de archivos virtual en consola implementado con Árboles Generales, Tries y Hash Maps.

## Descripción

Este proyecto simula la gestión jerárquica de archivos y carpetas de un sistema operativo (tipo Unix/Linux). A diferencia de una simulación simple, este sistema implementa **persistencia de datos en JSON** y utiliza estructuras de datos avanzadas para optimizar la búsqueda y el autocompletado.

## Estructura del Proyecto

```text
.
├── main.py           # Punto de entrada
├── sistema_arbol.json # Base de datos (Persistencia)
├── papelera.json     # Persistencia de eliminados
└── src/
    ├── arbol.py      # Lógica del Árbol y gestión de estado
    ├── cli.py        # Interfaz de Línea de Comandos (Cmd)
    ├── nodo.py       # Clase Nodo y serialización
    └── trie.py       # Estructura para búsqueda por prefijos
```

## Características Técnicas

* **Árbol General (N-ary Tree):** Modela la jerarquía de directorios.
* **Trie (Prefix Tree):** Motor de autocompletado y sugerencias de rutas en tiempo real.
* **Hash Map (Diccionario):** Acceso O(1) a cualquier nodo del sistema mediante IDs únicos.
* **Persistencia:** Serialización y deserialización recursiva a JSON.
* **Papelera de Reciclaje:** Eliminación lógica con capacidad de restauración.

## Proyecto

* [x] **Día 1:** Definir alcance mínimo (MVP), estructuras de datos y formato JSON.
* [x] **Día 2–3:** Implementar árbol general y operaciones básicas; pruebas unitarias
iniciales.
* [x] **Día 4:** Implementar persistencia (guardar/cargar JSON).
* [x] **Día 5–6:** Implementar Trie y endpoints de búsqueda/autocompletado; integrar con operaciones de árbol.
* [X] **Día 7–9:** Interfaz de consola completa y comandos; manejo de errores y papelera.
* [X] **Día 10–11:** Pruebas de integración, casos límite y performance con árboles grandes.
* [X] **Día 12:** Documentación de uso y README.
* [X] **Día 13:** Preparar demo y script de ejecución.
* [ ] **Día 14:** Presentación y retroalimentación.

## Guía de Comandos

| Comando | Argumentos | Descripción |
| :--- | :--- | :--- |
| `ls` | `[ruta]` | Lista el contenido del directorio actual o la ruta especificada. |
| `tree` | `[ruta]` | Muestra todo el arbol del directorio actual o la ruta especificada. |
| `cd` | `<ruta>` | Cambia el directorio actual. Soporta `..` para subir de nivel. |
| `mkdir` | `<nombre>` | Crea un nuevo directorio. |
| `touch` | `<nombre> [texto]` | Crea un archivo, opcionalmente con contenido. |
| `rename` | `<ruta> <nuevo_nombre>` | Renombra el archivo o carpeta indicado. |
| `mv` | `<origen> <destino>` | Mueve un archivo o carpeta a otra ubicación. |
| `rm` | `<ruta>` | Elimina un archivo o carpeta (envía a papelera). |
| `find` | `<prefijo>` | Busca globalmente archivos que coincidan con el prefijo (Usa Trie). |
| `lspap` | - | Lista el contenido de la papelera de reciclaje. |
| `restore`| `<id>` | Restaura un elemento eliminado dado su ID. |
| `clpap` | - | Vacía la papelera definitivamente. |
| `cls` | - | Limpiar Pantalla. |
| `exit` | - | Guarda cambios y cierra el programa. |

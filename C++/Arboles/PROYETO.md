# Gestor de Números con Árbol Binario de Búsqueda (BST)

Este proyecto implementa una aplicación de consola en C++ para gestionar un Árbol Binario de Búsqueda (BST). Permite la manipulación dinámica de nodos y visualización de recorridos, cumpliendo con los objetivos de aprendizaje de la materia de Estructura de Datos.

## Descripción

El sistema utiliza punteros para enlazar nodos dinámicamente. Cada nodo contiene un valor entero (`key`) y referencias a sus subárboles izquierdo y derecho.

### Estructuras de Datos

* **Nodo:** Estructura autorreferenciada con punteros `left` y `right`.
* **BST (Binary Search Tree):** Clase controladora que encapsula la lógica recursiva y mantiene el puntero a la `root` (raíz).

## Estructura del Proyecto

```text
.
├── PROYECTO.md
├── main.cpp          Interfaz de usuario y menú
└── src/
    ├── nodo.h        Definición de estructura
    ├── BST.h         Definición de la clase y métodos
    └── BST.cpp       Lógica e implementación
```

## Guía de Comandos

| Comando | Descripción | Complejidad |
| :--- | :--- | :--- |
| `insert <n>` | Agrega un valor único al árbol manteniendo el orden ($izq < raiz < der$). | $O(h)$ |
| `search <n>` | Busca un valor y muestra la ruta de acceso. | $O(h)$ |
| `delete <n>` | Elimina un nodo manejando los 3 casos (Hoja, 1 hijo, 2 hijos). | $O(h)$ |
| `inorder` | Muestra el recorrido In-Orden (Ascendente). | $O(n)$ |
| `preorder` | Muestra el recorrido Pre-Orden (Raíz-Izq-Der). | $O(n)$ |
| `postorder` | Muestra el recorrido Post-Orden (Izq-Der-Raíz). | $O(n)$ |
| `height` | Calcula la altura máxima del árbol (raíz a hoja más lejana). | $O(n)$ |
| `size` | Cuenta el número total de nodos en el árbol. | $O(n)$ |
| `export` | Guarda el recorrido In-Orden en un archivo de texto. | $O(n)$ |

## Caso de Prueba (Validación)

**Secuencia de inserción recomendada para validar la lógica:**
`45 -> 15 -> 79 -> 90 -> 10 -> 55 -> 12 -> 20 -> 50`

**Resultado esperado (In-Orden):**
`10 12 15 20 45 50 55 79 90`

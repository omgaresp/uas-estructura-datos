# Manual Técnico: Sistema de Archivos en Árboles

## 1. Arquitectura del Sistema

El proyecto sigue una arquitectura modular que separa la interfaz de usuario, la lógica de negocio y los modelos de datos para facilitar su mantenimiento y escalabilidad.

### Diagrama de Módulos

* **`main.py`**: Punto de entrada. Inicializa la interfaz de línea de comandos (CLI).
* **`src/cli.py` (Vista/Controlador):** Implementa la interfaz de usuario utilizando la librería estándar `cmd`. Se encarga de procesar la entrada del usuario y llamar a los métodos correspondientes de la clase `Arbol`.
* **`src/arbol.py` (Lógica/Modelo):** Clase principal que gestiona las operaciones del sistema. Contiene el Árbol General, el Hash Map de accesos directos y el Trie de búsqueda. También maneja la persistencia de datos (entrada/salida).
* **`src/nodo.py` (Estructura Base):** Define la unidad fundamental de almacenamiento, representando tanto archivos como carpetas.
* **`src/trie.py` (Índice):** Estructura auxiliar diseñada para optimizar las búsquedas por prefijo.

---

## 2. Estructuras de Datos Implementadas

### A. Árbol General (N-ary Tree)

El núcleo del sistema es un árbol general donde cada nodo puede tener $N$ hijos. A diferencia de un árbol binario, no existe un límite predefinido en la cantidad de subdirectorios o archivos que una carpeta puede contener.

* **Implementación:** Clase `Nodo` en `src/nodo.py`.
* **Atributos Clave:**
  * `self.hijos`: Una lista dinámica (`list`) que almacena las referencias a los nodos hijos.
  * `self.padre_id`: Una referencia al identificador del nodo contenedor. Esto permite la navegación hacia atrás (comando `cd ..`) y es fundamental para la lógica de restauración desde la papelera.

### B. Tabla Hash (Diccionario)

Para optimizar el rendimiento y evitar una complejidad de $O(N)$ (donde $N$ es el total de nodos) al buscar un archivo específico, se mantiene un índice paralelo.

* **Implementación:** `self.indice_ids = {}` en `src/arbol.py`.
* **Funcionamiento:** Asocia el identificador único (`id`) de cada nodo directamente a su objeto en memoria.
* **Beneficio:** Permite que operaciones como `cd`, `rm` o `mv`, que actúan sobre un destino conocido, tengan un tiempo de acceso promedio de **$O(1)$**, evitando la necesidad de recorrer el árbol desde la raíz.

### C. Trie (Árbol de Prefijos)

Se utiliza un Trie para indexar los nombres de todos los archivos y carpetas, facilitando funciones de autocompletado y búsqueda global eficiente.

* **Implementación:** Clase `Trie` en `src/trie.py`.
* **Funcionamiento:** Cada nodo del Trie representa un carácter. Al insertar un nombre de archivo, se recorre la estructura carácter por carácter creando la ruta correspondiente.
* **Caso de uso:** Comando `find <prefijo>` y autocompletado interno. La búsqueda toma un tiempo proporcional a la longitud de la palabra buscada $O(L)$, independientemente de la cantidad total de archivos en el sistema.

---

## 3. Persistencia y Serialización

El sistema implementa persistencia completa utilizando el formato **JSON**, cumpliendo con los requisitos funcionales del proyecto.

### Estrategia de Guardado

Se utiliza una estrategia de **serialización recursiva**:

1. El método `guardar_estado()` en `Arbol` invoca a `guardar_dicc()` comenzando desde la raíz.
2. Cada `Nodo` se convierte a un diccionario de Python y llama recursivamente a la función de guardado en todos sus hijos.
3. El resultado es un único objeto JSON anidado que representa la jerarquía completa del sistema.

### Archivos Generados

* `sistema_arbol.json`: Almacena la estructura del árbol activa.
* `papelera.json`: Almacena una lista plana de los nodos que han sido eliminados.

---

## 4. Lógica de Algoritmos Complejos

### Navegación (`cd` y resolución de rutas)

El método `obtener_nodo_desde_ruta` en `arbol.py` implementa un analizador de rutas similar al de sistemas Unix:

1. Divide la ruta utilizando el carácter separador `/`.
2. Itera sobre los componentes de la ruta:
   * Si el componente es `..`, utiliza `indice_ids` para saltar al nodo padre (`padre_id`).
   * Si es un nombre, realiza una búsqueda lineal en los `hijos` del nodo actual.
   * El sistema soporta tanto rutas absolutas (iniciando en raíz) como relativas.

### Papelera de Reciclaje y Restauración

La eliminación se maneja como un borrado lógico (*Soft Delete*).

1. **Eliminar (`rm`):** El nodo se desconecta de la lista `hijos` de su padre y se transfiere a la lista `self.papelera`. Se conserva la referencia de quién era su nodo padre.
2. **Restaurar (`restore`):**
   * Se verifica si el `padre_id` original aún existe en el árbol activo.
   * Si el padre existe, el nodo se reintegra a la lista de hijos de dicho padre.
   * Se ejecuta `_reindexar_recursivo` para volver a agregar el nodo y todos sus descendientes al `indice_ids` y al `Trie`.

---

## 5. Análisis de Complejidad (Big O)

| Operación | Estructura | Complejidad Promedio | Descripción |
| :--- | :--- | :--- | :--- |
| **Insertar (`mkdir`/`touch`)** | Árbol + Hash + Trie | $O(L)$ | Depende de la longitud del nombre para insertar en el Trie. La inserción en Hash es $O(1)$. |
| **Buscar (`find`)** | Trie | $O(P)$ | Donde $P$ es la longitud del prefijo buscado. Resulta altamente eficiente. |
| **Navegar (`cd`)** | Árbol | $O(R \cdot H)$ | Donde $R$ es la cantidad de segmentos en la ruta y $H$ el promedio de hijos por carpeta. |
| **Eliminar (`rm`)** | Hash Map | $O(1)$ | Acceso directo al nodo para su desconexión. |
| **Guardar Estado** | Recursión | $O(N)$ | Requiere recorrer todos los nodos ($N$) para serializar la estructura a JSON. |

---

## 6. Cobertura de Requisitos

Este desarrollo satisface las especificaciones estipuladas para el "Proyecto 1 de árboles":

* **Árbol General:** Implementación completa en `nodo.py`.
* **Persistencia JSON:** Funcionalidad asegurada en `arbol.py`.
* **Búsqueda (Trie y Hash):** Integrada para autocompletado y acceso rápido a elementos.
* **Operaciones CRUD:** Comandos `mkdir`, `touch`, `mv`, `rm` implementados en la capa de lógica y vista.
* **Papelera de Reciclaje:** Funcionalidad completa de listado (`lspap`), restauración (`restore`) y vaciado (`clpap`).

---

# Proyecto: Sistema de Archivos en Árboles

[Informacion del Proyecto (PDF)](7.%20Proyecto%201%20de%20árboles.pdf)

## MVP: Sistema de Archivos en Consola

Aplicación de consola que simula la gestión jerárquica de archivos y carpetas, implementando estructuras de datos avanzadas y persistencia.

### 1. Núcleo del Sistema

* **Árbol General:** Estructura principal en memoria RAM para modelar la jerarquía de directorios.
* **Persistencia JSON:** Motor de carga y guardado automático para mantener el estado del árbol en un archivo local entre ejecuciones.

### 2. Gestión de Datos y Operaciones

* **CRUD Completo:** Comandos para crear, mover, renombrar y listar contenidos.
* **Papelera de Reciclaje:** Implementación de eliminación lógica temporal con capacidad de restauración o purgado definitivo.
* **Exportación:** Generación de reportes de la estructura utilizando recorrido en **Preorden**.

### 3. Motores de Búsqueda Optimizados

* **Trie (Árbol de Prefijos):** Índice auxiliar para autocompletado rápido de nombres de archivos/carpetas.
* **Tabla Hash:** Mecanismo para búsquedas exactas eficientes por ID o nombre completo.

### 4. Interfaz de Usuario

* **Menú Interactivo:** Consola continua que procesa comandos tipo Unix/Linux.
* **UX/Manejo de Errores:** Validaciones de consistencia (rutas duplicadas, destinos inválidos) y retroalimentación clara al usuario.

## Proyecto

* [x] **Día 1:** Definir alcance mínimo (MVP), estructuras de datos y formato JSON.
* [ ] **Día 2–3:** Implementar árbol general y operaciones básicas; pruebas unitarias
iniciales.
* [ ] **Día 4:** Implementar persistencia (guardar/cargar JSON).
* [ ] **Día 5–6:** Implementar Trie y endpoints de búsqueda/autocompletado; integrar con operaciones de árbol.
* [ ] **Día 7–9:** Interfaz de consola completa y comandos; manejo de errores y papelera.
* [ ] **Día 10–11:** Pruebas de integración, casos límite y performance con árboles grandes.
* [ ] **Día 12:** Documentación de uso y README.
* [ ] **Día 13:** Preparar demo y script de ejecución.
* [ ] **Día 14:** Presentación y retroalimentación.

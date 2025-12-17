import cmd
import os
from src.arbol import Arbol

class CLI(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.sistema = Arbol()
        self.intro = """
=========================================
SISTEMA DE ARCHIVOS - ESTRUCTURA DE DATOS
=========================================
        """
        self._actualizar_prompt()

    def _actualizar_prompt(self):
        # Muestra la ruta completa estilo Linux
        ruta = self.sistema.obtener_ruta_actual()
        self.prompt = f"{ruta} $ "

    def iniciar(self):
        try:
            self.cmdloop()
        except KeyboardInterrupt:
            print("\nSaliendo...")

    def _completar_rutas(self, text):
        return self.sistema.sugerir_rutas(text)

    def do_ls(self, arg):
        nodo_objetivo = self.sistema.nodo_actual

        if arg:
            nodo_resuelto = self.sistema.obtener_nodo_desde_ruta(arg)
            if nodo_resuelto:
                if nodo_resuelto.tipo == "carpeta":
                    nodo_objetivo = nodo_resuelto
                else:
                    print(f"Error: '{arg}' no es un directorio.")
                    return
            else:
                print(f"Error: Ruta '{arg}' no encontrada.")
                return

        print(f"Directorio: {nodo_objetivo.nombre}")
        if not nodo_objetivo.hijos:
            print("  (vacio)")
        for hijo in nodo_objetivo.hijos:
            tag = "[CARPETA]" if hijo.tipo == "carpeta" else "[ARCHIVO]"
            print(f"  {tag} {hijo.nombre} (ID: {hijo.id})")

    def complete_ls(self, text, line, begidx, endidx):
        return self._completar_rutas(text)

    def do_cd(self, arg):
        if not arg: return

        nodo = self.sistema.obtener_nodo_desde_ruta(arg)

        if nodo:
            if nodo.tipo == "carpeta":
                self.sistema.nodo_actual = nodo
                self._actualizar_prompt()
            else:
                print(f"Error: '{nodo.nombre}' es un archivo.")
        else:
            print(f"Error: Ruta no encontrada.")

    def complete_cd(self, text, line, begidx, endidx):
        return self._completar_rutas(text)

    def do_mkdir(self, arg):
        # Soporta rutas: mkdir /home/nuevo  o  mkdir nuevo
        args = arg.split()
        if not args:
            print("Uso: mkdir <ruta/nombre>")
            return

        ruta_completa = args[0]

        # Logica para separar padre e hijo
        if "/" in ruta_completa:
            # Si es ruta compleja (ej: A/B/C), el padre es A/B y el nuevo es C
            ultimo_slash = ruta_completa.rfind("/")
            ruta_padre = ruta_completa[:ultimo_slash] or "/"
            nombre_nuevo = ruta_completa[ultimo_slash+1:]

            nodo_padre = self.sistema.obtener_nodo_desde_ruta(ruta_padre)
        else:
            # Ruta simple, padre es actual
            nodo_padre = self.sistema.nodo_actual
            nombre_nuevo = ruta_completa

        if nodo_padre:
            nuevo_id = f"carpeta_{nombre_nuevo}" # Generacion simple de ID
            if self.sistema.crear_nodo(nodo_padre.id, nuevo_id, nombre_nuevo, "carpeta"):
                print(f"Creado: {nombre_nuevo}")
        else:
            print("Error: Ruta contenedora no existe.")

    def complete_mkdir(self, text, line, begidx, endidx):
        # Autocompletamos la ruta donde se quiere crear
        return self._completar_rutas(text)

    def do_touch(self, arg):
        # Igual que mkdir pero para archivos
        args = arg.split()
        if not args:
            print("Uso: touch <ruta/nombre> [contenido]")
            return

        ruta_completa = args[0]
        contenido = " ".join(args[1:]) if len(args) > 1 else ""

        if "/" in ruta_completa:
            ultimo_slash = ruta_completa.rfind("/")
            ruta_padre = ruta_completa[:ultimo_slash]
            nombre_nuevo = ruta_completa[ultimo_slash+1:]
            if not ruta_padre: ruta_padre = "/"
            nodo_padre = self.sistema.obtener_nodo_desde_ruta(ruta_padre)
        else:
            nodo_padre = self.sistema.nodo_actual
            nombre_nuevo = ruta_completa

        if nodo_padre:
            nuevo_id = f"archivo_{nombre_nuevo}"
            if self.sistema.crear_nodo(nodo_padre.id, nuevo_id, nombre_nuevo, "archivo", contenido):
                print(f"Creado: {nombre_nuevo}")
        else:
            print("Error: Ruta contenedora no existe.")

    def complete_touch(self, text, line, begidx, endidx):
        return self._completar_rutas(text)

    def do_rm(self, arg):
        if not arg: return

        nodo = self.sistema.obtener_nodo_desde_ruta(arg)
        if nodo:
            # Necesitamos el ID para la funcion eliminar
            if self.sistema.eliminar_nodo(nodo.id):
                print(f"Eliminado: {nodo.nombre}")
        else:
            print("Error: Nodo no encontrado.")

    def complete_rm(self, text, line, begidx, endidx):
        return self._completar_rutas(text)

    def do_mv(self, arg):
        # Uso: mv <origen> <destino_carpeta>
        # Ejemplo: mv archivo.txt /docs/
        args = arg.split()
        if len(args) < 2:
            print("Uso: mv <ruta_origen> <ruta_destino_carpeta>")
            return

        origen = self.sistema.obtener_nodo_desde_ruta(args[0])
        destino = self.sistema.obtener_nodo_desde_ruta(args[1])

        if not origen:
            print(f"Error: Origen '{args[0]}' no existe.")
            return
        if not destino:
            print(f"Error: Destino '{args[1]}' no existe.")
            return

        if self.sistema.mover_nodo(origen.id, destino.id):
            print("Movido exitosamente.")

    def complete_mv(self, text, line, begidx, endidx):
        return self._completar_rutas(text)

    def do_rename(self, arg):
        # Uso: rename <ruta_actual> <nuevo_nombre>
        args = arg.split()

        # Validación de argumentos
        if len(args) < 2:
            print("Uso: rename <ruta_objetivo> <nuevo_nombre>")
            return

        ruta_objetivo = args[0]
        nuevo_nombre = args[1]

        # Validación de nombre vacío o inválido
        if not nuevo_nombre or "/" in nuevo_nombre:
            print("Error: El nuevo nombre no puede contener rutas (/). Use 'mv' para mover.")
            return

        # Obtener el objeto nodo desde la ruta string
        nodo = self.sistema.obtener_nodo_desde_ruta(ruta_objetivo)

        if nodo:
            # Ejecutar lógica de negocio
            if self.sistema.renombrar_nodo(nodo.id, nuevo_nombre):
                print(f"Renombrado exitosamente: '{ruta_objetivo}' -> '{nuevo_nombre}'")
        else:
            print(f"Error: La ruta '{ruta_objetivo}' no existe.")

    def complete_rename(self, text, line, begidx, endidx):
        # Solo autocompletamos el primer argumento (el archivo a renombrar)
        args = line.split()

        # Si estamos escribiendo el segundo argumento (el nuevo nombre), no sugerimos nada
        if len(args) > 2 or (len(args) == 2 and not text):
            return []

        return self._completar_rutas(text)

    def do_find(self, arg):
        if not arg: return
        res = self.sistema.buscar_autocompletado_global(arg)
        print(f"Coincidencias: {res}")

    def do_tree(self, arg):
        # Muestra la estructura en forma de arbol visual
        # Uso: tree [ruta_opcional]

        nodo_raiz = self.sistema.nodo_actual

        if arg:
            nodo_resuelto = self.sistema.obtener_nodo_desde_ruta(arg)
            if nodo_resuelto:
                nodo_raiz = nodo_resuelto
            else:
                print(f"Error: Ruta '{arg}' no encontrada.")
                return

        print(f". ({nodo_raiz.nombre})")
        self._imprimir_arbol_recursivo(nodo_raiz, "")

    def _imprimir_arbol_recursivo(self, nodo, prefijo):
        # Metodo auxiliar para dibujar las ramas
        hijos = nodo.hijos
        cantidad = len(hijos)

        for i, hijo in enumerate(hijos):
            es_ultimo = (i == cantidad - 1)
            conector = "└── " if es_ultimo else "├── "

            # Imprime la rama y el nombre
            tag = "/" if hijo.tipo == "carpeta" else ""
            print(f"{prefijo}{conector}{hijo.nombre}{tag}")

            # Prepara el prefijo para el siguiente nivel
            # Si era el ultimo, dejamos espacio vacio, si no, una barra vertical
            nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")

            # Recursion si es carpeta y tiene hijos
            if hijo.tipo == "carpeta":
                self._imprimir_arbol_recursivo(hijo, nuevo_prefijo)

    def complete_tree(self, text, line, begidx, endidx):
        return self._completar_rutas(text)

    def do_lspap(self, arg):
        # Lista el contenido de la papelera.
        print("--- Papelera de Reciclaje ---")
        if not self.sistema.papelera:
            print("  (vacia)")
            return

        for nodo in self.sistema.papelera:
            # Mostramos de donde vino para ayudar a decidir
            padre = self.sistema.buscar_por_id(nodo.padre_id)
            nombre_padre = padre.nombre if padre else "DESCONOCIDO (Borrado)"
            tag = "[CARPETA]" if nodo.tipo == "carpeta" else "[ARCHIVO]"
            print(f"  {tag} {nodo.nombre} (ID: {nodo.id}) -> Origen: {nombre_padre}")

    def do_clpap(self, arg):
        # Vacia la papelera definitivamente.
        if self.sistema.vaciar_papelera():
            print("Papelera vaciada.")

    def do_restore(self, arg):
        # Restaura un archivo de la papelera.
        # Uso: restore <id>
        if not arg:
            print("Uso: restore <id_nodo>")
            return

        if self.sistema.restaurar_nodo(arg):
            print("Restaurado exitosamente.")

    def complete_restore(self, text, line, begidx, endidx):
        # Autocompletado especial solo para IDs que esten en la papelera
        sugerencias = []
        for nodo in self.sistema.papelera:
            if nodo.id.startswith(text):
                sugerencias.append(nodo.id)
        return sugerencias

    def do_cls(self, arg):
        # Limpia la pantalla
        os.system('cls' if os.name == 'nt' else 'clear')

        print("""
=========================================
SISTEMA DE ARCHIVOS - ESTRUCTURA DE DATOS
=========================================
            """)

    def do_help(self, arg):
        if arg:
            super().do_help(arg)
        else:
            print("""
--- Comandos: [opcional] <necesario> ---
ls [ruta]                    : Listar directorio
tree [ruta]                  : Mostrar árbol de directorios
cd <ruta>                    : Cambiar directorio
mkdir <ruta>                 : Crear directorio
touch <ruta> [txt]           : Crear archivo
rename <ruta> <nuevo_nombre> : Renombrar nodo
rm <ruta>                    : Eliminar nodo
mv <orig> <dest>             : Mover nodo
find <prefijo>               : Buscar global
cls                          : Limpiar pantalla
lspap                        : Ver papelera
restore <id>                 : Restaurar elemento
clpap                        : Vaciar papelera
exit                         : Salir del programa
            """)

    def do_exit(self, arg):
        print("Saliendo...")
        return True

    def emptyline(self):
        pass

    def default(self, line):
        print("Comando desconocido.")
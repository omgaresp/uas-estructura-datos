class Nodo:
    def __init__(self, id, nombre, tipo, contenido=None):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo          # "Carpeta" o "Archivo"
        self.contenido = contenido # Texto (solo si es archivo)
        self.hijos = []           # Lista para guardar otros Nodos

    def __repr__(self):
        # Mejora el print de los nodos
        return f"<{self.tipo}: {self.nombre} (ID: {self.id})>"
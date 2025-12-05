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

    def guardar_dicc(self):
        # Convierte el nodo y sus hijos recursivamente a un diccionario.
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "contenido": self.contenido,
            # Aquí ocurre la magia recursiva: cada hijo se convierte a sí mismo
            "hijos": [hijo.guardar_dicc() for hijo in self.hijos]
        }

    @classmethod
    def cargar_dicc(cls, data):
        # Reconstruye un objeto Nodo (y sus hijos) desde un diccionario.
        # 1. Crear el nodo base con los datos planos
        nuevo_nodo = cls(
            id=data["id"],
            nombre=data["nombre"],
            tipo=data["tipo"],
            contenido=data["contenido"]
        )

        # 2. Reconstruir los hijos recursivamente
        if "hijos" in data:
            for hijo_dict in data["hijos"]:
                hijo_obj = cls.cargar_dicc(hijo_dict) # Recursividad
                nuevo_nodo.hijos.append(hijo_obj)

        return nuevo_nodo
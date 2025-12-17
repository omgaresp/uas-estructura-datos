class Nodo:
    def __init__(self, id, nombre, tipo, contenido=None, padre_id=None):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo           # "Carpeta" o "Archivo"
        self.contenido = contenido # Texto (solo si es archivo)
        self.hijos = []            # Lista para guardar otros Nodos
        self.padre_id = padre_id   # Para guardar de donde viene

    def __repr__(self):
        return f"<{self.tipo}: {self.nombre} (ID: {self.id})>"

    def guardar_dicc(self):
        # Serializa el nodo y su estructura descendente a un diccionario para facilitar el almacenamiento en JSON.
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "contenido": self.contenido,
            "padre_id": self.padre_id,
            # Serialización recursiva de los hijos
            "hijos": [hijo.guardar_dicc() for hijo in self.hijos]
        }

    @classmethod
    def cargar_dicc(cls, data):
        # Deserializa un diccionario y reconstruye la estructura de objetos Nodo de manera recursiva.
        # Instancia del nodo actual
        nuevo_nodo = cls(
            id=data["id"],
            nombre=data["nombre"],
            tipo=data["tipo"],
            contenido=data.get("contenido"),
            padre_id=data.get("padre_id")
        )

        # Reconstrucción de la jerarquía de hijos
        if "hijos" in data:
            for hijo_dict in data["hijos"]:
                hijo_obj = cls.cargar_dicc(hijo_dict)
                nuevo_nodo.hijos.append(hijo_obj)

        return nuevo_nodo
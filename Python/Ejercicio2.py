# Crear tipo definido / Clase
class Persona:
    def __init__(self, nombre, apellido1, apellido2):
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
    
    def __str__(self):
        return f"{self.nombre} {self.apellido1} {self.apellido2}"

# Utilizarlo en un Array
personas = [
    Persona("Juan", "García", "López"),
    Persona("María", "Rodríguez", "Martín"),
    Persona("Carlos", "Hernández", "Pérez")
]

# Mostrar el array
print("Array de Personas:")
for i, persona in enumerate(personas):
    print(f"[{i}]: {persona}")
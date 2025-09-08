# Tipo definido Persona
class Persona:
    def __init__(self, nombre, apellido1, apellido2):
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2

# ARRAY NORMAL
print("=== ARRAY NORMAL ===")
array_numeros = [11, 12, 13, 14, 15]

print("Recorrido inicial:")
for i, numero in enumerate(array_numeros):
    print(f"[{i}]: {numero}")

# Buscar el 13
print("\nBuscando el valor 13:")
encontrado = False
for i, numero in enumerate(array_numeros):
    if numero == 13:
        print(f"¡Encontrado! El valor 13 está en la posición {i}")
        encontrado = True
        break
    else:
        print(f"Posición {i}: {numero} - No es 13")

array_numeros.insert(2, 16)

print("\nRecorrido después de la inserción:")
for i, numero in enumerate(array_numeros):
    if numero == 16:
        print(f"[{i}]: {numero} ← NUEVO ELEMENTO INSERTADO")
    else:
        print(f"[{i}]: {numero}")

print("\nRecorrido inverso:")
for i, numero in reversed(list(enumerate(array_numeros))):
    print(f"[{i}]: {numero}")

# ARRAY CON TIPO DEFINIDO
print("\n=== ARRAY CON TIPO DEFINIDO ===")
personas = [
    Persona("Juan", "García", "López"),
    Persona("María", "Rodríguez", "Martín"),
    Persona("Carlos", "Hernández", "Pérez")
]

print("Recorrido inicial:")
for i, persona in enumerate(personas):
    print(f"[{i}]: {persona.nombre} {persona.apellido1} {persona.apellido2}")

# Buscar a María
print("\nBuscando a María:")
encontrado = False
for i, persona in enumerate(personas):
    if persona.nombre == "María":
        print(f"¡Encontrada! María está en la posición {i}")
        encontrado = True
        break
    else:
        print(f"Posición {i}: {persona.nombre} - No es María")

# Insertar nueva persona (Omar en posición 1)
personas.insert(1, Persona("Omar", "García", "Espinoza"))

print("\nRecorrido después de la inserción:")
for i, persona in enumerate(personas):
    if persona.nombre == "Omar":
        print(f"[{i}]: {persona.nombre} {persona.apellido1} {persona.apellido2} ← NUEVA PERSONA INSERTADA")
    else:
        print(f"[{i}]: {persona.nombre} {persona.apellido1} {persona.apellido2}")
        
print("\nRecorrido inverso:")
for i, persona in reversed(list(enumerate(personas))):
    print(f"[{i}]: {persona.nombre} {persona.apellido1} {persona.apellido2}")
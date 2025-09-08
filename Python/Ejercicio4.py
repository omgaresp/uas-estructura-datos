# Declarar e Inicializar la Matriz
matriz = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print("Matriz 3x3:")
for fila in matriz:
    print(fila)

print("\n=== Recorrido Horizontal ===")
for i in range(len(matriz)): # Filas
    for j in range(len(matriz[i])): # Columnas
        print(f"[{i}][{j}]: {matriz[i][j]}")

print("\n=== Recorrido Vertical ===")
for j in range(len(matriz[0])):  # Columnas
    for i in range(len(matriz)):  # Filas
        print(f"[{i}][{j}]: {matriz[i][j]}")
using System;

// Declarar e Inicializar la Matriz
int[,] matriz = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

Console.WriteLine("Matriz 3x3:");
for (int i = 0; i < matriz.GetLength(0); i++) {
    Console.Write("[");
    for (int j = 0; j < matriz.GetLength(1); j++) {
        Console.Write(matriz[i,j]);
        if (j < matriz.GetLength(1) - 1) Console.Write(", ");
    }
    Console.WriteLine("]");
}

Console.WriteLine("\n=== Recorrido Horizontal ===");
for (int i = 0; i < matriz.GetLength(0); i++) { // Filas
    for (int j = 0; j < matriz.GetLength(1); j++) { // Columnas
        Console.WriteLine($"[{i}][{j}]: {matriz[i,j]}");
    }
}

Console.WriteLine("\n=== Recorrido Vertical ===");
for (int j = 0; j < matriz.GetLength(1); j++) {  // Columnas
    for (int i = 0; i < matriz.GetLength(0); i++) {  // Filas
        Console.WriteLine($"[{i}][{j}]: {matriz[i,j]}");
    }
}
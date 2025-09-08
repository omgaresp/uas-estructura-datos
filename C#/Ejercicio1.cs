using System;

// Declarar un Array en C#
int[] array1 = new int[5];

// Inicializar un Array en C#
int[] array2 = {11, 12, 13, 14, 15};

// Mostrar los arrays
Console.Write("Array vacío: ");
foreach (int num in array1) {
    Console.Write(num + " ");
}
Console.WriteLine();

Console.Write("Array inicializado: ");
foreach (int num in array2) {
    Console.Write(num + " ");
}
Console.WriteLine();
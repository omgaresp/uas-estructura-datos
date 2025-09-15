using System;

void BubbleSortWithVisualization(int[] arr)
{
    int n = arr.Length;
    
    for (int i = 0; i < n - 1; i++)
    {
        bool huboIntercambio = false;
        
        for (int j = 0; j < n - i - 1; j++)
        {
            if (arr[j] > arr[j + 1])
            {
                // Intercambiar
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                huboIntercambio = true;
            }
        }
        
        Console.WriteLine($"Pasada {i + 1}: [" + string.Join(", ", arr) + "]");
        
        if (!huboIntercambio)
        {
            Console.WriteLine("Array ordenado.");
            break;
        }
    }
}

// Código principal del script
int[] arr = {64, 34, 25, 12, 22, 11, 90};
Console.WriteLine("=== BUBBLE SORT EN C# SCRIPT ===");
Console.WriteLine("Array inicial: [" + string.Join(", ", arr) + "]");

BubbleSortWithVisualization(arr);

Console.WriteLine("Array final: [" + string.Join(", ", arr) + "]");
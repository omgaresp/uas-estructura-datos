using System;

void SelectionSort(int[] arr)
{
    int n = arr.Length;
    for (int i = 0; i < n; i++) {
        int minIndex = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIndex]) {
                minIndex = j;
            }
        }
        int actual = arr[i];
        arr[i] = arr[minIndex];
        arr[minIndex] = actual;
    }
}

int[] arr = {64, 34, 25, 12, 22, 11, 90};
Console.WriteLine("=== SELECTION SORT EN C# SCRIPT ===");
Console.WriteLine("Array inicial: [" + string.Join(", ", arr) + "]");

SelectionSort(arr);

Console.WriteLine("Array final: [" + string.Join(", ", arr) + "]");
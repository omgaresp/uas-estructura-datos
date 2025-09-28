using System;

void InsertionSort(int[] arr)
{
    int n = arr.Length;
    for (int i = 1; i < n; i++)
    {
        int actual = arr[i];
        int j = i - 1;

        while (j >= 0 && arr[j] > actual)
        {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = actual;
    }
}

int[] arr = {64, 34, 25, 12, 22, 11, 90};
Console.WriteLine("=== INSERTION SORT EN C# SCRIPT ===");
Console.WriteLine("Array inicial: [" + string.Join(", ", arr) + "]");

InsertionSort(arr);

Console.WriteLine("Array final: [" + string.Join(", ", arr) + "]");
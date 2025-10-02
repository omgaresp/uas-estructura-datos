using System;

void ShellSort(int[] arr)
{
    int size = arr.Length;
    int gapSize = size / 2;

    while (gapSize > 0) {
        for (int i = gapSize; i < size; i++) {
            int temp = arr[i];
            int j = i;
            while (j >= gapSize && arr[j - gapSize] > temp) {
                arr[j] = arr[j - gapSize];
                j -= gapSize;
            }
            arr[j] = temp;
        }
        gapSize /= 2;
    }
}

int[] arr = {64, 34, 25, 12, 22, 11, 90};
Console.WriteLine("=== SHELL SORT EN C# SCRIPT ===");
Console.WriteLine("Array inicial: [" + string.Join(", ", arr) + "]");

ShellSort(arr);

Console.WriteLine("Array final: [" + string.Join(", ", arr) + "]");
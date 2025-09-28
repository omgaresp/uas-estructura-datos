using System;

void QuickSort(int[] arr, int l, int h)
{
    if (l < h) {
        int pi = Partition(arr, l, h);

        QuickSort(arr, l, pi - 1);
        QuickSort(arr, pi + 1, h);
    }
}

int Partition(int[] arr, int l, int h)
{
    int pvt = arr[h];
    int j = l - 1;

    for (int k = l; k < h; k++) {
        if (arr[k] < pvt) {
            j += 1;
            Swap(arr, j, k);
        }
    }

    Swap(arr, j + 1, h);
    return j + 1;
}

void Swap(int[] arr, int j, int k)
{
    int temp = arr[j];
    arr[j] = arr[k];
    arr[k] = temp;
}

int[] arr = {64, 34, 25, 12, 22, 11, 90};
Console.WriteLine("=== QUICK SORT EN C# SCRIPT ===");
Console.WriteLine("Array inicial: [" + string.Join(", ", arr) + "]");

QuickSort(arr, 0, arr.Length - 1);

Console.WriteLine("Array final: [" + string.Join(", ", arr) + "]");
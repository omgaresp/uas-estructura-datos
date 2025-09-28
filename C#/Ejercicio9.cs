using System;

void MergeSort(int[] arr, int l, int r)
{
    if (l < r) {
        int m = l + (r - l) / 2;

        MergeSort(arr, l, m);
        MergeSort(arr, m + 1, r);
        Merge(arr, l, m, r);
    }
}

void Merge(int[] arr, int l, int m, int r)
{
    int arr1 = m - l + 1;
    int arr2 = r - m;

    int[] tempL = new int[arr1];
    int[] tempR = new int[arr2];

    for (int idx = 0; idx < arr1; idx++) {
        tempL[idx] = arr[l + idx];
    }

    for (int idx = 0; idx < arr2; idx++) {
        tempR[idx] = arr[m + 1 + idx];
    }

    int i = 0;
    int j = 0;
    int k = l;

    while (i < arr1 && j < arr2) {
        if (tempL[i] <= tempR[j]) {
            arr[k] = tempL[i];
            i += 1;
        } else {
            arr[k] = tempR[j];
            j += 1;
        }
        k += 1;
    }

    while (i < arr1) {
        arr[k] = tempL[i];
        i += 1;
        k += 1;
    }

    while (j < arr2) {
        arr[k] = tempR[j];
        j += 1;
        k += 1;
    }
}

int[] arr = {64, 34, 25, 12, 22, 11, 90};
Console.WriteLine("=== MERGE SORT EN C# SCRIPT ===");
Console.WriteLine("Array inicial: [" + string.Join(", ", arr) + "]");

MergeSort(arr, 0, arr.Length - 1);

Console.WriteLine("Array final: [" + string.Join(", ", arr) + "]");
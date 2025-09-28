import java.util.Arrays;

public class Ejercicio9 {
    public static void main(String[] args) {
        int[] arr = {84, 54, 45, 32, 42, 31, 110};

        System.out.println("=== MERGE SORT EN JAVA ===");
        System.out.println("Array inicial: " + Arrays.toString(arr));

        mergeSort(arr, 0, arr.length - 1);

        System.out.println("Array final: " + Arrays.toString(arr));
    }

    public static void mergeSort(int[] arr, int l, int r) {
        if (l < r) {
            int m = l + (r - l) / 2;

            mergeSort(arr, l, m);
            mergeSort(arr, m + 1, r);
            merge(arr, l, m, r);
        }
    }

    public static void merge(int[] arr, int l, int m, int r) {
        int arr1 = m - l + 1;
        int arr2 = r - m;

        int[] tempL = new int[arr1];
        int[] tempR = new int[arr2];

        for (int j = 0; j < arr1; j++) {
            tempL[j] = arr[l + j];
        }

        for (int k = 0; k < arr2; k++) {
            tempR[k] = arr[m + 1 + k];
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
}
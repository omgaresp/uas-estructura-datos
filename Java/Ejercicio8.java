import java.util.Arrays;

public class Ejercicio8 {
    public static void main(String[] args) {
        int[] arr = {84, 54, 45, 32, 42, 31, 110};

        System.out.println("=== QUICK SORT EN JAVA ===");
        System.out.println("Array inicial: " + Arrays.toString(arr));

        quickSort(arr, 0, arr.length - 1);

        System.out.println("Array final: " + Arrays.toString(arr));
    }

    public static void quickSort(int[] arr, int l, int h) {
        if (l < h) {
            int pi = partition(arr, l, h);

            quickSort(arr, l, pi - 1);
            quickSort(arr, pi + 1, h);
        }
    }

    public static int partition(int[] arr, int l, int h) {
        int pvt = arr[h];
        int j = l - 1;

        for (int k = l; k < h; k++) {
            if (arr[k] < pvt) {
                j += 1;
                swap(arr, j, k);
            }
        }

        swap(arr, j + 1, h);
        return j + 1;
    }

    public static void swap(int[] arr, int j, int k) {
        int temp = arr[j];
        arr[j] = arr[k];
        arr[k] = temp;
    }
}
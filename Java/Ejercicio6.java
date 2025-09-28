import java.util.Arrays;

public class Ejercicio6 {
    public static void main(String[] args) {
        int[] arr = {84, 54, 45, 32, 42, 31, 110};

        System.out.println("=== INSERTION SORT EN JAVA ===");
        System.out.println("Array inicial: " + Arrays.toString(arr));

        insertionSort(arr);

        System.out.println("Array final: " + Arrays.toString(arr));
    }

    public static void insertionSort(int[] arr) {
        int n = arr.length;
        for (int i = 1; i < n; i++) {
            int actual = arr[i];
            int j = i - 1;
            while (j >= 0 && arr[j] > actual) {
                arr[j + 1] = arr[j];
                j = j - 1;
            }
            arr[j + 1] = actual;
        }
    }
}
import java.util.Arrays;

public class Ejercicio7 {
    public static void main(String[] args) {
        int[] arr = {84, 54, 45, 32, 42, 31, 110};

        System.out.println("=== SELECTION SORT EN JAVA ===");
        System.out.println("Array inicial: " + Arrays.toString(arr));

        selectionSort(arr);

        System.out.println("Array final: " + Arrays.toString(arr));
    }

    public static void selectionSort(int[] arr) {
        int n = arr.length;
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
}
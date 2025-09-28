import java.util.Arrays;

public class Ejercicio5 {
    public static void main(String[] args) {
        int[] arr = {84, 54, 45, 32, 42, 31, 110};

        System.out.println("=== BUBBLE SORT EN JAVA ===");
        System.out.println("Array inicial: " + Arrays.toString(arr));

        bubbleSort(arr);

        System.out.println("Array final: " + Arrays.toString(arr));
    }

    public static void bubbleSort(int[] arr) {
        int n = arr.length;

        for (int i = 0; i < n - 1; i++) {
            boolean huboIntercambio = false;

            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    huboIntercambio = true;
                }
            }

            System.out.println("Pasada " + (i + 1) + ": " + Arrays.toString(arr));

            if (!huboIntercambio) {
                System.out.println("Array ordenado.");
                break;
            }
        }
    }
}
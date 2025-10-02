import java.util.Arrays;

public class Ejercicio11 {
    public static void main(String[] args) {
        int[] arr = {84, 54, 45, 32, 42, 31, 110};

        System.out.println("=== SHELL SORT EN JAVA ===");
        System.out.println("Array inicial: " + Arrays.toString(arr));

        shellSort(arr);

        System.out.println("Array final: " + Arrays.toString(arr));
    }

    public static void shellSort(int[] arr) {
        int size = arr.length;
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
}
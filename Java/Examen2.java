import java.util.Arrays;

public class Examen2 {
    public static void main(String[] args) {
        int[] arr = {84, 54, 45, 32, 42, 31, 110};
        int[][] matriz = {
            {1, 8, 6},
            {3, 5, 4},
            {7, 2, 9}
        };
        int[][][] cubo = {
            {
                {  1,  2,  3,  4,  5 },
                {  6,  7,  8,  9, 10 },
                { 11, 12, 13, 14, 15 },
                { 16, 17, 18, 19, 20 },
                { 21, 22, 23, 24, 25 }
            },
            {
                { 26, 27, 28, 29, 30 },
                { 31, 32, 33, 34, 35 },
                { 36, 37, 38, 39, 40 },
                { 41, 42, 43, 44, 45 },
                { 46, 47, 48, 49, 50 }
            },
            {
                { 51, 52, 53, 54, 55 },
                { 56, 57, 58, 59, 60 },
                { 61, 62, 63, 64, 65 },
                { 66, 67, 68, 69, 70 },
                { 71, 72, 73, 74, 75 }
            },
            {
                { 76, 77, 78, 79, 80 },
                { 81, 82, 83, 84, 85 },
                { 86, 87, 88, 89, 90 },
                { 91, 92, 93, 94, 95 },
                { 96, 97, 98, 99,100 }
            },
            {
                {101,102,103,104,105 },
                {106,107,108,109,110 },
                {111,112,113,114,115 },
                {116,117,118,119,120 },
                {121,122,123,124,125 }
            }
        };

        System.out.println("=== 1D.1 ORDENAR ===");
        System.out.println("Array inicial: " + Arrays.toString(arr));

        mergeSort(arr, 0, arr.length - 1);

        System.out.println("Array ordenado: " + Arrays.toString(arr));
        System.out.println("\n=== 1D.2 BUSCAR ===");

        System.out.println("Buscando el valor 15:");
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == 84) {
                System.out.println("¡Encontrado! El valor 84 está en la posición " + i);
                break;
            } else {
                System.out.println("Posición " + i + ": " + arr[i] + " - No es 84");
            }
        }

        System.out.println("\n=== 2D VALOR MAXIMO ===");
        for (int i = 0; i < matriz.length; i++) {
            System.out.print("[");
            for (int j = 0; j < matriz[i].length; j++) {
                System.out.print(matriz[i][j]);
                if (j < matriz[i].length - 1) System.out.print(", ");
            }
            System.out.println("]");
        }

        int max = matriz[0][0];
        for (int i = 0; i < matriz.length; i++) {
            for (int j = 0; j < matriz[i].length; j++) {
                if (matriz[i][j] > max) {
                    max = matriz[i][j];
                }
            }
        }
        System.out.println("El valor máximo en la matriz es: " + max);

        System.out.println("\n=== 3D ORDENAR SUB ARRAYS ASC Y DESC, ALTERNANDO ===");
        for (int i = 0; i < cubo.length; i++) {
            System.out.println("Capa " + (i + 1) + ":");
            for (int j = 0; j < cubo[i].length; j++) {
                int[] fila = Arrays.copyOf(cubo[i][j], cubo[i][j].length);
                for (int a = 0; a < fila.length - 1; a++) {
                    for (int b = a + 1; b < fila.length; b++) {
                        if (fila[a] > fila[b]) {
                            int temp = fila[a];
                            fila[a] = fila[b];
                            fila[b] = temp;
                        }
                    }
                }
                if (j % 2 != 0) {
                    for (int a = 0; a < fila.length / 2; a++) {
                        int temp = fila[a];
                        fila[a] = fila[fila.length - 1 - a];
                        fila[fila.length - 1 - a] = temp;
                    }
                }
                System.out.print("[");
                for (int a = 0; a < fila.length; a++) {
                    System.out.print(fila[a]);
                    if (a < fila.length - 1) System.out.print(", ");
                }
                System.out.println("]");
            }
            System.out.println();
        }
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

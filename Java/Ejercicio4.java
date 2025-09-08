public class Ejercicio4 {
    public static void main(String[] args) {
        // Declarar e Inicializar la Matriz
        int[][] matriz = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };

        System.out.println("Matriz 3x3:");
        for (int i = 0; i < matriz.length; i++) {
            System.out.print("[");
            for (int j = 0; j < matriz[i].length; j++) {
                System.out.print(matriz[i][j]);
                if (j < matriz[i].length - 1) System.out.print(", ");
            }
            System.out.println("]");
        }

        System.out.println("\n=== Recorrido Horizontal ===");
        for (int i = 0; i < matriz.length; i++) { // Filas
            for (int j = 0; j < matriz[i].length; j++) { // Columnas
                System.out.println("[" + i + "][" + j + "]: " + matriz[i][j]);
            }
        }

        System.out.println("\n=== Recorrido Vertical ===");
        for (int j = 0; j < matriz[0].length; j++) {  // Columnas
            for (int i = 0; i < matriz.length; i++) {  // Filas
                System.out.println("[" + i + "][" + j + "]: " + matriz[i][j]);
            }
        }
    }
}
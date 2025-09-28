import java.util.Scanner;
import java.util.Random;

public class Proyecto2 {
    // Constantes del juego
    private static final int FILAS = 6;
    private static final int COLUMNAS = 7;
    private static final char VACIO = ' ';
    private static final char JUGADOR1 = 'X';
    private static final char JUGADOR2 = 'O';
    
    // Variables del juego
    private char[][] tablero;
    private Scanner scanner;
    private int jugadorActual;
    private String nombreJugador1;
    private String nombreJugador2;
    
    public Proyecto2() {
        tablero = new char[FILAS][COLUMNAS];
        scanner = new Scanner(System.in);
        inicializarTablero();
    }
    
    // Inicializar el tablero con espacios vacíos
    private void inicializarTablero() {
        for (int i = 0; i < FILAS; i++) {
            for (int j = 0; j < COLUMNAS; j++) {
                tablero[i][j] = VACIO;
            }
        }
    }
    
    // Configurar jugadores y determinar quién empieza
    private void configurarJugadores() {
        System.out.println("=== CONFIGURACIÓN DE JUGADORES ===");
        System.out.print("Ingresa el nombre del Jugador 1 (X): ");
        nombreJugador1 = scanner.nextLine().trim();
        if (nombreJugador1.isEmpty()) nombreJugador1 = "Jugador 1";
        
        System.out.print("Ingresa el nombre del Jugador 2 (O): ");
        nombreJugador2 = scanner.nextLine().trim();
        if (nombreJugador2.isEmpty()) nombreJugador2 = "Jugador 2";
    }
    
    // Determinar aleatoriamente quién empieza la partida
    private void determinarPrimerJugador() {
        Random random = new Random(System.currentTimeMillis());
        jugadorActual = random.nextInt(2) + 1;
        
        System.out.println("\nDeterminando quién empieza...");
        System.out.println(getNombreJugadorActual() + " (" + getSimboloJugadorActual() + ") comenzará el juego!");
    }
    
    // Mostrar el tablero en terminal
    private void mostrarTablero() {
        System.out.println("\n=== CONECTA 4 ===");
        System.out.println("    1   2   3   4   5   6   7");
        System.out.println("  +---+---+---+---+---+---+---+");
        
        for (int i = 0; i < FILAS; i++) {
            System.out.print("  |");
            for (int j = 0; j < COLUMNAS; j++) {
                System.out.print(" " + tablero[i][j] + " |");
            }
            System.out.println();
            
            if (i < FILAS - 1) {
                System.out.println("  +---+---+---+---+---+---+---+");
            }
        }
        
        System.out.println("  +---+---+---+---+---+---+---+");
        System.out.println("    1   2   3   4   5   6   7\n");
    }
    
    // Mostrar información del turno actual
    private void mostrarTurnoActual() {
        System.out.println("=== TURNO ACTUAL ===");
        System.out.println("Jugador: " + getNombreJugadorActual());
        System.out.println("Símbolo: " + getSimboloJugadorActual());
        System.out.println("====================");
    }
    
    // Verificar si una columna está llena
    private boolean columnaLlena(int columna) {
        return tablero[0][columna] != VACIO;
    }
    
    // Colocar ficha en una columna
    private boolean colocarFicha(int columna) {
        if (columna < 0 || columna >= COLUMNAS || columnaLlena(columna)) {
            return false;
        }
        
        // Buscar la fila más baja disponible en la columna
        for (int i = FILAS - 1; i >= 0; i--) {
            if (tablero[i][columna] == VACIO) {
                tablero[i][columna] = (jugadorActual == 1) ? JUGADOR1 : JUGADOR2;
                return true;
            }
        }
        return false;
    }
    
    // Verificación optimizada: verifica las 4 líneas desde la última ficha colocada
    private boolean verificarVictoria(int fila, int columna) {
        char ficha = tablero[fila][columna];
        if (ficha == VACIO) return false;
        
        // Verificar las 4 líneas posibles: horizontal, vertical, y las 2 diagonales
        // Para cada línea, contamos en ambas direcciones
        
        // 1. Línea horizontal
        if (contarLinea(fila, columna, 0, 1, ficha) >= 4) return true;
        
        // 2. Línea vertical
        if (contarLinea(fila, columna, 1, 0, ficha) >= 4) return true;
        
        // 3. Línea diagonal (\)
        if (contarLinea(fila, columna, 1, 1, ficha) >= 4) return true;
        
        // 4. Línea diagonal (/)
        if (contarLinea(fila, columna, 1, -1, ficha) >= 4) return true;
        
        return false;
    }
    
    // Contar fichas consecutivas en una línea (ambas direcciones)
    private int contarLinea(int fila, int columna, int deltaFila, int deltaColumna, char ficha) {
        int count = 1; // Empezar contando la ficha actual
        
        // Contar hacia una dirección
        int f = fila + deltaFila;
        int c = columna + deltaColumna;
        while (f >= 0 && f < FILAS && c >= 0 && c < COLUMNAS && tablero[f][c] == ficha) {
            count++;
            f += deltaFila;
            c += deltaColumna;
        }
        
        // Contar hacia la dirección opuesta
        f = fila - deltaFila;
        c = columna - deltaColumna;
        while (f >= 0 && f < FILAS && c >= 0 && c < COLUMNAS && tablero[f][c] == ficha) {
            count++;
            f -= deltaFila;
            c -= deltaColumna;
        }
        
        return count;
    }
    
    // Verificar si hay ganador después de colocar una ficha
    private boolean hayGanador(int ultimaFila, int ultimaColumna) {
        return verificarVictoria(ultimaFila, ultimaColumna);
    }
    
    // Verificar si el tablero está lleno (empate)
    private boolean tableroLleno() {
        for (int j = 0; j < COLUMNAS; j++) {
            if (!columnaLlena(j)) {
                return false;
            }
        }
        return true;
    }
    
    // Cambiar de jugador
    private void cambiarJugador() {
        jugadorActual = (jugadorActual == 1) ? 2 : 1;
    }
    
    // Obtener símbolo del jugador actual
    private char getSimboloJugadorActual() {
        return (jugadorActual == 1) ? JUGADOR1 : JUGADOR2;
    }
    
    // Obtener nombre del jugador actual
    private String getNombreJugadorActual() {
        return (jugadorActual == 1) ? nombreJugador1 : nombreJugador2;
    }
    
    // Limpiar pantalla (solo Windows)
    private void cls() {
        try {
            new ProcessBuilder("cmd", "/c", "cls").inheritIO().start().waitFor();
        } catch (Exception e) {
            // Si no se puede limpiar, simular con líneas vacías
            for (int i = 0; i < 50; i++) {
                System.out.println();
            }
        }
    }
    
    // Bucle principal del juego
    public void jugar() {
        System.out.println("=== CONECTA 4 ===");
        System.out.println("Conecta 4 fichas para ganar!");
        System.out.println("Horizontal, Vertical o Diagonal\n");
        
        configurarJugadores();
        
        boolean jugarOtraPartida = true;
        
        while (jugarOtraPartida) {
            // Reiniciar tablero para nueva partida
            inicializarTablero();
            determinarPrimerJugador();
            
            System.out.println("\nPresiona ENTER para comenzar...");
            scanner.nextLine();
            
            // Jugar una partida
            boolean partidaTerminada = jugarPartida();
            
            if (partidaTerminada) {
                System.out.print("\n¿Quieren jugar otra partida? (s/n): ");
                String respuesta = scanner.nextLine().trim().toLowerCase();
                jugarOtraPartida = respuesta.equals("s") || respuesta.equals("si");
                
                if (jugarOtraPartida) {
                    System.out.println("\n¡Nueva partida!");
                }
            } else {
                jugarOtraPartida = false;
            }
        }
        
        System.out.println("¡Gracias por jugar!");
        scanner.close();
    }
    
    // Jugar una partida completa
    private boolean jugarPartida() {
        int ultimaFila = -1, ultimaColumna = -1;
        
        while (true) {
            cls();
            mostrarTablero();
            mostrarTurnoActual();
            
            System.out.print("Elige columna (1-7) o 'q' para salir: ");
            String entrada = scanner.nextLine().trim();
            
            // Opción para salir
            if (entrada.equalsIgnoreCase("q")) {
                return false; // No terminó la partida normalmente
            }
            
            try {
                int columna = Integer.parseInt(entrada) - 1; // Convertir a índice (0-6)
                
                if (columna < 0 || columna >= COLUMNAS) {
                    System.out.println("Columna inválida. Elige entre 1 y 7.");
                    System.out.println("Presiona ENTER para continuar...");
                    scanner.nextLine();
                    continue;
                }
                
                if (columnaLlena(columna)) {
                    System.out.println("Esa columna está llena. Elige otra.");
                    System.out.println("Presiona ENTER para continuar...");
                    scanner.nextLine();
                    continue;
                }
                
                // Encontrar la fila donde caerá la ficha
                for (int i = FILAS - 1; i >= 0; i--) {
                    if (tablero[i][columna] == VACIO) {
                        ultimaFila = i;
                        break;
                    }
                }
                ultimaColumna = columna;
                
                // Colocar la ficha
                colocarFicha(columna);
                
                // Verificar si hay ganador (solo verifica la última ficha colocada)
                if (hayGanador(ultimaFila, ultimaColumna)) {
                    cls();
                    mostrarTablero();
                    System.out.println("=== GANADOR ===");
                    System.out.println(getNombreJugadorActual() + " (" + getSimboloJugadorActual() + ") ha ganado!");
                    System.out.println("===============");
                    return true; // Partida terminada normalmente
                }
                
                // Verificar empate
                if (tableroLleno()) {
                    cls();
                    mostrarTablero();
                    System.out.println("=== EMPATE ===");
                    System.out.println("El tablero está lleno!");
                    System.out.println("==============");
                    return true; // Partida terminada normalmente
                }
                
                // Cambiar de jugador
                cambiarJugador();
                
            } catch (NumberFormatException e) {
                System.out.println("Entrada inválida. Introduce un número del 1 al 7.");
                System.out.println("Presiona ENTER para continuar...");
                scanner.nextLine();
            }
        }
    }
    
    // Método main para ejecutar el juego
    public static void main(String[] args) {
        Proyecto2 juego = new Proyecto2();
        juego.jugar();
    }
}
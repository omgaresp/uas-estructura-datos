using System;

// Tablero del juego
char[,] tablero = new char[,] {
    {' ', ' ', ' '},
    {' ', ' ', ' '},
    {' ', ' ', ' '}
};

// Convertir número (1-9) a coordenadas
int[] NumeroAPosicion(int numero)
{
    int fila = (numero - 1) / 3;
    int columna = (numero - 1) % 3;
    return new int[] { fila, columna };
}

// Mostrar el tablero
void MostrarTablero()
{
    Console.Clear();
    Console.WriteLine("=== JUEGO DEL GATO ===\n");

    for (int i = 0; i < 3; i++)
    {
        Console.Write(" ");
        for (int j = 0; j < 3; j++)
        {
            Console.Write(tablero[i, j]);
            if (j < 2) Console.Write(" | ");
        }
        Console.WriteLine();
        if (i < 2) Console.WriteLine("-----------");
    }

    Console.WriteLine("\nPosiciones: 1-9");
}

// Realizar movimiento
bool RealizarMovimiento(int numero, char jugador)
{
    if (numero < 1 || numero > 9) return false;

    int[] pos = NumeroAPosicion(numero);
    if (tablero[pos[0], pos[1]] != ' ') return false;

    tablero[pos[0], pos[1]] = jugador;
    return true;
}

// Verificar ganador
char VerificarGanador()
{
    // Filas
    for (int i = 0; i < 3; i++)
        if (tablero[i, 0] != ' ' && tablero[i, 0] == tablero[i, 1] && tablero[i, 1] == tablero[i, 2])
            return tablero[i, 0];

    // Columnas
    for (int j = 0; j < 3; j++)
        if (tablero[0, j] != ' ' && tablero[0, j] == tablero[1, j] && tablero[1, j] == tablero[2, j])
            return tablero[0, j];

    // Diagonales
    if (tablero[0, 0] != ' ' && tablero[0, 0] == tablero[1, 1] && tablero[1, 1] == tablero[2, 2])
        return tablero[0, 0];

    if (tablero[0, 2] != ' ' && tablero[0, 2] == tablero[1, 1] && tablero[1, 1] == tablero[2, 0])
        return tablero[0, 2];

    // Empate
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            if (tablero[i, j] == ' ') return ' ';

    return 'E';
}

// Reiniciar tablero
void ReiniciarTablero()
{
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            tablero[i, j] = ' ';
}

// PROGRAMA PRINCIPAL
Console.Write("Jugador 1: ");
string jugador1 = Console.ReadLine();
Console.Write("Jugador 2: ");
string jugador2 = Console.ReadLine();

bool jugarOtra = true;
Random random = new Random();

while (jugarOtra)
{
    ReiniciarTablero();

    // Asignar X y O aleatoriamente (CORREGIDO)
    bool jugador1EsX = random.Next(2) == 0;
    string jugadorX = jugador1EsX ? jugador1 : jugador2;
    string jugadorO = jugador1EsX ? jugador2 : jugador1;

    Console.Clear();
    Console.WriteLine($"{jugadorX} = X (empieza), {jugadorO} = O");
    Console.ReadKey();

    char turno = 'X';
    char ganador = ' ';

    while (ganador == ' ')
    {
        MostrarTablero();
        string nombreActual = turno == 'X' ? jugadorX : jugadorO;
        Console.Write($"\n{nombreActual} ({turno}), elige posición (1-9): ");

        if (int.TryParse(Console.ReadLine(), out int pos) && RealizarMovimiento(pos, turno))
        {
            ganador = VerificarGanador();
            if (ganador == ' ') turno = turno == 'X' ? 'O' : 'X';
        }
    }

    MostrarTablero();

    if (ganador == 'E')
        Console.WriteLine("\n¡EMPATE!");
    else
        Console.WriteLine($"\n¡{(ganador == 'X' ? jugadorX : jugadorO)} GANA!");

    Console.Write("\n¿Otra partida? (1=Sí, 2=No): ");
    jugarOtra = Console.ReadLine() == "1";
}

Console.WriteLine("\n¡Gracias por jugar!");
Console.ReadKey();
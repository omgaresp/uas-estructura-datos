using System;
using System.Numerics;
using System.IO;
using System.Diagnostics;
using Raylib_cs;

// ============================================
// CLASE NODO
// ============================================
public class Nodo
{
    public Vector2 Posicion { get; set; }
    public Nodo? Siguiente { get; set; } // Referencia al siguiente nodo (puede ser nulo)
    public Nodo? Anterior { get; set; }  // Referencia al nodo anterior (puede ser nulo)

    // Constructor: Inicializa el nodo en una posición
    public Nodo(Vector2 pos)
    {
        Posicion = pos;
        Siguiente = null;
        Anterior = null;
    }
}

// ============================================
// CLASE LISTA SERPIENTE
// ============================================
public class ListaSerpiente
{
    public Nodo? Cabeza { get; private set; }
    public Nodo? Cola { get; private set; }
    public int Cantidad { get; private set; } // Contador de elementos

    // Agrega un nuevo nodo al frente (cabeza)
    public void AgregarCabeza(Vector2 pos)
    {
        Nodo nuevoNodo = new Nodo(pos);
        if (Cabeza == null) // Si la lista está vacía
        {
            Cabeza = nuevoNodo;
            Cola = nuevoNodo;
        }
        else // Si ya tiene elementos, enlaza el nuevo al principio
        {
            nuevoNodo.Siguiente = Cabeza;
            Cabeza.Anterior = nuevoNodo;
            Cabeza = nuevoNodo;
        }
        Cantidad++;
    }

    // Elimina el último nodo (cola) para simular movimiento
    public void RemoverCola()
    {
        if (Cola == null) return;

        if (Cabeza == Cola) // Si solo queda un elemento
        {
            Cabeza = null;
            Cola = null;
        }
        else // Si hay más, retrocede el puntero de la cola
        {
            Cola = Cola.Anterior;
            if (Cola != null) Cola.Siguiente = null;
            else Cabeza = null;
        }
        Cantidad--;
    }

    // Busca y elimina un nodo en una coordenada específica (usado para trampas)
    public void RemoverEnPosicion(Vector2 pos)
    {
        Nodo? actual = Cabeza;
        while (actual != null)
        {
            // Compara coordenadas enteras
            if ((int)actual.Posicion.X == (int)pos.X && (int)actual.Posicion.Y == (int)pos.Y)
            {
                // Ajusta los punteros dependiendo de si es Cabeza, Cola o Medio
                if (actual == Cabeza)
                {
                    Cabeza = actual.Siguiente;
                    if (Cabeza != null) Cabeza.Anterior = null;
                    else Cola = null;
                }
                else if (actual == Cola)
                {
                    Cola = actual.Anterior;
                    if (Cola != null) Cola.Siguiente = null;
                    else Cabeza = null;
                }
                else // Está en medio de la lista
                {
                    if (actual.Anterior != null) actual.Anterior.Siguiente = actual.Siguiente;
                    if (actual.Siguiente != null) actual.Siguiente.Anterior = actual.Anterior;
                }
                Cantidad--;
                return;
            }
            actual = actual.Siguiente;
        }
    }

    // Vacía la lista por completo
    public void Limpiar()
    {
        Cabeza = null;
        Cola = null;
        Cantidad = 0;
    }

    // Verifica si una posición ya está ocupada por un nodo
    public bool Contiene(Vector2 pos)
    {
        Nodo? actual = Cabeza;
        while (actual != null)
        {
            if ((int)actual.Posicion.X == (int)pos.X && (int)actual.Posicion.Y == (int)pos.Y)
                return true;
            actual = actual.Siguiente;
        }
        return false;
    }
}

// ============================================
// CLASE PRINCIPAL DEL JUEGO
// ============================================
class JuegoSnake
{
    const int AnchoPantalla = 800;
    const int AltoJuego = 600;
    const int AltoHUD = 60;
    const int AltoVentana = AltoJuego + AltoHUD;
    const int TamanoCelda = 25;

    // --- Paleta de Colores (Estilo Neón) ---
    Color ColorFondo = new Color(20, 20, 30, 255);
    Color ColorGrid = new Color(40, 40, 60, 100);
    Color ColorCabeza = new Color(0, 255, 128, 255);
    Color ColorCuerpo = new Color(0, 200, 100, 255);
    Color ColorComida = new Color(255, 60, 60, 255);
    Color ColorTrampa = new Color(160, 32, 240, 255);
    Color ColorTexto = new Color(230, 230, 230, 255);
    Color BotonNormal = new Color(50, 50, 70, 255);
    Color BotonHover = new Color(70, 70, 100, 255);

    // --- Estructuras de Datos ---
    ListaSerpiente serpiente = new ListaSerpiente();
    ListaSerpiente trampas = new ListaSerpiente();

    // --- Variables de Estado ---
    Vector2 comida;
    Vector2 direccionActual = new Vector2(1, 0);
    Vector2 direccionSiguiente = new Vector2(1, 0);

    int puntuacion = 0;
    int nivel = 1;
    float temporizadorMovimiento = 0;
    float intervaloMovimiento = 0.15f;
    string nombreJugador = "";
    int contadorFrames = 0;

    // --- Sistema de Audio ---
    Sound sonidoComer;
    Sound sonidoTrampa;
    Sound sonidoGameOver;
    Music musicaMenu;
    Music musicaJuego;
    float pitchMusica = 0.2f;
    bool audioCargado = false;
    bool salirDelJuego = false;

    // --- Control de Flujo ---
    bool estaPausado = false;
    Stopwatch cronometroJuego = new Stopwatch();
    Random aleatorio = new Random();

    // Estados posibles del juego
    enum Estado { Menu, IngresoNombre, Jugando, FinJuego, Puntuaciones }
    Estado estadoActual = Estado.Menu;

    // ============================================
    // MÉTODO PRINCIPAL
    // ============================================
    public void Ejecutar()
    {
        Raylib.InitWindow(AnchoPantalla, AltoVentana, "Snake - Estructuras de Datos");
        Raylib.InitAudioDevice();
        Raylib.SetTargetFPS(60);

        Image imagenIcono = Raylib.LoadImage("resources/icono.png");
        Raylib.SetWindowIcon(imagenIcono);
        Raylib.UnloadImage(imagenIcono);

        CargarAudio();

        // Bucle Principal del Juego
        while (!Raylib.WindowShouldClose() && !salirDelJuego)
        {
            GestionarMusica();
            contadorFrames++;

            // Máquina de Estados
            switch (estadoActual)
            {
                case Estado.Menu:
                    DibujarMenu();
                    break;
                case Estado.IngresoNombre:
                    ActualizarIngresoNombre();
                    DibujarIngresoNombre();
                    break;
                case Estado.Jugando:
                    ActualizarJuego();
                    DibujarJuego();
                    break;
                case Estado.FinJuego:
                    ActualizarFinJuego();
                    DibujarFinJuego();
                    break;
                case Estado.Puntuaciones:
                    if (Raylib.IsKeyPressed(KeyboardKey.Escape)) estadoActual = Estado.Menu;
                    DibujarPuntuaciones();
                    break;
            }
        }

        DescargarAudio();
        Raylib.CloseAudioDevice();
        Raylib.CloseWindow();

        Environment.Exit(0);
    }

    // ============================================
    // SISTEMA DE AUDIO
    // ============================================
    void CargarAudio()
    {
        try
        {
            // Carga los archivos desde la carpeta resources
            sonidoComer = Raylib.LoadSound("resources/comer.mp3");
            sonidoTrampa = Raylib.LoadSound("resources/trampa.mp3");
            sonidoGameOver = Raylib.LoadSound("resources/game-over.mp3");
            musicaMenu = Raylib.LoadMusicStream("resources/musica-menu.mp3");
            musicaJuego = Raylib.LoadMusicStream("resources/musica-juego.mp3");

            Raylib.PlayMusicStream(musicaMenu);
            Raylib.SetMusicVolume(musicaMenu, 0.2f);
            Raylib.SetMusicVolume(musicaJuego, 0.4f);

            audioCargado = true;
        }
        catch
        {
            Console.WriteLine("Error cargando audio. Verifica la carpeta resources.");
        }
    }

    void GestionarMusica()
    {
        if (!audioCargado) return;

        // Dependiendo del estado, actualizamos un stream u otro
        if (estadoActual == Estado.Menu || estadoActual == Estado.IngresoNombre || estadoActual == Estado.Puntuaciones)
        {
            if (!Raylib.IsMusicStreamPlaying(musicaMenu)) Raylib.PlayMusicStream(musicaMenu);
            Raylib.UpdateMusicStream(musicaMenu);
        }
        else if (estadoActual == Estado.Jugando)
        {
            Raylib.UpdateMusicStream(musicaJuego);
            Raylib.SetMusicPitch(musicaJuego, pitchMusica);
        }
    }

    void DescargarAudio()
    {
        if (audioCargado) {
            if (Raylib.IsMusicStreamPlaying(musicaMenu)) Raylib.StopMusicStream(musicaMenu);
            if (Raylib.IsMusicStreamPlaying(musicaJuego)) Raylib.StopMusicStream(musicaJuego);

            Raylib.UnloadSound(sonidoComer);
            Raylib.UnloadSound(sonidoTrampa);
            Raylib.UnloadSound(sonidoGameOver);
            Raylib.UnloadMusicStream(musicaMenu);
            Raylib.UnloadMusicStream(musicaJuego);
        }
    }

    // ============================================
    // ESTADO: MENÚ
    // ============================================
    void DibujarMenu()
    {
        Raylib.BeginDrawing();
        Raylib.ClearBackground(ColorFondo);

        CentrarTexto("SNAKE", 100, 50, ColorCabeza);

        if (DibujarBoton("JUGAR", AltoJuego / 2 - 50))
        {
            nombreJugador = "";
            estadoActual = Estado.IngresoNombre;
        }
        if (DibujarBoton("PUNTUACIONES", AltoJuego / 2 + 20))
        {
            estadoActual = Estado.Puntuaciones;
        }
        if (DibujarBoton("SALIR", AltoJuego / 2 + 90))
        {
            salirDelJuego = true;
        }

        Raylib.EndDrawing();
    }

    // ============================================
    // ESTADO: INGRESO NOMBRE
    // ============================================
    void ActualizarIngresoNombre()
    {
        // Captura caracteres del teclado
        int tecla = Raylib.GetCharPressed();
        while (tecla > 0)
        {
            // Filtro: Solo caracteres visibles y límite de 10
            if ((tecla >= 32 && tecla <= 125) && nombreJugador.Length < 10)
            {
                nombreJugador += (char)tecla;
            }
            tecla = Raylib.GetCharPressed();
        }

        // Borrar caracter
        if (Raylib.IsKeyPressed(KeyboardKey.Backspace) && nombreJugador.Length > 0)
        {
            nombreJugador = nombreJugador.Substring(0, nombreJugador.Length - 1);
        }

        // Confirmar nombre
        if (Raylib.IsKeyPressed(KeyboardKey.Enter) && nombreJugador.Length > 0)
        {
            IniciarPartida();
            estadoActual = Estado.Jugando;
        }
    }

    void DibujarIngresoNombre()
    {
        Raylib.BeginDrawing();
        Raylib.ClearBackground(ColorFondo);

        CentrarTexto("INGRESA TU NOMBRE", 200, 30, ColorTexto);
        CentrarTexto("(Limite 10 caracteres)", 250, 10, ColorTexto);

        // Dibuja caja de texto
        int anchoCaja = 300, altoCaja = 50, xCaja = (AnchoPantalla - anchoCaja) / 2, yCaja = 260;
        Raylib.DrawRectangle(xCaja, yCaja, anchoCaja, altoCaja, BotonNormal);
        Raylib.DrawRectangleLines(xCaja, yCaja, anchoCaja, altoCaja, ColorCabeza);

        // Efecto de parpadeo del cursor (_)
        string textoMostrar = nombreJugador;
        if ((contadorFrames / 30) % 2 == 0) textoMostrar += "_";

        int anchoTexto = Raylib.MeasureText(textoMostrar, 30);
        Raylib.DrawText(textoMostrar, xCaja + (anchoCaja - anchoTexto) / 2, yCaja + 10, 30, Color.White);

        CentrarTexto("Presiona ENTER para comenzar", 350, 20, Color.Gray);

        Raylib.EndDrawing();
    }

    // ============================================
    // LÓGICA DEL JUEGO
    // ============================================
    void IniciarPartida()
    {
        serpiente.Limpiar();
        trampas.Limpiar();

        int centroX = (AnchoPantalla / TamanoCelda) / 2;
        int centroY = (AltoJuego / TamanoCelda) / 2;

        // Crea la serpiente hacia atrás para evitar choque inicial
        for (int i = 4; i >= 0; i--)
        {
            serpiente.AgregarCabeza(new Vector2(centroX - i, centroY));
        }

        // Reset de variables
        direccionActual = new Vector2(1, 0);
        direccionSiguiente = new Vector2(1, 0);
        puntuacion = 0;
        nivel = 1;
        intervaloMovimiento = 0.15f;
        estaPausado = false;

        // Configuración de Música de Juego
        if (audioCargado)
        {
            Raylib.StopMusicStream(musicaMenu);
            Raylib.PlayMusicStream(musicaJuego);
            pitchMusica = 0.5f;
            Raylib.SetMusicPitch(musicaJuego, pitchMusica);
        }

        GenerarComida();
        GenerarTrampas();
        cronometroJuego.Restart();
    }

    void GenerarComida()
    {
        int cols = AnchoPantalla / TamanoCelda;
        int filas = AltoJuego / TamanoCelda;
        // Busca posición libre
        do {
            comida = new Vector2(aleatorio.Next(0, cols), aleatorio.Next(0, filas));
        } while (serpiente.Contiene(comida) || trampas.Contiene(comida));
    }

    void GenerarTrampas()
    {
        trampas.Limpiar();
        int cantidad = (nivel + 2) / 2;
        int cols = AnchoPantalla / TamanoCelda;
        int filas = AltoJuego / TamanoCelda;

        for (int i = 0; i < cantidad; i++)
        {
            Vector2 pos;
            do {
                pos = new Vector2(aleatorio.Next(0, cols), aleatorio.Next(0, filas));
            }
            while (serpiente.Contiene(pos) || trampas.Contiene(pos) || Vector2.Distance(pos, comida) < 3);
            trampas.AgregarCabeza(pos);
        }
    }

    void ActualizarJuego()
    {
        if (Raylib.IsKeyPressed(KeyboardKey.P)) estaPausado = !estaPausado;
        if (estaPausado) return;

        // Controles con buffer (evita girar 180 grados sobre sí mismo)
        if (Raylib.IsKeyDown(KeyboardKey.W) && direccionActual.Y == 0) direccionSiguiente = new Vector2(0, -1);
        if (Raylib.IsKeyDown(KeyboardKey.S) && direccionActual.Y == 0) direccionSiguiente = new Vector2(0, 1);
        if (Raylib.IsKeyDown(KeyboardKey.A) && direccionActual.X == 0) direccionSiguiente = new Vector2(-1, 0);
        if (Raylib.IsKeyDown(KeyboardKey.D) && direccionActual.X == 0) direccionSiguiente = new Vector2(1, 0);

        // Control de tiempo para movimiento
        temporizadorMovimiento += Raylib.GetFrameTime();
        if (temporizadorMovimiento >= intervaloMovimiento)
        {
            temporizadorMovimiento = 0;
            MoverSerpiente();
        }
    }

    void MoverSerpiente()
    {
        // Seguridad: Si la lista está vacía, no hace nada
        if (serpiente.Cabeza == null || serpiente.Cola == null) return;

        direccionActual = direccionSiguiente;
        Vector2 nuevaCabeza = serpiente.Cabeza.Posicion + direccionActual;

        // Lógica de "Mundo Infinito" (Teletransporte en bordes)
        int cols = AnchoPantalla / TamanoCelda;
        int filas = AltoJuego / TamanoCelda;

        if (nuevaCabeza.X >= cols) nuevaCabeza.X = 0;
        else if (nuevaCabeza.X < 0) nuevaCabeza.X = cols - 1;

        if (nuevaCabeza.Y >= filas) nuevaCabeza.Y = 0;
        else if (nuevaCabeza.Y < 0) nuevaCabeza.Y = filas - 1;

        // Detección de choque propio
        if (serpiente.Contiene(nuevaCabeza) && nuevaCabeza != serpiente.Cola.Posicion)
        {
            if (audioCargado) Raylib.PlaySound(sonidoTrampa);
            TerminarJuego();
            return;
        }

        serpiente.AgregarCabeza(nuevaCabeza);

        // Detección de colisiones con objetos
        if (Vector2.Distance(nuevaCabeza, comida) < 0.1f)
        {
            if (audioCargado) Raylib.PlaySound(sonidoComer);

            puntuacion += 10;
            // Si llega a tamaño 10, sube de nivel
            if (serpiente.Cantidad >= 10) SubirNivel();
            else GenerarComida();
        }
        else if (trampas.Contiene(nuevaCabeza))
        {
            if (audioCargado) Raylib.PlaySound(sonidoTrampa);

            trampas.RemoverEnPosicion(nuevaCabeza);
            serpiente.RemoverCola();

            // Si es muy pequeña, muere
            if (serpiente.Cantidad <= 1)
            {
                TerminarJuego();
                return;
            }

            serpiente.RemoverCola();
            puntuacion = Math.Max(0, puntuacion - 20);
        }
        else
        {
            serpiente.RemoverCola();
        }
    }

    void SubirNivel()
    {
        nivel++;
        puntuacion += 50;
        intervaloMovimiento *= 0.9f;

        // Aumenta el pitch (velocidad) de la música
        pitchMusica += 0.05f;

        // Reinicia tamaño a 5
        while (serpiente.Cantidad > 5)
        {
            serpiente.RemoverCola();
        }

        GenerarTrampas();
        GenerarComida();
    }

    void TerminarJuego()
    {
        estadoActual = Estado.FinJuego;
        cronometroJuego.Stop();
        if (audioCargado) {
            Raylib.StopMusicStream(musicaJuego);
            Raylib.PlaySound(sonidoGameOver);
        }
        GuardarPuntuacion();
    }

    void GuardarPuntuacion()
    {
        try
        {
            string tiempo = cronometroJuego.Elapsed.ToString(@"mm\:ss");
            string linea = $"{nombreJugador}|{puntuacion}|{tiempo}|{nivel}";
            File.AppendAllLines("registros_snake.txt", new[] { linea });
        }
        catch { }
    }

    // ============================================
    // DIBUJADO DEL JUEGO Y HUD
    // ============================================
    void DibujarJuego()
    {
        Raylib.BeginDrawing();
        Raylib.ClearBackground(ColorFondo);

        // Dibuja Grid
        for (int i = 0; i < AnchoPantalla / TamanoCelda; i++)
            Raylib.DrawLine(i * TamanoCelda, 0, i * TamanoCelda, AltoJuego, ColorGrid);
        for (int i = 0; i < AltoJuego / TamanoCelda; i++)
            Raylib.DrawLine(0, i * TamanoCelda, AnchoPantalla, i * TamanoCelda, ColorGrid);

        // Dibuja Trampas
        Nodo? nodoTrampa = trampas.Cabeza;
        while (nodoTrampa != null)
        {
            DibujarCelda(nodoTrampa.Posicion, ColorTrampa, true);
            nodoTrampa = nodoTrampa.Siguiente;
        }

        // Dibuja Comida
        DibujarCelda(comida, ColorComida, false);

        // Dibuja Serpiente
        Nodo? nodoSerpiente = serpiente.Cabeza;
        bool esCabeza = true;
        while (nodoSerpiente != null)
        {
            DibujarCelda(nodoSerpiente.Posicion, esCabeza ? ColorCabeza : ColorCuerpo, false);
            esCabeza = false;
            nodoSerpiente = nodoSerpiente.Siguiente;
        }

        // Interfaz
        Raylib.DrawRectangle(0, AltoJuego, AnchoPantalla, AltoHUD, new Color(15, 15, 20, 255));
        Raylib.DrawLine(0, AltoJuego, AnchoPantalla, AltoJuego, ColorCabeza);

        int yFila1 = AltoJuego + 10;
        int yFila2 = AltoJuego + 35;

        // Fila 1: Datos principales
        Raylib.DrawText($"JUGADOR: {nombreJugador}", 20, yFila1, 20, ColorTexto);
        Raylib.DrawText($"PUNTOS: {puntuacion}", 300, yFila1, 20, ColorTexto);
        Raylib.DrawText($"TIEMPO: {cronometroJuego.Elapsed:mm\\:ss}", 600, yFila1, 20, ColorTexto);

        // Fila 2: Estadísticas (Nivel, Tamaño, Velocidad)
        Raylib.DrawText($"NIVEL: {nivel}", 20, yFila2, 20, Color.Yellow);
        Raylib.DrawText($"TAMAÑO: {serpiente.Cantidad}", 300, yFila2, 20, Color.Orange);

        // Cálculo visual de velocidad (ej. 1.0x, 1.1x)
        float velocidadVisual = 0.15f / intervaloMovimiento;
        Raylib.DrawText($"VELOCIDAD: {velocidadVisual:0.0}x", 600, yFila2, 20, Color.Red);

        if (estaPausado) CentrarTexto("PAUSA", AltoJuego / 2, 40, Color.Yellow);

        Raylib.EndDrawing();
    }

    // Función auxiliar para dibujar un cuadro
    void DibujarCelda(Vector2 pos, Color color, bool esTrampa)
    {
        int x = (int)pos.X * TamanoCelda;
        int y = (int)pos.Y * TamanoCelda;
        Raylib.DrawRectangle(x + 2, y + 2, TamanoCelda - 4, TamanoCelda - 4, color);
        if (esTrampa) {
            // Dibuja una X en las trampas
            Raylib.DrawLine(x + 5, y + 5, x + TamanoCelda - 5, y + TamanoCelda - 5, Color.Black);
            Raylib.DrawLine(x + TamanoCelda - 5, y + 5, x + 5, y + TamanoCelda - 5, Color.Black);
        }
    }

    // ============================================
    // ESTADO: FIN DEL JUEGO
    // ============================================
    void ActualizarFinJuego()
    {
        if (Raylib.IsKeyPressed(KeyboardKey.Enter))
        {
            estadoActual = Estado.Menu;
            if (audioCargado) Raylib.PlayMusicStream(musicaMenu);
        }
    }

    void DibujarFinJuego()
    {
        Raylib.BeginDrawing();
        Raylib.DrawRectangle(0, AltoJuego/2 - 60, AnchoPantalla, 120, new Color(0,0,0,230));

        CentrarTexto("FIN DEL JUEGO", AltoJuego / 2 - 40, 40, Color.Red);
        CentrarTexto($"{nombreJugador} - Puntos: {puntuacion}", AltoJuego / 2 + 10, 20, ColorTexto);
        CentrarTexto("Presiona ENTER para volver al menú", AltoJuego / 2 + 40, 20, Color.Gray);

        Raylib.EndDrawing();
    }

    // ============================================
    // ESTADO: PUNTUACIONES
    // ============================================
    void DibujarPuntuaciones()
    {
        Raylib.BeginDrawing();
        Raylib.ClearBackground(ColorFondo);
        CentrarTexto("MEJORES PUNTUACIONES", 50, 40, ColorCabeza);

        if (File.Exists("registros_snake.txt"))
        {
            string[] lineas = File.ReadAllLines("registros_snake.txt");

            var registros = new System.Collections.Generic.List<(string nombre, int puntos, string tiempo, string nivel)>();
            foreach (var linea in lineas)
            {
                var partes = linea.Split('|');
                if (partes.Length == 4 && int.TryParse(partes[1], out int pts))
                {
                    registros.Add((partes[0], pts, partes[2], partes[3]));
                }
            }

            if (registros.Count == 0)
            {
                CentrarTexto("No hay registros válidos", 200, 20, Color.Gray);
            }
            else
            {
                registros.Sort((a, b) => b.puntos.CompareTo(a.puntos));
                int mostrar = Math.Min(10, registros.Count);
                int y = 120;
                for (int i = 0; i < mostrar; i++)
                {
                    var r = registros[i];
                    CentrarTexto($"{i + 1}. {r.nombre} - {r.puntos} pts - Nivel {r.nivel} - {r.tiempo}", y, 20, ColorTexto);
                    y += 30;
                }
            }
        }
        else
        {
            CentrarTexto("No hay registros aún", 200, 20, Color.Gray);
        }

        if (DibujarBoton("VOLVER", AltoJuego - 50))
        {
            estadoActual = Estado.Menu;
        }
        Raylib.EndDrawing();
    }

    // ============================================
    // FUNCIONES AUXILIARES
    // ============================================
    bool DibujarBoton(string texto, int y)
    {
        int ancho = 200, alto = 50, x = (AnchoPantalla - ancho) / 2;
        Rectangle rectBtn = new Rectangle(x, y, ancho, alto);

        Vector2 mousePos = Raylib.GetMousePosition();
        bool mouseEncima = Raylib.CheckCollisionPointRec(mousePos, rectBtn);

        Raylib.DrawRectangleRec(rectBtn, mouseEncima ? BotonHover : BotonNormal);
        Raylib.DrawRectangleLinesEx(rectBtn, 2, mouseEncima ? ColorCabeza : ColorGrid);

        int anchoTexto = Raylib.MeasureText(texto, 20);
        Raylib.DrawText(texto, x + (ancho - anchoTexto) / 2, y + 15, 20, ColorTexto);

        return mouseEncima && Raylib.IsMouseButtonPressed(MouseButton.Left);
    }

    void CentrarTexto(string texto, int y, int tamanoFuente, Color color)
    {
        int anchoTexto = Raylib.MeasureText(texto, tamanoFuente);
        Raylib.DrawText(texto, (AnchoPantalla - anchoTexto) / 2, y, tamanoFuente, color);
    }
}

// ============================================
// CLASE PROGRAMA
// ============================================
class Programa
{
    static void Main()
    {
        JuegoSnake juego = new JuegoSnake();
        juego.Ejecutar();
    }
}
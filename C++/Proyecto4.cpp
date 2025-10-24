#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cstdlib>
#include <ctime>
#include <algorithm>
#include <cmath>
#include <tuple>

using namespace std;

// ==================== CONSTANTES ====================
const int TAMANO_TABLERO = 20;
const int MAX_NIVELES = 5;

const string RESET = "\033[0m", ROJO = "\033[91m", VERDE = "\033[92m";
const string AMARILLO = "\033[93m", AZUL = "\033[94m", MAGENTA = "\033[95m";
const string CIAN = "\033[96m", BLANCO = "\033[97m", GRIS = "\033[90m";

struct ConfiguracionNivel {
    int cantidadVirus, barreras, antidotos, probabilidadPropagacion;
    string descripcion;
};

const ConfiguracionNivel NIVELES[MAX_NIVELES] = {
    {1, 10, 3, 10, "Tutorial - Conten el virus"},
    {2, 8, 2, 25, "Facil - La amenaza crece"},
    {3, 6, 2, 40, "Intermedio - Estrategia"},
    {5, 5, 1, 60, "Dificil - Alta presion"},
    {10, 4, 1, 85, "Extremo - Supervivencia"}
};

struct Posicion {
    int x, y;
    Posicion(int px = 0, int py = 0) : x(px), y(py) {}
};

// ==================== CLASE PRINCIPAL ====================
class VirusOutbreak {
private:
    char tablero[TAMANO_TABLERO][TAMANO_TABLERO];
    vector<Posicion> listaVirus;
    Posicion posJugador, posSalida;
    string nombreJugador, razonDerrota;
    int nivelActual, barreras, antidotos, turnos, puntuacionTotal;
    int barrerasIniciales, antidotosIniciales;
    bool juegoActivo, nivelCompletado;
    
    void limpiarPantalla() {
        system("cls");
    }
    
    bool esPosicionValida(int x, int y) {
        return x >= 0 && x < TAMANO_TABLERO && y >= 0 && y < TAMANO_TABLERO;
    }
    
    int obtenerDistancia(const Posicion& p1, const Posicion& p2) {
        return abs(p1.x - p2.x) + abs(p1.y - p2.y);
    }
    
    void generarNivel(int nivel) {
        // Limpiar tablero
        for (int i = 0; i < TAMANO_TABLERO; i++)
            for (int j = 0; j < TAMANO_TABLERO; j++)
                tablero[i][j] = '0';
        listaVirus.clear();
        
        // Jugador (centro, no en bordes extremos)
        posJugador.x = 2 + rand() % 16;
        posJugador.y = 2 + rand() % 16;
        tablero[posJugador.x][posJugador.y] = 'P';
        
        // Salida (lejos del jugador)
        do {
            posSalida.x = rand() % TAMANO_TABLERO;
            posSalida.y = rand() % TAMANO_TABLERO;
        } while (obtenerDistancia(posJugador, posSalida) < 8);
        tablero[posSalida.x][posSalida.y] = 'S';
        
        // Virus mejorados: distribuidos y separados
        int cantVirus = NIVELES[nivel - 1].cantidadVirus;
        int intentos = 0;
        
        while (listaVirus.size() < cantVirus && intentos < 1000) {
            Posicion v(rand() % TAMANO_TABLERO, rand() % TAMANO_TABLERO);
            intentos++;
            
            // Verificar celda vacía
            if (tablero[v.x][v.y] != '0') continue;
            
            // Lejos del jugador
            if (obtenerDistancia(posJugador, v) < 5) continue;
            
            // Lejos de la salida
            if (obtenerDistancia(posSalida, v) < 10) continue;
            
            // Lejos de otros virus
            bool muyCerca = false;
            for (const Posicion& otro : listaVirus) {
                if (obtenerDistancia(v, otro) < 8) {
                    muyCerca = true;
                    break;
                }
            }
            if (muyCerca) continue;
            
            // Colocar virus
            tablero[v.x][v.y] = 'V';
            listaVirus.push_back(v);
            intentos = 0;
        }
    }
    
    void renderizar() {
        limpiarPantalla();
        cout << CIAN << "================================================\n";
        cout << "    VIRUS OUTBREAK - Nivel " << nivelActual << "/" << MAX_NIVELES << "\n";
        cout << "================================================\n" << RESET;
        cout << CIAN << "| " << BLANCO << "Puntos: " << puntuacionTotal 
             << GRIS << " | Turnos: " << turnos << "                    " << CIAN << "|\n" << RESET;
        cout << CIAN << "| " << AZUL << "Barreras: " << barreras 
             << MAGENTA << " | Antidotos: " << antidotos << "                     " << CIAN << "|\n" << RESET;
        cout << CIAN << "| " << BLANCO << "Virus activos: " << listaVirus.size() 
             << " | Propagacion: " << NIVELES[nivelActual - 1].probabilidadPropagacion << "%     " << CIAN << "|\n" << RESET;
        cout << CIAN << "================================================\n" << RESET;
        
        for (int y = 0; y < TAMANO_TABLERO; y++) {
            cout << CIAN << "| " << RESET;
            for (int x = 0; x < TAMANO_TABLERO; x++) {
                switch (tablero[x][y]) {
                    case '0': cout << GRIS << "0 " << RESET; break;
                    case 'P': cout << VERDE << "P " << RESET; break;
                    case 'V': cout << ROJO << "V " << RESET; break;
                    case 'B': cout << AZUL << "B " << RESET; break;
                    case 'S': cout << AMARILLO << "S " << RESET; break;
                }
            }
            cout << CIAN << "|\n" << RESET;
        }
        
        cout << CIAN << "================================================\n" << RESET;
        cout << CIAN << "| " << BLANCO << "[WASD] Mover  [B] Barrera  [C] Antidoto       " << CIAN << "|\n" << RESET;
        cout << CIAN << "| " << BLANCO << "[G] Guardar   [Q] Salir                        " << CIAN << "|\n" << RESET;
        cout << CIAN << "================================================\n" << RESET;
    }
    
    void moverJugador(int dx, int dy) {
        int nuevoX = posJugador.x + dx;
        int nuevoY = posJugador.y + dy;
        
        if (!esPosicionValida(nuevoX, nuevoY)) return;
        
        char celdaObjetivo = tablero[nuevoX][nuevoY];
        if (celdaObjetivo == 'V' || celdaObjetivo == 'B') {
            cout << ROJO << "\nNo puedes moverte ahi!\n" << RESET;
            system("pause");
            return;
        }
        
        tablero[posJugador.x][posJugador.y] = '0';
        posJugador.x = nuevoX;
        posJugador.y = nuevoY;
        tablero[posJugador.x][posJugador.y] = 'P';
    }
    
    void colocarBarrera() {
        if (barreras <= 0) {
            cout << ROJO << "\nNo tienes barreras disponibles!\n" << RESET;
            system("pause");
            return;
        }
        
        cout << "\nDireccion para barrera [W/A/S/D]: ";
        char dir;
        cin >> dir;
        cin.ignore();
        
        int dx = 0, dy = 0;
        switch (tolower(dir)) {
            case 'w': dy = -1; break;
            case 's': dy = 1; break;
            case 'a': dx = -1; break;
            case 'd': dx = 1; break;
            default: return;
        }
        
        int objetivoX = posJugador.x + dx;
        int objetivoY = posJugador.y + dy;
        
        if (!esPosicionValida(objetivoX, objetivoY)) return;
        
        if (tablero[objetivoX][objetivoY] == '0') {
            tablero[objetivoX][objetivoY] = 'B';
            barreras--;
            cout << VERDE << "\nBarrera colocada!\n" << RESET;
        } else {
            cout << ROJO << "\nNo puedes colocar barrera ahi!\n" << RESET;
        }
        system("pause");
    }
    
    void usarAntidoto() {
        if (antidotos <= 0) {
            cout << ROJO << "\nNo tienes antidotos disponibles!\n" << RESET;
            system("pause");
            return;
        }
        
        int direcciones[8][2] = {{-1,-1},{0,-1},{1,-1},{-1,0},{1,0},{-1,1},{0,1},{1,1}};
        int virusEliminados = 0;
        
        for (int i = 0; i < 8; i++) {
            int verificarX = posJugador.x + direcciones[i][0];
            int verificarY = posJugador.y + direcciones[i][1];
            
            if (esPosicionValida(verificarX, verificarY) && tablero[verificarX][verificarY] == 'V') {
                tablero[verificarX][verificarY] = '0';
                for (auto it = listaVirus.begin(); it != listaVirus.end(); ++it) {
                    if (it->x == verificarX && it->y == verificarY) {
                        listaVirus.erase(it);
                        break;
                    }
                }
                virusEliminados++;
            }
        }
        
        antidotos--;
        cout << VERDE << "\nAntidoto usado! " << virusEliminados << " virus eliminados!\n" << RESET;
        system("pause");
    }
    
    void propagarVirus() {
        vector<Posicion> nuevosVirus;
        int direcciones[4][2] = {{0,-1},{0,1},{-1,0},{1,0}};
        
        for (const Posicion& virus : listaVirus) {
            for (int i = 0; i < 4; i++) {
                int nuevoX = virus.x + direcciones[i][0];
                int nuevoY = virus.y + direcciones[i][1];
                if (esPosicionValida(nuevoX, nuevoY) && tablero[nuevoX][nuevoY] == '0') {
                    tablero[nuevoX][nuevoY] = 'V';
                    nuevosVirus.push_back(Posicion(nuevoX, nuevoY));
                }
            }
        }
        
        for (const Posicion& pos : nuevosVirus) {
            listaVirus.push_back(pos);
        }
    }
    
    bool todosVirusContenidos() {
        if (listaVirus.size() < NIVELES[nivelActual - 1].cantidadVirus / 2) return false;
        
        int direcciones[4][2] = {{0,-1},{0,1},{-1,0},{1,0}};
        for (const Posicion& virus : listaVirus) {
            for (int i = 0; i < 4; i++) {
                int x = virus.x + direcciones[i][0];
                int y = virus.y + direcciones[i][1];
                if (esPosicionValida(x, y) && tablero[x][y] == '0') return false;
            }
        }
        return true;
    }
    
    bool tieneMovimientosValidos() {
        int direcciones[4][2] = {{0,-1},{0,1},{-1,0},{1,0}};
        for (int i = 0; i < 4; i++) {
            int x = posJugador.x + direcciones[i][0];
            int y = posJugador.y + direcciones[i][1];
            if (esPosicionValida(x, y)) {
                char c = tablero[x][y];
                if (c == '0' || c == 'S') return true;
            }
        }
        return false;
    }
    
    void verificarEstadoJuego() {
        // Victoria: Salida alcanzada
        if (posJugador.x == posSalida.x && posJugador.y == posSalida.y) {
            manejarNivelCompletado();
            return;
        }
        
        // Victoria: Virus contenidos
        if (listaVirus.size() > 0 && todosVirusContenidos()) {
            manejarNivelCompletado();
            return;
        }
        
        // Derrota: 90% infectado
        int celdasInfectadas = 0;
        for (int i = 0; i < TAMANO_TABLERO; i++)
            for (int j = 0; j < TAMANO_TABLERO; j++)
                if (tablero[i][j] == 'V') celdasInfectadas++;
        
        if (celdasInfectadas * 100 / (TAMANO_TABLERO * TAMANO_TABLERO) >= 90) {
            razonDerrota = "El virus infecto mas del 90% del tablero";
            manejarJuegoTerminado();
            return;
        }
        
        // Derrota: Sin movimientos
        if (!tieneMovimientosValidos()) {
            razonDerrota = "Quedaste atrapado sin movimientos validos";
            manejarJuegoTerminado();
            return;
        }
    }
    
    int calcularPuntuacionNivel() {
        int base = nivelActual * 200;
        int usadasBarreras = (barrerasIniciales - barreras) * 50;
        int usadosAntidotos = (antidotosIniciales - antidotos) * 100;
        int restantesBarreras = barreras * 30;
        int restantesAntidotos = antidotos * 80;
        int penalidad = listaVirus.size() * 2;
        int bonusTurnos = max(0, 50 - turnos);

        int resultado = max(0, base + usadasBarreras + usadosAntidotos + restantesBarreras + restantesAntidotos - penalidad + bonusTurnos);
        return resultado;
    }
    
    void manejarNivelCompletado() {
        nivelCompletado = true;
        int puntuacionNivel = calcularPuntuacionNivel();
        puntuacionTotal += puntuacionNivel;
        
        limpiarPantalla();
        cout << VERDE << "========================================\n";
        cout << "          NIVEL COMPLETADO!            \n";
        cout << "========================================\n" << RESET;
        cout << "  Nivel: " << nivelActual << "/" << MAX_NIVELES << "\n";
        cout << "  Puntos obtenidos: " << puntuacionNivel << "\n";
        cout << "  Puntos totales: " << puntuacionTotal << "\n";
        cout << VERDE << "========================================\n" << RESET;
        system("pause");
        
        if (nivelActual < MAX_NIVELES) {
            nivelActual++;
            iniciarNivel(nivelActual);
        } else {
            cout << AMARILLO << "\nFELICIDADES! Has completado todos los niveles!\n" << RESET;
            system("pause");
            guardarPuntuacion();
        }
    }
    
    void manejarJuegoTerminado() {
        nivelCompletado = true;
        limpiarPantalla();
        cout << ROJO << "========================================\n";
        cout << "            GAME OVER                   \n";
        cout << "========================================\n" << RESET;
        cout << "  " << razonDerrota << "\n";
        cout << "  Nivel alcanzado: " << nivelActual << "/" << MAX_NIVELES << "\n";
        cout << "  Puntos totales: " << puntuacionTotal << "\n";
        cout << ROJO << "========================================\n" << RESET;
        system("pause");
        guardarPuntuacion();
    }
    
    void procesarEntrada(char entrada) {
        entrada = tolower(entrada);
        switch (entrada) {
            case 'w': moverJugador(0, -1); break;
            case 's': moverJugador(0, 1); break;
            case 'a': moverJugador(-1, 0); break;
            case 'd': moverJugador(1, 0); break;
            case 'b': colocarBarrera(); break;
            case 'c': usarAntidoto(); break;
            case 'g': guardarPartida(); break;
            case 'q': nivelCompletado = juegoActivo = false; break;
        }
    }
    
    void bucleJuego() {
        while (!nivelCompletado && juegoActivo) {
            renderizar();
            cout << "\nTu movimiento: ";
            char entrada;
            cin >> entrada;
            cin.ignore();
            
            procesarEntrada(entrada);
            
            if (rand() % 100 < NIVELES[nivelActual - 1].probabilidadPropagacion)
                propagarVirus();
            
            verificarEstadoJuego();
            turnos++;
        }
    }
    
    void iniciarNivel(int nivel) {
        nivelActual = nivel;
        turnos = 0;
        nivelCompletado = false;
        barreras = NIVELES[nivel - 1].barreras;
        antidotos = NIVELES[nivel - 1].antidotos;
        barrerasIniciales = barreras;
        antidotosIniciales = antidotos;

        generarNivel(nivel);
        bucleJuego();
    }
    
    void guardarPartida() {
        ofstream archivo("guardado.txt");
        if (!archivo.is_open()) {
            cout << ROJO << "Error al guardar\n" << RESET;
            return;
        }
        
        archivo << "NOMBRE:" << nombreJugador << "\n";
        archivo << "NIVEL:" << nivelActual << "\n";
        archivo << "TURNO:" << turnos << "\n";
        archivo << "PUNTUACION:" << puntuacionTotal << "\n";
        archivo << "JUGADOR_X:" << posJugador.x << "\n";
        archivo << "JUGADOR_Y:" << posJugador.y << "\n";
        archivo << "BARRERAS:" << barreras << "\n";
        archivo << "ANTIDOTOS:" << antidotos << "\n";
        archivo << "BARRERAS_INI:" << barrerasIniciales << "\n";
        archivo << "ANTIDOTOS_INI:" << antidotosIniciales << "\n";
        archivo << "TABLERO\n";
        
        for (int y = 0; y < TAMANO_TABLERO; y++) {
            for (int x = 0; x < TAMANO_TABLERO; x++)
                archivo << tablero[x][y];
            archivo << "\n";
        }
        
        archivo.close();
        cout << VERDE << "\nPartida guardada!\n" << RESET;
        system("pause");
    }
    
    void cargarPartida() {
        ifstream archivo("guardado.txt");
        if (!archivo.is_open()) {
            cout << ROJO << "No hay partida guardada\n" << RESET;
            system("pause");
            return;
        }
        
        string linea, clave, valor;
        while (getline(archivo, linea) && linea != "TABLERO") {
            size_t pos = linea.find(':');
            if (pos != string::npos) {
                clave = linea.substr(0, pos);
                valor = linea.substr(pos + 1);
                
                if (clave == "NOMBRE") nombreJugador = valor;
                else if (clave == "NIVEL") nivelActual = stoi(valor);
                else if (clave == "TURNO") turnos = stoi(valor);
                else if (clave == "PUNTUACION") puntuacionTotal = stoi(valor);
                else if (clave == "JUGADOR_X") posJugador.x = stoi(valor);
                else if (clave == "JUGADOR_Y") posJugador.y = stoi(valor);
                else if (clave == "BARRERAS") barreras = stoi(valor);
                else if (clave == "ANTIDOTOS") antidotos = stoi(valor);
                else if (clave == "BARRERAS_INI") barrerasIniciales = stoi(valor);
                else if (clave == "ANTIDOTOS_INI") antidotosIniciales = stoi(valor);
            }
        }
        
        listaVirus.clear();
        for (int y = 0; y < TAMANO_TABLERO && getline(archivo, linea); y++) {
            for (int x = 0; x < TAMANO_TABLERO && x < (int)linea.length(); x++) {
                tablero[x][y] = linea[x];
                if (linea[x] == 'V') listaVirus.push_back(Posicion(x, y));
                else if (linea[x] == 'S') posSalida = Posicion(x, y);
            }
        }
        archivo.close();
        
        cout << VERDE << "\nPartida cargada!\n" << RESET;
        system("pause");
        bucleJuego();
    }
    
    void guardarPuntuacion() {
        vector<tuple<int, string, int>> puntuaciones;
        
        ifstream archivoEntrada("puntuaciones.txt");
        if (archivoEntrada.is_open()) {
            string linea;
            while (getline(archivoEntrada, linea)) {
                size_t pos1 = linea.find('|');
                size_t pos2 = linea.find('|', pos1 + 1);
                if (pos1 != string::npos && pos2 != string::npos) {
                    puntuaciones.push_back(tuple<int, string, int>(
                        stoi(linea.substr(0, pos1)),
                        linea.substr(pos1 + 1, pos2 - pos1 - 1),
                        stoi(linea.substr(pos2 + 1))
                    ));
                }
            }
            archivoEntrada.close();
        }
        
        puntuaciones.push_back(tuple<int, string, int>(puntuacionTotal, nombreJugador, nivelActual));
        sort(puntuaciones.begin(), puntuaciones.end(), 
             [](const tuple<int, string, int>& a, const tuple<int, string, int>& b) { 
                 return get<0>(a) > get<0>(b); 
             });
        
        ofstream archivoSalida("puntuaciones.txt");
        int contador = 0;
        for (const auto& p : puntuaciones) {
            if (contador++ >= 10) break;
            archivoSalida << get<0>(p) << "|" << get<1>(p) << "|" << get<2>(p) << "\n";
        }
        archivoSalida.close();
    }
    
    void mostrarPuntuaciones() {
        limpiarPantalla();
        cout << AMARILLO << "========================================\n";
        cout << "         TABLA DE PUNTUACIONES          \n";
        cout << "========================================\n" << RESET;
        
        ifstream archivo("puntuaciones.txt");
        if (!archivo.is_open()) {
            cout << "  No hay puntuaciones registradas\n";
        } else {
            string linea;
            int posicion = 1;
            while (getline(archivo, linea) && posicion <= 10) {
                size_t pos1 = linea.find('|');
                size_t pos2 = linea.find('|', pos1 + 1);
                if (pos1 != string::npos && pos2 != string::npos) {
                    cout << "  " << posicion++ << ". " << linea.substr(pos1 + 1, pos2 - pos1 - 1) 
                         << " - " << linea.substr(0, pos1) << " pts (Nivel " 
                         << linea.substr(pos2 + 1) << ")\n";
                }
            }
            archivo.close();
        }
        
        cout << AMARILLO << "========================================\n" << RESET;
        system("pause");
    }
    
public:
    VirusOutbreak() {
        srand(time(0));
        juegoActivo = true;
        nivelCompletado = false;
        nivelActual = 1;
        puntuacionTotal = 0;
        turnos = 0;
        barrerasIniciales = 0;
        antidotosIniciales = 0;
        razonDerrota = "";
    }
    
    void ejecutar() {
        while (juegoActivo) {
            limpiarPantalla();
            cout << CIAN << "========================================\n";
            cout << "         VIRUS OUTBREAK                 \n";
            cout << "========================================\n" << RESET;
            cout << "  1. Nueva Partida\n";
            cout << "  2. Cargar Partida\n";
            cout << "  3. Puntuaciones\n";
            cout << "  4. Salir\n";
            cout << CIAN << "========================================\n" << RESET;
            cout << "\nSelecciona una opcion: ";
            
            int opcion;
            cin >> opcion;
            cin.ignore();
            
            switch (opcion) {
                case 1: 
                    limpiarPantalla();
                    cout << CIAN << "Ingresa tu nombre: " << RESET;
                    getline(cin, nombreJugador);
                    nivelActual = 1;
                    puntuacionTotal = 0;
                    turnos = 0;
                    iniciarNivel(nivelActual);
                    break;
                case 2: cargarPartida(); break;
                case 3: mostrarPuntuaciones(); break;
                case 4: juegoActivo = false; break;
                default: 
                    cout << ROJO << "Opcion invalida!\n" << RESET;
                    system("pause");
            }
        }
    }
};

int main() {
    VirusOutbreak juego;
    juego.ejecutar();
    cout << CIAN << "\nGracias por jugar!\n" << RESET;
    return 0;
}
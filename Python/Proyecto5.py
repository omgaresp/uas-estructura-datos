# sudoku_juego.py
# Implementación completa en un solo archivo con todas las correcciones y añadidos.

import tkinter as tk
from tkinter import messagebox, simpledialog, font
import os
import random
import time

# ==============================================================================
# SECCIÓN 1: SUDOKU GENERATOR
# ==============================================================================

# Rangos de números iniciales (pistas) por categoría (0-4)
DIFFICULTY_RANGES = {
    0: (36, 49), # Muy Fácil
    1: (32, 35), # Fácil
    2: (28, 31), # Normal
    3: (24, 27), # Difícil
    4: (17, 23)  # Muy Difícil
}

class SudokuGenerator:
    """
    Generador de tableros de Sudoku.
    1. Crea una solución completa usando backtracking.
    2. "Puntúa" agujeros en la solución según la dificultad.
    """
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = None
        self.initial_board = None

    def _is_valid(self, grid, r, c, num):
        """Verifica si un número es válido en una celda (fila, col, caja 3x3)."""
        # Chequear fila
        for col in range(9):
            if grid[r][col] == num:
                return False
        
        # Chequear columna
        for row in range(9):
            if grid[row][c] == num:
                return False

        # Chequear caja 3x3
        start_row, start_col = 3 * (r // 3), 3 * (c // 3)
        for row in range(start_row, start_row + 3):
            for col in range(start_col, start_col + 3):
                if grid[row][col] == num:
                    return False
        
        return True

    def _find_empty(self, grid):
        """Encuentra la próxima celda vacía (valor 0)."""
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    return (r, c)
        return None

    def _generate_full_solution(self):
        """
        Rellena self.grid con una solución completa usando backtracking.
        Esto es un uso intensivo de arrays (listas anidadas).
        """
        empty = self._find_empty(self.grid)
        if not empty:
            return True  # Sudoku resuelto

        row, col = empty
        numbers = list(range(1, 10))
        random.shuffle(numbers) # Introduce aleatoriedad

        for num in numbers:
            if self._is_valid(self.grid, row, col, num):
                self.grid[row][col] = num

                if self._generate_full_solution():
                    return True

                self.grid[row][col] = 0 # Backtrack

        return False

    def _poke_holes(self):
        """
        Elimina números de la solución para crear el tablero inicial.
        """
        if self.solution is None:
            return None
        
        # Copia profunda de la solución para crear el tablero inicial
        self.initial_board = [row[:] for row in self.solution]
        
        min_clues, max_clues = DIFFICULTY_RANGES[self.difficulty]
        num_clues = random.randint(min_clues, max_clues)
        
        holes_to_make = 81 - num_clues
        cells = list(range(81))
        random.shuffle(cells)
        
        for i in range(holes_to_make):
            cell_index = cells[i]
            row = cell_index // 9
            col = cell_index % 9
            self.initial_board[row][col] = 0

    def generate(self):
        """
        Genera y devuelve el tablero inicial y la solución.
        """
        # 1. Generar la solución completa
        self._generate_full_solution()
        self.solution = [row[:] for row in self.grid] # Guardar copia

        # 2. Quitar números según la dificultad
        self._poke_holes()
        
        return self.initial_board, self.solution

# Función de conveniencia
def generate_sudoku(difficulty):
    """
    Genera un par (tablero_inicial, solucion) para la dificultad dada (0-4).
    """
    generator = SudokuGenerator(difficulty)
    return generator.generate()


# ==============================================================================
# SECCIÓN 2: SCORE MANAGER
# ==============================================================================

SCORE_FILE = "scores.txt"

def get_high_scores():
    """
    Lee scores.txt, los ordena y devuelve una lista de tuplas.
    """
    if not os.path.exists(SCORE_FILE):
        return []

    scores = []
    try:
        with open(SCORE_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        name, score, level = line.split('|')
                        scores.append((name, int(score), level))
                    except ValueError:
                        print(f"Línea malformada en scores.txt: {line}")
        
        # Ordenar por score descendente
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    except Exception as e:
        print(f"Error al leer scores: {e}")
        return []

def add_score(name, score, level):
    """
    Añade una nueva línea de score a scores.txt.
    """
    try:
        with open(SCORE_FILE, "a", encoding="utf-8") as f:
            f.write(f"{name}|{score}|{level}\n")
    except Exception as e:
        print(f"Error al guardar score: {e}")


# ==============================================================================
# SECCIÓN 3: SUDOKU ENGINE
# ==============================================================================

# --- Constantes del Juego ---
CATEGORIES = ["Muy Fácil", "Fácil", "Normal", "Difícil", "Muy Difícil"]
SCORE_MULTIPLIERS = [1.0, 1.5, 2.0, 2.5, 3.0]
TIME_PENALTIES = [0.05, 0.08, 0.10, 0.12, 0.15] # Penalización por minuto

class SudokuGame:
    """
    El "Motor" del juego. Maneja toda la lógica SIN interfaz gráfica.
    Utiliza extensivamente listas 2D (arrays) para el estado del tablero.
    """
    
    def __init__(self, player_name):
        self.player_name = player_name
        self.lives = 3
        self.max_lives = 3
        self.current_category = 0 # Índice 0-4
        self.current_level = 0    # Índice 0-4
        self.total_score = 0.0
        
        self.start_time = 0 # Timestamp de inicio del sudoku actual
        
        # Arrays 2D para el estado del tablero
        self.initial_grid = [] # El tablero con los números iniciales
        self.player_grid = []  # Los números colocados por el jugador
        self.solution_grid = [] # La solución completa (para validación rápida)
        
        # Estado para bonificaciones de categoría
        self.lives_lost_in_category = 0
        self.scores_for_category = [] # Lista de scores de los 5 niveles

    def start_new_game(self):
        """Inicia una partida nueva, reseteando estadísticas."""
        self.lives = 3
        self.max_lives = 3
        self.current_category = 0
        self.current_level = 0
        self.total_score = 0.0
        self.lives_lost_in_category = 0
        self.scores_for_category = []
        self.load_next_sudoku()

    def load_next_sudoku(self):
        """Carga el siguiente sudoku (nuevo nivel o nueva categoría)."""
        self.start_time = time.time()
        
        # Inicializa el array 2D del jugador como vacío
        self.player_grid = [[0 for _ in range(9)] for _ in range(9)]
        
        # Genera el nuevo tablero usando la función de la SECCIÓN 1
        self.initial_grid, self.solution_grid = generate_sudoku(self.current_category)

    def place_number(self, r, c, num):
        """Coloca un número en el array 2D del jugador."""
        if self.initial_grid[r][c] == 0:
            self.player_grid[r][c] = num
            return True
        return False # No se puede modificar un número inicial

    def clear_number(self, r, c):
        """Borra un número del array 2D del jugador."""
        return self.place_number(r, c, 0) # Borrar es colocar un 0

    def get_combined_grid(self):
        """
        Retorna un nuevo array 2D combinando el tablero inicial y el del jugador.
        """
        grid = [[0 for _ in range(9)] for _ in range(9)]
        for r in range(9):
            for c in range(9):
                if self.initial_grid[r][c] != 0:
                    grid[r][c] = self.initial_grid[r][c]
                else:
                    grid[r][c] = self.player_grid[r][c]
        return grid

    def check_solution(self):
        """
        Valida el tablero combinado contra las reglas del Sudoku.
        Uso intensivo de acceso a arrays 2D.
        """
        grid = self.get_combined_grid()
        
        # 1. Chequear si está completo (ningún 0)
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    return False

        # 2. Chequear filas y columnas
        for i in range(9):
            row_set = set()
            col_set = set()
            for j in range(9):
                # Chequeo de fila
                if grid[i][j] in row_set: return False
                row_set.add(grid[i][j])
                
                # Chequeo de columna
                if grid[j][i] in col_set: return False
                col_set.add(grid[j][i])

        # 3. Chequear cajas 3x3
        for r_box in range(0, 9, 3):
            for c_box in range(0, 9, 3):
                box_set = set()
                for r in range(r_box, r_box + 3):
                    for c in range(c_box, c_box + 3):
                        if grid[r][c] in box_set: return False
                        box_set.add(grid[r][c])
        
        return True # Si pasa todo, es correcto

    def get_elapsed_time(self):
        """Retorna tupla (minutos_enteros, segundos_enteros) del sudoku actual."""
        elapsed_seconds = int(time.time() - self.start_time)
        return elapsed_seconds // 60, elapsed_seconds % 60

    def _calculate_score(self, minutes):
        """Calcula el score base para un sudoku (sin bonus)."""
        base = 1000
        mult_cat = SCORE_MULTIPLIERS[self.current_category]
        penalty = TIME_PENALTIES[self.current_category]
        
        mult_time = max(0.3, 2.0 - (minutes * penalty))
        
        score = base * mult_cat * mult_time
        return score

    def on_sudoku_complete(self):
        """
        Llamado cuando el jugador verifica y el sudoku es correcto.
        Maneja puntuación, avance de nivel y lógica de vidas.
        """
        mins, secs = self.get_elapsed_time()
        minutes_total = mins + (secs / 60.0)
        
        score_won = self._calculate_score(minutes_total)
        self.scores_for_category.append(score_won)
        self.total_score += score_won
        
        self.current_level += 1
        
        result = {
            "status": "NEXT_LEVEL",
            "score_won": score_won,
            "bonus_applied": 0.0
        }

        # --- Lógica de Fin de Categoría ---
        if self.current_level == 5:
            # 1. Calcular Bonus de Vidas
            bonus_mult = 0.0
            if self.lives_lost_in_category == 0: bonus_mult = 0.50 # +50%
            elif self.lives_lost_in_category == 1: bonus_mult = 0.25 # +25%
            elif self.lives_lost_in_category == 2: bonus_mult = 0.10 # +10%
            
            category_score_sum = sum(self.scores_for_category)
            bonus_amount = category_score_sum * bonus_mult
            self.total_score += bonus_amount
            result["bonus_applied"] = bonus_amount

            # 2. Lógica de Vidas (¡MODIFICADA SEGÚN SOLICITUD!)
            if self.lives_lost_in_category == 0:
                # Si no perdió vidas, GANA 1 vida máxima
                self.max_lives = min(self.max_lives + 1, 10) 
            
            # Siempre se rellenan las vidas al máximo actual
            # (Si perdió vidas, no gana +1 max, pero SÍ rellena)
            self.lives = self.max_lives
            
            # 3. Resetear para siguiente categoría
            self.current_level = 0
            self.current_category += 1
            self.lives_lost_in_category = 0
            self.scores_for_category = []
            
            # 4. Chequear Victoria Total
            if self.current_category == 5:
                result["status"] = "GAME_WIN"
                self.save_to_scores(completed=True)
                self.delete_save_file()
                return result

        # Cargar el siguiente tablero
        self.load_next_sudoku()
        return result

    def restart_board(self):
        """Reinicia el tablero actual, perdiendo una vida."""
        self.lives -= 1
        self.lives_lost_in_category += 1
        
        # Resetea el tablero del jugador y el tiempo
        self.player_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.start_time = time.time()
        
        if self.lives == 0:
            self.save_to_scores(completed=False)
            self.delete_save_file()
            return "GAME_OVER"
        
        return "RESTARTED"

    def get_level_string(self, completed=False):
        """Genera el string de nivel para UI y scores."""
        if completed:
            return f"Nivel 25 - {CATEGORIES[4]} (Completado)"
        
        if self.current_category >= len(CATEGORIES):
            return "VICTORIA"
            
        total_level = (self.current_category * 5) + self.current_level + 1
        cat_name = CATEGORIES[self.current_category]
        return f"Nivel {total_level}/25 - {cat_name}"

    def get_lives_string(self):
        """Retorna string de vidas (ej. ♥♥♥♡)"""
        return f"{'♥' * self.lives}{'♡' * (self.max_lives - self.lives)}"

    # --- MÉTODOS DE TESTING ---

    def fill_randomly(self):
        """(TESTING) Llena las celdas vacías con números aleatorios (1-9)."""
        for r in range(9):
            for c in range(9):
                if self.initial_grid[r][c] == 0:
                    self.player_grid[r][c] = random.randint(1, 9)

    def fill_with_solution(self):
        """(TESTING) Llena las celdas vacías con la solución correcta."""
        for r in range(9):
            for c in range(9):
                if self.initial_grid[r][c] == 0:
                    self.player_grid[r][c] = self.solution_grid[r][c]

    # --- Persistencia (Manejo de Archivos) ---

    def _grid_to_string(self, grid):
        """Convierte un array 2D de 9x9 a un string de 81 dígitos."""
        return "".join(str(num) for row in grid for num in row)

    def _string_to_grid(self, s):
        """Convierte un string de 81 dígitos a un array 2D de 9x9."""
        grid = [[0 for _ in range(9)] for _ in range(9)]
        for r in range(9):
            for c in range(9):
                grid[r][c] = int(s[r*9 + c])
        return grid

    def save_game(self, filename="partida.txt"):
        """Guarda el estado completo del juego en partida.txt."""
        # Necesitamos guardar el estado de la categoría para los bonus
        scores_str = ",".join(map(str, self.scores_for_category))
        
        # AHORA HAY 10 LÍNEAS
        data = [
            self.player_name,
            f"{self.lives},{self.max_lives}",
            f"{self.current_category},{self.current_level}",
            str(int(self.total_score)),
            str(int(self.start_time)),
            self._grid_to_string(self.initial_grid),
            self._grid_to_string(self.player_grid),
            self._grid_to_string(self.solution_grid), # Guardar solución
            str(self.lives_lost_in_category),
            scores_str
        ]
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("\n".join(data))
            return True
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False

    @classmethod
    def load_from_file(cls, filename="partida.txt"):
        """
        Método de clase para crear una instancia de SudokuGame desde un archivo.
        """
        if not os.path.exists(filename):
            return None
        
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines()]
            
            # --- VALIDACIÓN AÑADIDA ---
            # Comprueba si el archivo tiene las 10 líneas esperadas
            if len(lines) < 10:
                print(f"Error al cargar: El archivo '{filename}' está corrupto o es de una versión anterior.")
                if os.path.exists(filename):
                    os.remove(filename) # Borra el archivo malo para evitar futuros errores
                return None
            # --- FIN DE VALIDACIÓN ---

            game = cls(lines[0]) # Inicializa con nombre de jugador
            
            game.lives, game.max_lives = map(int, lines[1].split(','))
            game.current_category, game.current_level = map(int, lines[2].split(','))
            game.total_score = float(lines[3])
            game.start_time = int(lines[4])
            
            game.initial_grid = game._string_to_grid(lines[5])
            game.player_grid = game._string_to_grid(lines[6])
            game.solution_grid = game._string_to_grid(lines[7])
            
            game.lives_lost_in_category = int(lines[8])
            
            if lines[9]:
                game.scores_for_category = list(map(float, lines[9].split(',')))
            else:
                game.scores_for_category = []
            
            return game
        except Exception as e:
            print(f"Error al cargar: {e}")
            return None

    def delete_save_file(self, filename="partida.txt"):
        """Elimina el archivo de partida guardada."""
        if os.path.exists(filename):
            os.remove(filename)

    def save_to_scores(self, completed=False):
        """
        Guarda el resultado final en scores.txt.
        Llama a la función de la SECCIÓN 2.
        """
        level_str = self.get_level_string(completed=completed)
        # Llama a la función global 'add_score'
        add_score(self.player_name, int(self.total_score), level_str)


# ==============================================================================
# SECCIÓN 4: INTERFAZ GRÁFICA (TKINTER)
# ==============================================================================

# --- Configuración de Estilos ---
BG_COLOR = "#F0F0F0"
GRID_BG = "#FFFFFF"
CELL_COLOR = "#EEEEFF"
CELL_SELECTED_COLOR = "#B4D5FF"
FIXED_CELL_COLOR = "#E0E0E0"
FIXED_FONT_COLOR = "#333333"
USER_FONT_COLOR = "#0000AA"

class SudokuApp:
    """
    La aplicación principal de Tkinter.
    Maneja toda la UI y se comunica con el SudokuGame (el motor).
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.root.geometry("500x720") # -> Altura aumentada para los nuevos botones
        self.root.configure(bg=BG_COLOR)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close_window)

        self.game_engine = None # Instancia de SudokuGame (SECCIÓN 3)
        
        # --- Fuentes ---
        self.cell_font = font.Font(family="Helvetica", size=18)
        self.fixed_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.status_font = font.Font(family="Helvetica", size=12)
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        # --- FUENTE AÑADIDA (CORRECCIÓN ERROR 'weight') ---
        self.status_font_bold = font.Font(family="Helvetica", size=12, weight="bold")


        # --- Frames Principales ---
        self.main_menu_frame = tk.Frame(root, bg=BG_COLOR)
        self.game_frame = tk.Frame(root, bg=BG_COLOR)

        # --- Array 2D de UI (Labels) ---
        # Este array de widgets se mapea directamente a los arrays del motor
        self.cell_labels = [[None for _ in range(9)] for _ in range(9)]
        self.selected_cell = None # Tupla (r, c)
        
        self.create_game_widgets()
        self.create_main_menu()

    def create_main_menu(self):
        """Muestra el menú principal y oculta el juego."""
        self.game_frame.pack_forget()
        self.main_menu_frame.pack(fill="both", expand=True)

        for widget in self.main_menu_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_menu_frame, text="SUDOKU GAME", font=self.title_font, bg=BG_COLOR, pady=40).pack()

        btn_style = {"font": self.status_font, "width": 20, "pady": 10}
        
        tk.Button(self.main_menu_frame, text="Nueva Partida", **btn_style, command=self.new_game).pack(pady=10)
        tk.Button(self.main_menu_frame, text="Cargar Partida", **btn_style, command=self.load_game).pack(pady=10)
        tk.Button(self.main_menu_frame, text="Scores", **btn_style, command=self.show_scores).pack(pady=10)
        tk.Button(self.main_menu_frame, text="Salir", **btn_style, command=self.on_close_window).pack(pady=10)

        # Actualiza el estado del botón "Cargar Partida"
        self.update_load_button_state()

    def update_load_button_state(self):
        """Desactiva el botón Cargar si no existe partida.txt"""
        load_button_exists = False
        for child in self.main_menu_frame.winfo_children():
            if child.cget("text") == "Cargar Partida":
                load_button_exists = True
                if not os.path.exists("partida.txt"):
                    child.config(state="disabled")
                else:
                    child.config(state="normal")
        return load_button_exists


    def create_game_widgets(self):
        """Crea los widgets del juego (tablero, botones), pero los mantiene ocultos."""
        
        # --- 1. Frame de Estado (Superior) ---
        stats_frame = tk.Frame(self.game_frame, bg=BG_COLOR)
        stats_frame.pack(fill="x", pady=10)
        
        self.status_label = tk.Label(stats_frame, text="Nivel 1 - Muy Fácil", font=self.status_font, bg=BG_COLOR)
        self.status_label.pack(side="left", padx=10)
        
        self.score_label = tk.Label(stats_frame, text="Score: 0", font=self.status_font, bg=BG_COLOR)
        self.score_label.pack(side="right", padx=10)

        # --- 2. Frame de Vidas y Tiempo ---
        info_frame = tk.Frame(self.game_frame, bg=BG_COLOR)
        info_frame.pack(fill="x", pady=5)
        
        self.lives_label = tk.Label(info_frame, text="Vidas: ♥♥♥", font=self.status_font, bg=BG_COLOR)
        self.lives_label.pack(side="left", padx=10)
        
        self.time_label = tk.Label(info_frame, text="Tiempo: 00:00", font=self.status_font, bg=BG_COLOR)
        self.time_label.pack(side="right", padx=10)
        
        # --- 3. Frame del Tablero (Central) ---
        grid_frame = tk.Frame(self.game_frame, bg=GRID_BG, bd=2, relief="solid")
        grid_frame.pack(pady=10)

        for r in range(9):
            for c in range(9):
                cell = tk.Label(grid_frame,
                                text="",
                                font=self.cell_font,
                                width=2,
                                height=1,
                                bd=1,
                                relief="solid",
                                bg=CELL_COLOR)
                
                # Padding para crear las líneas 3x3 más gruesas
                pad_x = (1, 4) if (c + 1) % 3 == 0 and c != 8 else (1, 1)
                pad_y = (1, 4) if (r + 1) % 3 == 0 and r != 8 else (1, 1)
                
                cell.grid(row=r, column=c, padx=pad_x, pady=pad_y)
                
                # Bindings para clic y teclas
                cell.bind("<Button-1>", lambda e, r=r, c=c: self.on_cell_click(r, c))
                
                self.cell_labels[r][c] = cell # Guardar en el array 2D de widgets

        # Binds de teclado globales
        self.root.bind("<Key>", self.on_key_press)
        
        # --- 4. Frame de Botones (Inferior) ---
        button_frame = tk.Frame(self.game_frame, bg=BG_COLOR)
        button_frame.pack(fill="x", pady=5) # Padding reducido
        
        btn_style = {"font": self.status_font, "width": 12}

        tk.Button(button_frame, text="Verificar", **btn_style, command=self.check_board).pack(side="left", expand=True)
        tk.Button(button_frame, text="Guardar", **btn_style, command=self.save_game).pack(side="left", expand=True)
        tk.Button(button_frame, text="Salir al Menú", **btn_style, command=self.quit_to_menu).pack(side="left", expand=True)

        # --- 5. Frame de Botones de PRUEBA (AÑADIDO) ---
        test_button_frame = tk.Frame(self.game_frame, bg=BG_COLOR)
        test_button_frame.pack(fill="x", pady=(5, 10)) # Padding superior e inferior

        tk.Label(test_button_frame, text="--- Testing ---", font=self.status_font, bg=BG_COLOR).pack()

        test_btn_style = {"font": self.status_font, "width": 15}
        tk.Button(test_button_frame, text="Llenar Aleatorio", **test_btn_style, command=self.fill_random).pack(side="left", expand=True, padx=5)
        tk.Button(test_button_frame, text="Llenar Solución", **test_btn_style, command=self.fill_solution).pack(side="right", expand=True, padx=5)


    def start_game_ui(self):
        """Muestra la UI del juego y oculta el menú."""
        self.main_menu_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)
        
        self.update_board_ui()
        self.update_stats_ui()
        self.update_timer()

    # --- Lógica de Interacción ---

    def new_game(self):
        if os.path.exists("partida.txt"):
            if not messagebox.askyesno("Sobrescribir",
                                       "Ya existe una partida guardada. ¿Deseas sobrescribirla?"):
                return
        
        player_name = simpledialog.askstring("Nuevo Jugador", "Ingresa tu nombre:")
        if not player_name or player_name.strip() == "":
            return # Canceló

        self.game_engine = SudokuGame(player_name.strip()) # Usa la clase de SECCIÓN 3
        self.game_engine.start_new_game()
        self.start_game_ui()

    def load_game(self):
        self.game_engine = SudokuGame.load_from_file() # Usa la clase de SECCIÓN 3
        if self.game_engine is None:
            messagebox.showerror("Error", "No se pudo cargar la partida.\nEl archivo puede estar corrupto o no existe.")
            self.update_load_button_state() # Desactiva el botón si falló la carga
            return
        
        self.start_game_ui()

    def save_game(self):
        if self.game_engine:
            if self.game_engine.save_game():
                messagebox.showinfo("Guardado", "Partida guardada exitosamente.")
            else:
                messagebox.showerror("Error", "No se pudo guardar la partida.")
        # Actualiza el estado del botón Cargar en el menú principal
        self.update_load_button_state()


    def quit_to_menu(self):
        if not self.game_engine:
            self.create_main_menu()
            return
            
        choice = messagebox.askyesnocancel("Salir", "¿Deseas guardar la partida antes de salir?")
        
        if choice is True: # Sí (Guardar)
            self.save_game()
            self.game_engine = None
            self.create_main_menu()
        elif choice is False: # No (Descartar)
            # Como se especificó: Salir sin guardar guarda en scores (partida terminada)
            self.game_engine.save_to_scores(completed=False)
            self.game_engine.delete_save_file()
            self.game_engine = None
            self.create_main_menu()
        # elif choice is None: # Cancelar
            # No hacer nada

    def on_close_window(self):
        """Maneja el clic en la [X] de la ventana."""
        if self.game_engine:
            self.quit_to_menu()
            # Si el usuario cancela quit_to_menu, el juego sigue.
            # Si el juego ya no existe (porque salió al menú), cerramos.
            if self.game_engine is None:
                self.root.destroy()
        else:
            self.root.destroy()

    def show_scores(self):
        scores = get_high_scores() # Usa la función de SECCIÓN 2
        
        score_window = tk.Toplevel(self.root, bg=BG_COLOR)
        score_window.title("Tabla de Scores")
        score_window.geometry("450x400")
        
        tk.Label(score_window, text="TABLA DE SCORES", font=self.title_font, bg=BG_COLOR, pady=10).pack()

        header_frame = tk.Frame(score_window, bg=BG_COLOR, pady=5)
        header_frame.pack(fill="x", padx=20)
        
        # --- LÍNEAS CORREGIDAS (usando self.status_font_bold) ---
        tk.Label(header_frame, text="Nombre", font=self.status_font_bold, bg=BG_COLOR, anchor="w").pack(side="left", expand=True)
        tk.Label(header_frame, text="Score", font=self.status_font_bold, bg=BG_COLOR, anchor="e").pack(side="right")
        # --- FIN DE CORRECCIÓN ---
        
        tk.Frame(score_window, height=2, bg="black").pack(fill="x", padx=20)

        list_frame = tk.Frame(score_window, bg=BG_COLOR)
        list_frame.pack(fill="both", expand=True, padx=20)

        if not scores:
            tk.Label(list_frame, text="Aún no hay scores.", font=self.status_font, bg=BG_COLOR, pady=20).pack()
        else:
            for i, (name, score, level) in enumerate(scores[:10]): # Top 10
                entry_frame = tk.Frame(list_frame, bg=BG_COLOR)
                entry_frame.pack(fill="x", pady=2)
                
                label_text = f"{i+1}. {name} ({level})"
                tk.Label(entry_frame, text=label_text, font=self.status_font, bg=BG_COLOR, anchor="w").pack(side="left", expand=True)
                tk.Label(entry_frame, text=f"{score}", font=self.status_font, bg=BG_COLOR, anchor="e").pack(side="right")

        tk.Button(score_window, text="Cerrar", command=score_window.destroy, font=self.status_font, width=10).pack(pady=10)
        score_window.transient(self.root)
        score_window.grab_set()

    # --- Actualizadores de UI ---

    def update_board_ui(self):
        """
        Sincroniza el array 2D de widgets (cell_labels) con los
        arrays 2D de datos (initial_grid, player_grid) del motor.
        """
        if not self.game_engine:
            return

        initial = self.game_engine.initial_grid
        player = self.game_engine.player_grid

        for r in range(9):
            for c in range(9):
                cell = self.cell_labels[r][c]
                if initial[r][c] != 0:
                    cell.config(text=str(initial[r][c]),
                                font=self.fixed_font,
                                fg=FIXED_FONT_COLOR,
                                bg=FIXED_CELL_COLOR)
                else:
                    text = str(player[r][c]) if player[r][c] != 0 else ""
                    cell.config(text=text,
                                font=self.cell_font,
                                fg=USER_FONT_COLOR,
                                bg=CELL_COLOR)
        
        # Resaltar celda seleccionada
        if self.selected_cell:
            r, c = self.selected_cell
            if initial[r][c] == 0:
                self.cell_labels[r][c].config(bg=CELL_SELECTED_COLOR)

    def update_stats_ui(self):
        """Actualiza todos los labels de estado (vidas, score, etc.)."""
        if not self.game_engine:
            return
            
        self.status_label.config(text=self.game_engine.get_level_string())
        self.score_label.config(text=f"Score: {int(self.game_engine.total_score)}")
        self.lives_label.config(text=f"Vidas: {self.game_engine.get_lives_string()}")

    def update_timer(self):
        """Se llama a sí mismo cada segundo para actualizar el reloj."""
        if self.game_engine:
            mins, secs = self.game_engine.get_elapsed_time()
            self.time_label.config(text=f"Tiempo: {mins:02}:{secs:02}")
            self.root.after(1000, self.update_timer) # Llama a esta función de nuevo en 1 seg

    # --- Manejadores de Eventos (Clics y Teclas) ---

    def on_cell_click(self, r, c):
        """Manejador para cuando se hace clic en una celda del tablero."""
        if not self.game_engine:
            return
            
        # Limpiar selección anterior
        self.update_board_ui() 
        
        # No se pueden seleccionar celdas iniciales
        if self.game_engine.initial_grid[r][c] != 0:
            self.selected_cell = None
        else:
            self.selected_cell = (r, c)
            self.cell_labels[r][c].config(bg=CELL_SELECTED_COLOR)

    def on_key_press(self, event):
        """Manejador para cuando se presiona una tecla."""
        if not self.game_engine or self.selected_cell is None:
            return
        
        r, c = self.selected_cell
        key = event.char
        
        if '1' <= key <= '9':
            num = int(key)
            self.game_engine.place_number(r, c, num)
            self.cell_labels[r][c].config(text=str(num)) # Actualización visual inmediata
            
        elif event.keysym == "BackSpace" or event.keysym == "Delete" or key == '0':
            self.game_engine.clear_number(r, c)
            self.cell_labels[r][c].config(text="") # Actualización visual inmediata

    # --- Handlers de Testing (AÑADIDOS) ---

    def fill_random(self):
        """(TESTING) Llama al motor para llenar aleatoriamente y actualiza la UI."""
        if not self.game_engine:
            return
        # 1. Llama al motor
        self.game_engine.fill_randomly()
        # 2. Actualiza la UI para mostrar los números
        self.update_board_ui()
        # 3. Mantiene la celda seleccionada (opcional, pero cómodo)
        if self.selected_cell:
            r, c = self.selected_cell
            self.cell_labels[r][c].config(bg=CELL_SELECTED_COLOR)

    def fill_solution(self):
        """(TESTING) Llama al motor para llenar con la solución y actualiza la UI."""
        if not self.game_engine:
            return
        # 1. Llama al motor
        self.game_engine.fill_with_solution()
        # 2. Actualiza la UI
        self.update_board_ui()
        # 3. Mantiene la celda seleccionada
        if self.selected_cell:
            r, c = self.selected_cell
            self.cell_labels[r][c].config(bg=CELL_SELECTED_COLOR)

    # --- Lógica principal del juego ---

    def check_board(self):
        """Lógica de verificación (el botón [V])."""
        if not self.game_engine:
            return
        
        is_correct = self.game_engine.check_solution()
        
        if is_correct:
            # --- Flujo: CORRECTO ---
            mins, secs = self.game_engine.get_elapsed_time()
            
            # on_sudoku_complete avanza el nivel y calcula el score
            result = self.game_engine.on_sudoku_complete()
            
            score_msg = f"Score obtenido: +{int(result['score_won'])}"
            if result['bonus_applied'] > 0:
                score_msg += f"\nBonus de Categoría: +{int(result['bonus_applied'])}"
            score_msg += f"\nScore total: {int(self.game_engine.total_score)}"
            
            messagebox.showinfo("¡Sudoku Completado!",
                                f"Tiempo: {mins:02}:{secs:02}\n{score_msg}")
            
            if result["status"] == "GAME_WIN":
                messagebox.showinfo("¡VICTORIA!",
                                    f"¡Felicidades, {self.game_engine.player_name}!\n"
                                    "Has completado todos los 25 sudokus.\n"
                                    f"Score Final: {int(self.game_engine.total_score)}")
                self.game_engine = None
                self.create_main_menu()
            else:
                # Cargar siguiente nivel
                self.selected_cell = None
                self.update_board_ui()
                self.update_stats_ui()
                
        else:
            # --- Flujo: INCORRECTO ---
            self.show_incorrect_menu()

    def show_incorrect_menu(self):
        """
        Muestra el menú [S/R/Q] usando un messagebox.
        Sí = Seguir, No = Reiniciar, Cancelar = Salir.
        """
        lives_str = self.game_engine.get_lives_string()
        
        choice = messagebox.askyesnocancel(
            "Sudoku Incorrecto",
            f"El sudoku tiene errores.\nVidas restantes: {lives_str}\n\n"
            "¿Qué deseas hacer?\n\n"
            "[Sí] = Seguir jugando (sin penalización)\n"
            "[No] = Reiniciar tablero (-1 vida)\n"
            "[Cancelar] = Salir al menú (termina la partida)"
        )
        
        if choice is True:
            # [S] Seguir jugando: no hacer nada
            pass
            
        elif choice is False:
            # [R] Reiniciar
            self.handle_restart()
            
        elif choice is None:
            # [Q] Salir al menú
            self.handle_quit_incorrect()

    def handle_restart(self):
        """Lógica para el botón [R] Reiniciar."""
        status = self.game_engine.restart_board()
        
        if status == "GAME_OVER":
            messagebox.showerror("Game Over",
                                 "¡Te has quedado sin vidas!\n"
                                 f"Score Final: {int(self.game_engine.total_score)}")
            self.game_engine = None
            self.create_main_menu()
        else:
            messagebox.showinfo("Reiniciado", "Tablero reiniciado. Has perdido una vida.")
            self.selected_cell = None
            self.update_board_ui()
            self.update_stats_ui()

    def handle_quit_incorrect(self):
        """Lógica para el botón [Q] Salir (desde menú incorrecto)."""
        if messagebox.askyesno("Confirmar Salida",
                               "¿Estás seguro? Esto terminará tu partida y guardará tu score."):
            self.game_engine.save_to_scores(completed=False)
            self.game_engine.delete_save_file()
            self.game_engine = None
            self.create_main_menu()
        # Si dice "No", vuelve al juego.

# ==============================================================================
# SECCIÓN 5: PUNTO DE ENTRADA
# ==============================================================================
if __name__ == "__main__":
    main_root = tk.Tk()
    app = SudokuApp(main_root)
    main_root.mainloop()
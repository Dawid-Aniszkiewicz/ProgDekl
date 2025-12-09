import pygame
import math
from typing import List, Optional, Tuple

# Stałe
SIZE = 20
CELL_SIZE = 50
WIDTH = SIZE * CELL_SIZE
HEIGHT = SIZE * CELL_SIZE + 150
FPS = 60

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.wall = False
        self.visited = False
        self.g = float('inf')
        self.h = 0.0
        self.f = float('inf')
        self.parent: Optional[Cell] = None

    def reset(self):
        self.visited = False
        self.g = float('inf')
        self.h = 0.0
        self.f = float('inf')
        self.parent = None

def heuristic(a: Cell, b: Cell) -> float:
    dx = b.x - a.x
    dy = b.y - a.y
    return math.sqrt(dx * dx + dy * dy)

def find_lowest(open_list: List[Cell]) -> int:
    best = 0
    for i in range(1, len(open_list)):
        if open_list[i].f < open_list[best].f:
            best = i
    return best

def is_in_list(cell_list: List[Cell], cell: Cell) -> bool:
    for c in cell_list:
        if c.x == cell.x and c.y == cell.y:
            return True
    return False

class AStarVisualizer:
    def __init__(self, grid: List[List[Cell]], start: Cell, goal: Cell):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.open_list = []
        self.steps = 0
        self.finished = False
        self.path = []

        # Reset wszystkich komórek
        for row in grid:
            for cell in row:
                cell.reset()

        # Inicjalizacja
        start.g = 0
        start.h = heuristic(start, goal)
        start.f = start.g + start.h
        self.open_list.append(start)

    def step(self) -> bool:
        """Wykonaj jeden krok algorytmu. Zwraca True jeśli kontynuować."""
        if self.finished or not self.open_list:
            if not self.open_list and not self.finished:
                self.finished = True
            return False

        self.steps += 1
        idx = find_lowest(self.open_list)
        current = self.open_list[idx]

        if current == self.goal:
            # Znaleziono ścieżkę
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            self.path = path
            self.finished = True
            return False

        self.open_list.pop(idx)
        current.visited = True

        # Sprawdź sąsiadów
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = current.x + dx, current.y + dy

            if nx < 0 or nx >= SIZE or ny < 0 or ny >= SIZE:
                continue

            neighbor = self.grid[nx][ny]
            if neighbor.wall or neighbor.visited:
                continue

            new_g = current.g + 1
            if new_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = new_g
                neighbor.h = heuristic(neighbor, self.goal)
                neighbor.f = neighbor.g + neighbor.h
                if not is_in_list(self.open_list, neighbor):
                    self.open_list.append(neighbor)

        return True

def draw_grid(screen: pygame.Surface, grid: List[List[Cell]], start: Cell,
              goal: Cell, path: List[Cell], open_list: List[Cell],
              value_font: pygame.font.Font, label_font: pygame.font.Font):
    screen.fill(WHITE)

    # Rysuj komórki
    for i in range(SIZE):
        for j in range(SIZE):
            cell = grid[i][j]
            x = j * CELL_SIZE
            y = i * CELL_SIZE

            on_path = any(p.x == cell.x and p.y == cell.y for p in path)
            in_open = any(p.x == cell.x and p.y == cell.y for p in open_list)

            if cell == start:
                color = GREEN
            elif cell == goal:
                color = RED
            elif on_path:
                color = YELLOW
            elif cell.wall:
                color = BLACK
            elif in_open:
                color = BLUE
            elif cell.visited:
                color = LIGHT_GRAY
            else:
                color = WHITE

            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)

            # Rysuj wartość f dla odwiedzonych i otwartych komórek
            if (cell.visited or in_open) and not cell.wall and cell != start and cell != goal:
                # f-score (wyśrodkowany)
                if cell.f != float('inf'):
                    f_text = value_font.render(f'{cell.f:.1f}', True, BLACK if not in_open else WHITE)
                    f_rect = f_text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                    screen.blit(f_text, f_rect)

    # Narysuj oznaczenia
    if start:
        x = start.y * CELL_SIZE + CELL_SIZE // 2
        y = start.x * CELL_SIZE + CELL_SIZE // 2
        text = label_font.render('START', True, BLACK)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)

    if goal:
        x = goal.y * CELL_SIZE + CELL_SIZE // 2
        y = goal.x * CELL_SIZE + CELL_SIZE // 2
        text = label_font.render('CEL', True, WHITE)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("A* Pathfinding Visualization")
    clock = pygame.time.Clock()
    value_font = pygame.font.Font(None, 28)
    label_font = pygame.font.Font(None, 18)
    info_font = pygame.font.Font(None, 24)

    # Inicjalizacja siatki
    grid = [[Cell(i, j) for j in range(SIZE)] for i in range(SIZE)]

    # Ustawienia początkowe
    start = grid[2][2]
    goal = grid[17][17]

    # Tworzenie ścian (jak w oryginalnym kodzie)
    for i in range(7, 15):
        grid[i][9].wall = True
    for j in range(9, 15):
        grid[5][j].wall = True
    for i in range(3, 15):
        grid[i][2].wall = True
    grid[5][10].wall = False
    for i in range(2, 12):
        grid[i][12].wall = True
    for j in range(4, 11):
        grid[10][j].wall = True
    grid[15][15].wall = True
    grid[15][16].wall = True
    """
    sciany wokol
    grid[17][16].wall = True
    grid[16][17].wall = True
    grid[18][17].wall = True
    grid[17][18].wall = True
    sciana = cel
    grid[17][17].wall = True
    """
    path = []
    steps = 0
    distance = heuristic(start, goal)
    visualizer = None
    auto_play = False
    step_delay = 100
    last_step_time = 0

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if visualizer is None:
                        visualizer = AStarVisualizer(grid, start, goal)
                        auto_play = True
                elif event.key == pygame.K_RETURN:
                    if visualizer is None:
                        visualizer = AStarVisualizer(grid, start, goal)
                    if not visualizer.finished:
                        visualizer.step()
                elif event.key == pygame.K_r:
                    # Reset
                    for row in grid:
                        for cell in row:
                            cell.reset()
                    path = []
                    visualizer = None
                    auto_play = False
                elif event.key == pygame.K_UP:
                    step_delay = max(10, step_delay - 20)
                elif event.key == pygame.K_DOWN:
                    step_delay = min(500, step_delay + 20)
                elif event.key == pygame.K_p:
                    auto_play = not auto_play

        # Auto-play
        if auto_play and visualizer and not visualizer.finished:
            if current_time - last_step_time > step_delay:
                visualizer.step()
                last_step_time = current_time

        # Rysowanie
        open_list = visualizer.open_list if visualizer else []
        path = visualizer.path if visualizer else []
        draw_grid(screen, grid, start, goal, path, open_list, value_font, label_font)

        # Informacje na dole ekranu
        info_y = SIZE * CELL_SIZE + 10

        text1 = info_font.render(f"Odleglosc euklidesowa: {distance:.2f}", True, BLACK)
        screen.blit(text1, (10, info_y))

        if visualizer:
            text2 = info_font.render(f"Krokow: {visualizer.steps}", True, BLACK)
            screen.blit(text2, (300, info_y))

            if visualizer.finished:
                if visualizer.path:
                    text3 = info_font.render(f"Dlugosc sciezki: {len(visualizer.path)}", True, GREEN)
                    screen.blit(text3, (10, info_y + 35))
                else:
                    text3 = info_font.render("NIE ZNALEZIONO SCIEZKI!", True, RED)
                    screen.blit(text3, (10, info_y + 35))
            else:
                text3 = info_font.render(f"Otwartych wezlow: {len(visualizer.open_list)}", True, BLUE)
                screen.blit(text3, (600, info_y))

        speed_text = info_font.render(f"Opoznienie: {step_delay}ms", True, PURPLE)
        screen.blit(speed_text, (10, info_y + 70))

        # Instrukcje - większa czcionka
        text_instr = info_font.render("SPACJA - Auto | ENTER - Krok | P - Pauza | R - Reset | UP/DOWN - Szybkosc", True, BLACK)
        screen.blit(text_instr, (10, info_y + 105))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

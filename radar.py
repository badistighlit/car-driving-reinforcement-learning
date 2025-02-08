import pygame  # ✅ Ajout de l'import manquant
from utils import detect_gazon
from config import BLUE, RED, GREEN


def draw_radar(window, car):
    """Dessine le radar"""
    levels = [40, 70, 100]
    directions = [0, 45, -45, 90, -90, 135, -135, 180]

    car.update_radar_matrix(levels, directions, window)

    for level in levels:
        pygame.draw.circle(window, (200, 200, 200), (int(car.car_x), int(car.car_y)), level, 1)

    radar_points = car.get_radar_points(levels, directions)
    for direction_points in radar_points:
        for x, y in direction_points:
            color = RED if detect_gazon(x, y, window) else GREEN
            pygame.draw.circle(window, color, (int(x), int(y)), 3)
        pygame.draw.line(window, BLUE, (car.car_x, car.car_y), direction_points[-1], 1)

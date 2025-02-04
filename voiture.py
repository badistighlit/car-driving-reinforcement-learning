import pygame
import math
from config import WIDTH, HEIGHT
from utils import detect_gazon

class Voiture:
    def __init__(self):
        self.car_image = pygame.image.load('assets/car.png')
        self.car_image = pygame.transform.scale(self.car_image, (60, 60))
        self.car_x, self.car_y = WIDTH // 5, HEIGHT // 5
        self.car_angle = 0
        self.car_speed = 0
        self.radar_matrix = []

    def update_position(self):
        new_x = self.car_x + self.car_speed * math.cos(math.radians(self.car_angle))
        new_y = self.car_y - self.car_speed * math.sin(math.radians(self.car_angle))

        if not (0 <= new_x <= WIDTH - 60 and 0 <= new_y <= HEIGHT - 60):
            self.reset_position()
        else:
            self.car_x = new_x
            self.car_y = new_y

    def get_radar_points(self, levels, directions):
        radar_points = []
        for direction in directions:
            angle = math.radians(self.car_angle + direction)
            points_for_direction = []
            for level in levels:
                x = self.car_x + math.cos(angle) * level
                y = self.car_y - math.sin(angle) * level
                points_for_direction.append((x, y))
            radar_points.append(points_for_direction)
        return radar_points

    def update_radar_matrix(self, levels, directions, window):
        radar_points = self.get_radar_points(levels, directions)
        self.radar_matrix = []
        for direction_points in radar_points:
            direction_data = []
            for x, y in direction_points:
                is_gazon = detect_gazon(x, y, window)
                direction_data.append(1 if is_gazon else 0)
            self.radar_matrix.append(direction_data)

    def reset_position(self):
        self.car_x = WIDTH // 2 - 70  # Juste à côté de la ligne
        self.car_y = 150
        self.car_angle = 0
        self.car_speed = 0

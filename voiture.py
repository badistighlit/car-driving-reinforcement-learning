import pygame
import math
from config import WIDTH, HEIGHT

class Voiture:
    def __init__(self):
        self.car_image = pygame.image.load('assets/car.png')  # ✅ On ajoute 'assets/' au chemin
        self.car_image = pygame.transform.scale(self.car_image, (60, 60))
        self.car_x, self.car_y = WIDTH // 5, HEIGHT // 5
        self.car_angle = 0
        self.car_speed = 0

    def update_position(self):
        self.car_x += self.car_speed * math.cos(math.radians(self.car_angle))
        self.car_y -= self.car_speed * math.sin(math.radians(self.car_angle))

    def reset_position(self):
        self.car_x = WIDTH // 2 - 70
        self.car_y = 150
        self.car_angle = 0
        self.car_speed = 0

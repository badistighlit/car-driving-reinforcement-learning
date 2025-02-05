import pygame
import math
import os
from config import WIDTH, HEIGHT

class Voiture:
    def __init__(self):
        car_image_path = 'assets/car.png'
        if not os.path.exists(car_image_path):
            raise FileNotFoundError(f"Erreur : L'image '{car_image_path}' est introuvable. Vérifiez son emplacement !")

        self.car_image = pygame.image.load(car_image_path)
        self.car_image = pygame.transform.scale(self.car_image, (60, 60))
        self.car_x, self.car_y = WIDTH // 5, HEIGHT // 5
        self.car_angle = 0
        self.car_speed = 0

    def update_position(self):
        self.car_x += self.car_speed * math.cos(math.radians(self.car_angle))
        self.car_y -= self.car_speed * math.sin(math.radians(self.car_angle))

    def reset_position(self):
        self.car_x = WIDTH -350  # ✅ Centre de la piste après la ligne d'arrivée
        self.car_y = HEIGHT // 4  # ✅ Après la ligne d'arrivée (100 + 120 pixels)
        self.car_angle = 0
        self.car_speed = 0



from enum import Enum
import pygame
import math
import sys

# Initialisation
pygame.init()

# Fenêtre
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JE ROUUULE !!!!!")

# La voiture
class Voiture:
    def __init__(self):
        self.car_image = pygame.image.load('car.png')
        self.car_image = pygame.transform.scale(self.car_image, (60, 60))
        self.car_x, self.car_y = WIDTH // 5, HEIGHT // 5
        self.car_angle = 0
        self.car_speed = 0

    def update_position(self):
        self.car_x += self.car_speed * math.cos(math.radians(self.car_angle))
        self.car_y -= self.car_speed * math.sin(math.radians(self.car_angle))

# Paramètres du jeu
turning_speed = 3   # Vitesse de rotation
acceleration = 0.2  # Accélération
max_speed = 5       # Vitesse maximale
friction = 0.05     # Friction

# Récompenses
class Reward(Enum):
    STOPPED = -500
    GOAL = 1000
    WALL = -100
    DEFAULT = -1

def draw_track():
    # bordure blanche piste
    pygame.draw.rect(window, (255, 255, 255), (90, 90, WIDTH - 180, HEIGHT - 180), border_radius=100)
    # route grise
    pygame.draw.rect(window, (100, 100, 100), (100, 100, WIDTH - 200, HEIGHT - 200), border_radius=90)
    # bordure blanche autour du gazon central
    pygame.draw.rect(window, (255, 255, 255), (190, 190, WIDTH - 380, HEIGHT - 380), border_radius=60)
    # gazon centrale
    pygame.draw.rect(window, (0, 150, 0), (200, 200, WIDTH - 400, HEIGHT - 400), border_radius=50)
    # ligne de départ : boucle rouge / blanche etc ...
    start_line_x = WIDTH // 2 - 30
    pygame.draw.rect(window, (255, 255, 255), (start_line_x, 100, 20, 50))
    for i in range(10):
        color = (255, 0, 0) if i % 2 == 0 else (255, 255, 255)
        pygame.draw.rect(window, color, (start_line_x, 100 + i * 10, 20, 10))


# Jeu principal
class Game:
    def run(self):
        car = Voiture()  # Initialisation de la voiture
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            # Gestion des touches
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:  # avancer
                car.car_speed = min(car.car_speed + acceleration, max_speed)
            elif keys[pygame.K_DOWN]:  # reculer
                car.car_speed = max(car.car_speed - acceleration, -max_speed / 2)
            else:
                # Ralenti automatique
                if car.car_speed > 0:
                    car.car_speed -= friction
                elif car.car_speed < 0:
                    car.car_speed += friction

            if keys[pygame.K_LEFT]:  # tourner à gauche
                car.car_angle += turning_speed
            if keys[pygame.K_RIGHT]:  # tourner à droite
                car.car_angle -= turning_speed

            # Mise à jour de la position de la voiture
            car.update_position()

            # Effacer l'écran (pelouse verte)
            window.fill((0, 150, 0))

            # piste
            draw_track()

            # Rotation et affichage de la voiture
            rotated_car = pygame.transform.rotate(car.car_image, car.car_angle)
            car_rect = rotated_car.get_rect(center=(car.car_x, car.car_y))
            window.blit(rotated_car, car_rect.topleft)

            # Mise à jour de l'affichage
            pygame.display.flip()
            clock.tick(60)  # 60 FPS

# Exécution du jeu
if __name__ == "__main__":
    game = Game()
    game.run()

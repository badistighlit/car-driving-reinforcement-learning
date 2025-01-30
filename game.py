import pygame
import sys
from config import WIDTH, HEIGHT, ACCELERATION, MAX_SPEED, TURNING_SPEED, FRICTION
from voiture import Voiture
from track import draw_track
from radar import draw_radar
from qlearning import QTable

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("JE ROUUULE !!!!!")
        self.car = Voiture()
        self.qtable = QTable()
        self.clock = pygame.time.Clock()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            # ✅ Gestion des touches pour faire avancer la voiture
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:  # Avancer
                self.car.car_speed = min(self.car.car_speed + ACCELERATION, MAX_SPEED)
            elif keys[pygame.K_DOWN]:  # Reculer
                self.car.car_speed = max(self.car.car_speed - ACCELERATION, -MAX_SPEED / 2)
            else:
                # Ajout de la friction
                if self.car.car_speed > 0:
                    self.car.car_speed = max(0, self.car.car_speed - FRICTION)
                elif self.car.car_speed < 0:
                    self.car.car_speed = min(0, self.car.car_speed + FRICTION)

            if keys[pygame.K_LEFT]:  # Tourner à gauche
                self.car.car_angle += TURNING_SPEED
            if keys[pygame.K_RIGHT]:  # Tourner à droite
                self.car.car_angle -= TURNING_SPEED

            # ✅ Mettre à jour la position de la voiture
            self.car.update_position()

            # Effacer l'écran (gazon vert)
            self.window.fill((0, 150, 0))

            # Dessiner la piste et le radar
            draw_track(self.window)
            draw_radar(self.window, self.car)

            # Rotation et affichage de la voiture
            rotated_car = pygame.transform.rotate(self.car.car_image, self.car.car_angle)
            car_rect = rotated_car.get_rect(center=(self.car.car_x, self.car.car_y))
            self.window.blit(rotated_car, car_rect.topleft)

            # Mise à jour de l'affichage
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS

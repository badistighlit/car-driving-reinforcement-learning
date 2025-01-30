import pygame
import sys
from config import WIDTH, HEIGHT, ACCELERATION, MAX_SPEED, TURNING_SPEED, FRICTION, MAX_REVERSE_SPEED
from voiture import Voiture
from track import draw_track
from qlearning import QLearning

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("JE ROUUULE !!!!!")
        self.car = Voiture()
        self.qlearning = QLearning()
        self.clock = pygame.time.Clock()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            position = (int(self.car.car_x), int(self.car.car_y), int(self.car.car_angle))
            action = self.qlearning.get_action(position)

            reward = -1  # Pénalité par défaut
            if action == pygame.K_UP:
                self.car.car_speed = min(self.car.car_speed + ACCELERATION, MAX_SPEED)
            elif action == pygame.K_DOWN:
                self.car.car_speed = max(self.car.car_speed - ACCELERATION, MAX_REVERSE_SPEED)
            elif action == pygame.K_LEFT:
                self.car.car_angle += TURNING_SPEED
            elif action == pygame.K_RIGHT:
                self.car.car_angle -= TURNING_SPEED

            self.car.update_position()

            # Détection de collision
            if self.car.car_x < 100 or self.car.car_x > WIDTH - 100 or self.car.car_y < 100 or self.car.car_y > HEIGHT - 100:
                reward = -100
                self.car.reset_position()

            # Vérifier si la ligne d’arrivée est franchie
            if WIDTH // 2 - 30 <= self.car.car_x <= WIDTH // 2 - 10 and 100 <= self.car.car_y <= 200:
                reward = 1000  # ✅ Récompense pour un tour réussi !
                print("🚗💨 Ligne d'arrivée franchie !")
                self.car.reset_position()

            next_position = (int(self.car.car_x), int(self.car.car_y), int(self.car.car_angle))
            self.qlearning.update(position, action, reward, next_position)

            self.window.fill((0, 150, 0))
            draw_track(self.window)

            rotated_car = pygame.transform.rotate(self.car.car_image, self.car.car_angle)
            car_rect = rotated_car.get_rect(center=(self.car.car_x, self.car.car_y))
            self.window.blit(rotated_car, car_rect.topleft)

            pygame.display.flip()
            self.clock.tick(60)

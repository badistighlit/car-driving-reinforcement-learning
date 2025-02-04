import pygame
import sys
import random
from config import WIDTH, HEIGHT, ACCELERATION, MAX_SPEED, TURNING_SPEED, FRICTION
from voiture import Voiture
from track import draw_track
from radar import draw_radar
from qlearning import QTable
from reward import Reward

# Mode automatique (True) ou manuel (False)
AUTO_MODE = True

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("JE ROUUULE !!!!!")
        self.car = Voiture()
        self.car.car_x = WIDTH - 350  # Positionner la voiture derrière la ligne d'arrivée
        self.car.car_y = HEIGHT // 4
        self.car.car_angle = 180  # Orientation vers la gauche
        self.qtable = QTable()
        self.clock = pygame.time.Clock()
        self.last_reward = None  # Stocke la dernière récompense pour éviter les répétitions
        self.actions = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]

    def choose_action(self, state):
        if state in self.qtable.qtable and random.random() > 0.1:  # Exploration vs Exploitation
            return max(self.qtable.qtable[state], key=self.qtable.qtable[state].get)
        return random.choice(self.actions)

    def run(self):
        global AUTO_MODE
        running = True
        finish_line_x = WIDTH // 2 - 30
        finish_line_y_min = 100
        finish_line_y_max = 150
        print(finish_line_x, WIDTH, HEIGHT)
        while running:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:  # Touche 'M' pour basculer entre modes
                        AUTO_MODE = not AUTO_MODE
                        print(f"Mode {'Automatique' if AUTO_MODE else 'Manuel'} activé")

            # Déterminer l'action selon le mode
            if AUTO_MODE:
                state = (int(self.car.car_x), int(self.car.car_y))
                action = self.choose_action(state)
            else:
                action = None
                if keys[pygame.K_UP]:
                    action = pygame.K_UP
                if keys[pygame.K_DOWN]:
                    action = pygame.K_DOWN
                if keys[pygame.K_LEFT]:
                    action = pygame.K_LEFT
                if keys[pygame.K_RIGHT]:
                    action = pygame.K_RIGHT

            # Initialiser la récompense
            reward = Reward.DEFAULT.value

            # Appliquer l'action
            if action == pygame.K_UP:
                self.car.car_speed = min(self.car.car_speed + ACCELERATION, MAX_SPEED)
            if action == pygame.K_DOWN:
                self.car.car_speed = max(self.car.car_speed - ACCELERATION, -MAX_SPEED / 2)
            if action == pygame.K_LEFT:
                self.car.car_angle += TURNING_SPEED
            if action == pygame.K_RIGHT:
                self.car.car_angle -= TURNING_SPEED
            if action is None:
                if self.car.car_speed > 0:
                    self.car.car_speed = max(0, self.car.car_speed - FRICTION)
                elif self.car.car_speed < 0:
                    self.car.car_speed = min(0, self.car.car_speed + FRICTION)

            # Mettre à jour la position de la voiture
            prev_x = self.car.car_x  # Stocker la position précédente
            self.car.update_position()
            new_x = self.car.car_x  # Nouvelle position

            if (prev_x > finish_line_x and new_x <= finish_line_x and 
                self.car.car_y >= finish_line_y_min and self.car.car_y <= finish_line_y_max and
                self.car.car_speed < 0):
                reward = Reward.GOAL_WRONG.value  # Passage incorrect (gauche -> droite)
            elif (prev_x < finish_line_x and new_x >= finish_line_x and
                self.car.car_y >= finish_line_y_min and self.car.car_y <= finish_line_y_max and
                self.car.car_speed > 0):
                reward = Reward.GOAL.value  # Passage correct (droite -> gauche)
            else:
                reward = Reward.DEFAULT.value

            # Vérification des collisions sur les bords extérieurs
            if (self.car.car_x < 100 or self.car.car_x > WIDTH - 100 or
                self.car.car_y < 100 or self.car.car_y > HEIGHT - 100):
                reward = Reward.WALL.value

            # Vérification si la voiture se trouve sur le gazon central
            elif (200 <= self.car.car_x <= WIDTH - 200 and
                200 <= self.car.car_y <= HEIGHT - 200):
                reward = Reward.WALL.value

            # Obtenir le nouvel état
            new_state = (int(self.car.car_x), int(self.car.car_y))
            if AUTO_MODE:
                self.qtable.set(state, action, reward, new_state)

            # Afficher uniquement si la récompense change
            if reward != self.last_reward:
                print(f"Nouvelle récompense: {reward}")
                self.last_reward = reward

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
            self.clock.tick(60)

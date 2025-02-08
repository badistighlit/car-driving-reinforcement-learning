import pygame
import sys
import random
from config import WIDTH, HEIGHT, ACCELERATION, MAX_SPEED, TURNING_SPEED, FRICTION
from utils import detect_gazon, detect_proximite_gazon
from voiture import Voiture
from track import draw_track
from radar import draw_radar
from qlearning import QTable
from reward import Reward

AUTO_MODE = True

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("JE ROUUULE !!!!!")
        self.car = Voiture()
        self.car.car_x = WIDTH - 350  # Behind the finish line
        self.car.car_y = HEIGHT // 4
        self.car.car_angle = 180  # Facing left
        self.qtable = QTable()
        self.reward = 0
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.stuck_time = 0
        self.epsilon = 1.0  # Initial exploration rate
        self.epsilon_decay = 0.9995
        self.epsilon_min = 0.1
        self.actions = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        self.nmbrTour = 0
        self.reward_max=0


        # Ajout pour détecter l'immobilité
        self.stationary_time = 0
        self.last_position = (self.car.car_x, self.car.car_y)
        self.stationary_penalty_threshold = 300

    def choose_action(self, state):
        possible_actions = self.actions.copy()
        return self.qtable.choose_action(state, self.epsilon, possible_actions,self.window)

    def update_rewards(self, prev_x, new_x, prev_angle):

        # DETAILS LIGNE DARRIVEE + CHECKPOINT
        finish_line_x = WIDTH // 2 - 30
        checkpoint_x = WIDTH // 2 - 30

        finish_line_x = WIDTH // 2 - 30
        finish_line_y_min, finish_line_y_max = 100, 150
        checkpoint_y = HEIGHT - 200


        direction_reward = 100 if self.car.car_speed > 0 else -200
        self.reward += direction_reward

        # pénalités si marche arriere
        if self.car.car_speed < 0:
            self.reward -= abs(self.car.car_speed) * 100

        if detect_proximite_gazon(self,self.car.car_x,self.car.car_y,10):
            self.reward -= 500

        self.reward += self.check_stationary_penalty()

        # 🏁 **5. Récompense pour franchir la ligne d'arrivée**
        if (prev_x > finish_line_x + 10 and new_x <= finish_line_x + 10 and
                self.car.car_y >= finish_line_y_min and self.car.car_y <= finish_line_y_max):
            if self.car.car_speed < 0:
                self.nmbrTour += 1
                self.reward -= 6000   # Réduction de la pénalité si en marche arrière
            else:
                self.nmbrTour += 1
                self.reward += 10000 * self.nmbrTour  # Augmentation de la récompense
                print(f"🏆 REWARDDDDDD !!!!!!!!!!!!!!!!!!!!!!!!")

        if (prev_x > finish_line_x+ 10 and new_x <= finish_line_x +10 and
                checkpoint_y <= self.car.car_y <= checkpoint_y + 60):  # Largeur ajustée
            if self.car.car_speed > 0:
                self.reward += 5000
                print("✅ CHECKPOINT FRANCHI !")

        # Pénalités principales
        if detect_gazon(self.car.car_x, self.car.car_y, self.window):
            self.reward -= 10000
            return  # Arrête l'évaluation des autres récompenses si sur le gazon
        if (detect_gazon(self.car.car_x, self.car.car_y, self.window)== False):
            speed_bonus = abs(self.car.car_speed) * 5
            if self.car.car_speed > 0:
                self.reward += speed_bonus
            self.reward += 100
        # Récompenses pour la conduite


            # Bonus pour conduite fluide
            if abs(prev_angle - self.car.car_angle) < 45:
                self.reward += 50

        # Pénalité légère pour l'immobilité
        if abs(self.car.car_speed) < 0.1:
            self.reward -= 10
        if self.car.car_speed < 0:
            self.reward-=2000


        if abs(prev_angle - self.car.car_angle) > 90:
            self.reward -= 50  # Réduire la récompense pour un virage trop brusque
        # Pénalité pour marche arrière pendant que l'agent roule en arrière
        if self.car.car_speed < 0:
            self.reward -= 50  # Pénalité plus légère pour marche arrière continue

    def run(self):
        """Main game loop, handling events, updating the game state, and rendering the display."""
        global AUTO_MODE
        running = True
        while running:
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    AUTO_MODE = not AUTO_MODE
                    print(f"Mode {'Automatique' if AUTO_MODE else 'Manuel'} activé")

            if AUTO_MODE:
                self.car.update_radar_matrix([20, 40, 60], [-90, -45, 0, 45, 90], self.window)

                # Discretize position
                state = (
                    int(self.car.car_x),
                    int(self.car.car_y),
                    tuple(map(tuple, self.car.radar_matrix)),
                    int(self.car.car_angle // 30)
                )

                action = self.choose_action(state)

            else:
                action = next((key for key in self.actions if keys[key]), None)

            # Apply action
            if action == pygame.K_UP:
                self.car.car_speed = min(self.car.car_speed + ACCELERATION, MAX_SPEED)
                self.reward += 2  # Bonus for moving forward
            if action == pygame.K_DOWN:
                self.car.car_speed = max(self.car.car_speed - ACCELERATION, -MAX_SPEED / 2)
                self.reward -= 50  # Penalty for reversing
            if action == pygame.K_LEFT:
                self.car.car_angle += TURNING_SPEED
            if action == pygame.K_RIGHT:
                self.car.car_angle -= TURNING_SPEED
                self.reward -= 0.5
            if action is None:
                self.car.car_speed = max(0, self.car.car_speed - FRICTION) if self.car.car_speed > 0 else min(0, self.car.car_speed + FRICTION)

            prev_x = self.car.car_x
            isRenitialiser = self.car.update_position()
            if isRenitialiser:
                self.reward = 0
                self.nmbrTour = 0  # Reset if necessary
            prev_angle = self.car.car_angle
            self.update_rewards(prev_x, self.car.car_x, prev_angle)

            #if self.reward <= -30000000:
             #   #print("🚨 Réinitialisation : trop de points négatifs accumulés !")
              #  self.car.reset_position()
               # self.reward = 0
                #self.stuck_time = 0  # Remet aussi le compteur de blocage à zéro

            # Avoid getting stuck
            if abs(self.car.car_speed) < 3:  # Only if really stuck
                self.stuck_time += 1
                if self.stuck_time > 500:  # Increase patience before resetting
                    self.car.reset_position()
                    self.stuck_time = 0
                    self.reward = 0
            else:
                self.stuck_time = 0

            # Discretize new position
            new_grid_x = int(self.car.car_x)
            new_grid_y = int(self.car.car_y)
            new_state = (
                new_grid_x,
                new_grid_y,
                tuple(map(tuple, self.car.radar_matrix)),
                int(self.car.car_angle // 30)
            )

            self.qtable.set(state, action, self.reward, new_state,self.window)

            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

            # Rendering
            self.window.fill((0, 150, 0))
            draw_track(self.window)
            draw_radar(self.window, self.car)
            rotated_car = pygame.transform.rotate(self.car.car_image, self.car.car_angle)
            self.window.blit(rotated_car, rotated_car.get_rect(center=(self.car.car_x, self.car.car_y)).topleft)

            reward_text = self.font.render(f'Reward: {self.reward}', True, (255, 255, 255))
            mode_text = self.font.render(f"Mode: {'AUTO' if AUTO_MODE else 'MANUEL'}", True, (255, 255, 255))
            if self.reward > self.reward_max : self.reward_max = self.reward
            scoremax = self.font.render(f'scoremax: {self.reward_max}', True, (255, 255, 255))
            self.window.blit(reward_text, (10, 10))
            self.window.blit(mode_text, (10, 50))
            self.window.blit(scoremax, (10, 100))
            pygame.display.flip()
            self.clock.tick(120)

    def get_grid_position(self):
        """Retourne la position de la voiture sur une grille de 50x50 pixels"""
        grid_x = int(self.car.car_x // 50)
        grid_y = int(self.car.car_y // 50)
        return (grid_x, grid_y)

    def check_stationary_penalty(self):
        """Vérifie si la voiture est restée trop longtemps dans la même zone et applique une pénalité"""
        current_grid_pos = self.get_grid_position()

        # Initialiser les attributs s'ils n'existent pas
        if not hasattr(self, 'last_grid_pos'):
            self.last_grid_pos = current_grid_pos
            self.grid_stationary_time = 0
            return 0

        # Si on est dans la même case
        if current_grid_pos == self.last_grid_pos:
            self.grid_stationary_time += 1
            # Appliquer une pénalité si on reste trop longtemps (plus de 60 frames ~ 0.5 seconde à 120 FPS)
            if self.grid_stationary_time > 60:
                return -500  # Pénalité pour stagnation
        else:
            # Réinitialiser le compteur si on change de case
            self.grid_stationary_time = 0
            self.last_grid_pos = current_grid_pos

        return 0
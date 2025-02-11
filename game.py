import pygame
import sys
from config import WIDTH, HEIGHT, ACCELERATION, MAX_SPEED, TURNING_SPEED, FRICTION
from utils import detect_gazon, detect_proximite_gazon
from voiture import Voiture
from track import draw_track
from radar import draw_radar
from qlearning import QTable

AUTO_MODE = True

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("JE ROUUULE !!!!!")
        self.car = Voiture()

        #self.car.car_x = WIDTH - 350  #  juste avant la ligne darrivee
        #self.car.car_y = HEIGHT // 4
        #self.car.car_angle = 180
        self.car.reset_position()

        self.qtable = QTable()
        self.reward = 0
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)


        self.stuck_time = 0
        self.epsilon = 0.6  # exploration rate
        self.epsilon_decay = 0.999
        self.epsilon_min = 0.2
        self.actions = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]


        self.nmbrTour = 0
        self.reward_max=0


        # détecter l'immobilité
        self.stationary_time = 0
        self.last_position = (self.car.car_x, self.car.car_y)
        self.stationary_penalty_threshold = 300

    def choose_action(self, state):
        possible_actions = self.actions.copy()
        x =self.qtable.choose_action(state, self.epsilon, possible_actions,self.window)
        #print(x)
        return x

    def update_rewards(self, prev_x, new_x, prev_angle):

        # DETAILS LIGNE DARRIVEE + CHECKPOINT
        finish_line_x = WIDTH // 2 - 30
        checkpoint_x = WIDTH // 2 - 30

        finish_line_x = WIDTH // 2 - 30
        finish_line_y_min, finish_line_y_max = 100, 150
        checkpoint_y = HEIGHT - 200







        # si stationnée
        self.reward += self.check_stationary_penalty()



        # SI AVANCE SUR LA ROUTE a bonne vitesse
        if (detect_gazon(self.car.car_x, self.car.car_y, self.window)== False):
            #print("route")
            if self.car.car_speed > 0:
                optimal_speed = 7
                speed_diff = abs(self.car.car_speed - optimal_speed)
                self.reward += max(0, 50 - (speed_diff * 2))
            self.reward += 1


        #  Récompense pour franchir la ligne darrivee
        if (prev_x > finish_line_x + 10 and new_x <= finish_line_x + 10 and
                self.car.car_y >= finish_line_y_min and self.car.car_y <= finish_line_y_max):
            if self.car.car_speed < 0:
                self.nmbrTour += 1
                self.reward -= 6000
                print(f" FAUUUUUUX !!!!!!!!!!!!!!!!!!!!!!!!") # pénalité si en marche arrière
            else:
                self.nmbrTour += 1
                self.reward += 10000 * self.nmbrTour  #récompense
                print(f" GOAAAAAAAAAAAL !!!!!!!!!!!!!!!!!!!!!!!!")
        # checkpoint
        if (prev_x > finish_line_x+ 10 and new_x <= finish_line_x +10 and
                checkpoint_y <= self.car.car_y <= checkpoint_y + 60):
            if self.car.car_speed > 0:
                self.reward += 5000
                print("CHECKPOINT FRANCHI !")

        if abs(prev_angle - self.car.car_angle) > 70:
            self.reward -= 20
        elif 10 < abs(prev_angle - self.car.car_angle) <= 60:
            self.reward += 10

        # GESTION VIRAGE
        if (self.get_grid_position() in [(5, 1), (6, 3), (2, 4), (1, 3)]):
            if abs(prev_angle - self.car.car_angle) > 60:
                self.reward -= 30  #  virage trop brusque
            elif 15 < abs(prev_angle - self.car.car_angle) <= 60:
                self.reward += 50  # bon angle de virage

            # Encourager une vitesse modérée dans le virage
            if 3 <= self.car.car_speed <= 7:
                self.reward += 100  #  bonne gestion de vitesse
            elif self.car.car_speed > 9:
                self.reward -= 50  # Trop rapide

        # acceleration sans toucher le gazon bieeeeeeen
        if prev_x < self.car.car_x and not detect_gazon(self.car.car_x, self.car.car_y, self.window):
            self.reward += 100


            # Pénalités

        # si gazon
        if detect_gazon(self.car.car_x, self.car.car_y, self.window):
            self.reward -= 100
            # si mur proche
            if (abs(WIDTH - self.car.car_x) < 10 or self.car.car_x < 10):
                self.reward-=2000


            if (abs(HEIGHT - self.car.car_y) < 10 or self.car.car_y < 10):
                self.reward-=2000

            #print("gazon")
            return  # Arrête l'évaluation



        # si pas très loin du gazon
        if detect_proximite_gazon(self,self.car.car_x,self.car.car_y,1):
            self.reward -= 1

        if self.get_grid_position() == (6, 1) and -100 <= self.car.car_angle <= -50:
            self.reward += 200
            if  -85 <= self.car.car_angle <= -95 :
                self.reward += 200
            print(self.car.car_angle)# Récompense pour bien prendre le virage

        if self.get_grid_position() == (5, 1) and -100 <= self.car.car_angle <= -50:
            self.reward += 200

            print(self.car.car_angle)# Récompense pour bien prendre le virage






        # Pénalité pour marche arrière
        if self.car.car_speed < 0:
            self.reward -= 1000

    def run(self):
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
                    int(self.car.car_angle)
                )

                action = self.choose_action(state)

            else:
                action = next((key for key in self.actions if keys[key]), None)

            # Apply action
            if action == pygame.K_UP:
                self.car.car_speed = min(self.car.car_speed + ACCELERATION, MAX_SPEED)
            if action == pygame.K_DOWN:
                self.car.car_speed = max(self.car.car_speed - ACCELERATION, -MAX_SPEED / 2)
                #self.reward -= 100
            if action == pygame.K_LEFT:
                self.car.car_angle += TURNING_SPEED+10
            if action == pygame.K_RIGHT:
                self.car.car_angle -= TURNING_SPEED+10
                #self.reward -= 0.5
            if action is None:
                self.car.car_speed = max(0, self.car.car_speed - FRICTION) if self.car.car_speed > 0 else min(0, self.car.car_speed + FRICTION)



            prev_x = self.car.car_x
            isRenitialiser = self.car.update_position()
            if isRenitialiser:
                self.reward = 0
                self.nmbrTour = 0  # Reset
            prev_angle = self.car.car_angle



            #MAJ REWARDS
            self.update_rewards(prev_x, self.car.car_x, prev_angle)



            # si trop de points négatifs rénitialiser
            if self.reward <= -100000:
                #print("🚨 Réinitialisation : trop de points négatifs !")
                self.car.reset_position()
                self.reward = 0
                self.stuck_time = 0

            # si la voiture est bloquee
            if abs(self.car.car_speed) < 3:
                self.stuck_time += 1
                if self.stuck_time > 500:
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
                int(self.car.car_angle)
            )

            self.qtable.set(state, action, self.reward+10, new_state,self.window)


            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

            # Affichage
            self.window.fill((0, 150, 0))
            draw_track(self.window)
            draw_radar(self.window, self.car)
            rotated_car = pygame.transform.rotate(self.car.car_image, self.car.car_angle)
            self.window.blit(rotated_car, rotated_car.get_rect(center=(self.car.car_x, self.car.car_y)).topleft)

            reward_text = self.font.render(f'Reward: {self.reward}', True, (255, 255, 255))
            mode_text = self.font.render(f"Mode: {'AUTO' if AUTO_MODE else 'MANUEL'}", True, (255, 255, 255))
            if self.reward > self.reward_max : self.reward_max = self.reward
            scoremax = self.font.render(f'scoremax: {self.reward_max}', True, (0, 0, 0))
            self.window.blit(reward_text, (10, 10))
            self.window.blit(mode_text, (10, 50))
            self.window.blit(scoremax, (10, 100))
            pygame.display.flip()
            self.clock.tick(120)

    def get_grid_position(self):
        grid_x = int(self.car.car_x // 100)
        grid_y = int(self.car.car_y // 100)
        return (grid_x, grid_y)

    def check_stationary_penalty(self):
        current_grid_pos = self.get_grid_position()

        # Initialiser les attributs
        if not hasattr(self, 'last_grid_pos'):
            self.last_grid_pos = current_grid_pos
            self.grid_stationary_time = 0
            return 0

        # Si on est dans la même case
        if current_grid_pos == self.last_grid_pos:
            self.grid_stationary_time += 1


            if  abs(self.car.car_speed<1):
                #print("+60!")
                return -1 * self.grid_stationary_time
        else:
            # Réinitialiser le compteur si on change de case
            self.grid_stationary_time = 0
            self.last_grid_pos = current_grid_pos

        return 0
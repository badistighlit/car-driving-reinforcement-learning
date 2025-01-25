import pygame  # Pour le jeu
import math  # Pour les calculs mathématiques
import random  # Pour les choix aléatoires (ε-greedy)
import sys  # Pour gérer la sortie du programme
from enum import Enum  # Pour gérer les récompenses en tant qu'énumérations

# Initialisation de pygame
pygame.init()

# Récompenses
class Reward(Enum):
    STOPPED = -500
    GOAL = 1000
    WALL = -100
    DEFAULT = -1

# Fenêtre
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JE ROUUULE !!!!!")

# Classe pour la voiture
class Voiture:
    def __init__(self):
        self.car_image = pygame.image.load('car.png')  # Assurez-vous que l'image car.png existe
        self.car_image = pygame.transform.scale(self.car_image, (60, 60))
        self.car_x, self.car_y = WIDTH // 5, HEIGHT // 5
        self.car_angle = 0
        self.car_speed = 0

    def update_position(self):
        self.car_x += self.car_speed * math.cos(math.radians(self.car_angle))
        self.car_y -= self.car_speed * math.sin(math.radians(self.car_angle))

# Détection de collision (gazon)
def detect_gazon(x, y):
    try:
        color = window.get_at((int(x), int(y)))[:3]
        return color == (0, 150, 0)  # True si vert
    except IndexError:
        return True


def draw_track():
    # Bordure extérieure blanche
    pygame.draw.rect(window, (255, 255, 255), (90, 90, WIDTH - 180, HEIGHT - 180), border_radius=100)
    # Route grise
    pygame.draw.rect(window, (100, 100, 100), (100, 100, WIDTH - 200, HEIGHT - 200), border_radius=90)
    # Bordure intérieure blanche
    pygame.draw.rect(window, (255, 255, 255), (190, 190, WIDTH - 380, HEIGHT - 380), border_radius=60)
    # Gazon central
    pygame.draw.rect(window, (0, 150, 0), (200, 200, WIDTH - 400, HEIGHT - 400), border_radius=50)

    # Ligne de départ/arrivée
    finish_line_x = WIDTH // 2 - 30  # Position horizontale
    pygame.draw.rect(window, (255, 255, 255), (finish_line_x, 100, 20, 50))  # Rectangle blanc
    pygame.draw.rect(window, (255, 0, 0), (finish_line_x, 150, 20, 50))  # Rectangle rouge


# Q-Learning
class QLearning:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = {}
        self.alpha = alpha  # Taux d'apprentissage
        self.gamma = gamma  # Facteur de réduction
        self.epsilon = epsilon  # Taux d'exploration

    def get_max_action(self, state):
        if state not in self.q_table:
            self.q_table[state] = {pygame.K_UP: 0, pygame.K_DOWN: 0, pygame.K_LEFT: 0, pygame.K_RIGHT: 0}
        return max(self.q_table[state], key=self.q_table[state].get)

    def get_action(self, state):
        if random.random() < self.epsilon:
            return random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        else:
            return self.get_max_action(state)

    def update(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = {pygame.K_UP: 0, pygame.K_DOWN: 0, pygame.K_LEFT: 0, pygame.K_RIGHT: 0}
        if next_state not in self.q_table:
            self.q_table[next_state] = {pygame.K_UP: 0, pygame.K_DOWN: 0, pygame.K_LEFT: 0, pygame.K_RIGHT: 0}

        max_q_next = max(self.q_table[next_state].values())
        self.q_table[state][action] += self.alpha * (reward + self.gamma * max_q_next - self.q_table[state][action])

# Classe principale du jeu
class Game:
    def run(self):
        car = Voiture()
        qlearning = QLearning()
        running = True
        clock = pygame.time.Clock()

        prev_state = (int(car.car_x), int(car.car_y), int(car.car_angle))

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            # État actuel
            position = (int(car.car_x), int(car.car_y), int(car.car_angle))

            # Choix de l'action
            action = qlearning.get_action(position)

            # Appliquer l'action
            reward = Reward.DEFAULT.value
            if action == pygame.K_UP:
                car.car_speed = min(car.car_speed + 0.2, 5)  # Accélération
            elif action == pygame.K_DOWN:
                car.car_speed = max(car.car_speed - 0.2, -2.5)  # Frein
            elif action == pygame.K_LEFT:
                car.car_angle += 3  # Rotation à gauche
            elif action == pygame.K_RIGHT:
                car.car_angle -= 3  # Rotation à droite

            car.update_position()

            # Vérification de collision
            if car.car_x < 100 or car.car_x > WIDTH - 100 or car.car_y < 100 or car.car_y > HEIGHT - 100:
                reward = Reward.WALL.value
                car.car_speed = 0  # Arrêt de la voiture
                print(f"Malus pris ! Position: ({car.car_x}, {car.car_y}), Récompense: {reward}")

            # Nouvel état après action
            next_state = (int(car.car_x), int(car.car_y), int(car.car_angle))

            # Mise à jour de la Q-table
            qlearning.update(position, action, reward, next_state)

            # Affichage
            window.fill((0, 150, 0))  # Gazon
            draw_track()  # Piste

            # Dessiner la voiture
            rotated_car = pygame.transform.rotate(car.car_image, car.car_angle)
            car_rect = rotated_car.get_rect(center=(car.car_x, car.car_y))
            window.blit(rotated_car, car_rect.topleft)

            # Mise à jour de l'écran
            pygame.display.flip()
            clock.tick(60)

def check_finish_line(car):
    """Vérifie si la voiture traverse la ligne d'arrivée."""
    finish_line_x = WIDTH // 2 - 30
    return finish_line_x <= car.car_x <= finish_line_x + 20 and 100 <= car.car_y <= 200



def reset_position(self):
    self.car_x = WIDTH // 2 - 70  # Juste à côté de la ligne
    self.car_y = 150
    self.car_angle = 0
    self.car_speed = 0




# Lancer le jeu
if __name__ == "__main__":
    game = Game()
    game.run()

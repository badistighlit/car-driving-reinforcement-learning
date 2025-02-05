import pygame
import sys
import matplotlib.pyplot as plt
from config import WIDTH, HEIGHT, ACCELERATION, MAX_SPEED, TURNING_SPEED, FRICTION, MAX_REVERSE_SPEED
from voiture import Voiture
from track import draw_track
from qlearning import QLearning


class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("JE ROUUULE !!!!!")
        self.car = Voiture()

        # ✅ Positionner la voiture JUSTE DERRIÈRE la ligne d'arrivée
        self.car.car_x = WIDTH // 2  # Centre de la piste
        self.car.car_y = HEIGHT - 150  # Juste en bas de la ligne d'arrivée
        self.car.car_angle = 270  # ✅ Orientation vers le haut (vers la ligne d'arrivée)

        self.qlearning = QLearning()
        self.clock = pygame.time.Clock()

        # ✅ Suivi de l'apprentissage
        self.success_count = 0
        self.total_reward = 0
        self.episode_count = 0
        self.rewards = []

        # ✅ Dernière récompense pour éviter les répétitions
        self.last_reward = None
        self.actions = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]


        # ✅ Positionner la voiture derrière la ligne d'arrivée
        self.car.car_x = WIDTH - 350
        self.car.car_y = HEIGHT // 4
        self.car.car_angle = 180  # Orientation vers la gauche

        self.qlearning = QLearning()
        self.clock = pygame.time.Clock()

        # ✅ Suivi de l'apprentissage
        self.success_count = 0
        self.total_reward = 0
        self.episode_count = 0
        self.rewards = []

        # ✅ Dernière récompense pour éviter les répétitions
        self.last_reward = None
        self.actions = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            # ✅ Obtenir l'état actuel et choisir une action avec Q-Learning
            position = (int(self.car.car_x), int(self.car.car_y), int(self.car.car_angle))
            action = self.qlearning.get_action(position)

            # ✅ Initialisation de la récompense
            reward = -1

            # ✅ Appliquer l'action sélectionnée
            if action == pygame.K_UP:
                self.car.car_speed = min(self.car.car_speed + ACCELERATION, MAX_SPEED)
            elif action == pygame.K_DOWN:
                self.car.car_speed = max(self.car.car_speed - ACCELERATION, MAX_REVERSE_SPEED)
            elif action == pygame.K_LEFT:
                self.car.car_angle += TURNING_SPEED
            elif action == pygame.K_RIGHT:
                self.car.car_angle -= TURNING_SPEED

            # ✅ Mise à jour de la position de la voiture
            self.car.update_position()

            # ✅ Vérifier si la voiture touche un mur
            if self.car.car_x < 100 or self.car.car_x > WIDTH - 100 or self.car.car_y < 100 or self.car.car_y > HEIGHT - 100:
                reward = -100
                self.car.reset_position()

            # ✅ Vérifier si la voiture atteint la ligne d'arrivée
            if WIDTH // 2 - 30 <= self.car.car_x <= WIDTH // 2 - 10 and 100 <= self.car.car_y <= 200:
                reward = 10000000000000000  # ✅ Récompense pour avoir terminé le circuit
                self.success_count += 1
                print(f"🚗 Succès ! La voiture a atteint l’arrivée {self.success_count} fois ! 🎉")
                self.car.reset_position()

            # ✅ Mise à jour de la table Q
            next_position = (int(self.car.car_x), int(self.car.car_y), int(self.car.car_angle))
            self.qlearning.update(position, action, reward, next_position)

            # ✅ Suivi des récompenses pour analyse
            self.rewards.append(reward)
            self.total_reward += reward
            self.episode_count += 1

            # ✅ Affichage des statistiques toutes les 100 itérations
            if self.episode_count % 100 == 0:
                print(f"📊 Moyenne des récompenses: {self.total_reward / 100}")
                plt.plot(self.rewards)
                plt.xlabel("Épisodes")
                plt.ylabel("Récompense cumulée")
                plt.title("Progression de l’apprentissage")
                plt.show()
                self.total_reward = 0

                # ✅ Affichage du jeu
            self.window.fill((0, 150, 0))
            draw_track(self.window)

            rotated_car = pygame.transform.rotate(self.car.car_image, self.car.car_angle)
            car_rect = rotated_car.get_rect(center=(self.car.car_x, self.car.car_y))
            self.window.blit(rotated_car, car_rect.topleft)

            pygame.display.flip()
            self.clock.tick(60)

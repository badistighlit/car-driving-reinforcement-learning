import pygame
import math
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JE ROUUULE !!!!!")

# Waypoints de la piste
waypoints = [
    (150, 300),  # Point 1
    (300, 150),  # Point 2
    (500, 150),  # Point 3
    (650, 300),  # Point 4
    (500, 450),  # Point 5
    (300, 450),  # Point 6
    (150, 300)   # Retour au point 1
]

# Classe Voiture
class Voiture:
    def __init__(self):
        self.car_image = pygame.image.load('car.png')
        self.car_image = pygame.transform.scale(self.car_image, (60, 60))
        self.car_x, self.car_y = waypoints[0]  # Démarre au premier waypoint
        self.car_angle = 0
        self.car_speed = 2
        self.current_waypoint_index = 1  # Commence à viser le deuxième waypoint

    def update_position(self):
        # Coordonnées du waypoint cible
        target_x, target_y = waypoints[self.current_waypoint_index]

        # Calcul de la direction vers le waypoint
        dx = target_x - self.car_x
        dy = target_y - self.car_y
        distance = math.hypot(dx, dy)

        # Si la voiture est proche du waypoint, passer au suivant
        if distance < 10:
            self.current_waypoint_index = (self.current_waypoint_index + 1) % len(waypoints)
            return

        # Calculer l'angle vers le waypoint
        angle_rad = math.atan2(-dy, dx)  # -dy car l'axe Y est inversé dans Pygame
        self.car_angle = math.degrees(angle_rad)

        # Déplacer la voiture vers le waypoint
        self.car_x += self.car_speed * math.cos(angle_rad)
        self.car_y -= self.car_speed * math.sin(angle_rad)

# Fonction pour dessiner la piste
def draw_track():
    # Bordure blanche extérieure
    pygame.draw.rect(window, (255, 255, 255), (90, 90, WIDTH - 180, HEIGHT - 180), border_radius=100)
    # Route grise
    pygame.draw.rect(window, (100, 100, 100), (100, 100, WIDTH - 200, HEIGHT - 200), border_radius=90)
    # Bordure blanche intérieure
    pygame.draw.rect(window, (255, 255, 255), (190, 190, WIDTH - 380, HEIGHT - 380), border_radius=60)
    # Gazon central
    pygame.draw.rect(window, (0, 150, 0), (200, 200, WIDTH - 400, HEIGHT - 400), border_radius=50)
    # Ligne de départ
    start_line_x = WIDTH // 2 - 30
    pygame.draw.rect(window, (255, 255, 255), (start_line_x, 100, 20, 50))
    for i in range(10):
        color = (255, 0, 0) if i % 2 == 0 else (255, 255, 255)
        pygame.draw.rect(window, color, (start_line_x, 100 + i * 10, 20, 10))

# Jeu principal
class Game:
    def run(self):
        car = Voiture()
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            # Effacer l'écran (pelouse verte)
            window.fill((0, 150, 0))

            # Dessiner la piste
            draw_track()

            # Mise à jour de la position de la voiture
            car.update_position()

            # Rotation et affichage de la voiture
            rotated_car = pygame.transform.rotate(car.car_image, car.car_angle)
            car_rect = rotated_car.get_rect(center=(car.car_x, car.car_y))
            window.blit(rotated_car, car_rect.topleft)

            # Mise à jour de l'affichage
            pygame.display.flip()
            clock.tick(60)  # Limite à 60 FPS

# Lancer le jeu
if __name__ == "__main__":
    game = Game()
    game.run()

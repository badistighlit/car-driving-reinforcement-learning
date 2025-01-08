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

        # matrice du radar
        self.radar_matrix = []

    def update_position(self):
        self.car_x += self.car_speed * math.cos(math.radians(self.car_angle))
        self.car_y -= self.car_speed * math.sin(math.radians(self.car_angle))

    def get_radar_points(self, levels, directions):
        """Calcule les points radar sur 6 ongle"""
        radar_points = []
        for direction in directions:
            angle = math.radians(self.car_angle + direction)
            points_for_direction = []
            for level in levels:
                x = self.car_x + math.cos(angle) * level
                y = self.car_y - math.sin(angle) * level
                points_for_direction.append((x, y))
            radar_points.append(points_for_direction)
        return radar_points

    def update_radar_matrix(self, levels, directions):
        """MAJ du radar et détection du gazon"""
        radar_points = self.get_radar_points(levels, directions)
        self.radar_matrix = []  # Réinitialisation du radar
        for direction_points in radar_points:
            direction_data = []
            for x, y in direction_points:
                is_gazon = detect_gazon(x, y)
                direction_data.append(1 if is_gazon else 0)  # 1 = gazon, 0 = route
            self.radar_matrix.append(direction_data)


# Paramètres du jeu
turning_speed = 3   # Vitesse de rotation
acceleration = 0.2  # Accélération
max_speed = 5       # Vitesse maximale
friction = 0.05     # Friction

# Détection du gazon
def detect_gazon(x, y):
    """x,y coordonnée donnée, renvoi si le point est dans le gazon"""
    try:
        color = window.get_at((int(x), int(y)))[:3]
        return color == (0, 150, 0)  # True si c'est  vert
    except IndexError:
        return True

# Piste
def draw_track():
    pygame.draw.rect(window, (255, 255, 255), (90, 90, WIDTH - 180, HEIGHT - 180), border_radius=100)
    pygame.draw.rect(window, (100, 100, 100), (100, 100, WIDTH - 200, HEIGHT - 200), border_radius=90)
    pygame.draw.rect(window, (255, 255, 255), (190, 190, WIDTH - 380, HEIGHT - 380), border_radius=60)
    pygame.draw.rect(window, (0, 150, 0), (200, 200, WIDTH - 400, HEIGHT - 400), border_radius=50)
    start_line_x = WIDTH // 2 - 30
    pygame.draw.rect(window, (255, 255, 255), (start_line_x, 100, 20, 50))
    for i in range(10):
        color = (255, 0, 0) if i % 2 == 0 else (255, 255, 255)
        pygame.draw.rect(window, color, (start_line_x, 100 + i * 10, 20, 10))

# Radar
def draw_radar(car):
    """Dessine le radar """
    levels = [50, 100, 150]  # 3 niveau du radar
    directions = [0, 45, -45, 90, -90, 135, -135, 180]  # les ongles

    # Mettre à jour la matrice radar
    car.update_radar_matrix(levels, directions)

    for level in levels:
        pygame.draw.circle(window, (200, 200, 200), (int(car.car_x), int(car.car_y)), level, 1)

    # Dessiner les lignes et points radar
    radar_points = car.get_radar_points(levels, directions)
    for direction_points in radar_points:
        for i, (x, y) in enumerate(direction_points):
            color = (255, 0, 0) if detect_gazon(x, y) else (0, 255, 0)
            pygame.draw.circle(window, color, (int(x), int(y)), 3)
        pygame.draw.line(window, (0, 0, 255), (car.car_x, car.car_y), direction_points[-1], 1)

    # Afficher la matrice radar dans la console
  #  print("Radar Matrix:", car.radar_matrix)


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
                if car.car_speed > 0:
                    car.car_speed = max(0, car.car_speed - friction)
                elif car.car_speed < 0:
                    car.car_speed = min(0, car.car_speed + friction)


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

            # Radar
            draw_radar(car)

            # Mise à jour de l'affichage
            pygame.display.flip()
            clock.tick(60)  # 60 FPS

# Exécution du jeu
if __name__ == "__main__":
    game = Game()
    game.run()

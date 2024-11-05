import pygame
import math
import sys



# initialisation
pygame.init()

# fenêtre
WIDTH=800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JE ROUUULE !!!!!")

# la voiture
class Voiture:
    def __init__(self):
        self.car_image = pygame.image.load('car.png')
        self.car_image = pygame.transform.scale(self.car_image, (50, 50))
        self.car_x, self.car_y = WIDTH //5, HEIGHT // 5
        self.car_angle = 0
        self.car_speed = 0
    def update_position(self):
        self.car_x += self.car_speed * math.cos(math.radians(self.car_angle))
        self.car_y -= self.car_speed * math.sin(math.radians(self.car_angle))



# parametres du jeu
turning_speed = 3   # Vitesse de rotation
acceleration = 0.2  # Accélération
max_speed = 5       # Vitesse maximale
friction = 0.05     # Friction




#  jeu
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
            if keys[pygame.K_UP]:  #avancer
                car.car_speed = min(car.car_speed + acceleration, max_speed)
                print(car.car_speed)
            elif keys[pygame.K_DOWN]:  # reculer
                car.car_speed = max(car.car_speed - acceleration, -max_speed / 2)
            else:
                # ralenti automatique avec vitesse de départ
                if car.car_speed > 0:
                    car.car_speed -= friction
                elif car.car_speed < 0:
                    car.car_speed += friction

            if keys[pygame.K_LEFT]:  #  à gauche
                car.car_angle += turning_speed
            if keys[pygame.K_RIGHT]:  # à droite
                car.car_angle -= turning_speed


            ##### MAJ DE LECRAN

            # MAJ position
            car.update_position()

            # Effacer l'écran
            window.fill((0, 150, 0))  # pelouse

            # Dessiner une route simple avec des virages
            pygame.draw.rect(window, (100, 100, 100), (100, 100, WIDTH - 200, HEIGHT - 200), border_radius=50)

            # Rotation et affichage de la voiture
            rotated_car = pygame.transform.rotate(car.car_image, car.car_angle)
            car_rect = rotated_car.get_rect(center=(car.car_x, car.car_y))
            window.blit(rotated_car, car_rect.topleft)

            # MAJ l'affichage
            pygame.display.flip()
            clock.tick(60)  # 60 FPS

# Exécution du jeu
if __name__ == "__main__":
    game = Game()
    game.run()
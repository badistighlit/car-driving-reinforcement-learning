import pygame
from config import WIDTH, HEIGHT, WHITE, GREY, GREEN, RED

def draw_track(window):
    pygame.draw.rect(window, WHITE, (90, 90, WIDTH - 180, HEIGHT - 180), border_radius=100)
    pygame.draw.rect(window, GREY, (100, 100, WIDTH - 200, HEIGHT - 200), border_radius=90)
    pygame.draw.rect(window, WHITE, (190, 190, WIDTH - 380, HEIGHT - 380), border_radius=60)
    pygame.draw.rect(window, GREEN, (200, 200, WIDTH - 400, HEIGHT - 400), border_radius=50)

    start_line_x = WIDTH // 2 - 30
    pygame.draw.rect(window, WHITE, (start_line_x, 100, 20, 50))
    pygame.draw.rect(window, RED, (start_line_x, 150, 20, 50))

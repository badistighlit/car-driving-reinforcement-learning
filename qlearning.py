import pygame
import random

class QLearning:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.5):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

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

        # ✅ Réduction progressive d'epsilon pour moins d'exploration
        if self.epsilon > 0.01:
            self.epsilon *= 0.995

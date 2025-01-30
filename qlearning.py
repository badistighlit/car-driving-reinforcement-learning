import pygame


class QTable:
    def __init__(self, learning_rate=0.8, discount_factor=0.9):
        self.qtable = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

    def set(self, position, action, reward, new_position):
        if position not in self.qtable:
            self.qtable[position] = {pygame.K_UP: 0, pygame.K_DOWN: 0, pygame.K_LEFT: 0, pygame.K_RIGHT: 0}
        if new_position not in self.qtable:
            self.qtable[new_position] = {pygame.K_UP: 0, pygame.K_DOWN: 0, pygame.K_LEFT: 0, pygame.K_RIGHT: 0}

        change = reward + self.discount_factor * max(self.qtable[new_position].values()) - self.qtable[position][action]
        self.qtable[position][action] += self.learning_rate * change

    def __repr__(self):
        res = ' ' * 15 + 'UP     DOWN     LEFT     RIGHT\r\n'
        for state in self.qtable:
            res += f'{state} '
            for action in self.qtable[state]:
                res += f'{self.qtable[state][action]:8.1f} '
            res += '\r\n'
        return res

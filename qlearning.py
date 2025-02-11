import random
import pygame
import pickle
import os
import numpy as np

QTABLE_FILE = "qtable.pkl"

class QTable:
    def __init__(self, learning_rate=0.5, discount_factor=0.9):
        self.qtable = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.replay_buffer = []
        self.max_replay_buffer_size = 10000
        self.replay_batch_size = 32
        self.load_qtable()

    def simplify_radar_data(self, radar_data):
        directions = [0, 180, -90, 90]
        radar_state = []
        thresholds = [20, 40, 60, 80]

        for i, direction in enumerate(directions):
            if i < len(radar_data):
                distances = radar_data[i]
                min_distance = min(distances) if distances else float('inf')

                for j, threshold in enumerate(thresholds):
                    if min_distance <= threshold:
                        danger_level = len(thresholds) - j
                        break
                else:
                    danger_level = 0
                radar_state.append(danger_level)
            else:
                radar_state.append(0)

        return tuple(radar_state)

    def get_state_key(self, state, window):
        if not state:
            return None

        position_x, position_y, radar_data, car_angle = state
        grid_x = int(position_x // 50)
        grid_y = int(position_y // 50)
        angle_index = int((car_angle % 360) // 30)
        radar_state = self.simplify_radar_data(radar_data)

        return (grid_x, grid_y, radar_state, angle_index)

    def choose_action(self, state, epsilon, actions, window):
        state_key = self.get_state_key(state, window)
        if state_key is None:
            return random.choice(actions)

        if state_key not in self.qtable:
            self.qtable[state_key] = {a: 5.0 for a in actions}

        if random.random() < epsilon:
            return random.choice(actions)

        return max(self.qtable[state_key], key=self.qtable[state_key].get)

    def set(self, state, action, reward, next_state, window):
        if not state or not next_state:
            return

        current_state_key = self.get_state_key(state, window)
        next_state_key = self.get_state_key(next_state, window)

        if current_state_key is None or next_state_key is None:
            return

        # Initialisation des nouveaux états
        for state_key in [current_state_key, next_state_key]:
            if state_key not in self.qtable:
                self.qtable[state_key] = {pygame.K_UP: 5.0, pygame.K_DOWN: 5.0,
                                          pygame.K_LEFT: 5.0, pygame.K_RIGHT: 5.0}

        # Limitation des récompenses
        reward = np.clip(reward, -100, 100)

        # Récupération des valeurs Q actuelles
        current_q = self.qtable[current_state_key].get(action, 0)
        next_max_q = max(self.qtable[next_state_key].values(), default=0)

        # Vérification des valeurs NaN ou Inf
        if np.isnan(reward) or np.isinf(reward):
            reward = 0
        if np.isnan(current_q) or np.isinf(current_q):
            current_q = 0
        if np.isnan(next_max_q) or np.isinf(next_max_q):
            next_max_q = 0

        # Mise à jour Q-learning
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_max_q - current_q)

        # Vérification NaN / Inf après calcul
        if np.isnan(new_q) or np.isinf(new_q):
            new_q = 0

        self.qtable[current_state_key][action] = new_q

        # Ajout à l'experience replay
        self.add_to_replay_buffer(current_state_key, action, reward, next_state_key)

        # Experience replay périodique
        if len(self.replay_buffer) >= self.replay_batch_size:
            self.perform_experience_replay()

        self.save_qtable()

    def add_to_replay_buffer(self, state, action, reward, next_state):
        self.replay_buffer.append((state, action, reward, next_state))
        if len(self.replay_buffer) > self.max_replay_buffer_size:
            self.replay_buffer.pop(0)

    def perform_experience_replay(self):
        if len(self.replay_buffer) < self.replay_batch_size:
            return

        batch = random.sample(self.replay_buffer, self.replay_batch_size)
        for state, action, reward, next_state in batch:
            if state in self.qtable and next_state in self.qtable:
                current_q = self.qtable[state].get(action, 0)
                next_max_q = max(self.qtable[next_state].values(), default=0)

                # Vérification NaN/Inf
                if np.isnan(current_q) or np.isinf(current_q):
                    current_q = 0
                if np.isnan(next_max_q) or np.isinf(next_max_q):
                    next_max_q = 0

                # Mise à jour Q-learning
                new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_max_q - current_q)

                if np.isnan(new_q) or np.isinf(new_q):
                    new_q = 0

                self.qtable[state][action] = new_q

    def save_qtable(self):
        with open(QTABLE_FILE, "wb") as f:
            pickle.dump(self.qtable, f)

    def load_qtable(self):
        if os.path.exists(QTABLE_FILE) and os.path.getsize(QTABLE_FILE) > 0:
            with open(QTABLE_FILE, "rb") as f:
                self.qtable = pickle.load(f)
            print(f"QTable chargée ({len(self.qtable)} états)")
        else:
            self.qtable = {}
            print("Aucune QTable existante trouvée, démarrage avec une table vide.")

    def __repr__(self):
        res = ' ' * 15 + 'UP      DOWN    LEFT    RIGHT\n'
        for state in list(self.qtable.keys())[:10]:
            grid_x, grid_y, radar, angle_index = state
            res += f'({grid_x},{grid_y}) A:{angle_index} R:{radar} '
            for action in self.qtable[state]:
                res += f'{self.qtable[state][action]:7.1f} '
            res += '\n'
        return res + f"\nTotal States: {len(self.qtable)}"

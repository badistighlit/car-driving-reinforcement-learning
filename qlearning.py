import random
import pygame
import pickle
import os


QTABLE_FILE = "qtable.pkl"

class QTable:
    def __init__(self, learning_rate=0.35, discount_factor=0.8):
        self.qtable = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.max_reward = float('-inf')  # Initialise avec une très petite valeur
        self.min_reward = float('inf')   # Initialise avec une très grande valeur
        self.load_qtable()  # Charger la Q-table au démarrage
        self.state_visits = {}

    def simplify_radar_data(self, radar_data):

        #Simplifie le radar en 4 directions avec 3 niveaux de danger.

        #  devant  derrière  à gauche, à droite
        directions = [0, 180, -90, 90]
        radar_state = []

        thresholds = [40, 70, 100]  # Niveaux de distance pour faible, moyen, élevé

        for i, direction in enumerate(directions):
            if i < len(radar_data):
                distances = radar_data[i]
                if not distances:
                    radar_state.append(0)  # Pas de danger
                    continue

                min_distance = min(distances)

                #le niveau de danger
                if min_distance <= thresholds[0]:
                    danger_level = 2  # Élevé
                elif min_distance <= thresholds[1]:
                    danger_level = 1  # Moyen
                else:
                    danger_level = 0  # Faible

                radar_state.append(danger_level)

        return tuple(radar_state)

    def get_state_key(self, state, window):

        if not state:
            return None

        position_x, position_y, radar_data, car_angle = state

        # Simplifier la position en grille en case de 25 PX
        grid_x = int(position_x // 25)
        grid_y = int(position_y // 25)
        #print(f"position: ({grid_x}, {grid_y}), angle: {car_angle}, radar: {radar_data}")

        # Simplifier l'angle en 12 en 30 degres
        angle_index = int((car_angle % 360) // 30)

        radar_state = self.simplify_radar_data(radar_data)

        # Détection du gazon
        #on_grass = 1 if detect_gazon(position_x, position_y, window) else 0

        # Retourner l'état complet
        return (grid_x, grid_y, radar_state, angle_index)

    def choose_action(self, state, epsilon, actions, window):


        state_key = self.get_state_key(state, window)
        if state_key is None:
            return random.choice(actions)

        #état est inconnu
        if state_key not in self.qtable:
            return random.choice(actions)

        # Exploration
        if random.random() < epsilon:
            return random.choice(actions)

        # Exploitation : on choisit l'action ayant la meilleure Q-value pour l'état donné
        #print(self.qtable[state_key])
        return max(self.qtable[state_key], key=self.qtable[state_key].get)

    def set(self, state, action, reward, next_state, window):
        if not state or not next_state:
            return

        current_state_key = self.get_state_key(state, window)
        next_state_key = self.get_state_key(next_state, window)

        if current_state_key is None or next_state_key is None:
            return

        # Initialize if new state
        if current_state_key not in self.qtable:

            self.qtable[current_state_key] = {
                pygame.K_UP: 1.0,
                pygame.K_DOWN: -1.0,
                pygame.K_LEFT: 0.0,
                pygame.K_RIGHT: 0.0
            }
            print(f"Nouvel état ajouté : {current_state_key} | Total états : {len(self.qtable)}")

        if next_state_key not in self.qtable:
            self.qtable[next_state_key] = {
                pygame.K_UP: 1.0,
                pygame.K_DOWN: -1.0,
                pygame.K_LEFT: 0.0,
                pygame.K_RIGHT: 0.0
            }

        # Update reward
        self.max_reward = max(self.max_reward, reward)
        self.min_reward = min(self.min_reward, reward)

        # Scale reward
        reward_range = max(1, int(self.max_reward - self.min_reward))
        scaled_reward = (reward - self.min_reward) / reward_range
        scaled_reward = max(-1, min(1, scaled_reward))  # Garde les valeurs entre -1 et 1

        current_q = self.qtable[current_state_key][action]

        next_max_q = max(self.qtable[next_state_key].values())

        momentum = 0.1
        new_q = current_q + self.learning_rate * (
                scaled_reward +
                self.discount_factor * next_max_q -
                current_q +
                momentum * (next_max_q - current_q)  # Add momentum term
        )

        self.qtable[current_state_key][action] = new_q

        self.save_qtable()

    def save_qtable(self):
        """Sauvegarde"""
        with open(QTABLE_FILE, "wb") as f:
            pickle.dump(self.qtable, f)
        #print(f"QTable sauvegardée ({len(self.qtable)} états)")

    def load_qtable(self):
        """Charge """
        if os.path.exists(QTABLE_FILE):
            with open(QTABLE_FILE, "rb") as f:
                self.qtable = pickle.load(f)
            print(f"QTable chargée ({len(self.qtable)} états)")
        else:
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

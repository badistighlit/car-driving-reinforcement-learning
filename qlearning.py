import random
import pygame
import pickle
import os
from config import WIDTH, HEIGHT
from utils import detect_gazon

QTABLE_FILE = "qtable.pkl"

class QTable:
    def __init__(self, learning_rate=0.2, discount_factor=0.8):
        self.qtable = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.max_reward = float('-inf')  # Initialise avec une très petite valeur
        self.min_reward = float('inf')   # Initialise avec une très grande valeur
        self.load_qtable()  # Charger la Q-table au démarrage

    def simplify_radar_data(self, radar_data):
        """
        Simplifie les données radar en zones de danger plus précises
        """
        n_angles = len(radar_data)  # Nombre de directions radar
        radar_state = []

        # Définir des seuils de distance plus précis
        thresholds = [20, 40, 60, 80]  # Très proche, proche, moyen, loin

        for i in range(n_angles):
            # Conversion des distances en niveaux de danger
            distances = radar_data[i]
            if not distances:  # Si pas de données pour cet angle
                radar_state.append(0)
                continue

            # Trouve la distance minimale pour cet angle
            min_distance = min(distances)

            # Conversion en niveau de danger (0 = pas de danger, 4 = danger maximal)
            if min_distance <= thresholds[0]:
                danger_level = 4  # Danger maximal
            elif min_distance <= thresholds[1]:
                danger_level = 3
            elif min_distance <= thresholds[2]:
                danger_level = 2
            elif min_distance <= thresholds[3]:
                danger_level = 1
            else:
                danger_level = 0  # Pas de danger

            radar_state.append(danger_level)

        return tuple(radar_state)

    def get_state_key(self, state, window):
        """
        Crée une clé d'état qui inclut les données radar simplifiées
        """
        if not state:
            return None

        position_x, position_y, radar_data, car_angle = state

        # Simplifier la position en grille plus large
        grid_x = int(position_x // 50)  # Grille de 50x50 pixels
        grid_y = int(position_y // 50)

        # Simplifier l'angle en 8 directions (45 degrés chacune)
        angle_index = int((car_angle % 360) //45)

        # Obtenir les données radar simplifiées
        radar_state = self.simplify_radar_data(radar_data)

        # Détection du gazon
        on_grass = 1 if detect_gazon(position_x, position_y, window) else 0

        # Retourner l'état complet
        return (grid_x, grid_y, radar_state, angle_index, on_grass)

    def choose_action(self, state, epsilon, actions,window):
        """Choisit une action avec epsilon-greedy."""
        if random.random() < epsilon:
            return random.choice(actions)

        state_key = self.get_state_key(state,window)
        if state_key is None or state_key not in self.qtable:
            return random.choice(actions)

        return max(self.qtable[state_key], key=self.qtable[state_key].get)

    def set(self, state, action, reward, next_state, window):
        """Updates Q-table with improved reward scaling and momentum"""
        if not state or not next_state:
            return

        current_state_key = self.get_state_key(state, window)
        next_state_key = self.get_state_key(next_state, window)

        if current_state_key is None or next_state_key is None:
            return

        # Initialize if new state
        if current_state_key not in self.qtable:
            # Bias initial values towards forward movement
            self.qtable[current_state_key] = {
                pygame.K_UP: 1.0,  # Slight bias for forward
                pygame.K_DOWN: -1.0,  # Negative bias for reverse
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

        # Update reward tracking
        self.max_reward = max(self.max_reward, reward)
        self.min_reward = min(self.min_reward, reward)

        # Scale reward to prevent extreme values
        scaled_reward = reward / max(abs(self.max_reward), abs(self.min_reward)) if self.max_reward != float(
            '-inf') else reward

        # Get current Q value
        current_q = self.qtable[current_state_key][action]

        # Get max Q value for next state
        next_max_q = max(self.qtable[next_state_key].values())

        # Update Q value with momentum
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
        """Sauvegarde la Q-table dans un fichier."""
        with open(QTABLE_FILE, "wb") as f:
            pickle.dump(self.qtable, f)
        #print(f"QTable sauvegardée ({len(self.qtable)} états)")

    def load_qtable(self):
        """Charge la Q-table depuis un fichier."""
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

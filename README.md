# Jeu de Courses avec Apprentissage par Renforcement

Ce projet est un jeu de course de voiture dans lequel un agent apprend à naviguer sur un circuit en utilisant l'apprentissage par renforcement avec une Q-table.

![image](https://github.com/user-attachments/assets/ec6d12fa-0d6d-4edb-bbd2-282f50deaa79)

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine :

- Python 3.x
- pip (gestionnaire de paquets Python)

## Installation

Clonez ce dépôt et installez les dépendances nécessaires :

```sh
# Cloner le dépôt
git clone https://github.com/badistighlit/car-driving-reinforcement-learning


# Installer les dépendances
pip install -r requirements.txt
```

## Lancement du Jeu

Exécutez le script principal pour démarrer l'entraînement de l'agent et jouer :

```sh
python main.py
```



## Algorithme d'Apprentissage

L'agent utilise l'algorithme Q-Learning pour apprendre la meilleure stratégie de conduite.

1. Initialisation de la Q-table
2. Sélection d'une action (exploration/exploitation)
3. Exécution de l'action et observation de la récompense
4. Mise à jour de la Q-table
5. Répétition du processus pour améliorer les performances

## Diagramme de Progression
![image](https://github.com/user-attachments/assets/f3bda24e-56f7-4319-bd1d-e6194ff69b93)



## Améliorations Futures

- Ajouter des obstacles dynamiques
- Implémenter Deep Q-Learning pour une meilleure performance
- Intégration avec une interface graphique






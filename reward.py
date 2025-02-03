from enum import Enum  

class Reward(Enum):
    STOPPED = -500
    GOAL = 1000
    WALL = -100
    DEFAULT = -1
    GOAL_WRONG = -800
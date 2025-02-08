from enum import Enum  

class Reward(Enum):
    STOPPED = -10
    GOAL = 10000
    WALL = -6000
    DEFAULT = +100
    GOAL_WRONG = -8000
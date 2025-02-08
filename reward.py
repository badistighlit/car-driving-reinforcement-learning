from enum import Enum  

class Reward(Enum):
    STOPPED = -10      # Less extreme penalty
    GOAL = 10000       # Still high but not as extreme
    WALL = -6000       # Less extreme penalty
    DEFAULT = +100      # Smaller step penalty
    GOAL_WRONG = -8000 # Less extreme penalty
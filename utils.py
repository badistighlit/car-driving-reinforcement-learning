from config import WIDTH, HEIGHT, WHITE, GREY, GREEN, RED

def detect_gazon(x, y,window):


    """Détecte ::; le gazon """

    if x < 100 or x > WIDTH - 100 or y < 100 or y > HEIGHT - 100:
        return True


    if 100 <= x <= WIDTH - 100 and 100 <= y <= HEIGHT - 100:

        if 200 <= x <= WIDTH - 200 and 200 <= y <= HEIGHT - 200:
            return True

    return False


def detect_proximite_gazon(self, x, y, distance=30):
    for dx in [-distance, 0, distance]:
        for dy in [-distance, 0, distance]:
            if detect_gazon(x + dx, y + dy, self.window):
                return True
    return False


def detect_gazon(x, y, window):
    """x, y coordonnée donnée, renvoi si le point est dans le gazon"""
    try:
        color = window.get_at((int(x), int(y)))[:3]
        return color == (0, 150, 0)  # True si c'est vert
    except IndexError:
        return True

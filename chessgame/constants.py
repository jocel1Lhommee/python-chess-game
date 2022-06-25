# taille de la fenêtre
WINDOW_WIDTH = WINDOW_HEIGHT = 800
# Nombre de rafraichissement par seconde
FPS = 60

# nombre de ligne/colonne du plateau et taille d'une case
ROWS = COLS = 8
SQUARE_SIZE = min(WINDOW_WIDTH, WINDOW_HEIGHT)//max(ROWS, COLS)

# couleurs rgb
SQUARE_COLOR_LIGHT = (104, 123, 171)
SQUARE_COLOR_DARK = (236, 236, 236)
SQUARE_COLOR_SELECTED = (255, 0, 0)

# Fenêtre de choix de couleur de jeu
BACKGROUND_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 128)
X_POSITION, Y_POSITION = (WINDOW_WIDTH//5.5, WINDOW_HEIGHT//2.5)

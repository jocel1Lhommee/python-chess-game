import pygame as p
from chessgame.constants import WINDOW_WIDTH, WINDOW_HEIGHT, TEXT_COLOR, X_POSITION, Y_POSITION, BACKGROUND_COLOR, FPS,\
    SQUARE_SIZE, SQUARE_COLOR_LIGHT, SQUARE_COLOR_DARK, ROWS, COLS, SQUARE_COLOR_SELECTED
from chessgame.board import Board, createPieceByType


def init_surface(width, height):
    """Initialisation de l'affichage

    Args:
        width (int): largeur de la fenêtre
        height (_type_): hauteur de la fenêtre

    Returns:
        (pygame.object,pygame.object): (fenêtre pygame,clock pygame)
    """
    p.init()
    WINDOW = p.display.set_mode((width, height))
    p.display.set_caption('chessGame')
    fpsClock = p.time.Clock()
    return WINDOW, fpsClock


def blit_text(surface, text, pos, font, color=p.Color('black')):
    """Affichage pygame de texte sur plusieurs lignes

    Args:
        surface (object): "pygame.Surface"
        text (string): texte qui s'affiche
        pos (tuple[2 int]): position du coin supérieur gauche
        font (object): police d'écriture
        color (tuple[3 int]): couleur du texte
    """
    # 2D array where each row is a list of words.
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def get_human_color(WINDOW, fpsClock, FPS):
    """Choix Couleur du joueur

    Args:
        WINDOW (pygame object): fenêtre pygame
        fpsClock (pygame object): clock pygame
        FPS (int): nombre de FPS de l'affichage

    Returns:
        boolean: L'humain joue les blancs
    """
    font = p.font.Font('freesansbold.ttf', 32)
    text = "Choisissez votre couleur\n"\
        "Tapez sur B pour choisir les Blanc\n"\
        "Tapez sur N pour choisir les Noirs"
    WINDOW.fill(BACKGROUND_COLOR)
    blit_text(WINDOW, text, (X_POSITION, Y_POSITION), font, TEXT_COLOR)
    while True:
        # WINDOW.fill(BACKGROUND_COLOR)
        #blit_text(WINDOW, text, (X_POSITION, Y_POSITION), font, TEXT_COLOR)
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
            elif event.type == p.KEYDOWN:
                if event.key == p.K_b:
                    return True
                if event.key == p.K_n:
                    return False
            p.display.update()
            fpsClock.tick(FPS)


def getPromotion(WINDOW, fpsClock, FPS, isWhitePiece):
    if isWhitePiece:
        typeFirstLetter = "w"
    else:
        typeFirstLetter = "b"
    font = p.font.Font('freesansbold.ttf', 32)
    text = "Choisissez votre Promotion\n"\
        "Tapez sur D pour choisir une Dame\n"\
        "Tapez sur T pour choisir une Tour\n"\
        "Tapez sur F pour choisir un Fou\n"\
        "Tapez sur C pour choisir un Cavalier"
    WINDOW.fill(BACKGROUND_COLOR)
    blit_text(WINDOW, text, (X_POSITION, Y_POSITION), font, TEXT_COLOR)
    while True:
        # WINDOW.fill(BACKGROUND_COLOR)
        #blit_text(WINDOW, text, (X_POSITION, Y_POSITION), font, TEXT_COLOR)
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
            elif event.type == p.KEYDOWN:
                if event.key == p.K_d:
                    return createPieceByType(typeFirstLetter+"Q")
                if event.key == p.K_t:
                    return createPieceByType(typeFirstLetter+"R")
                if event.key == p.K_f:
                    return createPieceByType(typeFirstLetter+"B")
                if event.key == p.K_c:
                    return createPieceByType(typeFirstLetter+"N")
            p.display.update()
            fpsClock.tick(FPS)


def continueGameChoice(WINDOW, fpsClock, FPS, result, colorIsWhite):
    if result == "pat":
        text = "Match nul sur pat\n"\
            "Tapez sur ENTER pour rejouer\n"
    else:
        if colorIsWhite:
            text = "Les Noirs ont gagnés\n"\
                "Tapez sur ENTER pour rejouer\n"
        else:
            text = "Les Blancs ont gagnés\n"\
                "Tapez sur RETURN pour rejouer\n"
    font = p.font.Font('freesansbold.ttf', 32)
    WINDOW.fill(BACKGROUND_COLOR)
    blit_text(WINDOW, text, (X_POSITION, Y_POSITION), font, TEXT_COLOR)
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
            elif event.type == p.KEYDOWN:
                if event.key == p.K_RETURN:
                    game(WINDOW, fpsClock, FPS, IMAGES, humanColorIsWhite)
            p.display.update()
            fpsClock.tick(FPS)


def loadImages(SQUARE_SIZE):
    """Charge dans un dictionnaire Les images de pièces à la bonne taille

    Args:
        SQUARE_SIZE (int): taille d'une case

    Returns:
        dic(string:image pygame): dictionnaire d'images en fonction du type de pièce
    """
    IMAGES = {}
    PIECE = ["wP", "wN", "wB", "wR", "wQ", "wK",
             "bP", "bN", "bB", "bR", "bQ", "bK"]
    for piece in PIECE:
        image = p.image.load("chessgame/images/"+piece+".png")
        IMAGES[piece] = p.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
    return IMAGES


def game(WINDOW, fpsClock, FPS, IMAGES, humanColorIsWhite):
    board = Board(humanColorIsWhite)
    run = True
    fpsClock = p.time.Clock()
    humanTour = humanColorIsWhite
    chessEvent = None
    while run:
        WINDOW.fill(BACKGROUND_COLOR)
        draw_squares(WINDOW)
        # ajouter "and humanTour" ne plus avoir les actions de l'engine
        if board.selectedPosition != None:
            draw_moves(board.arrayBoard, board.selectedPosition, WINDOW)
        drawPieces(WINDOW, board.arrayBoard)
        # si c'est le tour de l'Humain|mettre humanTour à la place du True
        if True:
            for event in p.event.get():
                move = None
                if event.type == p.QUIT:
                    p.quit()
                # si click gauche
                # ajouter and humanTour pour ne pas pouvoir bouger pièce couleur opposée
                if p.mouse.get_pressed()[0]:
                    location = p.mouse.get_pos()
                    row, col = get_position(location)
                    # si la case est vide
                    if board.arrayBoard[row][col] == None:
                        # si est dans les moves possibles de la pièce sélectionée ajouter condition de couleur en deuxième place pour empêcher jouer couleur adverse: and board.arrayBoard[board.selectedPosition[0]][board.selectedPosition[1]].isWhite() == humanColorIsWhite
                        if board.selectedPosition != None and (row, col) in board.arrayBoard[board.selectedPosition[0]][board.selectedPosition[1]].availableMove:
                            # prise en passant ou bouge juste
                            enPassant = enPassantSituation(board, (row, col))

                            if not enPassant:
                                # on bouge la pièce
                                chessEvent = board.moveTo(
                                    board.selectedPosition, (row, col))
                                board.selectedPosition = None
                            else:
                                if board.arrayBoard[board.selectedPosition[0]][board.selectedPosition[1]].isWhite() == board.whiteBottom:
                                    board.enPassant(
                                        board.selectedPosition, (row+1, col), (row, col))
                                else:
                                    board.enPassant(
                                        board.selectedPosition, (row-1, col), (row, col))
                                board.selectedPosition = None
                            move = True
                        else:
                            # on déselectionne la pièce sélectionée
                            board.selectedPosition = None
                    # si la case à une pièce
                    else:
                        # si est dans les moves possibles de la pièce sélectionée
                        if board.selectedPosition != None and (row, col) in board.arrayBoard[board.selectedPosition[0]][board.selectedPosition[1]].availableMove:
                            roque = roqueSituation(board, (row, col))
                            # si pas roque
                            if not roque:
                                # on mange la pièce
                                chessEvent = board.eatTo(
                                    board.selectedPosition, (row, col))
                                board.selectedPosition = None
                            # sinon on roque
                            else:
                                board.roque((row, col))
                                board.selectedPosition = None
                            move = True
                        else:
                            if board.selectedPosition != (row, col):
                                # on sélectionne la nouvelle pièce
                                board.selectedPosition = (row, col)
                                board.getAvailableMove(
                                    board.selectedPosition)
                    # si bougé on vérifie échec et mat
                    if move:
                        pat, colorIsWhite = patSituation(board)
                        if pat:
                            checkmate = checkmateSituation(board, colorIsWhite)
                            if checkmate:
                                continueGameChoice(
                                    WINDOW, fpsClock, FPS, "checkmate", colorIsWhite)
                            else:
                                continueGameChoice(
                                    WINDOW, fpsClock, FPS, "pat", colorIsWhite)
                if chessEvent == "Promotion":
                    board.arrayBoard[row][col] = getPromotion(
                        WINDOW, fpsClock, FPS, board.arrayBoard[row][col].isWhite())
                    chessEvent = None

                p.display.update()
                fpsClock.tick(FPS)

#sélected:(3, 3)
# pointe vers:(2, 2)


def enPassantSituation(board, clickPosition):
    # si est un pion sélectionné
    if board.arrayBoard[board.selectedPosition[0]][board.selectedPosition[1]].type[1] == "P":
        # si blanc en bas et piece blanche ou si noir en bas et piece noir
        if board.arrayBoard[board.selectedPosition[0]][board.selectedPosition[1]].isWhite() == board.whiteBottom:
            # si colonne supérieure à 0
            if board.selectedPosition[1] > 0:
                # si click est diagonale vers haut gauche
                if clickPosition == (board.selectedPosition[0]-1, board.selectedPosition[1]-1):
                    return True
            # si colonne inférieure à 7
            if board.selectedPosition[1] < 7:
                # si click est diagonale vers haut droite
                if clickPosition == (board.selectedPosition[0]-1, board.selectedPosition[1]+1):
                    return True
        else:
            # si colonne supérieure à 0
            if board.selectedPosition[1] > 0:
                # si click est diagonale vers bas gauche
                if clickPosition == (board.selectedPosition[0]+1, board.selectedPosition[1]-1):
                    return True
            # si colonne inférieure à 7
            if board.selectedPosition[1] < 7:
                # si click est diagonale vers bas droite
                if clickPosition == (board.selectedPosition[0]+1, board.selectedPosition[1]+1):
                    return True
    return False


def roqueSituation(board, clickPosition):
    if board.arrayBoard[board.selectedPosition[0]][board.selectedPosition[1]].type[1] == "K":
        if board.arrayBoard[clickPosition[0]][clickPosition[1]].type[1] == "R":
            if board.arrayBoard[clickPosition[0]][clickPosition[1]].isWhite() == board.arrayBoard[board.selectedPosition[0]][board.selectedPosition[1]].isWhite():
                return True
    return False


def checkmateSituation(board, colorPatIsWhite):
    for row in range(8):
        for col in range(8):
            piece = board.arrayBoard[row][col]
            if piece != None and piece.isWhite() != colorPatIsWhite:
                board.getAvailableMove((row, col))
                for move in piece.availableMove:
                    movePiece = board.arrayBoard[move[0]][move[1]]
                    if movePiece != None and movePiece.type[1] == "K":
                        return True
    return False


def patSituation(board):
    moveWhite, moveBlack = False, False
    for row in range(8):
        for col in range(8):
            piece = board.arrayBoard[row][col]
            if piece != None:
                if (moveWhite, moveBlack) == (True, True):
                    return False, None
                whitePiece = piece.isWhite()
                if not moveWhite and whitePiece:
                    board.getAvailableMove((row, col))
                    if piece.availableMove != []:
                        moveWhite = True
                if not moveBlack and not whitePiece:
                    board.getAvailableMove((row, col))
                    if piece.availableMove != []:
                        moveBlack = True
    if not moveWhite:
        return True, True
    else:
        return True, False


def draw_moves(arrayBoard, selectedPosition, window):
    """Dessine les moves réalisables par la pièce sélectionnée

    Args:
        board (tab[Piece]): tableau qui rep l'emplacement des pièces'
        selectedPosition (Tuple(int,int)): (ligne,colonne) de la pièce sélectionnée
        window (pygame object): fenêtre pygame
    """
    for position in (arrayBoard[selectedPosition[0]][selectedPosition[1]]).availableMove + [(selectedPosition[0], selectedPosition[1])]:
        p.draw.rect(
            window, SQUARE_COLOR_SELECTED, (position[1]*SQUARE_SIZE, position[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawPieces(WINDOW, board):
    """Dessine les pièces du plateau sur la fenêtre de jeu

    Args:
        WINDOW (pygame object): fenêtre pygame
        board (object): plateau de jeu
    """
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != None:
                if piece.type in ["wP", "wN", "wB", "wR", "wQ", "wK", "bP", "bN", "bB", "bR", "bQ", "bK"]:
                    WINDOW.blit(IMAGES[piece.type], p.Rect(
                        col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def get_position(location):
    """converti coordonées de fenêtre en ligne, colonne du plateau

    Args:
        location (Tuple(int,int)): coordonées absolu dans la fenêtre (X,Y)

    Returns:
        Tuple(int,int): coordonées de la case (ligne,colonne)
    """
    return(location[1]//SQUARE_SIZE, location[0]//SQUARE_SIZE)


def draw_squares(WINDOW):
    """Dessine le patern bicolor du plateau de jeu

    Args:
        WINDOW (pygame object): fenêtre pygame
    """
    WINDOW.fill(SQUARE_COLOR_DARK)
    for row in range(ROWS):
        for col in range(row % 2, COLS, 2):
            p.draw.rect(WINDOW, SQUARE_COLOR_LIGHT, (row*SQUARE_SIZE,
                        col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


if __name__ == '__main__':
    p.init()
    WINDOW = p.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    p.display.set_caption('chessGame')
    fpsClock = p.time.Clock()
    IMAGES = loadImages(SQUARE_SIZE)
    #WINDOW, fpsClock = init_surface(WINDOW_WIDTH, WINDOW_HEIGHT)
    humanColorIsWhite = get_human_color(WINDOW, fpsClock, FPS)
    game(WINDOW, fpsClock, FPS, IMAGES, humanColorIsWhite)

import time

import board
import numpy as np
import pygame

# Width and height of pygame window
WIDTH, HEIGHT = 700, 600

# Colours to be used
BACKGROUND_COLOUR = (0, 0, 0)
GRID_COLOUR = (21, 27, 84)
PLAYER_COLOUR = (255, 255, 0)
AI_COLOUR = (255, 0, 0)
HIGHLIGHT_COLOUR = (21, 70, 84)
TEXT_COLOUR = (255, 255, 255)
RESTARTBUTTON_COLOUR = (173, 216, 230)

# Position of restart button when game is finished
RESTARTBUTTON = (WIDTH - 150, 25, 120, 35)


def rel_coord(x):
    """
    Rounds coordinates to closest relative lattice point

    Args:
        x (float): Pygame window x coordinate

    Returns:
        int: Closest lattice point using integer representation
    """
    return np.floor(7 * x / WIDTH)


def grid_coord(x_rel_pos, y_rel_pos):
    """
    Converts relative coordinates to grid coordinates

    Args:
        x_rel_pos (int): Relative x coordinate
        y_rel_pos (int): Relative y coordinate

    Returns:
        float: Respective grid coordinate
    """
    return (x_rel_pos + 0.5) * (WIDTH / 7), (5.5 - y_rel_pos) * (WIDTH / 7)


def isin(pos, rect):
    """
    Checks whether coordinates of point are in a rectangle

    Args:
        pos (int): Coordinates of point
        rect (list): Coordinates of rectangle: (top left edge x, top left edge y, width, height)

    Returns:
        bool: True if point in rectangle else False
    """
    x, y = pos
    top_leftx, top_lefty = rect[0], rect[1]
    bottom_rightx, bottom_righty = rect[0] + rect[2], rect[1] + rect[3]

    return x > top_leftx and x < bottom_rightx and y > top_lefty and y < bottom_righty


def draw(state, window):
    """
    Draw board on window

    Args:
        state (Board): connect4 board
        window (pygame.window): window to draw board on
    """
    window.fill(GRID_COLOUR)

    def draw_circle(xrel, yrel, colour):

        radius = WIDTH / 15
        pygame.draw.circle(window, colour, grid_coord(xrel, yrel), radius)

    # Highlight column the mouse is hovered over as long as game is running
    # Note: Done BEFORE counters are drawn, so counters not covered by highlighted column
    if not state.checkwin():

        x, _ = pygame.mouse.get_pos()
        x = rel_coord(x) * WIDTH / 7

        pygame.draw.rect(window, HIGHLIGHT_COLOUR, (x, 0, WIDTH / 7, HEIGHT))

    # Drawing counters
    mat1, mat2 = state.matrix_rep()

    for column, row in state:

        if mat1[row, column] == 1:
            draw_circle(column, row, PLAYER_COLOUR)

        elif mat2[row, column] == 1:
            draw_circle(column, row, AI_COLOUR)

        else:
            draw_circle(column, row, BACKGROUND_COLOUR)

    # Draw line through winnning counters if someone has won and insert a restart button
    if state.checkwin():
        orientation, (column, row) = state.checkwin_move()

        if orientation == "ROW":
            endpoints = grid_coord(column, row), grid_coord(column + 3, row)

        if orientation == "COLUMN":
            endpoints = grid_coord(column, row + 3), grid_coord(column, row)

        if orientation == "LEFTDIAG":
            endpoints = grid_coord(column, row), grid_coord(column + 3, row + 3)

        if orientation == "RIGHTDIAG":
            endpoints = grid_coord(column, row - 1), grid_coord(column + 3, row - 4)

        pygame.draw.line(window, BACKGROUND_COLOUR, *endpoints, 8)

        # Restart Button
        pygame.font.init()

        restart_font = pygame.font.SysFont("Arial", 25)
        pos = pygame.mouse.get_pos()

        if isin(pos, RESTARTBUTTON):

            pygame.draw.rect(window, RESTARTBUTTON_COLOUR, RESTARTBUTTON, 2)

            restart_surface = restart_font.render(
                "RESTART", False, RESTARTBUTTON_COLOUR, 35
            )
            window.blit(restart_surface, (RESTARTBUTTON[0] + 5, RESTARTBUTTON[1] + 5))
        else:
            pygame.draw.rect(window, TEXT_COLOUR, RESTARTBUTTON, 2)

            restart_surface = restart_font.render("RESTART", False, TEXT_COLOUR, 35)
            window.blit(restart_surface, (RESTARTBUTTON[0] + 5, RESTARTBUTTON[1] + 5))


def main():
    """
    Deals with the animation and updating of the Board parameters
    """
    # Draw pygame window
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect4")

    # Keeping the simulation running
    run = True
    clock = pygame.time.Clock()

    my_board = board.Board()

    while run:

        # Limiting the frame rate to 60fps
        clock.tick(60)

        draw(my_board, win)

        for event in pygame.event.get():

            # If the close button is pressed the Pygame window is stopped
            if event.type == pygame.QUIT:

                run = False

            # Handling mouse input
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not my_board.checkwin():

                    pos = pygame.mouse.get_pos()
                    move = int(rel_coord(pos[0]))

                    if move in my_board.legalmoves():

                        # Update the Board with the move
                        my_board += move

                        # Try updating the Board with the AI move as long as the game isn't won
                        if not my_board.checkwin():
                            move = my_board.engine_move()
                            start = time.time()
                            move = my_board.engine_move()

                            if move in my_board.legalmoves():
                                my_board += move
                            else:
                                my_board += np.random.choice(my_board.legalmoves())

                else:

                    # Handling mouse input when the game is over
                    pos = pygame.mouse.get_pos()

                    if isin(pos, RESTARTBUTTON):
                        my_board = board.Board()

        # Refreshing the window
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

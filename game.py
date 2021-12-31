import sys
import pygame as pg
import logic
from view import View


class Game:
    """Main Pygame class to manage game loop and store important
    attributes."""

    def __init__(self):
        pg.init()

        # Class object to manage everything that is shown on the screen.
        self.view = View()

        # Grid representing the game board of 2048.
        self.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        # Temporary grid to check for changes in the game board.
        self.temp_grid = None

        self.score = 0
        self.high_score = logic.read_score()

        # phase is used to determine what to display on screen and
        # won-flag is used to only show win screen once.
        self.phase = "play"
        self.won = False

        # Create two starting numbers.
        logic.new_number(self.grid)
        logic.new_number(self.grid)

    def run(self):
        """Check for events and display current game state."""
        while True:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()

                # In this phase it is possible to play the game or start a
                # new game.
                if self.phase == "play":

                    if event.type == pg.KEYDOWN:

                        if event.key == pg.K_LEFT or event.key == pg.K_a:
                            logic.move_board(self, "left")
                            logic.check_win(self)
                            logic.check_game_over(self)

                        elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                            logic.move_board(self, "right")
                            logic.check_win(self)
                            logic.check_game_over(self)

                        elif event.key == pg.K_UP or event.key == pg.K_w:
                            logic.move_board(self, "up")
                            logic.check_win(self)
                            logic.check_game_over(self)

                        elif event.key == pg.K_DOWN or event.key == pg.K_s:
                            logic.move_board(self, "down")
                            logic.check_win(self)
                            logic.check_game_over(self)

                    elif event.type == pg.MOUSEBUTTONDOWN:

                        if event.button == 1:
                            if logic.button_hovered(View.NEW_GAME_BTN):
                                logic.new_game(self)

                    logic.update_high_score(self)

                    self.view.show_game(self)

                # In this phase the game over-screen will be shown and the only
                # possible move is to click try again-button.
                elif self.phase == "game_over":

                    self.view.show_game(self)

                    self.view.show_game_over_screen()

                    if event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if logic.button_hovered(View.GAME_OVER_BTN):
                                logic.new_game(self)

                # In this phase the win-screen will be shown, and you can
                # either click on keep going- or try again-button.
                elif self.phase == "win":

                    self.view.show_game(self)

                    self.view.show_win_screen()

                    if event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if logic.button_hovered(View.WIN_KEEP_BTN):
                                self.phase = "play"

                    if event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if logic.button_hovered(View.WIN_AGAIN_BTN):
                                logic.new_game(self)

            pg.display.flip()


if __name__ == "__main__":
    gm = Game()
    gm.run()

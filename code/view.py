import pygame as pg
import os
import logic


class View:
    """Class to manage everything that is shown on screen."""

    WHITE = (255, 255, 255)
    WINDOW_SIZE = (500, 579)
    FONT_SIZE = 30
    NEW_GAME_BTN = ((395, 495), (5, 75))
    GAME_OVER_BTN = ((195, 305), (313, 350))
    WIN_KEEP_BTN = ((108, 220), (283, 325))
    WIN_AGAIN_BTN = ((280, 392), (283, 325))

    def __init__(self):
        self.screen = pg.display.set_mode(View.WINDOW_SIZE)
        pg.display.set_caption("2048 by JW30")

        pg.font.init()
        self.font = pg.font.SysFont("Arial Black", View.FONT_SIZE)

        self._load_images()
        self._load_translator()

    def _load_images(self):
        self.bg = pg.image.load(os.path.join("..", "images", "bg.png"))
        self.top = pg.image.load(os.path.join("..", "images", "top_menu.png"))
        self.top2 = pg.image.load(os.path.join("..", "images", "top_menu2.png"))
        self.go = pg.image.load(os.path.join("..", "images", "game_over.png"))
        self.go2 = pg.image.load(os.path.join("..", "images", "game_over2.png"))
        self.win = pg.image.load(os.path.join("..", "images", "win.png"))
        self.win2 = pg.image.load(os.path.join("..", "images", "win2.png"))
        self.win3 = pg.image.load(os.path.join("..", "images", "win3.png"))
        self.n2 = pg.image.load(os.path.join("..", "images", "2.png"))
        self.n4 = pg.image.load(os.path.join("..", "images", "4.png"))
        self.n8 = pg.image.load(os.path.join("..", "images", "8.png"))
        self.n16 = pg.image.load(os.path.join("..", "images", "16.png"))
        self.n32 = pg.image.load(os.path.join("..", "images", "32.png"))
        self.n64 = pg.image.load(os.path.join("..", "images", "64.png"))
        self.n128 = pg.image.load(os.path.join("..", "images", "128.png"))
        self.n256 = pg.image.load(os.path.join("..", "images", "256.png"))
        self.n512 = pg.image.load(os.path.join("..", "images", "512.png"))
        self.n1024 = pg.image.load(os.path.join("..", "images", "1024.png"))
        self.n2048 = pg.image.load(os.path.join("..", "images", "2048.png"))
        self.n4096 = pg.image.load(os.path.join("..", "images", "4096.png"))
        self.n8192 = pg.image.load(os.path.join("..", "images", "8192.png"))
        self.n16384 = pg.image.load(os.path.join("..", "images", "16384.png"))
        self.n32768 = pg.image.load(os.path.join("..", "images", "32768.png"))
        self.n65536 = pg.image.load(os.path.join("..", "images", "65536.png"))
        self.n131072 = pg.image.load(os.path.join("..", "images", "131072.png"))

    def _load_translator(self):
        """Translate numbers to Pygame image objects. Used to show game
        grid on screen."""
        self.translator = {
            2: self.n2,
            4: self.n4,
            8: self.n8,
            16: self.n16,
            32: self.n32,
            64: self.n64,
            128: self.n128,
            256: self.n256,
            512: self.n512,
            1024: self.n1024,
            2048: self.n2048,
            4096: self.n4096,
            8192: self.n8192,
            16384: self.n16384,
            32768: self.n32768,
            65536: self.n65536,
            131072: self.n131072
        }

    def _show_background(self):
        self.screen.blit(self.bg, (0, 80))

    def _show_top_menu(self, phase):
        """Show top menu with hover effect if game phase is "play"
        else without."""
        if phase == "play":
            if logic.button_hovered(View.NEW_GAME_BTN):
                self._show_cursor_hand()
                self.screen.blit(self.top2, (0, 0))
            else:
                self._show_cursor_arrow()
                self.screen.blit(self.top, (0, 0))
        else:
            self.screen.blit(self.top, (0, 0))

    def _show_score(self, score, which):
        # Param which is used to differentiate between normal score
        # (which == 0) and high score (which == 1).
        offset_x = 5 if which == 0 else 200
        score_str = logic.shorten(score)
        score_surface = self.font.render(score_str, False, View.WHITE)
        score_x = 190 / 2 - score_surface.get_rect().width / 2 + offset_x
        self.screen.blit(score_surface, (score_x, 25))

    def _show_tiles(self, grid):
        """Display the current game board."""
        for i, row in enumerate(grid):
            for j, num in enumerate(grid[i]):
                if num:
                    self.screen.blit(
                        self.translator[num],
                        (((j+1) * 15 + j * 106), ((i+1) * 15 + i * 106) + 80))

    @staticmethod
    def _show_cursor_hand():
        pg.mouse.set_cursor(pg.cursors.Cursor(pg.SYSTEM_CURSOR_HAND))

    @staticmethod
    def _show_cursor_arrow():
        pg.mouse.set_cursor(pg.cursors.Cursor(pg.SYSTEM_CURSOR_ARROW))

    def show_game(self, game):
        """Group show-methods of basic game elements."""
        self._show_background()
        self._show_top_menu(game.phase)
        self._show_score(game.score, 0)
        self._show_score(game.high_score, 1)
        self._show_tiles(game.grid)

    def show_game_over_screen(self):
        """Show game over-overlay with try again button hover effect."""
        if logic.button_hovered(View.GAME_OVER_BTN):
            self._show_cursor_hand()
            self.screen.blit(self.go2, (0, 0))
        else:
            self._show_cursor_arrow()
            self.screen.blit(self.go, (0, 0))

    def show_win_screen(self):
        """Show win screen-overlay with buttons and hover effects."""
        if logic.button_hovered(View.WIN_KEEP_BTN):
            self._show_cursor_hand()
            self.screen.blit(self.win2, (0, 0))
        elif logic.button_hovered(View.WIN_AGAIN_BTN):
            self._show_cursor_hand()
            self.screen.blit(self.win3, (0, 0))
        else:
            self._show_cursor_arrow()
            self.screen.blit(self.win, (0, 0))

import sys
import pygame

from settings import Settings
from chessboard import ChessBoard


class ChessKingdom:
    """A class dedicated to managing the resources and the way the game works."""


    def __init__(self):
        """Initializing the game and creating its resources."""
        pygame.init()
        self.settings = Settings()
        self.chessboard = ChessBoard()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Chess Kingdom")

        self.display_mode = "board"
        self.random_mode = False
        self.randomize_pieces = False
        self.custom_mode = False
        self.input_black = ""
        self.input_white = ""
        self.active_input = None

    def run_game(self):
        """Starting the main loop of the program."""
        self.randomized = False
        self.random_board = None

        self._draw_menu()
        self.screen.fill(self.settings.bg_color)
        self.chessboard.draw_board(self.screen)
        self._draw_menu()
        self._update_screen()
        while True:
            self._check_events()
            self.screen.fill(self.settings.bg_color)
            if self.display_mode == "board":
                self.chessboard.draw_board(self.screen)
                self.randomized = False
                self.random_board = None
            elif self.random_mode:
                try:
                    black = int(self.input_black) if self.input_black else 2
                    white = int(self.input_white) if self.input_white else 2
                except ValueError:
                    black, white = 3, 4
                black = min(black, 16)
                white = min(white, 16)
                if not self.randomized:
                    self.random_board = pygame.Surface(self.screen.get_size())
                    self.chessboard.random_piece_arrangement(self.random_board, black, white)
                    self.randomized = True
                self.screen.blit(self.random_board, (0, 0))
            elif self.custom_mode:
                self.chessboard.draw_board(self.screen)
                self.randomized = False
                self.random_board = None
            self._draw_menu()
            self._update_screen()

    def _draw_menu(self):
        """Draws the menu on the screen."""
        font = pygame.font.Font(None, 36)
        text = font.render("Chess Kingdom", True, self.settings.white_color)
        text_rect = text.get_rect(center=(150, 50))
        self.screen.blit(text, text_rect)

        font = pygame.font.Font(None, 24)
        text = font.render("Select display mode:", True, self.settings.white_color)
        text_rect = text.get_rect(center=(150, 100))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, self.settings.white_color, (50, 150, 200, 50))
        text = font.render("Random piece arrangement", True, self.settings.black_color)
        text_rect = text.get_rect(center=(150, 175))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255,255,255), (50, 210, 90, 40), 2 if self.active_input == "black" else 1)
        pygame.draw.rect(self.screen, (255,255,255), (160, 210, 90, 40), 2 if self.active_input == "white" else 1)
        font_small = pygame.font.Font(None, 28)
        black_text = font_small.render(self.input_black or "Black", True, (0,0,0))
        white_text = font_small.render(self.input_white or "White", True, (0,0,0))
        self.screen.blit(black_text, (55, 220))
        self.screen.blit(white_text, (165, 220))

        font_limit = pygame.font.Font(None, 22)
        limit_text = font_limit.render("Max: 16 black, 16 white pieces", True, (255, 255, 0))
        self.screen.blit(limit_text, (50, 255))

        pygame.draw.rect(self.screen, self.settings.white_color, (50, 300, 200, 50))
        text = font.render("Custom piece arrangement", True, self.settings.black_color)
        text_rect = text.get_rect(center=(150, 325))
        self.screen.blit(text, text_rect)

        if self.display_mode != "board":
            pygame.draw.rect(self.screen, self.settings.white_color, (50, 310, 200, 40))
            font = pygame.font.Font(None, 28)
            text = font.render("Back to menu", True, self.settings.black_color)
            text_rect = text.get_rect(center=(150, 330))
            self.screen.blit(text, text_rect)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 50 < event.pos[0] < 140 and 210 < event.pos[1] < 250:
                    self.active_input = "black"
                elif 160 < event.pos[0] < 250 and 210 < event.pos[1] < 250:
                    self.active_input = "white"
                elif 50 < event.pos[0] < 250 and 150 < event.pos[1] < 200:
                    self.random_mode = True
                    self.custom_mode = False
                    self.display_mode = "random"
                elif 50 < event.pos[0] < 250 and 250 < event.pos[1] < 300:
                    self.random_mode = False
                    self.custom_mode = True
                    self.display_mode = "custom"
                elif 50 < event.pos[0] < 250 and 310 < event.pos[1] < 350:
                    self.display_mode = "board"
                    self.random_mode = False
                    self.custom_mode = False
                    self.active_input = None
                else:
                    self.active_input = None
            elif event.type == pygame.KEYDOWN and self.active_input:
                if event.key == pygame.K_BACKSPACE:
                    if self.active_input == "black":
                        self.input_black = self.input_black[:-1]
                    else:
                        self.input_white = self.input_white[:-1]
                elif event.unicode.isdigit() and len(event.unicode) == 1:
                    if self.active_input == "black":
                        self.input_black += event.unicode
                    else:
                        self.input_white += event.unicode


    def _update_screen(self):
        """Updates the images on the screen and goes to a new screen."""
        # Waiting for a key or mouse button to be pressed.
        pygame.display.flip()

if __name__ == '__main__':
    # Creation of a copy of the game and its launch.
    ai = ChessKingdom()
    ai.run_game()
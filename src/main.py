import sys
import threading
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
        self.custom_board = None
        self.custom_mode = False
        self.input_black = ""
        self.input_white = ""
        self.active_input = None
        self.input_error = ""

    def run_game(self):
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
            self.input_error = ""  # Resetuj błąd na początku każdej pętli

            if self.display_mode == "board":
                self.chessboard.draw_board(self.screen)
                self.randomized = False
                self.random_board = None
                self.custom_board = None
            elif self.random_mode:
                try:
                    black = int(self.input_black) if self.input_black else 2
                    white = int(self.input_white) if self.input_white else 2
                except ValueError:
                    black, white = 3, 4

                if black > 16 or white > 16:
                    self.input_error = "Max 16 pieces for each color! Please enter again."
                    self.randomized = False
                    self.random_board = None
                else:
                    if not self.randomized:
                        self.random_board = pygame.Surface(self.screen.get_size())
                        self.chessboard.random_piece_arrangement(self.random_board, black, white)
                        self.randomized = True
                    self.screen.blit(self.random_board, (0, 0))
            elif self.custom_mode:
                if self.custom_board:
                    self.screen.blit(self.custom_board, (0, 0))
                else:
                    self.chessboard.draw_board(self.screen)
                self.randomized = False
                self.random_board = None
            self._draw_menu()
            self._update_screen()

    def _draw_menu(self):
        """Draws the menu on the screen."""
        font = pygame.font.Font(None, 36)
        text = font.render("Chess Kingdom", True, self.settings.white_color)
        text_rect = text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height - 600))
        self.screen.blit(text, text_rect)

        font = pygame.font.Font(None, 24)
        text = font.render("Select display mode:", True, self.settings.white_color)
        text_rect = text.get_rect(center=(150, 100))
        self.screen.blit(text, text_rect)

        random_button = pygame.Rect(50, 150, 250, 50)
        self.draw_button(
            self.screen,
            random_button,
            "Random piece arrangement",
            font,
            bg_color=(220, 220, 220),
            text_color=(30, 30, 30),
            border_color=(100, 100, 100),
            shadow_color=(180, 180, 180)
        )

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

        if self.input_error:
            font_error = pygame.font.Font(None, 26)
            error_text = font_error.render(self.input_error, True, (255, 0, 0))
            self.screen.blit(error_text, (50, 270))

        custom_button = pygame.Rect(50, 300, 250, 50)
        self.draw_button(
            self.screen,
            custom_button,
            "Custom piece arrangement",
            font,
            bg_color=(220, 220, 220),
            text_color=(30, 30, 30),
            border_color=(100, 100, 100),
            shadow_color=(180, 180, 180)
        )

        if self.display_mode != "board":
            back_button = pygame.Rect(50, 500, 250, 50)
            self.draw_button(
                self.screen,
                back_button,
                "Back to menu",
                font,
                bg_color=(220, 220, 220),
                text_color=(30, 30, 30),
                border_color=(100, 100, 100),
                shadow_color=(180, 180, 180)
            )


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
                elif 50 < event.pos[0] < 250 and 300 < event.pos[1] < 350:
                    threading.Thread(target=self._load_custom_position_thread).start()
                    self.display_mode = "custom"
                    self.custom_mode = True
                    self.randomized = False
                    self.random_board = None
                elif 50 < event.pos[0] < 300 and 500 < event.pos[1] < 550:
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


    def draw_button(self, surface, rect, text, font, bg_color, text_color, border_color, shadow_color):
        # Shadow
        shadow_rect = pygame.Rect(rect.x + 4, rect.y + 4, rect.width, rect.height)
        pygame.draw.rect(surface, shadow_color, shadow_rect, border_radius=12)
        # Background
        pygame.draw.rect(surface, bg_color, rect, border_radius=12)
        # Border
        pygame.draw.rect(surface, border_color, rect, width=2, border_radius=12)
        # Text
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)


    def _load_custom_position_thread(self):
        board_surface = self.chessboard.load_custom_position()
        if board_surface:
            self.custom_board = board_surface
        else:
            self.custom_board = None


    def _update_screen(self):
        """Updates the images on the screen and goes to a new screen."""
        # Waiting for a key or mouse button to be pressed.
        pygame.display.flip()

if __name__ == '__main__':
    # Creation of a copy of the game and its launch.
    ai = ChessKingdom()
    ai.run_game()

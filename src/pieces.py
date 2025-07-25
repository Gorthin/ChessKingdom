import pygame
from settings import Settings

class Piece():
    def __init__(self):
        self.settings = Settings()
        self.pieces = {
            "white_pawn":   "♙",
            "white_knight": "♘",
            "white_bishop": "♗",
            "white_rook":   "♖",
            "white_king":   "♔",
            "white_queen":  "♕",
            "black_pawn":   "♟",
            "black_knight": "♞",
            "black_bishop": "♝",
            "black_rook":   "♜",
            "black_king":   "♚",
            "black_queen":  "♛"
        }
        self.offset_x = self.settings.screen_width // 2 - 50
        self.offset_y = self.settings.screen_height // 4 - 50


    def draw_piece(
        self,
        screen: pygame.Surface,
        piece_name: str,
        row: int,
        col: int
    ) -> None:
        # Downloading font
        font = pygame.font.Font("Arial Unicode MS.TTF", 40)

        # Text rendering
        text = font.render(self.pieces[piece_name], True, (0, 0, 0))

        # Calculating text position
        text_rect = text.get_rect(center=(col * 50 + 25 + self.offset_x, row * 50 + 25 + self.offset_y))

        # Drawing text on the screen
        screen.blit(text, text_rect)

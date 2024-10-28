import random
import pygame

from settings import Settings
from pieces import Piece

class ChessBoard():
    """A class dedicated to managing the resources and drawing chess board."""


    def __init__(self):
        """Initializing the resources."""
        self.settings = Settings()
        self.pieces = Piece()
        self.offset_x = self.settings.screen_width // 2 - 50
        self.offset_y = self.settings.screen_height // 4 - 50
        self.font = pygame.font.Font(None, 24)


    def draw_square(self, screen, col, row, color):
        """Draws a square on the chessboard."""
        pygame.draw.rect(screen, color, (self.offset_x + col * self.settings.square_size,
                                           self.offset_y + row * self.settings.square_size,
                                           self.settings.square_size,
                                           self.settings.square_size))



    def draw_board(self, screen):
        """Draws the chessboard."""
        piece_positions = {
            "black": {
                "rook": [(0, 0), (0, 7)],
                "knight": [(0, 1), (0, 6)],
                "bishop": [(0, 2), (0, 5)],
                "queen": [(0, 3)],
                "king": [(0, 4)],
                "pawn": [(1, col) for col in range(8)],
            },
            "white": {
                "rook": [(7, 0), (7, 7)],
                "knight": [(7, 1), (7, 6)],
                "bishop": [(7, 2), (7, 5)],
                "queen": [(7, 3)],
                "king": [(7, 4)],
                "pawn": [(6, col) for col in range(8)],
            }
        }
        
        for row in range(8):
            for col in range(8):
                color = self.settings.white_color if (row + col) % 2 == 0 else self.settings.black_color
                self.draw_square(screen, col, row, color)

                for color_name, pieces in piece_positions.items():
                    for piece, positions in pieces.items():
                        if (row, col) in positions:
                            self.pieces.draw_piece(screen, f"{color_name}_{piece}", row, col)

        """Drawing description on all sides"""
        for i in range(8):
            # Row numbers
            text = self.font.render(str(8 - i), True, self.settings.white_color)
            for x in [self.offset_x - self.settings.square_size // 2,
                      self.offset_x + 8 * self.settings.square_size + self.settings.square_size // 2]:
                text_rect = text.get_rect(center=(x, self.offset_y + i * self.settings.square_size + self.settings.square_size // 2))
                screen.blit(text, text_rect)

            # Column letters
            text = self.font.render(chr(ord('A') + i), True, self.settings.white_color)
            for y in [self.offset_y - self.settings.square_size // 2,
                      self.offset_y + 8 * self.settings.square_size + self.settings.square_size // 2]:
                text_rect = text.get_rect(center=(self.offset_x + (i + 1) * self.settings.square_size - self.settings.square_size // 2, y))
                screen.blit(text, text_rect)
            screen.blit(text, text_rect)

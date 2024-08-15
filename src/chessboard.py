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


    def draw_white_square(self, screen, col, row):
        """Draws a white square on the chessboard."""
        pygame.draw.rect(screen, self.settings.white_color, (self.offset_x + col * self.settings.square_size,
                                                                self.offset_y + row * self.settings.square_size,
                                                               self.settings.square_size,
                                                               self.settings.square_size))


    def draw_black_square(self, screen, col, row):
        """Draws a black square on the chessboard."""
        pygame.draw.rect(screen, self.settings.black_color, (self.offset_x + col * self.settings.square_size,
                                                               self.offset_y + row * self.settings.square_size,
                                                               self.settings.square_size,
                                                               self.settings.square_size))


    def draw_board(self, screen):
        """Draws the chessboard."""
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    self.draw_white_square(screen, col, row)
                else:
                    self.draw_black_square(screen, col, row)
                # Drawing pieces based on their initial position
                if row == 0 and col in [0, 7]:
                    self.pieces.draw_piece(screen, "black_rook", row, col)
                elif row == 0 and col in [1, 6]:
                    self.pieces.draw_piece(screen, "black_knight", row, col)
                elif row == 0 and col in [2, 5]:
                    self.pieces.draw_piece(screen, "black_bishop", row, col)
                elif row == 0 and col == 3:
                    self.pieces.draw_piece(screen, "black_queen", row, col)
                elif row == 0 and col == 4:
                    self.pieces.draw_piece(screen, "black_king", row, col)
                elif row == 1:
                    self.pieces.draw_piece(screen, "black_pawn", row, col)
                elif row == 7 and col in [0, 7]:
                    self.pieces.draw_piece(screen, "white_rook", row, col)
                elif row == 7 and col in [1, 6]:
                    self.pieces.draw_piece(screen, "white_knight", row, col)
                elif row == 7 and col in [2, 5]:
                    self.pieces.draw_piece(screen, "white_bishop", row, col)
                elif row == 7 and col == 3:
                    self.pieces.draw_piece(screen, "white_queen", row, col)
                elif row == 7 and col == 4:
                    self.pieces.draw_piece(screen, "white_king", row, col)
                elif row == 6:
                    self.pieces.draw_piece(screen, "white_pawn", row, col)

        """Drawing description on all sides"""
        for i in range(8):
            # Row numbers – left side
            text = self.font.render(str(8 - i), True, self.settings.white_color)
            text_rect = text.get_rect(center=(self.offset_x - self.settings.square_size // 2,
                                              self.offset_y + i * self.settings.square_size + self.settings.square_size // 2))
            screen.blit(text, text_rect)

            # Row numbers - right side
            text = self.font.render(str(8 - i), True, self.settings.white_color)
            text_rect = text.get_rect(center=(self.offset_x + 8 * self.settings.square_size + self.settings.square_size // 2,
                                              self.offset_y + i * self.settings.square_size + self.settings.square_size // 2))
            screen.blit(text, text_rect)

            # Column letters - top side
            text = self.font.render(chr(ord('A') + i), True, self.settings.white_color)
            text_rect = text.get_rect(center=(self.offset_x + (i + 1) * self.settings.square_size - self.settings.square_size // 2,
                                              self.offset_y - self.settings.square_size // 2))
            screen.blit(text, text_rect)

            # Column letters - bottom side
            text = self.font.render(chr(ord('A') + i), True, self.settings.white_color)
            text_rect = text.get_rect(center=(self.offset_x + (i + 1) * self.settings.square_size - self.settings.square_size // 2,
                                              self.offset_y + 8 * self.settings.square_size + self.settings.square_size // 2))
            screen.blit(text, text_rect)

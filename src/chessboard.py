import random
import sys
import pygame
import tkinter as tk
from tkinter import filedialog

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

        self.draw_board_descriptions(screen)


    def draw_board_descriptions(self, screen):
        """Draws row numbers and column letters around the chessboard."""
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


    def random_piece_arrangement(self, screen, num_black_pieces, num_white_pieces):
        """Displays a random arrangement of specified number of black and white pieces on the chessboard."""
        # Draw an empty board
        for row in range(8):
            for col in range(8):
                color = self.settings.white_color if (row + col) % 2 == 0 else self.settings.black_color
                self.draw_square(screen, col, row, color)

        all_positions = [(r, c) for r in range(8) for c in range(8)]
        random.shuffle(all_positions)

        # Piece type limits
        piece_types = [
            ("king", 1),
            ("queen", 1),
            ("rook", 2),
            ("bishop", 2),
            ("knight", 2),
            ("pawn", 8)
        ]

        # --- BLACK PIECES ---
        black_pool = []
        for piece, limit in piece_types:
            black_pool += [piece] * limit
        random.shuffle(black_pool)
        black_pool = black_pool[:min(num_black_pieces, len(black_pool))]

        for piece in black_pool:
            pos = all_positions.pop()
            self.pieces.draw_piece(screen, f"black_{piece}", pos[0], pos[1])

        # --- WHITE PIECES ---
        white_pool = []
        for piece, limit in piece_types:
            white_pool += [piece] * limit
        random.shuffle(white_pool)
        white_pool = white_pool[:min(num_white_pieces, len(white_pool))]

        for piece in white_pool:
            pos = all_positions.pop()
            self.pieces.draw_piece(screen, f"white_{piece}", pos[0], pos[1])

        self.draw_board_descriptions(screen)


    def load_custom_position(self) -> 'pygame.Surface | None':
        """
        Loads piece positions from a .txt file and returns a Surface with the custom board drawn.
        Supports chess notation, e.g. white_pawn C6, black_queen F3.
        Returns the Surface if loaded successfully, None otherwise.
        """
        pygame.event.clear()

        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Select position file",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        root.destroy()

        if not file_path:
            return None

        board_surface = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        board_surface.fill(self.settings.bg_color)

        # Draw empty board
        for row in range(8):
            for col in range(8):
                color = self.settings.white_color if (row + col) % 2 == 0 else self.settings.black_color
                self.draw_square(board_surface, col, row, color)

        # Helper to convert chess notation to (row, col)
        def chess_notation_to_coords(pos):
            if len(pos) != 2:
                return None
            col_letter = pos[0].upper()
            row_digit = pos[1]
            if col_letter < 'A' or col_letter > 'H' or row_digit < '1' or row_digit > '8':
                return None
            col = ord(col_letter) - ord('A')
            row = 8 - int(row_digit)
            return row, col

        try:
            with open(file_path, "r") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        piece_name, pos = parts
                        coords = chess_notation_to_coords(pos)
                        if coords and piece_name in self.pieces.pieces:
                            self.pieces.draw_piece(board_surface, piece_name, coords[0], coords[1])
            self.draw_board_descriptions(board_surface)
            return board_surface
        except Exception as e:
            print(f"Error loading file: {e}")
            return None

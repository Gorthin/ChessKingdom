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


    def draw_piece(self, screen, piece_name, row, col):
            # Pobieranie czcionki
            font = pygame.font.Font("Arial Unicode MS.ttf", 50)

            # Renderowanie tekstu
            text = font.render(self.pieces[piece_name], True, (0, 0, 0))

            # Obliczanie pozycji tekstu
            text_rect = text.get_rect(center=(col * 50 + 25 + self.offset_x, row * 50 + 25 + self.offset_y))

            # Rysowanie tekstu na ekranie
            screen.blit(text, text_rect)
import pygame
import os

# Load piece images
def load_images():
    pieces = {}
    piece_types = ["p", "r", "n", "b", "q", "k"]
    colors = ["w", "b"]
    
    for color in colors:
        for piece_type in piece_types:
            # Try to load from res/chess_piece folder
            image_path = os.path.join("res", "chess_piece", f"{color}{piece_type}.png")
            if os.path.exists(image_path):
                try:
                    image = pygame.image.load(image_path)
                    pieces[f"{color}{piece_type}"] = image
                except pygame.error:
                    pieces[f"{color}{piece_type}"] = None
            else:
                pieces[f"{color}{piece_type}"] = None
    
    return pieces

# Global piece images dictionary
PIECE_IMAGES = None

class Piece:
    """Base class for all chess pieces"""
    def __init__(self, color, row, col):
        self.color = color  # "white" or "black"
        self.row = row
        self.col = col
        self.has_moved = False
        self.piece_type = "piece"  # Will be overridden by subclasses
    
    def draw(self, screen, x, y, square_size):
        """Draw the piece on the screen"""
        global PIECE_IMAGES
        
        # Initialize images if not already done
        if PIECE_IMAGES is None:
            PIECE_IMAGES = load_images()
        
        # Convert the color to single letter code
        color_code = "w" if self.color == "white" else "b"
        # Convert the piece type to single letter code
        piece_codes = {"pawn": "p", "rook": "r", "knight": "n", "bishop": "b", "queen": "q", "king": "k"}
        piece_code = piece_codes.get(self.piece_type, "p")
        
        image_key = f"{color_code}{piece_code}"
        image = PIECE_IMAGES.get(image_key)
        
        if image:
            # Resize image to fit the square
            resized_image = pygame.transform.scale(image, (square_size - 10, square_size - 10))
            screen.blit(resized_image, (x + 5, y + 5))
        else:
            # Fallback to drawing a circle with a letter
            color = (255, 255, 255) if self.color == "white" else (0, 0, 0)
            border_color = (0, 0, 0) if self.color == "white" else (255, 255, 255)
            
            # Draw piece circle
            pygame.draw.circle(screen, color, (x + square_size // 2, y + square_size // 2), 
                              square_size // 2 - 10)
            pygame.draw.circle(screen, border_color, (x + square_size // 2, y + square_size // 2), 
                              square_size // 2 - 10, 2)
            
            # Draw piece letter
            font = pygame.font.SysFont("Arial", 20, bold=True)
            text = font.render(self.piece_type[0].upper(), True, border_color)
            text_rect = text.get_rect(center=(x + square_size // 2, y + square_size // 2))
            screen.blit(text, text_rect)
    
    def get_possible_moves(self, board, check_king_safety=True):
        """Get all possible moves for this piece"""
        # To be implemented by subclasses
        return []

class Pawn(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.piece_type = "pawn"
    
    def get_possible_moves(self, board, check_king_safety=True):
        moves = []
        direction = -1 if self.color == "white" else 1  # White moves up, black moves down
        
        # Forward move
        new_row = self.row + direction
        if board.is_valid_position(new_row, self.col) and board.get_piece(new_row, self.col) is None:
            moves.append((new_row, self.col))
            
            # Double move from starting position
            if not self.has_moved:
                new_row = self.row + 2 * direction
                if board.is_valid_position(new_row, self.col) and board.get_piece(new_row, self.col) is None:
                    moves.append((new_row, self.col))
        
        # Capture diagonally
        for col_offset in [-1, 1]:
            new_col = self.col + col_offset
            new_row = self.row + direction
            
            if board.is_valid_position(new_row, new_col):
                piece = board.get_piece(new_row, new_col)
                if piece and piece.color != self.color:
                    moves.append((new_row, new_col))
        
        # En passant
        if board.en_passant_target:
            target_row, target_col = board.en_passant_target
            # Check if the en passant target is diagonally adjacent to this pawn
            if abs(target_col - self.col) == 1 and self.row == target_row:
                # Make sure the pawn is on the correct rank for en passant
                correct_rank = 3 if self.color == "white" else 4
                if self.row == correct_rank:
                    # En passant capture square (diagonal to the target pawn)
                    capture_row = self.row + direction
                    capture_col = target_col
                    moves.append((capture_row, capture_col))
                
        return moves

class Rook(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.piece_type = "rook"
    
    def get_possible_moves(self, board, check_king_safety=True):
        moves = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, down, left, up
        
        for dr, dc in directions:
            for i in range(1, 8):  # Maximum 7 squares in any direction
                new_row, new_col = self.row + i * dr, self.col + i * dc
                
                if not board.is_valid_position(new_row, new_col):
                    break
                
                piece = board.get_piece(new_row, new_col)
                if piece is None:
                    moves.append((new_row, new_col))
                elif piece.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves

class Knight(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.piece_type = "knight"
    
    def get_possible_moves(self, board, check_king_safety=True):
        moves = []
        # All possible L-shaped moves
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dr, dc in knight_moves:
            new_row, new_col = self.row + dr, self.col + dc
            
            if board.is_valid_position(new_row, new_col):
                piece = board.get_piece(new_row, new_col)
                if piece is None or piece.color != self.color:
                    moves.append((new_row, new_col))
        
        return moves

class Bishop(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.piece_type = "bishop"
    
    def get_possible_moves(self, board, check_king_safety=True):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Diagonals
        
        for dr, dc in directions:
            for i in range(1, 8):  # Maximum 7 squares in any direction
                new_row, new_col = self.row + i * dr, self.col + i * dc
                
                if not board.is_valid_position(new_row, new_col):
                    break
                
                piece = board.get_piece(new_row, new_col)
                if piece is None:
                    moves.append((new_row, new_col))
                elif piece.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves

class Queen(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.piece_type = "queen"
    
    def get_possible_moves(self, board, check_king_safety=True):
        moves = []
        # Queen can move like a rook and a bishop combined
        directions = [
            (0, 1), (1, 0), (0, -1), (-1, 0),  # Horizontal and vertical
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonals
        ]
        
        for dr, dc in directions:
            for i in range(1, 8):  # Maximum 7 squares in any direction
                new_row, new_col = self.row + i * dr, self.col + i * dc
                
                if not board.is_valid_position(new_row, new_col):
                    break
                
                piece = board.get_piece(new_row, new_col)
                if piece is None:
                    moves.append((new_row, new_col))
                elif piece.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves

class King(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.piece_type = "king"
    
    def get_possible_moves(self, board, check_king_safety=True):
        moves = []
        # King can move one square in any direction
        directions = [
            (0, 1), (1, 0), (0, -1), (-1, 0),  # Horizontal and vertical
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonals
        ]
        
        for dr, dc in directions:
            new_row, new_col = self.row + dr, self.col + dc
            
            if board.is_valid_position(new_row, new_col):
                piece = board.get_piece(new_row, new_col)
                if piece is None or piece.color != self.color:
                    moves.append((new_row, new_col))
        
        # Castling logic
        if not check_king_safety or not self.has_moved and not board.is_in_check(self.color):
            # Kingside castling
            if board.castling_rights[self.color]["kingside"]:
                if all(board.get_piece(self.row, c) is None for c in range(self.col + 1, 7)):
                    rook = board.get_piece(self.row, 7)
                    if rook and rook.piece_type == "rook" and not rook.has_moved:
                        # Check if squares in between are not under attack
                        if check_king_safety:
                            if not any(board.would_be_in_check_after_move(self.row, self.col, self.row, c, self.color) 
                                    for c in range(self.col + 1, self.col + 3)):
                                moves.append((self.row, self.col + 2))
                        else:
                            moves.append((self.row, self.col + 2))
            
            # Queenside castling
            if board.castling_rights[self.color]["queenside"]:
                if all(board.get_piece(self.row, c) is None for c in range(1, self.col)):
                    rook = board.get_piece(self.row, 0)
                    if rook and rook.piece_type == "rook" and not rook.has_moved:
                        # Check if squares in between are not under attack
                        if check_king_safety:
                            if not any(board.would_be_in_check_after_move(self.row, self.col, self.row, c, self.color) 
                                    for c in range(self.col - 1, self.col - 3, -1)):
                                moves.append((self.row, self.col - 2))
                        else:
                            moves.append((self.row, self.col - 2))
        
        return moves 
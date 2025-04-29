import pygame
from chess_pieces import Pawn, Rook, Knight, Bishop, Queen, King
from config import BOARD_SIZE, SQUARE_SIZE, BOARD_MARGIN, LIGHT_SQUARE, DARK_SQUARE, HIGHLIGHT_COLOR

class ChessBoard:
    def __init__(self):
        # Board dimensions
        self.rows = BOARD_SIZE
        self.cols = BOARD_SIZE
        self.square_size = SQUARE_SIZE
        self.board_margin = BOARD_MARGIN
        
        # Board colors
        self.light_square = LIGHT_SQUARE
        self.dark_square = DARK_SQUARE
        self.highlight_color = HIGHLIGHT_COLOR
        
        # Initialize board with pieces
        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.setup_pieces()
        
        # Game state tracking
        self.last_moved_piece = None
        self.white_king_pos = (7, 4)  # Initial position of white king
        self.black_king_pos = (0, 4)  # Initial position of black king
        self.castling_rights = {
            "white": {"kingside": True, "queenside": True},
            "black": {"kingside": True, "queenside": True}
        }
        
        # For tracking en passant
        self.en_passant_target = None
    
    def setup_pieces(self):
        """Set up the initial chess board with all pieces"""
        # Setup pawns
        for col in range(self.cols):
            self.board[1][col] = Pawn("black", 1, col)
            self.board[6][col] = Pawn("white", 6, col)
        
        # Setup rooks
        self.board[0][0] = Rook("black", 0, 0)
        self.board[0][7] = Rook("black", 0, 7)
        self.board[7][0] = Rook("white", 7, 0)
        self.board[7][7] = Rook("white", 7, 7)
        
        # Setup knights
        self.board[0][1] = Knight("black", 0, 1)
        self.board[0][6] = Knight("black", 0, 6)
        self.board[7][1] = Knight("white", 7, 1)
        self.board[7][6] = Knight("white", 7, 6)
        
        # Setup bishops
        self.board[0][2] = Bishop("black", 0, 2)
        self.board[0][5] = Bishop("black", 0, 5)
        self.board[7][2] = Bishop("white", 7, 2)
        self.board[7][5] = Bishop("white", 7, 5)
        
        # Setup queens
        self.board[0][3] = Queen("black", 0, 3)
        self.board[7][3] = Queen("white", 7, 3)
        
        # Setup kings
        self.board[0][4] = King("black", 0, 4)
        self.board[7][4] = King("white", 7, 4)
    
    def draw(self, screen):
        """Draw the chess board and its pieces"""
        # Draw the chess board squares
        for row in range(self.rows):
            for col in range(self.cols):
                color = self.light_square if (row + col) % 2 == 0 else self.dark_square
                x = col * self.square_size + self.board_margin
                y = row * self.square_size + self.board_margin
                pygame.draw.rect(screen, color, (x, y, self.square_size, self.square_size))
                
                # Draw coordinates
                if col == 0:  # Row numbers on the left
                    font = pygame.font.SysFont("Arial", 12)
                    text = font.render(str(8 - row), True, (0, 0, 0))
                    screen.blit(text, (self.board_margin - 15, y + self.square_size // 2 - 6))
                
                if row == 7:  # Column letters on the bottom
                    font = pygame.font.SysFont("Arial", 12)
                    text = font.render(chr(97 + col), True, (0, 0, 0))
                    screen.blit(text, (x + self.square_size // 2 - 4, 
                                      self.board_margin + 8 * self.square_size + 5))
                
                # Draw piece if there is one
                piece = self.board[row][col]
                if piece:
                    piece.draw(screen, x, y, self.square_size)
    
    def highlight_square(self, screen, row, col, color):
        """Highlight a square on the board"""
        x = col * self.square_size + self.board_margin
        y = row * self.square_size + self.board_margin
        
        highlight = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        highlight.fill(color)
        screen.blit(highlight, (x, y))
    
    def screen_to_board_pos(self, pos):
        """Convert screen coordinates to board position"""
        x, y = pos
        
        # Check if click is within board boundaries
        if (x < self.board_margin or x >= self.board_margin + self.square_size * 8 or
            y < self.board_margin or y >= self.board_margin + self.square_size * 8):
            return None
        
        # Calculate board position
        col = (x - self.board_margin) // self.square_size
        row = (y - self.board_margin) // self.square_size
        
        return row, col
    
    def get_piece(self, row, col):
        """Return the piece at the given position or None if empty"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.board[row][col]
        return None
    
    def is_valid_position(self, row, col):
        """Check if a position is valid on the board"""
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def get_valid_moves(self, row, col):
        """Get all valid moves for a piece at the given position"""
        piece = self.get_piece(row, col)
        if not piece:
            return []
        
        # Get all possible moves for this piece
        possible_moves = piece.get_possible_moves(self)
        
        # Filter out moves that would put or leave the king in check
        valid_moves = []
        for move_row, move_col in possible_moves:
            if not self.would_be_in_check_after_move(row, col, move_row, move_col, piece.color):
                valid_moves.append((move_row, move_col))
        
        return valid_moves
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        """Move a piece from one position to another"""
        piece = self.board[from_row][from_col]
        if not piece:
            return False
            
        # Reset en passant target
        self.en_passant_target = None
        
        # Update king position if king is moved
        if piece.piece_type == "king":
            if piece.color == "white":
                self.white_king_pos = (to_row, to_col)
            else:
                self.black_king_pos = (to_row, to_col)
            
            # Update castling rights
            self.castling_rights[piece.color]["kingside"] = False
            self.castling_rights[piece.color]["queenside"] = False
            
            # Handle castling move
            if abs(from_col - to_col) == 2:
                # Kingside castling
                if to_col > from_col:
                    rook = self.board[from_row][7]
                    self.board[from_row][5] = rook
                    self.board[from_row][7] = None
                    if rook:
                        rook.row, rook.col = from_row, 5
                # Queenside castling
                else:
                    rook = self.board[from_row][0]
                    self.board[from_row][3] = rook
                    self.board[from_row][0] = None
                    if rook:
                        rook.row, rook.col = from_row, 3
        
        # Update rook's castling rights
        if piece.piece_type == "rook":
            if piece.color == "white":
                if from_row == 7 and from_col == 0:  # Queenside rook
                    self.castling_rights["white"]["queenside"] = False
                elif from_row == 7 and from_col == 7:  # Kingside rook
                    self.castling_rights["white"]["kingside"] = False
            else:
                if from_row == 0 and from_col == 0:  # Queenside rook
                    self.castling_rights["black"]["queenside"] = False
                elif from_row == 0 and from_col == 7:  # Kingside rook
                    self.castling_rights["black"]["kingside"] = False
                    
        # Handle pawn special moves
        if piece.piece_type == "pawn":
            # Check for double move (for en passant)
            if abs(from_row - to_row) == 2:
                self.en_passant_target = (to_row, to_col)
                
            # Check for en passant capture
            if abs(from_col - to_col) == 1 and self.board[to_row][to_col] is None:
                # This must be an en passant capture since normal diagonal moves require a piece
                captured_pawn_row = from_row
                captured_pawn_col = to_col
                self.board[captured_pawn_row][captured_pawn_col] = None
        
            # Handle pawn promotion
            if to_row == 0 or to_row == 7:
                self.board[from_row][from_col] = None
                # Create a new Queen at the promoted position
                self.board[to_row][to_col] = Queen(piece.color, to_row, to_col)
                # Set last_moved_piece for checking
                self.last_moved_piece = self.board[to_row][to_col]
                return True
        
        # Regular move
        captured_piece = self.board[to_row][to_col]
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        
        # Update piece coordinates
        piece.row, piece.col = to_row, to_col
        piece.has_moved = True
        
        self.last_moved_piece = piece
        return True
    
    def is_in_check(self, color):
        """Check if the king of the given color is in check"""
        # Get king position
        king_pos = self.white_king_pos if color == "white" else self.black_king_pos
        king_row, king_col = king_pos
        
        # Check if any opponent piece can attack the king
        opponent_color = "black" if color == "white" else "white"
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.get_piece(row, col)
                if piece and piece.color == opponent_color:
                    moves = piece.get_possible_moves(self, check_king_safety=False)
                    if king_pos in moves:
                        return True
        
        return False
    
    def would_be_in_check_after_move(self, from_row, from_col, to_row, to_col, color):
        """Check if the king would be in check after a move"""
        # Save current board state
        piece = self.board[from_row][from_col]
        captured_piece = self.board[to_row][to_col]
        
        # Save king position
        orig_white_king_pos = self.white_king_pos
        orig_black_king_pos = self.black_king_pos
        
        # Update king position if king is moved
        if piece and piece.piece_type == "king":
            if piece.color == "white":
                self.white_king_pos = (to_row, to_col)
            else:
                self.black_king_pos = (to_row, to_col)
        
        # Temporarily make the move
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        
        # Check if king is in check
        in_check = self.is_in_check(color)
        
        # Restore board state
        self.board[from_row][from_col] = piece
        self.board[to_row][to_col] = captured_piece
        
        # Restore king position
        self.white_king_pos = orig_white_king_pos
        self.black_king_pos = orig_black_king_pos
        
        return in_check
    
    def is_checkmate(self, color):
        """Check if the player of the given color is in checkmate"""
        # First check if king is in check
        if not self.is_in_check(color):
            return False
        
        # See if any piece can make a move to get out of check
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.get_piece(row, col)
                if piece and piece.color == color:
                    valid_moves = self.get_valid_moves(row, col)
                    if valid_moves:
                        return False
        
        # No valid moves and king in check means checkmate
        return True
    
    def is_stalemate(self, color):
        """Check if the player of the given color is in stalemate"""
        # First check if king is in check
        if self.is_in_check(color):
            return False
        
        # See if any piece can make a move
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.get_piece(row, col)
                if piece and piece.color == color:
                    valid_moves = self.get_valid_moves(row, col)
                    if valid_moves:
                        return False
        
        # No valid moves and king not in check means stalemate
        return True 
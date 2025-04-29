import pygame
from chess_board import ChessBoard
from chess_pieces import Piece
from time_clock import TimeClock
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, DEFAULT_TIME_MINUTES

class ChessGame:
    def __init__(self):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Multiplayer Chess")
        
        # Load resources
        self.load_resources()
        
        # Create chess board
        self.board = ChessBoard()
        
        # Set up game state
        self.current_player = "white"
        self.selected_piece = None
        self.available_moves = []
        
        # Set up time clocks (10 minutes per player)
        self.time_clocks = {
            "white": TimeClock(DEFAULT_TIME_MINUTES * 60),
            "black": TimeClock(DEFAULT_TIME_MINUTES * 60)
        }
        
        # Start white's clock since they go first
        self.time_clocks["white"].start()
        self.clocks_active = True
        
        # Game state
        self.game_over = False
        self.winner = None
        
    def load_resources(self):
        """Load game resources like images and sounds"""
        # This will be implemented to load piece images and other assets
        pass
    
    def handle_event(self, event):
        """Handle pygame events"""
        if self.game_over:
            # Only handle restart or quit events if game is over
            return
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position
            pos = pygame.mouse.get_pos()
            
            # Convert screen position to board position
            board_pos = self.board.screen_to_board_pos(pos)
            
            if board_pos:
                row, col = board_pos
                
                # If a piece is already selected
                if self.selected_piece:
                    # Check if clicked position is in available moves
                    if (row, col) in self.available_moves:
                        # Move the piece
                        old_row, old_col = self.selected_piece
                        self.board.move_piece(old_row, old_col, row, col)
                        
                        # If this is the first move of the game
                        if not self.clocks_active:
                            self.clocks_active = True
                        else:
                            # Stop the current player's clock
                            self.time_clocks[self.current_player].stop()
                        
                        # Switch player turn
                        self.current_player = "black" if self.current_player == "white" else "white"
                        
                        # Start the new current player's clock
                        self.time_clocks[self.current_player].start()
                        
                        # Check for checkmate
                        if self.board.is_checkmate(self.current_player):
                            self.game_over = True
                            self.winner = "white" if self.current_player == "black" else "black"
                            # Stop all clocks when game is over
                            self.time_clocks["white"].stop()
                            self.time_clocks["black"].stop()
                            
                    # Reset selection
                    self.selected_piece = None
                    self.available_moves = []
                else:
                    # Check if there's a piece at the clicked position
                    piece = self.board.get_piece(row, col)
                    if piece and piece.color == self.current_player:
                        self.selected_piece = (row, col)
                        self.available_moves = self.board.get_valid_moves(row, col)
    
    def update(self):
        """Update game state"""
        if self.clocks_active and not self.game_over:
            # Only update active clocks (only one should be active at a time)
            for player, clock in self.time_clocks.items():
                if clock.active:
                    clock.update()
                    
                    # Check if time ran out for the active clock
                    if clock.time_left <= 0:
                        self.game_over = True
                        self.winner = "white" if player == "black" else "black"
                        # Stop all clocks when game is over
                        self.time_clocks["white"].stop()
                        self.time_clocks["black"].stop()
    
    def render(self):
        """Render the game"""
        # Fill background
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw chess board
        self.board.draw(self.screen)
        
        # Highlight selected piece and available moves
        if self.selected_piece:
            row, col = self.selected_piece
            self.board.highlight_square(self.screen, row, col, (0, 255, 0, 100))  # Green for selected
            
            # Highlight available moves
            for move_row, move_col in self.available_moves:
                self.board.highlight_square(self.screen, move_row, move_col, (0, 0, 255, 100))  # Blue for moves
        
        # Draw time clocks - reversed order (black on top, white on bottom)
        self.time_clocks["black"].draw(self.screen, (self.screen_width - 200, 50))
        self.time_clocks["white"].draw(self.screen, (self.screen_width - 200, self.screen_height - 100))
        
        # Draw current player indicator
        font = pygame.font.SysFont("Arial", 24)
        text = font.render(f"Current Player: {self.current_player.capitalize()}", True, (0, 0, 0))
        self.screen.blit(text, (50, 20))
        
        # Draw game over message if applicable
        if self.game_over:
            self.draw_game_over_message()
    
    def draw_game_over_message(self):
        """Draw game over message"""
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.SysFont("Arial", 48)
        if self.winner:
            text = font.render(f"{self.winner.capitalize()} wins!", True, (255, 255, 255))
        else:
            text = font.render("Game Over - Draw", True, (255, 255, 255))
        
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(text, text_rect) 
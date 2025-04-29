import pygame
import sys
from chess_game import ChessGame
from chess_board import ChessBoard
from chess_pieces import Pawn, Rook, Knight, Bishop, Queen, King
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE

def setup_demo_board(board):
    """Set up a specific chess position for demonstration"""
    # Clear the board
    board.board = [[None for _ in range(board.cols)] for _ in range(board.rows)]
    
    # Set up a position close to checkmate
    # White pieces
    board.board[7][4] = King("white", 7, 4)
    board.board[7][0] = Rook("white", 7, 0)
    board.board[7][7] = Rook("white", 7, 7)
    board.board[6][5] = Pawn("white", 6, 5)
    board.board[6][6] = Pawn("white", 6, 6)
    board.board[6][7] = Pawn("white", 6, 7)
    board.board[5][3] = Queen("white", 5, 3)
    
    # Black pieces
    board.board[0][4] = King("black", 0, 4)
    board.board[1][5] = Pawn("black", 1, 5)
    board.board[2][3] = Knight("black", 2, 3)
    board.board[1][7] = Rook("black", 1, 7)
    
    # Update king positions
    board.white_king_pos = (7, 4)
    board.black_king_pos = (0, 4)
    
    # Set pieces as moved for castling logic
    for row in range(board.rows):
        for col in range(board.cols):
            piece = board.get_piece(row, col)
            if piece:
                piece.has_moved = True

def main():
    """Run a chess game demo"""
    # Initialize pygame
    pygame.init()
    
    # Create screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE + " - Demo")
    
    # Create game instance
    game = ChessGame()
    
    # Set up demo board
    setup_demo_board(game.board)
    
    # Show a message for the demo
    font = pygame.font.SysFont("Arial", 16)
    demo_text = font.render("Demo Mode: White to move and checkmate in 2", True, (0, 0, 0))
    
    # Create clock for capping framerate
    clock = pygame.time.Clock()
    
    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Handle game events
            game.handle_event(event)
        
        # Update game state
        game.update()
        
        # Render game
        game.render()
        
        # Draw demo message
        screen.blit(demo_text, (50, SCREEN_HEIGHT - 30))
        
        # Update display
        pygame.display.flip()
        
        # Cap the framerate
        clock.tick(FPS)

if __name__ == "__main__":
    main() 
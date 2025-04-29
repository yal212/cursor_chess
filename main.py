import pygame
import sys
from chess_game import ChessGame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE

def main():
    # Initialize pygame
    pygame.init()
    
    # Create screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    
    # Create game instance
    game = ChessGame()
    
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
        
        # Update display
        pygame.display.flip()
        
        # Cap the framerate
        clock.tick(FPS)

if __name__ == "__main__":
    main() 
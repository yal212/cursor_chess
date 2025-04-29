import pygame
import time

class TimeClock:
    def __init__(self, initial_time_seconds):
        """Initialize a chess clock with the given time in seconds"""
        self.initial_time = initial_time_seconds
        self.time_left = initial_time_seconds
        self.last_update = time.time()
        self.active = False
    
    def start(self):
        """Start the clock"""
        if not self.active:
            self.last_update = time.time()
            self.active = True
    
    def stop(self):
        """Stop the clock"""
        if self.active:
            self.update()
            self.active = False
    
    def reset(self):
        """Reset the clock to initial time"""
        self.time_left = self.initial_time
        self.active = False
    
    def update(self):
        """Update the clock based on elapsed time"""
        if self.active:
            current_time = time.time()
            elapsed = current_time - self.last_update
            self.time_left -= elapsed  # Count down time
            self.last_update = current_time
            
            # Ensure time doesn't go below zero
            if self.time_left < 0:
                self.time_left = 0
                self.active = False
    
    def format_time(self):
        """Format the time left as MM:SS"""
        minutes = int(self.time_left) // 60
        seconds = int(self.time_left) % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def draw(self, screen, position):
        """Draw the clock on the screen"""
        x, y = position
        # Draw clock background
        pygame.draw.rect(screen, (200, 200, 200), (x, y, 120, 40), border_radius=5)
        pygame.draw.rect(screen, (50, 50, 50), (x, y, 120, 40), 2, border_radius=5)
        
        # Draw time text
        font = pygame.font.SysFont("Arial", 24, bold=True)
        time_text = self.format_time()
        color = (0, 0, 0) if self.time_left > 30 else (255, 0, 0)  # Red when time is low
        text = font.render(time_text, True, color)
        text_rect = text.get_rect(center=(x + 60, y + 20))
        screen.blit(text, text_rect) 
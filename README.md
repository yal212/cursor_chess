# Multiplayer Chess Game

A simple multiplayer chess game built with Pygame.

## Features

- Complete chess board with all standard pieces
- Legal move validation
- Check and checkmate detection
- Player time clocks
- Visual highlighting of selected pieces and available moves

## Requirements

- Python 3.7+
- Pygame

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/chess-game.git
cd chess-game
```

2. Install the required packages:
```
pip install -r requirements.txt
```

## How to Play

Run the game:
```
python main.py
```

### Game Controls

- **Mouse Click**: Select and move pieces
- The game follows standard chess rules
- The clock for each player starts when the first move is made
- The game ends when a player is checkmated or when a player's time runs out

## Custom Chess Pieces

You can add custom chess piece images by placing them in the `res` directory with the following naming convention:
- `white_pawn.png`
- `white_rook.png`
- `white_knight.png`
- `white_bishop.png`
- `white_queen.png`
- `white_king.png`
- `black_pawn.png`
- `black_rook.png`
- `black_knight.png`
- `black_bishop.png`
- `black_queen.png`
- `black_king.png`

If no images are found, the game will use simple shape representations for the pieces.

## Future Improvements

- En passant move
- Network multiplayer
- Game saving/loading
- AI opponent
- Customizable time controls

## License

This project is open source and available under the [MIT License](LICENSE). 